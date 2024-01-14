#!/usr/bin/python
# -*- coding: UTF-8 -*-
from lxml import etree
import html2text
from datetime import datetime


def html2markdown(details_html, base_str, replace_str):
    """
    <span>
        <span class="pl">导演</span>:
        <span class="attrs">
            <a href="/celebrity/1480279/" rel="v:directedBy">特伦特·科雷</a>
            /
            <a href="/celebrity/1359015/" rel="v:directedBy">乔西·特立尼达</a>
        </span>
    </span>
    将含有链接的文本转变为markdown格式,并补全对应平台的信息
    :param details_html: 待转换文本
    :param base_str: 文本中待替换字符串
    :param replace_str: 替换字符串
    :return markdown 转换后的文本
    """
    # 获取并解析详细信息块
    details_html_texts = [
        etree.tostring(info_item, encoding='utf-8', method='html').decode('utf-8') for info_item in details_html]
    markdown = []
    for raw_html_text in details_html_texts:
        # 补全信息
        raw_html_text = raw_html_text.replace(base_str, replace_str)
        # 将信息转为markdown
        raw_html_text = html2text.html2text(raw_html_text).replace('\n', '')
        markdown.append(raw_html_text.replace('*', ""))
    return markdown


def date_str_to_ios_8601(date_str):
    # 将字符串转换为日期对象
    date_object = datetime.strptime(date_str, '%Y-%m-%d')
    # 将日期对象转换为 ISO 8601 格式的字符串
    iso_format_date = date_object.isoformat()
    return iso_format_date
