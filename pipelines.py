# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
import pymysql


class WangyiyunPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.list=[]

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
        self.connection = pymysql.connect(host='127.0.0.1',
                                     port=3306,
                                     user='root',
                                     password='393622951',
                                     db='wyy_music',
                                     charset='utf8')
        self.db = self.client[self.mongo_db]



    def process_item(self, item, spider):
        print(item)
        # self.list.append(item['song_name'])
        # print(item['_id'])
        cursor = self.connection.cursor()
        sql = f"INSERT INTO `wyy_singer` (`singer_id`, `singer_name`,`singer_classify`,`singer_classify_id`,`singer_img`) VALUES ('{item['singer_id']}','{item['singer_name']}','{item['singer_classify']}','{item['singer_classify_id']}','{item['singer_img']}')"
        print(sql)
        effect_row = cursor.execute(sql)
        effect_row = cursor.execute(
            'INSERT INTO `wyy_song` (`song_id`, `song_name`,`album`,`song_img`,`singer_id`,`singer_name`,`download_url`) VALUES (%s, %s,%s,%s,%s,%s,%s)',
            (item['_id'], item['song_name'], item['album'], item['song_img'],item['singer_id'],item['singer_name'],
             item['download_url']))
        print(effect_row)
        self.connection.commit()
        cursor.close()
        result = self.db['wyy_music'].insert_one(item)
        return item

    def close_spider(self, spider):
        # self.list = list(set(self.list))
        print(self.list)
