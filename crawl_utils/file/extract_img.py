from urllib.parse import urljoin, urlparse


def pad_host_for_images(host, url):
    """
    网站上的图片可能有如下几种格式：

    完整的绝对路径：https://xxx.com/1.jpg
    完全不含 host 的相对路径： /1.jpg
    含 host 但是不含 scheme:  xxx.com/1.jpg 或者  ://xxx.com/1.jpg

    :param host:
    :param url:
    :return:
    """
    if url.startswith('http'):
        return url
    parsed_uri = urlparse(host)
    scheme = parsed_uri.scheme
    if url.startswith(':'):
        return f'{scheme}{url}'
    if url.startswith('//'):
        return f'{scheme}:{url}'
    return urljoin(host, url)


def extract_img(img_list, content_list, original_url):
    """
    content_list 中为包含文章正文和图片链接顺序的, 需要结合 img_list, 拼接为完整的 img 链接

    :param img_list: 文章正文中的图片链接
    :param content_list: 包含文章正文和图片链接顺序
    :param original_url: 该文章的链接
    :return: 顺序的文章正文和完整图片链接
    """
    img_list = [_.strip() for _ in img_list if _.strip()]
    for img in img_list:
        if img not in content_list:
            continue
        img_index = content_list.index(img)
        content_list[img_index] = pad_host_for_images(original_url, img)
    return content_list
