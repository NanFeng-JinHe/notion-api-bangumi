#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
from requests.adapters import HTTPAdapter
import time
import random
from util import header
header_list = header.header_list

# 超时时间(插入信息都比较多需要更多的Read time)
# (连接超时, 读取超时)
TIMEOUT = 50  # (3.07, 25)
# 超时重试次数
MAX_RETRIES = 3


def create_session():
    """创建会话"""
    s = requests.Session()
    s.trust_env = False
    s.mount('http://', HTTPAdapter(max_retries=MAX_RETRIES))
    s.mount('https://', HTTPAdapter(max_retries=MAX_RETRIES))
    return s


def retry_request(session, url, method='get', headers=None, data=None, json=None):
    """尝试进行请求，支持重试机制"""
    if headers is None:
        headers = {
            "User-Agent": random.choice(header_list),
        }
    for attempt in range(MAX_RETRIES):
        try:
            if method.lower() == 'get':
                response = session.get(url, headers=headers, timeout=TIMEOUT, proxies=None)
            elif method.lower() == 'post':
                response = session.post(url, headers=headers, data=data, json=json, timeout=TIMEOUT, proxies=None)
            else:
                raise ValueError("不支持的请求类型")
            response.raise_for_status()  # 检查请求是否成功
            # 设置响应内容的字符编码
            response.encoding = 'utf-8'
            return response
        except requests.exceptions.RequestException as e:
            print(f"第 {attempt + 1} 次连接失败: ERROR: {e}")
            if attempt < MAX_RETRIES - 1:
                print("重试中....")
            else:
                print("已达到最大重试次数, 正在退出....")
                break
    print(time.strftime('%Y-%m-%d %H:%M:%S'))


def get(url, headers=None):
    """发起 GET 请求"""
    session = create_session()
    return retry_request(session, url, method='get', headers=headers)


def post(url, data=None, json=None, headers=None):
    """发起 POST 请求"""
    session = create_session()
    return retry_request(session, url, method='post', headers=headers, data=data, json=json)

