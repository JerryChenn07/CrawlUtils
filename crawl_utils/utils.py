import hashlib
import re
import time
import unicodedata

from lxml.html import fromstring


def fingerprint(s):
    """
    md5加密字符串
    :param s: 需要加密的字符串，一般为文章url
    :return: 加密值
    """
    m1 = hashlib.md5()
    m1.update(s.strip().encode("utf-8"))
    ret = m1.hexdigest()
    return ret


def get_date():
    """获取日期"""
    time_array = time.localtime(time.time())
    return time.strftime("%Y-%m-%d %H:%M:%S", time_array)


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
