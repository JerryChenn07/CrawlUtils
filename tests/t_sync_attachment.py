from crawl_utils.file import extract_attachment

url = 'http://www.xinjiang.gov.cn/xinjiang/fgwjx/202009/d9bafda1ba5541db8d8d499934c20208.shtml'
with open('./htmls/attachment/sync_attachment.html') as f:
    html = f.read()

attachment_list = extract_attachment(html, url, attachment_format_list=['txt'])
print(attachment_list)
