import logging
import re

from parsel.selector import Selector

logger = logging.getLogger(__name__)


def extract_attachment(response):
    """
    用于提取 html 中的附件名字及链接
    :param response: scrapy 的 response 对象
    :return: e.g. [{"attachment_name": "附件1", "attachment_url": "http://gks.mof.gov.cn/ztztz/zhengfucaigouguanli/201802/P020180202506411419197.pdf"}]
    """
    attachment_list = []
    attachment_format_patten = re.compile(r'\.(pdf|xls|doc|ppt|wps)[a-z]?$', flags=re.IGNORECASE)
    suspect_attachment_list = response.xpath('//a')
    for s in suspect_attachment_list:
        if not s.xpath('./@href').re_first(attachment_format_patten): continue
        origin_file_name = s.xpath('string()').get('').strip()
        if not origin_file_name:
            logger.warning(f"获取附件为空：{s.get()}, url={response.url}")
            # continue # 存在一些附件名为空的情况

        attachment_name = attachment_format_patten.sub('', origin_file_name)
        part_attachment_url = s.xpath('./@href').get()
        # file_info = {'attachment_name': attachment_name, 'attachment_url': response.urljoin(part_attachment_url)}
        file_info = {'attachment_name': attachment_name, 'attachment_url': part_attachment_url}
        logger.debug(f"获取附件一个：{file_info}")
        attachment_list.append(file_info)

    return attachment_list


if __name__ == '__main__':
    a = ''
    response = Selector(a)
    attachment_list = extract_attachment(response)
    print(attachment_list)
