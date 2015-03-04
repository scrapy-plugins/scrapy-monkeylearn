import unittest

import os

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.settings import Settings
from test.test.spiders.test_spider import TestSpider
from test.test.pipelines import DB

class TestSimple(unittest.TestCase):

    def setUp(self):
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'test.settings')
        self.spider = TestSpider()
        self.crawler = Crawler(Settings())
        self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        self.crawler.configure()

    def test_run(self):
        self.crawler.crawl(self.spider)
        self.crawler.start()
        log.start()
        reactor.run()

    def test_item(self):
        self.assertEqual(length(DB), 1)

if __name__ == '__main__':
    unittest.main()
