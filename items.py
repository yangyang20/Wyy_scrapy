# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WangyiyunItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    download_url =  scrapy.Field()
    song_name = scrapy.Field()
    album = scrapy.Field()
    song_img = scrapy.Field()

    singer_id = scrapy.Field()
    singer_name = scrapy.Field()
    singer_classify = scrapy.Field()
    singer_classify_id = scrapy.Field()
    singer_img = scrapy.Field()
    _id = scrapy.Field()
    # singId = scrapy.Field()
    # pass
