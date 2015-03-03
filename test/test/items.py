# -*- coding: utf-8 -*-
import scrapy


class TestItem(scrapy.Item):
    title = scrapy.Field()
    desc = scrapy.Field()
    category = scrapy.Field()
