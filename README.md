# CrawlUtils

爬虫中常用到的工具类

---

## Install Or Update

`pip install --upgrade git+https://github.com/cjr0707/CrawlUtils.git@master`

## Usage

### crawl_utils/file

1. `extract_attachment.py` 的使用

```
from crawl_utils.file import extract_attachment

attachment_list = extract_attachment(text, url, attachment_format_list=['your_format'])
print(attachment_list)

```

2. `extract_img.py` 的使用

```
from parsel.selector import Selector
from crawl_utils.file import extract_img

html = '正文的html'
s = Selector(html)
content_list = s.xpath("//text() | //img/@src").getall()
content_list = extract_img(result['images'], content_list, url)
print(content_list)
```

### crawl_utils/scrapy

1. `item.py`

在 `spider` 文件中添加

```
import scrapy
from crawl_utils.scrapy.items import GeneralNewsItem


class TestSpider(scrapy.Spider):
    def parse(self, response):
        item = GeneralNewsItem()
        
```   

2. `middlewares.py` 和 `pipelines.py`

添加到你的 `scrapy` 项目下的 `setting.py` 文件中即可开启使用

```
DOWNLOADER_MIDDLEWARES = {
    'your_project.middlewares.YourMiddleware': 77,
    'crawl_utils.scrapy.middlewares.RandomUserAgentMiddleware': 100,
    'crawl_utils.scrapy.middlewares.AsyncProxyMiddleware': 101,
}

ITEM_PIPELINES = {
    'your_project.pipelines.YourPipelines': 1,
    'crawl_utils.scrapy.pipelines.SelfItemPipeline': 2,
    'crawl_utils.scrapy.pipelines.MongoPipeline': 101,
}
```

## TODO

提取附件时存在重复的url，同时可能还会存在url虽然相同，但是名字一个可能为空或较短字符
http://www.jiangxi.gov.cn/art/2020/8/7/art_5178_2697256.html

## Package Command

```
python setup.py sdist bdist_wheel
git tag -a v0.2.7 -m 'add attachment format & replace !-- character in order to avoid being commented & add title extract'
git push origin --tags
```