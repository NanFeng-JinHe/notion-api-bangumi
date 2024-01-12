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

