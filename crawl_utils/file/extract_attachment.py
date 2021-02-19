import logging
import re
from urllib.parse import urljoin

from parsel.selector import Selector

logger = logging.getLogger(__name__)


def extract_attachment(text, content_url, attachment_format_list=[]):
    """
    用于提取 html 中的附件名字及链接

    :param text: html
    :param content_url: text的原文url, 用于拼接附件链接
    :param attachment_format_list: 除了基础的附件格式 pdf, xls, doc, ppt, wps，txt, ceb 还可新增附件格式，如: xxx
    :return: e.g. [{"attachment_name": "附件1", "attachment_url": "http://xxx.com/P020180202506411419197.pdf"}]
    :return:
    """
    if not isinstance(text, str):
        raise Exception('new version has removed response obj, please change codes or upgrade')
    attachment_list = []

    base_attachment_format_list = ['pdf', 'xls', 'doc', 'ppt', 'wps', 'txt', 'ceb', 'rar', 'zip']
    attachment_format = '|'.join(set(base_attachment_format_list + attachment_format_list))  # 'pdf|xls|doc|ppt|wps...'
    attachment_format_patten = re.compile(f'\.({attachment_format})[a-z]?$', flags=re.IGNORECASE)

    get_node_a_list = re.findall('<a .*?</a>', text, re.DOTALL | re.IGNORECASE)
    # 替换 <!--<a href="" target="_blank" >-->xxxx<!--</a>--></em> 中的 !--，防止后续代码被注释
    suspect_attachment_list = Selector(''.join(get_node_a_list).replace('!--', '')).xpath('//a')
    attachment_set = set()
    for s in suspect_attachment_list:
        if not s.xpath('./@href').re_first(attachment_format_patten):
            continue
        origin_file_name_from_text = s.xpath('string()').get('').strip()
        origin_file_name_from_title = s.xpath('./@title').get('') or s.xpath('./@textvalue').get('')
        if not origin_file_name_from_text and not origin_file_name_from_title:
            # continue # 存在一些附件名为空的情况
            logger.warning(f"Get a empty attachment name, origin node is ==={s.get()}===, content_url={content_url}")

        origin_file_name = origin_file_name_from_text or origin_file_name_from_title
        attachment_name = attachment_format_patten.sub('', origin_file_name)
        attachment_url = urljoin(content_url, s.xpath('./@href').get())
        if attachment_name + attachment_url in attachment_set:
            continue

        attachment_set.add(attachment_name + attachment_url)
        file_info = {'attachment_name': attachment_name, 'attachment_url': attachment_url}
        logger.debug(f"Get attachment successful: {file_info}")
        attachment_list.append(file_info)

    return attachment_list
