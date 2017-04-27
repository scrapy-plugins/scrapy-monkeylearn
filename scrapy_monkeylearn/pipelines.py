# -*- coding: utf-8 -*-
import logging
from threading import Thread, Lock, Event

import six
from monkeylearn import MonkeyLearn
from scrapy.exceptions import NotConfigured
from scrapy import signals
from twisted.internet import defer

logger = logging.getLogger(__name__)


class MonkeyLearnPipeline(object):

    MAX_DELAY_BETWEEN_REQUESTS = 10

    def __init__(self, token, module_id, fields_to_classify,
                 field_classification_output, batch_size, use_sandbox, crawler):
        self.deferreds = []
        self.token = token
        self.module_id = module_id
        self.ml = MonkeyLearn(token)
        if isinstance(fields_to_classify, six.string_types):
            fields_to_classify = [fields_to_classify]
        elif not isinstance(fields_to_classify, (list, tuple)):
            fields_to_classify = []
        self.fields_to_classify = fields_to_classify
        self.field_classification_output = field_classification_output
        self.batch_size = batch_size
        self.use_sandbox = use_sandbox
        self.crawler = crawler
        self._lock = Lock()
        self._requester_thread = Thread(target=self._run_requester_thread)
        self._event = Event()
        self._stopped = False

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise NotConfigured otherwise
        required_settings = [
            'MONKEYLEARN_TOKEN',
            'MONKEYLEARN_MODULE',
            'MONKEYLEARN_FIELD_OUTPUT',
            'MONKEYLEARN_FIELD_TO_PROCESS'
        ]
        if not all(crawler.settings.get(s) for s in required_settings):
            raise NotConfigured

        token = crawler.settings.get('MONKEYLEARN_TOKEN')
        module_id = crawler.settings.get('MONKEYLEARN_MODULE')
        fields_to_classify = crawler.settings.getlist('MONKEYLEARN_FIELD_TO_PROCESS')
        field_classification_output = crawler.settings.get('MONKEYLEARN_FIELD_OUTPUT')
        batch_size = crawler.settings.get('MONKEYLEARN_BATCH_SIZE', 200)
        use_sandbox = crawler.settings.get('MONKEYLEARN_USE_SANDBOX', False)

        pipeline = cls(token, module_id,
                       fields_to_classify, field_classification_output,
                       batch_size, use_sandbox, crawler)
        crawler.signals.connect(pipeline.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signal=signals.spider_closed)

        return pipeline

    def process_item(self, item, spider):
        if (not self.fields_to_classify or
                not all([f in item for f in self.fields_to_classify])):
            return item
        dfd = defer.Deferred()
        with self._lock:
            self.deferreds.append((dfd, item))
            if len(self.deferreds) >= self.batch_size:
                self._event.set()
        return dfd

    def _run_requester_thread(self):
        while True:
            self._event.wait(self.MAX_DELAY_BETWEEN_REQUESTS)
            self._event.clear()
            if self._stopped:
                break
            # Requests to MonkeyLearn API should be issued from a separate thread.
            # This happens because pipeline returns deferreds that are activated
            # by the following method. If spider finishes before required amount of
            # items is collected in the batch this pipeline should call the API one
            # final time to cleanup. This cleanup cannot be done in spider_closed or
            # spider_idle handler because it causes job to deadlock. Requests associated
            # with the remaining items are not removed from active set in the engine slot
            # because respective deferreds were not activated yet and this blocks
            # spider_idle and spider_closed signals.
            logger.info('Sending request to MonkeyLearn API')
            try:
                self._analyze_items_batch_with_monkeylearn()
            except:
                logger.exception('Error requesting MonkeyLearn API')

    def _analyze_items_batch_with_monkeylearn(self):
        with self._lock:
            deferreds, self.deferreds = self.deferreds, []
        if not deferreds:
            return
        text_list = []
        for _, item in deferreds:
            text = ' '.join([
                six.text_type(item[f]).strip() for f in self.fields_to_classify
            ]).strip()
            text_list.append(text)
        self.crawler.stats.inc_value('monkeylearn_api/requests_count')
        if self.module_id.startswith('cl_'):
            result = self.ml.classifiers.classify(
                self.module_id, text_list, sandbox=self.use_sandbox).result
        elif self.module_id.startswith('ex_'):
            result = self.ml.extractors.extract(self.module_id, text_list).result
        else:
            result = self.ml.pipelines.run(self.module_id, text_list).result
        for i, (dfd, item) in enumerate(deferreds):
            item[self.field_classification_output] = result[i]
            # activate deferred
            dfd.callback(item)

    def spider_opened(self, spider):
        self._requester_thread.start()

    def spider_closed(self, spider):
        self._stopped = True
        self._event.set()
        self._requester_thread.join()
