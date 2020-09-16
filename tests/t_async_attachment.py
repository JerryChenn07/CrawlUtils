from crawl_utils.file import extract_attachment

url = 'http://www.xizang.gov.cn/zwgk/xxfb/gsgg_428/202008/t20200829_171961.html'
with open('./files/attachment/async_attachment.html') as f:
    text = f.read()

attachment_list = extract_attachment(text, url)
print(attachment_list)
