import requests
import time
from requests.adapters import HTTPAdapter

default_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/54.0.2840.99 Safari/537.36"
}

# 超时时间
timeout = 20
# 超时重试
max_retries = 5


def get(url, headers=None):
    # 设置超时后重试https&http
    if headers is None:
        headers = default_header
    for attempt in range(max_retries):
        try:
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries))
            s.mount('https://', HTTPAdapter(max_retries))
            # 设置超时时间5s
            rp = s.get(url, headers=headers, timeout=timeout)
            rp.encoding = 'utf-8'
            return rp
        except requests.exceptions.RequestException as e:
            print(f"第 {attempt + 1} 次连接失败:ERROR: {e}")
            if attempt < max_retries - 1:
                print("重试中....")
            else:
                print("已达到最大重试次数,正在退出....")
                break

    print(time.strftime('%Y-%m-%d %H:%M:%S'))


def post(url, data=None, headers=None):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, data=data, headers=headers, timeout=timeout)
            response.raise_for_status()  # 检查请求是否成功
            print(response.text)  # 输出响应内容
            break  # 如果请求成功，退出循环
        except requests.exceptions.RequestException as e:
            print(f"第 {attempt + 1} 次连接失败:ERROR: {e}")
            if attempt < max_retries - 1:
                print("重试中....")
            else:
                print("已达到最大重试次数,正在退出....")



