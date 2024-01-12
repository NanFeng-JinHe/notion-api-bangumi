# 用于统计耗时
import time
# 豆瓣与bangumi网站的视频信息id
from subject import bangumi_subject, douban_movie_subject
# 数据来源(解析网页的脚本)
from crawler import bangumi_api, bangumi, douban
# 构建notion-api请求格式的脚本
from notion import build_notion_page as bnp, build_notion_children as bnc
# 用于日志
from log import logger
log = logger.setup_logging(log_file='./log/logging.log')


def main():
    print("数据源:【1:豆瓣】【2:bangumi】【3:豆瓣&bangumi】")
    index = input()
    if index in ["1", "3"]:
        douban_parse()
    if index in ["2", "3"]:
        bangumi_parse()


def timing(start_time):
    """耗时统计"""
    # 记录结束时间
    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算耗时
    log.info(f"总耗时: {elapsed_time:.2f} 秒")
    print(f"总耗时: {elapsed_time:.2f} 秒")


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


def bangumi_parse():
    """
    从bangumi网站爬取信息并上传到notion
    """
    for anime in bangumi_subject.a_list:
        # 记录开始时间
        start_time = time.time()

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

        # 记录结束时间
        timing(start_time)


def douban_parse():
    """
    从douban网站爬取信息并上传到notion
    """
    for movie in douban_movie_subject.m_list:
        # 记录开始时间
        start_time = time.time()

        # 从douban中爬取数据
        data_obj = douban.get_movie_info(movie)
        # 上传到notion
        url = data_obj.base_url + movie
        parse_and_upload(data_obj, data_obj.title, url)

        # 记录结束时间
        timing(start_time)


if __name__ == "__main__":
    main()
