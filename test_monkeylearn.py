# -*- coding: utf-8 -*-
import json

from mock import Mock

from scrapy import Item, Field, Spider
from scrapy.http import Response
from scrapy.utils.test import get_crawler
from twisted.internet.defer import Deferred
from twisted.trial import unittest

from scrapy_monkeylearn import MonkeyLearnPipeline


class TestSpider(Spider):
    name = 'example_spider'

    def parse(self, response):
        pass


class TestItem(Item):
    title = Field()
    desc = Field()
    category = Field()


class MonkeyLearnPipelineTest(unittest.TestCase):
    def setUp(self):
        settings = {
            'MONKEYLEARN_CLASSIFIER': 'dummyclassifier',
            'MONKEYLEARN_AUTH_TOKEN': 'notsosecret',
            'MONKEYLEARN_CLASSIFIER_FIELDS': ['title', 'desc'],
            'MONKEYLEARN_CATEGORIES_FIELD': 'category'}
        self.crawler = get_crawler(settings_dict=settings)
        self.crawler.engine = Mock()
        self.crawler.engine.download = Mock(return_value=Deferred())
        # workaround to set crawler during instantiation
        self.spider = TestSpider().set_crawler(self.crawler)
        self.item = TestItem({
            'title': u'Foo bar',
            'desc': u'For Guido\'s sake'})

    def test_check_response(self):
        pipe = MonkeyLearnPipeline(self.crawler)

        def get_response(item, status=200):
            return Response(
                'http://api.monkeylearn.com/',
                status=status,
                body=json.dumps({'result': 'python'}))

        response = get_response(self.item)
        updated_item = pipe.check_response(response, self.item.copy())
        self.assertEqual(updated_item['category'], 'python')

        response = get_response(self.item, status=404)
        updated_item = pipe.check_response(response, self.item.copy())
        self.assertEqual(updated_item, self.item)
