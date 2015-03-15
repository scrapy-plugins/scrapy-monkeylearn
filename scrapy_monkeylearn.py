# -*- coding: utf-8 -*-
import json
import scrapy

from scrapy.exceptions import NotConfigured


CLASSIFY_TEXT_URL = 'https://api.monkeylearn.com/api/v1/categorizer/{classifier}/classify_text/'

ML_CLASSIFIER = 'MONKEYLEARN_CLASSIFIER'
ML_AUTH = 'MONKEYLEARN_AUTH_TOKEN'
ML_CLASSIFY_FIELDS = 'MONKEYLEARN_CLASSIFIER_FIELDS'
ML_CATEGORIES_FIELD = 'MONKEYLEARN_CATEGORIES_FIELD'


class ConfigError(Exception):
    """Raised when the value of a configuration option is different from the
    expected one."""

    def __init__(self, option_name, expected_type, found_type):
        """Constructor."""
        self.option_name = option_name
        self.expected_type = expected_type
        self.found_type = found_type

    def __str__(self):
        msg = "The value of %s should be of type %s, but found %s."
        return msg % (self.option_name,
                      self.expected_type.__name__,
                      self.found_type.__name__)


class MonkeyLearnPipeline(object):
    """A pipeline to classify items."""

    log_header = '[MonkeyLearnPipeline] '

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        "Constructor."
        super(MonkeyLearnPipeline, self).__init__()
        self.crawler = crawler

        # Extract configuration
        self.classifier = crawler.settings.get(ML_CLASSIFIER)
        self.auth_token = crawler.settings.get(ML_AUTH)
        self.classifier_fields = crawler.settings.get(ML_CLASSIFY_FIELDS)
        self.categories_field = crawler.settings.get(ML_CATEGORIES_FIELD)

        # Check required options
        if not all((
                self.classifier,
                self.auth_token,
                self.classifier_fields,
                self.categories_field)):
            raise NotConfigured('missing options')

        # Validate options
        if not isinstance(self.classifier, str):
            raise ConfigError(option_name=ML_CLASSIFIER,
                              expected_type=str,
                              found_type=type(self.classifier))

        if not isinstance(self.auth_token, str):
            raise ConfigError(option_name=ML_AUTH,
                              expected_type=str,
                              found_type=type(self.auth_token))

        if not isinstance(self.classifier_fields, list):
            raise ConfigError(option_name=ML_CLASSIFY_FIELDS,
                              expected_type=list,
                              found_type=type(self.classifier_fields))

        if not isinstance(self.categories_field, str):
            raise ConfigError(option_name=ML_CATEGORIES_FIELD,
                              expected_type=str,
                              found_type=type(self.category_field))

    def process_item(self, item, spider):
        request = self._make_request(item, spider)
        dfd = self.crawler.engine.download(request, spider)
        dfd.addCallback(self.check_response, item)
        dfd.addErrback(self.handle_error, item)
        return dfd

    def _make_request(self, item, spider):
        text_to_classify = u' '.join([item[field_name]
                                     for field_name in self.classifier_fields])
        body = json.dumps({'text': text_to_classify})
        request = scrapy.Request(
            CLASSIFY_TEXT_URL.format(classifier=self.classifier),
            method='POST',
            headers={
                'Authorization': 'Token {}'.format(self.auth_token),
                'Content-Type': 'application/json'},
            body=body)
        self.crawler.stats.inc_value('monkeylearn_api/requests_count')
        return request

    def check_response(self, response, item):
        self.crawler.stats.inc_value('monkeylearn_api/response_count')
        self.crawler.stats.inc_value(
            'monkeylearn_api/response_status_count/{}'.format(response.status))
        if response.status != 200:
            scrapy.log.msg(
                self.log_header % 'Non 200 response from api {0}'.format(response.url),
                scrapy.log.ERROR)
            return item

        json_data = json.loads(response.body)
        categories = json_data['result']
        item[self.categories_field] = categories
        return item

    def handle_error(self, failure, item):
        message = 'error when parsing api response {0} Traceback'.format(item.get('url'))
        message += failure.getBriefTraceback()
        scrapy.log.err(self.log_header + message)
        return item
