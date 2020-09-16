from crawl_utils.file import extract_attachment

url = 'http://www.xinjiang.gov.cn/xinjiang/fgwjx/202009/d9bafda1ba5541db8d8d499934c20208.shtml'
with open('./files/attachment/sync_attachment.html') as f:
    text = f.read()

attachment_list = extract_attachment(text, url, attachment_format_list=['txt'])
print(attachment_list)
