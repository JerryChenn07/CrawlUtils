import re
import unicodedata

from lxml.html import fromstring


def html2element(html):
    html = re.sub('</?br.*?>', '', html)
    element = fromstring(html)
    return element


def normalize_text(html):
    """
    使用 NFKC 对网页源代码进行归一化，把特殊符号转换为普通符号
    :param html:
    :return:
    """
    return unicodedata.normalize('NFKC', html)
