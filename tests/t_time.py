from crawl_utils.file import TimeExtractor
from crawl_utils.utils import normalize_text, html2element

with open('./htmls/attachment/sync_attachment.html') as f:
    html = f.read()
normal_html = normalize_text(html)
element = html2element(normal_html)
pub_time = 'passive' + TimeExtractor().extractor(element)
print(pub_time)
