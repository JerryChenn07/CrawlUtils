from crawl_utils.file import extract_attachment

url = 'http://www.xizang.gov.cn/zwgk/xxfb/gsgg_428/202008/t20200829_171961.html'
with open('./htmls/attachment/async_attachment.html') as f:
    html = f.read()

attachment_list = extract_attachment(html, url)
print(attachment_list)
