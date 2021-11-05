import logging
import re
from urllib.parse import urljoin

from parsel.selector import Selector

from crawl_utils.patterns import ATTACHMENT_REGEXES
from crawl_utils.utils import fingerprint

logger = logging.getLogger(__name__)


def remove_noise_chars(text: str) -> str:
    # 替换 <!--<a href="" target="_blank" >-->xxxx<!--</a>--></em> 中的 !--，防止后续代码被注释
    return text.replace('!--', '').strip()


def node_a_to_text(html: str) -> str:
    get_node_a_list = re.findall('<a .*?</a>', html, re.DOTALL | re.IGNORECASE)
    return remove_noise_chars(''.join(get_node_a_list))


def extract_attachment(html: str, content_url: str, attachment_format_list=[]) -> list:
    """
    用于提取 html 中的附件名字及链接

    :param html: html
    :param content_url: html的原文url, 用于拼接附件链接
    :param attachment_format_list: 除了基础的附件格式 pdf, xls, doc, ppt, wps，txt, ceb 还可新增附件格式，如: xxx
    :return: e.g. [{"attachment_name": "附件1", "attachment_url": "http://xxx.com/P020180202506411419197.pdf"}]
    """
    attachment_format = '|'.join(set(ATTACHMENT_REGEXES + attachment_format_list))  # 'pdf|xls|doc|ppt|wps...'
    attachment_format_pattern = re.compile(f'\.({attachment_format})[a-z]?$', flags=re.IGNORECASE)

    suspect_attachment_list = Selector(node_a_to_text(html)).xpath('//a')
    attachment_dict = {}
    for s in suspect_attachment_list:
        if not s.xpath('./@href').re_first(attachment_format_pattern):
            continue
        origin_file_name = s.xpath('string()').get('').strip() or \
                           s.xpath('./@title').get('').strip() or \
                           s.xpath('./@textvalue').get('').strip()
        if not origin_file_name:
            # continue # 存在一些附件名为空的情况
            logger.warning(f"Get a empty attachment name, origin node is ==={s.get()}===, content_url={content_url}")

        attachment_name = attachment_format_pattern.sub('', origin_file_name)
        attachment_url = urljoin(content_url, s.xpath('./@href').get())
        fp = fingerprint(attachment_url)
        if attachment_dict.get(fp) is not None and \
                len(attachment_name) <= len(attachment_dict[fp]['attachment_name']):  # 取文件名最长的
            continue
        file_info = {'attachment_name': attachment_name, 'attachment_url': attachment_url}
        logger.debug(f"Get attachment successful: {file_info}")
        attachment_dict[fp] = file_info

    return list(attachment_dict.values())
