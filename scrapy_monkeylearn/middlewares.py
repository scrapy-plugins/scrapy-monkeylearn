import scrapy
from monkeylearn import MonkeyLearn
from scrapy.exceptions import NotConfigured


class MonkeylearnMiddleware(object):
    def __init__(self, token, module_id, field_to_classify,
                 field_classification_output, batch_size, use_sandbox):
        self.items = []
        self.token = token
        self.module_id = module_id
        self.ml = MonkeyLearn(token)
        self.field_to_classify = field_to_classify
        self.field_classification_output = field_classification_output
        self.batch_size = batch_size
        self.use_sandbox = use_sandbox

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        if (not crawler.settings.get('MONKEYLEARN_TOKEN') or
                not crawler.settings.get('MONKEYLEARN_MODULE') or
                not crawler.settings.get('MONKEYLEARN_FIELD_OUTPUT') or
                not crawler.settings.get('MONKEYLEARN_FIELD_TO_PROCESS')):
            raise NotConfigured

        token = crawler.settings.get('MONKEYLEARN_TOKEN')
        module_id = crawler.settings.get('MONKEYLEARN_MODULE')
        field_to_classify = crawler.settings.get('MONKEYLEARN_FIELD_TO_PROCESS')
        field_classification_output = crawler.settings.getlist('MONKEYLEARN_FIELD_OUTPUT')
        batch_size = crawler.settings.get('MONKEYLEARN_BATCH_SIZE', 200)
        use_sandbox = crawler.settings.get('MONKEYLEARN_USE_SANDBOX', False)

        middleware = cls(token, module_id, field_to_classify,
                         field_classification_output, batch_size, use_sandbox)

        return middleware

    def process_spider_output(self, response, result, spider):
        for elem in result:
            if isinstance(elem, scrapy.Item):
                if ((isinstance(self.field_to_classify, list) or
                        isinstance(self.field_to_classify, tuple)) and
                        all([field in elem for field in self.field_to_classify])):
                    self.items.append(elem)
                elif isinstance(self.field_to_classify, basestring) and self.field_to_classify in elem:
                    self.items.append(elem)
                else:
                    yield elem
            else:
                yield elem

        if len(self.items) > self.batch_size:
            if isinstance(self.field_to_classify, list) or isinstance(self.field_to_classify, tuple):
                text_list = [
                    ' '.join([unicode(item[elem]) for elem in self.field_to_classify])
                    for item in self.items
                ]
            else:
                text_list = [unicode(item[self.field_to_classify]) for item in self.items]
            if self.module_id.startswith('cl_'):
                res = self.ml.classifiers.classify(
                    self.module_id,
                    text_list,
                    sandbox=self.use_sandbox
                ).result
            elif self.module_id.startswith('ex_'):
                res = self.ml.extractors.extract(
                    self.module_id,
                    text_list
                ).result
            else:
                res = self.ml.pipelines.run(
                    self.module_id,
                    text_list
                ).result
            items = self.items
            self.items = []
            for i, item in enumerate(items):
                item[self.field_classification_output] = res[i]
                yield item
