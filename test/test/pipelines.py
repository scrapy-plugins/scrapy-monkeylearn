# Pipelines

DB = []

class StorePipeline(object):

    def __init__(self):
        "Constructor."
        super(StorePipeline, self).__init__()

    def process_item(self, item, spider):
        "Add the item to the DB."
        DB.append(item)
        return item
