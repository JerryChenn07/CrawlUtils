import logging
import lzma

import pymongo

from crawl_utils.file import TimeExtractor
from crawl_utils.utils import fingerprint, get_date, normalize_text, html2element

logger = logging.getLogger(__name__)


class SelfItemPipeline:
    def process_item(self, item, spider):
        for k in item.fields.keys():
            if not isinstance(item.get(k), str):
                continue
            item[k] = item[k].strip()
        item['content'] = [c.strip() for c in item['content'] if c.strip()]
        item['content_uuid'] = fingerprint(item['content_url'])
        item['create_time'] = get_date()

        if html := item.get('html', 0):
            item['html'] = lzma.compress(item['html'].encode('utf-8'))  # 压缩文章内容

            if item.get('pub_time'):
                return item

            normal_html = normalize_text(html)
            element = html2element(normal_html)
            time_extract = TimeExtractor().extractor(element)
            if not time_extract:
                return item
            pub_time = 'passive' + time_extract
            logger.info(f"被动提取到 pub_time={pub_time}，content_url={item['content_url']}")
            item['pub_time'] = pub_time
        elif html is None:
            logger.warning("你忘记加源码了！！！快去 parse_detail 中添加 item['html'] = response.text")
        else:
            # 有些直接为附件，在 parse_list 中，忽略即可
            pass

        return item


class MongoPipeline:
    def __init__(self, log_level, scheduler, host, port, username, password, db, collection, timer_tasks_collection):
        self.log_level = log_level
        self.scheduler = scheduler
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db = db
        self.collection = collection
        self.timer_tasks_collection = timer_tasks_collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            log_level=crawler.settings.get('LOG_LEVEL'),
            scheduler=crawler.settings.get('SCHEDULER'),
            host=crawler.settings.get('MONGODB_HOST'),
            port=crawler.settings.get('MONGODB_PORT'),
            username=crawler.settings.get('MONGODB_USERNAME'),
            password=crawler.settings.get('MONGODB_PASSWORD'),
            db=crawler.settings.get('MONGODB_DB'),
            collection=crawler.settings.get('MONGODB_COLLECTION'),
            timer_tasks_collection=crawler.settings.get('TIMER_TASKS_COLLECTION')
        )

    def open_spider(self, spider):
        # 日志等级为 DEBUG，数据不入库
        if self.log_level == 'DEBUG':
            logger.warning('请注意，现在处于测试阶段的配置，数据未保存，如要入库，请将 LOG 等级修改到大于 DEBUG！！！')
            logger.warning('请注意，现在处于测试阶段的配置，数据未保存，如要入库，请将 LOG 等级修改到大于 DEBUG！！！')
            logger.warning('请注意，现在处于测试阶段的配置，数据未保存，如要入库，请将 LOG 等级修改到大于 DEBUG！！！')
        else:
            self.client = pymongo.MongoClient(host=self.host, port=self.port,
                                              username=self.username, password=self.password)
            self.mydb = self.client[self.db]
            # 如果爬虫队列使用 scrapy_redis，则为增量抓取
            if self.scheduler == "scrapy_redis.scheduler.Scheduler":
                self.mycollection = self.mydb[self.timer_tasks_collection]
                logger.info('增量抓取，数据库：{}，集合：{}'.format(self.db, self.timer_tasks_collection))
            else:
                self.mycollection = self.mydb[self.collection]
                logger.info('单机抓取，数据库：{}，集合：{}'.format(self.db, self.collection))

    def process_item(self, item, spider):
        if self.log_level == 'DEBUG':
            # debug 模式不显示
            item['html'] = 'debug 模式下不显示'
        else:
            self.mycollection.insert_one(dict(item))
            # self.mycollection.update_one(dict(item), {'$set': dict(item)}, upsert=True) #适用于数据量小的
        return item

    def close_spider(self, spider):
        if self.log_level == 'DEBUG':
            logger.warning('再次提醒，请注意，现在处于测试阶段的配置，数据未保存，如要入库，请将 LOG 等级修改到大于 DEBUG！！！')
            logger.warning('再次提醒，请注意，现在处于测试阶段的配置，数据未保存，如要入库，请将 LOG 等级修改到大于 DEBUG！！！')
            logger.warning('再次提醒，请注意，现在处于测试阶段的配置，数据未保存，如要入库，请将 LOG 等级修改到大于 DEBUG！！！')
        else:
            # debug 模式下不用关
            self.client.close()
