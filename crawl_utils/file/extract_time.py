import re

from lxml.html import HtmlElement

from crawl_utils.patterns import TIME_META, TIME_REGEXES


class TimeExtractor:
    def extractor(self, element: HtmlElement) -> str:
        publish_time = (self.extract_from_meta(element)  # 第一优先级从 Meta 中提取
                        or self.extract_from_text(element))  # 最坏的情况从正文中提取
        return publish_time

    def extract_from_meta(self, element: HtmlElement) -> str:
        """
        一些很规范的新闻网站，会把新闻的发布时间放在 META 中，因此应该优先检查 META 数据
        :param element: 网页源代码对应的Dom 树
        :return: str
        """
        for xpath in TIME_META:
            publish_time = element.xpath(xpath)
            if publish_time:
                return ''.join(publish_time)
        return ''

    def extract_from_text(self, element: HtmlElement) -> str:
        text = ''.join(element.xpath('.//text()'))
        for dt in TIME_REGEXES:
            dt_obj = re.search(dt, text)
            if dt_obj:
                return dt_obj.group(1)
        else:
            return ''
