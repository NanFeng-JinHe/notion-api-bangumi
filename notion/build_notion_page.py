from notion import notion_token
from util import client

api_database_id = notion_token.api_database_id
api_secret = notion_token.api_secret

headers = {
    "Authorization": "Bearer " + api_secret,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


def update_notion_database_page(title, alias, url, year, area, type, tags, summary, children):
    """
    将信息上传到notion
    :param title: 标题
    :param alias: 别名
    :param url: 原文地址(数据源)
    :param year: 年份
    :param area: 上映地区
    :param type: 类型
    :param tags: 标签列表
    :param summary: 简介
    :param children: 详细信息
    :return: response响应
    """
    # 构建tags
    tags_json = []
    for tag in tags:
        if tag != '':
            tags_json.append({"name": tag})
    # 解析网页

    p = {
        "parent": {
            "type": "database_id",
            "database_id": api_database_id
        },
        "properties": {
            "名称": {
                "type": "title",
                "title": [{"type": "text", "text": {"content": title}}]
            },
            "别名": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                             "content": alias
                         }
                    }
                ]},
            "状态": {
                "type": "select",
                "select": {
                    "name": "完结"
                }
            },
            "上映年份": {
                "date": {
                    "start": year
                }
            },
            "类型": {
                "type": "select",
                "select": {
                    "name": type
                }
            },
            "标签": {
                "multi_select": tags_json
            },
            "地区": {
                "multi_select": [
                    {"name": area},
                ],
            },
            "数据源": {
                "url": url
            },
            "简介": {"rich_text": [{"type": "text", "text": {"content": summary}}]},
        },
        # 内容
        "children": children
    }

    response = client.post("https://api.notion.com/v1/pages", json=p, headers=headers)
    return response

