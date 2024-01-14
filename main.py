#!/usr/bin/python
# -*- coding: UTF-8 -*-
import concurrent.futures
# 用于统计耗时
# 豆瓣与bangumi网站的视频信息id
from subject import bangumi_subject, douban_movie_subject
# 数据来源(解析网页的脚本)
from crawler import bangumi_api, bangumi, douban
# 构建notion-api请求格式的脚本
from notion import build_notion_page as bnp, build_notion_children as bnc
# 用于日志
from log import logger
log = logger.setup_logging(log_file='./log/logging.log')


# 失败列表
douban_fail_list = []


def main():
    mode = ''
    while mode != '0':
        # 现在，json 是包含 JSON 数据的 Python 字典
        mode = input('======================更新模式======================\n'
                     '【1:批量插入:从文件中读取】\n【2:输入插入:从控制台输入】\n【0:退出】\n')
        if mode == '0':
            break
        menu_main(mode)


def menu_main(mode):
    if mode == '1':
        index = input("数据源:\n【1:豆瓣】\n【2:bangumi】\n【3:豆瓣 + bangumi】\n")
        if index in ["1", "3"]:
            thread_func(douban_parse, douban_movie_subject.m_list, 3)
            print("第二次重试开始!!")
            thread_func(douban_parse, douban_fail_list, 3)
            print("最终失败列表:")
            for i in douban_fail_list:
                print(f'\'{i.group()}\'')
            log.error(douban_fail_list)
        if index in ["2", "3"]:
            thread_func(bangumi_parse, bangumi_subject.a_list, 20)
    elif mode == '2':
        index = input("数据源:\n【1:豆瓣】\n【2:bangumi】\n")
        if index == '1':
            douban_parse(input("请输入1个豆瓣subject_id:"))
        elif index == '2':
            bangumi_parse(input("请输入1个bangumi subject_id:"))


def thread_func(function_name, params, max_workers):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(function_name, params))


def parse_and_upload(data_obj, title, url, alias=''):
    """
    :param data_obj: 封装后的数据
    :param title: 标题
    :param url: 原文地址(数据源)
    :param alias: 别名
    """
    children = bnc.build_children(data_obj.cover, data_obj.details)
    response = bnp.update_notion_database_page(
        title,
        alias,
        url,
        data_obj.date,
        data_obj.area,
        data_obj.type,
        data_obj.tags,
        data_obj.summary,
        children,
    )
    if response.status_code != 200:
        log.error(response.json())
        log_list = ["=====>插入失败:", response.status_code, title]
        log.error(''.join(log_list))
        print("\033[31m=====>插入失败:\033[0m", response.status_code, title)
    else:
        log_list = ["=====>插入成功:", title]
        log.info(''.join(log_list))
        print("\033[32m=====>插入成功:\033[0m", title)


def bangumi_parse(anime):
    """
    从bangumi网站爬取信息并上传到notion
    """
    # 从bangumi中爬取数据
    data_obj = bangumi.get_bangumi_info(anime)
    # 从bangumi-api中解析数据
    data_obj_api = bangumi_api.get_bangumi_info(anime)
    # 中文名
    alias = data_obj_api.name_cn if data_obj_api.name_cn else ''
    title = data_obj_api.name_cn if data_obj_api.name_cn else data_obj.title
    # 组合数据
    data_obj.area = data_obj_api.area
    data_obj.date = data_obj_api.date
    # 上传到notion
    url = data_obj.base_url + anime
    parse_and_upload(data_obj, title, url,  alias)


def douban_parse(movie):
    """
    从douban网站爬取信息并上传到notion
    """
    # 从douban中爬取数据
    data_obj = douban.get_movie_info(movie)

    if data_obj is None:
        # 如果数据为None,说明豆瓣返回200,页面内容缺失,进行一次重试
        print("内容缺失,重新解析", movie)
        douban_fail_list.append(movie)
        data_obj = douban.get_movie_info(movie)

    if data_obj is not None:
        # 上传到notion
        url = data_obj.base_url + movie
        parse_and_upload(data_obj, data_obj.title, url, data_obj.alias)
        # 第一次重试状态
        if movie in douban_fail_list:
            print("重试成功!", movie, data_obj.title)
            douban_fail_list.remove(movie)

    if data_obj is None:
        # 第一次重试状态
        print(movie, "重试失败")


if __name__ == "__main__":
    main()
