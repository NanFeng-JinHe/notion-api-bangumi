# 读取数据
import json


def search_name_site(json_data, search_term, site_name):
    # 存放结果集
    filtered_data = []
    for obj in json_data['items']:
        # 检测日语标题
        if search_term.lower() in obj['title'].lower():
            filtered_data.append(obj)
        # 是否存在中文翻译
        for lang in ['zh-Hans', 'zh-Hant']:
            has_zh_hans = obj['titleTranslate'].get(lang)
            if has_zh_hans is not None:
                for zh_hans in has_zh_hans:
                    # 剧名中是否存在指定字符串
                    if search_term.lower() in zh_hans.lower():
                        filtered_data.append(obj)
        # 是否存在繁体翻译

    # 结果集去重
    result_list = []
    [result_list.append(x) for x in filtered_data if x not in result_list]
    # 输出结果集
    for obj in result_list:
        for site in obj['sites']:
            if site['site'] == site_name:
                print("    '", site['id'], "',  # ", obj['title'], sep='')


file_path = 'data.json'
json_data = None
# 打开文件并解析 JSON 数据
with open(file_path, 'r', encoding='utf-8') as file:
    json_data = json.load(file)
search_term = ''


while search_term != '0':
    # 现在，json 是包含 JSON 数据的 Python 字典
    search_term = input('请输入搜索动漫名称:(exit:0)\n')
    if search_term == '0':
        break
    search_name_site(json_data, search_term, "bangumi")

