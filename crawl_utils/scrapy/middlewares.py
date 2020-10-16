import asyncio
import logging
import random
import sys

import aiohttp
import twisted.internet
from twisted.internet.asyncioreactor import AsyncioSelectorReactor

reactor = AsyncioSelectorReactor(asyncio.get_event_loop())

# install AsyncioSelectorReactor
twisted.internet.reactor = reactor
sys.modules['twisted.internet.reactor'] = reactor

logger = logging.getLogger(__name__)


class PriorityMiddleware(object):
    def process_request(self, request, spider):
        retries = request.meta.get('retry_times', 0)
        request.priority -= retries


class RandomUserAgentMiddleware(object):
    def __init__(self, select_pc_ua, pc_ua, phone_ua):
        self.select_pc_ua = select_pc_ua
        self.pc_ua = pc_ua
        self.phone_ua = phone_ua

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            select_pc_ua=crawler.settings.get('SELECT_PC_UA'),
            pc_ua=crawler.settings.get('PC_USER_AGENT'),
            phone_ua=crawler.settings.get('PHONE_USER_AGENT'),
        )

    def process_request(self, request, spider):
        ua = random.choice(self.pc_ua) if self.select_pc_ua else ua = random.choice(self.phone_ua)
        request.headers["User-Agent"] = ua


class AsyncProxyMiddleware(object):
    def __init__(self, ip_url):
        self.ip_url = ip_url

    @classmethod
    def from_crawler(cls, crawler):
        return cls(ip_url=crawler.settings.get('IP_URL'))

    async def get_proxy(self):
        """
        get proxy from proxy pool
        """
        kwargs = {}
        kwargs['timeout'] = 10
        kwargs['url'] = f'{self.ip_url}/get/'
        # logger.debug('get proxy using kwargs %s', kwargs)

        try:
            async with aiohttp.ClientSession() as client:
                response = await client.get(**kwargs)
                if response.status == 200:
                    json_ret = await response.json()
                    proxy = json_ret['proxy']
                    # logger.debug('get proxy %s', proxy)
                    return proxy
        except:
            logger.error('error occurred while fetching proxy', exc_info=True)

    async def process_request(self, request, spider):
        proxy = await self.get_proxy()

        # skip invalid
        if not proxy:
            logger.error('can not get proxy from proxy pool')
            return

        request.meta['proxy'] = f'http://{proxy}'
