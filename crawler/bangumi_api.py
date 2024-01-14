from util import client


class AnimeApi:
    """
    动漫信息结构
    Attributes:
    - base_url (str) : 信息来源站点
    - date(str): 上映日期 2019-9-23
    - area(list(str)): 上映地区 固定为"日本"
    - title (str): 标题
    - name_cn (str): 译名
    - cover (str): 封面
    - summary (str): 简介
    - tags (list[str]): 标签列表
    - details (str): 详细信息
    - type (str) : 条目类型
        # 1 为 书籍
        # 2 为 动画
        # 3 为 音乐
        # 4 为 游戏
        # 6 为 三次元
        # 没有 5
    """
    base_url = 'https://api.bgm.tv/v0/subjects/'
    date: str
    area: str
    title: str
    name_cn: str
    cover: str
    summary: str
    tags: list[str]
    details: dict
    type: str


def get_bangumi_info(subject_id):
    """
    api文档说明: https://bangumi.github.io/api/
    从bangumi提供的接口中获取信息
    :param subject_id: https://api.bgm.tv/v0/subjects/{subject_id}
    """
    animeapi = AnimeApi()
    url = AnimeApi.base_url + subject_id
    data_obj = client.get(url).json()
    # 日期
    date = data_obj['date']
    # AnimeApi.date = utils.date_str_to_ios_8601(date)
    animeapi.date = date
    animeapi.area = ["日本"]
    # 封面# small\grid\large\medium\common
    animeapi.cover = data_obj['images']['common']
    # 简介
    animeapi.summary = data_obj['summary']
    # 原名
    animeapi.title = data_obj['name']
    # 中文译名
    animeapi.name_cn = data_obj['name_cn']
    # 标签
    tags_l = [item['name'] for item in data_obj['tags']]
    animeapi.tags = (tags_l + [''] * 4)[:4]
    # 详细信息
    animeapi.details = data_obj['infobox']
    # for item in data_obj['infobox']:
    #     if isinstance(item['value'], list):
    #         print(item['key'])
    #         for i in item['value']:
    #             print(i['v'])
    #     else:
    #         print(item['key'], item['value'])
    animeapi.type = data_obj['type']
    if animeapi.type == '1':
        animeapi.type = "书籍"
    elif animeapi.type == '2':
        animeapi.type = "动漫"
    elif animeapi.type == '3':
        animeapi.type = "音乐"
    elif animeapi.type == '4':
        animeapi.type = "游戏"
    elif animeapi.type == '6':
        animeapi.type = "三次元"

    return animeapi

