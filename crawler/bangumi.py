from lxml import etree
from util import utils, client


class Anime:
    """
    动漫信息结构
    Attributes:
    - base_url (str) : 信息来源站点
    - title (str) : 标题
    - cover (str): 封面
    - summary (str): 简介
    - tags (list[str]): 标签列表
    - details (str): 详细信息
    - type (str): 类型,固定为"动漫"
    """
    base_url = 'https://bgm.tv/subject/'
    title: str
    cover: str
    summary: str
    tags: list[str]
    details: list[str]
    type: str


def get_bangumi_info(subject_id):
    """获取动漫信息
    :param subject_id: 例如:https://bgm.tv/subject/302561
                        其中的302561
    :return: :class:`Anime <Anime>` object
    :rtype: Anime
    """
    # =============获取原始数据=============
    url = Anime.base_url + subject_id
    response = client.get(url)
    # 调用 etree 模块的 HTML() 方法来创建 HTML 解析对象
    html_tree = etree.HTML(response.content)

    # =============解析数据=============
    # --标题
    Anime.title = "".join(html_tree.xpath('//*[@property="v:itemreviewed"]/text()'))
    # --封面
    cover = "".join(html_tree.xpath('//*[@id="bangumiInfo"]/div/div[1]/a/img/@src'))
    # 此时的cover清晰度较低,删除字符串的'/r/400/pic'是高清图片
    Anime.cover = "https:" + cover.replace("/r/400", "")
    # --简介
    summary = ''
    summary_list = html_tree.xpath('//*[@id="subject_summary"]/text()')

    decoded_str_list = [s.encode().decode('utf-8') for s in summary_list]
    for decoded_str in decoded_str_list:
        summary += decoded_str
    Anime.summary = summary

    # --标签
    tags_list = html_tree.xpath('//*[@id="subject_detail"]/div[@class="subject_tag_section"]'
                                '/div[@class="inner"]/a/span/text()')
    # 获取前四个元素,如果不足四个使用''补充
    tags = (tags_list + [''] * 4)[:4]
    Anime.tags = tags

    # --详细信息
    details_info = html_tree.xpath('//*[@id="infobox"]/li')
    markdown = utils.html2markdown(details_info, 'href="/person/', 'href="https://bgm.tv/person/')
    Anime.details = markdown
    # --类型固定为 "动漫"
    Anime.type = "动漫"
    return Anime



