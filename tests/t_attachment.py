from urllib.parse import urljoin

from parsel.selector import Selector

from crawl_utils.file import extract_attachment

with open('./files/t_attachment.txt') as f:
    text = f.read()
response = Selector(text)
attachment_list = extract_attachment(response, attachment_format_list=['txt'])
print(attachment_list)

for i in attachment_list:
    i['attachment_url'] = urljoin(
        'http://www.xinjiang.gov.cn/xinjiang/fgwjx/202009/d9bafda1ba5541db8d8d499934c20208.shtml', i['attachment_url'])
    print(i)
