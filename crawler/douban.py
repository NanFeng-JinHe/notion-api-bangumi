from lxml import etree
from util import utils, client
import re


class Movie:
    """
    动漫信息结构
    Attributes:
    - base_url (str) : 信息来源站点
    - date (str) : 上映日期
    - area (str) : 上映地区
    - title (str) : 标题
    - cover (str): 封面
    - summary (str): 简介
    - tags (list[str]): 标签列表
    - details (str): 详细信息
    - type (str): 类型,固定为"电影 "
    """
    base_url = 'https://movie.douban.com/subject/'
    date: str
    area: str
    title: str
    cover: str
    summary: str
    tags: list[str]
    details: list[str]
    type: str


def split_markdown(markdown):
    """
    爬取的豆瓣详情中的信息是整体的字符串
    按照定义好的分割信息分割成不同的块
    :param markdown:
    :return:
    """
    # 定义字符串数组
    delimiters = ['导演:', '编剧:', '主演:', '类型:', '制片国家/地区:', '语言:',
                  '首播:', '季数:', '集数:', '单集片长:', '上映日期:', '片长:',
                  '又名:', 'IMDb:']
    # 使用正则表达式的re.split()方法和正向预查
    result = re.split("(?=" + "|".join(map(re.escape, delimiters)) + ")", markdown)
    # 过滤空字符串
    result = [item.strip() for item in result if item]
    # 输出结果
    return result


def get_movie_info(subject_id):
    url = Movie.base_url + subject_id
    html_tree = etree.HTML(client.get(url).text)
    # --名称
    Movie.title = "".join(html_tree.xpath('.//h1/span[1]/text()')[0])
    # --封面
    cover_base_url = ("https://movie.douban.com/subject/" + subject_id +
                      "/photos?type=R&start=0&sortby=size&size=a&subtype=o")
    cover_tree = etree.HTML(client.get(cover_base_url).text)
    cover_list = cover_tree.xpath('//*[@id="content"]//*/ul/li/@data-id')
    # l s m
    # https://img1.doubanio.com/view/photo/l/public/p2902597000.webp
    Movie.cover = "".join("https://img1.doubanio.com/view/photo/l/public/p" + cover_list[0] + ".webp")
    # -- 简介
    summary = ''
    summary_list = html_tree.xpath("//*[@id='link-report-intra']/span/text()")
    decoded_str_list = [s.encode().decode('utf-8') for s in summary_list]
    for decoded_str in decoded_str_list:
        summary += decoded_str
    # 去除多余空格
    Movie.summary = re.sub('\\s+', ' ', summary)
    # --标签
    tags_list = html_tree.xpath('//*[@property="v:genre"]/text()')
    # 获取前四个元素,如果不足四个使用''补充
    tags = (tags_list + [''] * 4)[:4]
    Movie.tags = tags
    # -- 详细信息
    details = html_tree.xpath('//*[@id="info"]')
    markdown = utils.html2markdown(details, 'href="/', 'href="https://movie.douban.com/')
    # 将返回的信息拆分成块
    markdown = split_markdown(markdown[0])
    Movie.details = markdown
    # --日期地区
    date_area = html_tree.xpath('//*[@property="v:initialReleaseDate"]/text()')
    # 定义正则表达式模式，用于匹配日期&地区
    pattern = re.compile(r'(\d{4}-\d{2}-\d{2})\((.*)\)')
    matches = pattern.findall(date_area[0])
    for match in matches:
        # Movie.date = utils.date_str_to_ios_8601(match[0])
        Movie.date = match[0]
        Movie.area = match[1]
    # --类型固定为"电影"
    Movie.type = "电影"
    return Movie





