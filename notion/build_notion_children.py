import json
import re


# 当前脚本将构建多个页面中的块级元素,(build-children)
# 每一个块级元素是对应markdown中的无序列表,列表中分为普通文本和链接
# 可参考example-children.py中的children

def build_children(cover, details):
    children = []
    # 使用 json.dumps() 将 Python 对象转换为 JSON 字符串
    image = json.dumps({"type": "image", "image": {"type": "external", "external": {"url": cover}}})
    # 将json字符串解析为对象添加
    children.append(json.loads(image))

    # 构建详细信息的notion api对应的json对象
    for item in details:
        # 超长的item有比较大的概率会超时
        # 按照文本与链接分类的数据
        block_item_list = build_details_li_href(item)
        # 分次取出不超过100个切片做为1个块
        for block_item in block_item_list:
            # 用于存放处理后的json
            block_json = []
            for details in block_item:
                # 构建一个li中的块级元素
                if details['link'] != "":
                    # 块级元素包含链接
                    block_json.append(
                        {
                            "type": "text",
                            "text": {
                                "content": details['text'],
                                "link": {"type": "url", "url": details['link']}
                            },
                        }
                    )
                else:
                    # 块级元素纯文本
                    block_json.append(
                        {
                            "type": "text",
                            "text": {"content": details['text']},
                        },
                    )
            block = json.dumps(
                {
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": block_json
                    }
                },
            )
            # 将构建好的json数据加入children
            children.append(json.loads(block))
    return children


def build_details_li_href(item_content):
    """
    将markdown中无序列表中的普通文本与链接差分开来
    """
    # 定义正则表达式模式，用于匹配链接和普通文本
    pattern = re.compile(r'\[([^]]+)]\(([^)]+)\)|([^\[]+)(?=\[|$)')
    # 使用 findall() 方法找到所有匹配的内容
    matches = pattern.findall(item_content)

    # 遍历匹配项
    result = []
    for match in matches:
        text = match[0] or match[2]  # 提取普通文本
        link = match[1]  # 提取链接
        if link != "":
            # 链接中只保留https或http链接
            link = re.compile(r'\b(?:https?://\S+|www\.\S+)\b').findall(link)[0]
        result.append({"text": text, "link": link})
    # api限制一个块级元素最多只能有100个,所以此处进行切片
    # https://developers.notion.com/reference/request-limits#limits-for-property-values
    result = split_list(result, 100)
    return result


def split_list(input_list, chunk_size):
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]


