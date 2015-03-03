CLASSIFY_TEXT_URL = 'https://app.monkeylearn.com/api/v1/categorizer/%s/classify_text/'

def classify_text(classifier, text, token):
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

    def __init__(self):
        pass

    def process_item(self, item, spider):
        return item
