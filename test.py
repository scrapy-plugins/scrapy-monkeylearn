import unittest

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from test.test.spiders.test_spider import TestSpider
from scrapy.utils.project import get_project_settings

class TestSimple(unittest.TestCase):

    def test_shuffle(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
