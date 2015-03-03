CLASSIFY_TEXT_URL = 'https://app.monkeylearn.com/api/v1/categorizer/%s/classify_text/'

ML_CLASSIFIER = 'MONKEYLEARN_CLASSIFIER'
ML_AUTH = 'MONKEYLEARN_AUTH_TOKEN'
ML_CLASSIFY_FIELDS = 'MONKEYLEARN_CLASSIFIER_FIELDS'
ML_CATEGORY_FIELD = 'MONKEYLEARN_CATEGORY_FIELD'

def _classify_text(classifier, text, token):
    return requests.post(
        CLASSIFY_TEXT_URL % classifier,
        headers={
            "Authorization": "token " + token,
        },
        params={
            "text": text
        }
    )

class MonkeyLearnPipeline(object):
    """A pipeline to classify items."""

    classifier = None
    auth_token = None
    classifier_fields = None
    category_field = None

    def __init__(self, crawler):
        "Constructor, extract configuration information."
        super(MonkeyLearnPipeline, self).__init__()
        self.classifier = crawler.settings[ML_CLASSIFIER]
        self.auth_token = crawler.settings[ML_AUTH]
        self.classifier_fields = crawler.settings[ML_CLASSIFY_FIELDS]
        self.category_field = crawler.settings[ML_CATEGORY_FIELD]

    def process_item(self, item, spider):
        "Classify an item."
        # Extract fields
        text_to_classify = ""
        # Classify item
        # Store category
        # Return item
        return item
