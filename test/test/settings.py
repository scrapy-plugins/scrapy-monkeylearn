# -*- coding: utf-8 -*-

BOT_NAME = 'test'

SPIDER_MODULES = ['test.spiders']
NEWSPIDER_MODULE = 'test.spiders'

MONKEYLEARN_CLASSIFIER = 'abc'
MONKEYLEARN_AUTH_TOKEN = '123'
MONKEYLEARN_CLASSIFIER_FIELDS = ['title', 'desc']
MONKEYLEARN_CATEGORIES_FIELD = 'category'
MONKEYLEARN_DEBUG = True

ITEM_PIPELINES = {
    'scrapy_monkeylearn.MonkeyLearnPipeline': 100,
    'test.pipelines.StorePipeline': 200
}
