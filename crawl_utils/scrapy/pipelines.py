import hashlib
import logging
import lzma
import time

import pymongo

logger = logging.getLogger(__name__)


class SelfItemPipeline:
    def process_item(self, item, spider):
        for k in item.fields.keys():
            if not isinstance(item.get(k), str):
                continue
            item[k] = item[k].strip()
        item['content'] = [c.strip() for c in item['content'] if c.strip()]
        item['content_uuid'] = self.fingerprint(item['content_url'])
        item['create_time'] = self.get_date()

        html = item.get('html', 0)
        if html:
            item['html'] = lzma.compress(item['html'].encode('utf-8'))  # 压缩文章内容
        elif html is None:
            logger.warning("你忘记加源码了！！！快去 parse_detail 中添加 item['html'] = response.text")
        else:
            # 有些直接为附件，在 parse_list 中，忽略即可
            pass

        return item

    @staticmethod
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

    @staticmethod
    def get_date():
        """获取日期"""
        time_array = time.localtime(time.time())
        return time.strftime("%Y-%m-%d %H:%M:%S", time_array)


class MongoPipeline(object):
    def __init__(self, log_level, host, port, username, password, db, collection):
        self.log_level = log_level
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db = db
        self.collection = collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            log_level=crawler.settings.get('LOG_LEVEL'),
            host=crawler.settings.get('MONGODB_HOST'),
            port=crawler.settings.get('MONGODB_PORT'),
            username=crawler.settings.get('MONGODB_USERNAME'),
            password=crawler.settings.get('MONGODB_PASSWORD'),
            db=crawler.settings.get('MONGODB_DB'),
            collection=crawler.settings.get('MONGODB_COLLECTION')
        )

    def open_spider(self, spider):
        if self.log_level != 'DEBUG':
            self.client = pymongo.MongoClient(host=self.host, port=self.port,
                                              username=self.username, password=self.password)
            self.mydb = self.client[self.db]
            self.mycollection = self.mydb[self.collection]
            logger.info('数据库：{}，集合：{}'.format(self.db, self.collection))
        else:
            logger.warning('请注意，现在处于测试阶段的配置，数据未保存，如要入库，请将 LOG 等级修改到大于 DEBUG！！！')
            logger.warning('请注意，现在处于测试阶段的配置，数据未保存，如要入库，请将 LOG 等级修改到大于 DEBUG！！！')
            logger.warning('请注意，现在处于测试阶段的配置，数据未保存，如要入库，请将 LOG 等级修改到大于 DEBUG！！！')

    def process_item(self, item, spider):
        if self.log_level != 'DEBUG':
            self.mycollection.insert_one(dict(item))
            # self.mycollection.update_one(dict(item), {'$set': dict(item)}, upsert=True) #适用于数据量小的
        return item

    def close_spider(self, spider):
        if self.log_level != 'DEBUG':
            self.client.close()
        else:
            logger.warning('再次提醒，请注意，现在处于测试阶段的配置，数据未保存，如要入库，请将 LOG 等级修改到大于 DEBUG！！！')
            logger.warning('再次提醒，请注意，现在处于测试阶段的配置，数据未保存，如要入库，请将 LOG 等级修改到大于 DEBUG！！！')
            logger.warning('再次提醒，请注意，现在处于测试阶段的配置，数据未保存，如要入库，请将 LOG 等级修改到大于 DEBUG！！！')
