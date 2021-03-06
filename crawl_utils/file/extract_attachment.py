import logging
import re
from urllib.parse import urljoin

from parsel.selector import Selector

from crawl_utils.patterns import ATTACHMENT_REGEXES

logger = logging.getLogger(__name__)


def remove_noise_chars(text):
    # 替换 <!--<a href="" target="_blank" >-->xxxx<!--</a>--></em> 中的 !--，防止后续代码被注释
    return text.replace('!--', '').strip()


def extract_attachment(html, content_url, attachment_format_list=[]):
    """
    用于提取 html 中的附件名字及链接

    :param html: html
    :param content_url: html的原文url, 用于拼接附件链接
    :param attachment_format_list: 除了基础的附件格式 pdf, xls, doc, ppt, wps，txt, ceb 还可新增附件格式，如: xxx
    :return: e.g. [{"attachment_name": "附件1", "attachment_url": "http://xxx.com/P020180202506411419197.pdf"}]
    :return:
    """
    if not isinstance(html, str):
        raise Exception('new version has removed response obj, please change codes or upgrade')
    attachment_list = []

    attachment_format = '|'.join(set(ATTACHMENT_REGEXES + attachment_format_list))  # 'pdf|xls|doc|ppt|wps...'
    attachment_format_pattern = re.compile(f'\.({attachment_format})[a-z]?$', flags=re.IGNORECASE)

    get_node_a_list = re.findall('<a .*?</a>', html, re.DOTALL | re.IGNORECASE)
    node_a_to_text = remove_noise_chars(''.join(get_node_a_list))
    suspect_attachment_list = Selector(node_a_to_text).xpath('//a')
    attachment_set = set()
    for s in suspect_attachment_list:
        if not s.xpath('./@href').re_first(attachment_format_pattern):
            continue
        origin_file_name_from_text = s.xpath('string()').get('').strip()
        origin_file_name_from_title = s.xpath('./@title').get('') or s.xpath('./@textvalue').get('')
        if not origin_file_name_from_text and not origin_file_name_from_title:
            # continue # 存在一些附件名为空的情况
            logger.warning(f"Get a empty attachment name, origin node is ==={s.get()}===, content_url={content_url}")

        origin_file_name = origin_file_name_from_text or origin_file_name_from_title
        attachment_name = attachment_format_pattern.sub('', origin_file_name)
        attachment_url = urljoin(content_url, s.xpath('./@href').get())
        if attachment_name + attachment_url in attachment_set:
            continue

        attachment_set.add(attachment_name + attachment_url)
        file_info = {'attachment_name': attachment_name, 'attachment_url': attachment_url}
        logger.debug(f"Get attachment successful: {file_info}")
        attachment_list.append(file_info)

    return attachment_list
