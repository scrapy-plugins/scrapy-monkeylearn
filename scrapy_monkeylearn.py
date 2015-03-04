import requests
import json

CLASSIFY_TEXT_URL = 'https://api.monkeylearn.com/api/v1/categorizer/%s/classify_text/'

ML_CLASSIFIER = 'MONKEYLEARN_CLASSIFIER'
ML_AUTH = 'MONKEYLEARN_AUTH_TOKEN'
ML_CLASSIFY_FIELDS = 'MONKEYLEARN_CLASSIFIER_FIELDS'
ML_CATEGORIES_FIELD = 'MONKEYLEARN_CATEGORIES_FIELD'
ML_DEBUG = 'MONKEYLEARN_DEBUG'


def _classify_text(classifier, token, text):
    resp = requests.post(
        CLASSIFY_TEXT_URL % classifier,
        headers={
            'Authorization': 'Token ' + token,
            'Content-Type': 'application/json'
        },
        data=json.dumps({
            'text': text
        })
    )
    return resp.json()['result']


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

    classifier = None
    auth_token = None
    classifier_fields = None
    category_field = None

    def __init__(self, crawler):
        "Constructor."
        super(MonkeyLearnPipeline, self).__init__()

        # Extract configuration
        self.classifier = crawler.settings[ML_CLASSIFIER]
        self.auth_token = crawler.settings[ML_AUTH]
        self.classifier_fields = crawler.settings[ML_CLASSIFY_FIELDS]
        self.categories_field = crawler.settings[ML_CATEGORIES_FIELD]
        self.debug = crawler.settings[ML_DEBUG]

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

        if not isinstance(self.category_field, str):
            raise ConfigError(option_name=ML_CATEGORY_FIELD,
                              expected_type=str,
                              found_type=type(self.category_field))

    def process_item(self, item, spider):
        "Classify an item."
        # Extract fields
        text_to_classify = ""
        for field_name in self.classifier_fields:
            text = item[field_name]
            text_to_classify += text
        # Classify item
        if self.debug:
            categories = {}
        else:
            categories = _classify_text(classifier=self.classifier,
                                        token=self.auth_token,
                                        text=text_to_classify)
        # Store category
        item[self.categories_field] = categories
        # Return item
        return item
