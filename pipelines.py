# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo

class WangyiyunPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        '''
        爬虫启动之后，这个方法被执行
        :param crawler:
        :return:
        '''
        # pass
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'music')
        )

    def open_spider(self, spider):
        '''
        性能意义所在：
        :param spider:
        :return:
        '''

        self.client = pymongo.MongoClient(host='127.0.0.1',port=27017)
        self.db = self.client['wyy_music']



    def process_item(self, item, spider):
        print("111111111111")
        print(item)
        result = self.db['music'].insert_one(dict(item))
        return item
