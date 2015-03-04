import scrapy
from test.items import TestItem

class TestSpider(scrapy.Spider):
    name = 'test_spider'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com/']

    def parse(self, response):
        yield MyItem(title='Test', desc='Test')
