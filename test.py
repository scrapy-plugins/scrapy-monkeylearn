import unittest

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals, Item, Field
from scrapy.settings import Settings

from scrapy_monkeylearn import MonkeyLearnPipeline


class TestItem(Item):
    title = Field()
    desc = Field()
    category = Field()


class TestSimple(unittest.TestCase):

    def setUp(self):
        # Configure settings
        settings = Settings()
        settings.set('MONKEYLEARN_CLASSIFIER', 'abc')
        settings.set('MONKEYLEARN_AUTH_TOKEN', '123')
        settings.set('MONKEYLEARN_CLASSIFIER_FIELDS', ['title', 'desc'])
        settings.set('MONKEYLEARN_CATEGORIES_FIELD', 'category')
        settings.set('MONKEYLEARN_DEBUG', True)

        self.crawler = Crawler(settings)
        self.crawler.configure()

    def test_process_item(self):
        pipeline = MonkeyLearnPipeline.from_crawler(self.crawler)
        item = TestItem(title='test', desc='test')
        processed = pipeline.process_item(item, None)
        self.assertEqual(processed['category'], [{'label': 'None'}])

if __name__ == '__main__':
    unittest.main()
