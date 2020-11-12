import scrapy
import re
from wangyiyun.items import WangyiyunItem
from scrapy_selenium import SeleniumRequest


class WangYiYunSpider(scrapy.Spider):
    name = "wyy_spider"

    # start_urls = []
    start_urls = ["https://music.163.com/discover/artist/cat?id=1001"]

    # def start_requests(self):
    #     for i in ['1001','1002','1003','2001','2002','2003','6001','6003','7001','7002','7003']:
    #         url = f"https://music.163.com/discover/artist/cat?id={i}"
    #         yield scrapy.Request(url, callback=self.parse,encoding="utf-8",meta={'flag':False,'dont_merge_cookies': True})

    def parse(self, response):
        # print(response.xpath('//html').get())
        list = response.xpath('//ul[@id="m-artist-box"]/li')
        singClassify = response.xpath('//a[contains(@class,"z-slt")]/text()').get()
        request_url = response.request.url
        singClassifyId = re.findall(r'id=(\d+)',request_url)[0]
        # print(list.getall())
        for item in list :
            # print(item.get())
            href = item.xpath('.//a[@class="msk"]/@href').get()
            singer_id = re.findall('id=(\d+)',href)[0]
            singer = {}
            singer['singer_classify'] = singClassify
            singer['singer_classify_id'] = singClassifyId
            # print(data)
            url = f"https://music.163.com/artist?id={singer_id}"
            # print("--------------------------")

            # request = scrapy.Request(url, callback=self.parse_singer,errback=self.err_singer, encoding="utf-8", meta={'flag': False,'dont_merge_cookies': True},
            #                          cb_kwargs={'singer':singer})
            yield SeleniumRequest(url=url,callback=self.parse_singer,errback=self.err_singer, encoding="utf-8", meta={'flag': False,'dont_merge_cookies': True},
                                    cb_kwargs={'singer':singer})
        # print(list)

    def parse_singer(self,response,singer):
        singer_img = response.xpath('//div[contains(@class,"n-artist")]/img/@src').get()
        list = response.xpath('//div[@id="song-list-pre-cache"]/ul[@class="f-hide"]/li')
        if not list:
            return None
        # print(list.getall())
        # print(singer)
        singer_id = response.xpath('//h2[@id="artist-name"]/@data-rid').get()
        singer_name = response.xpath('//h2[@id="artist-name"]/text()').get()
        for item in list:
            # print("----------------")
            if not item.get():
                continue
            # print(item.get())
            href = item.xpath('.//a/@href').get()
            # print(href)
            song_id = re.findall(r'id=(\d+)',href)[0]
            data = WangyiyunItem()
            data['song_name'] = item.xpath('.//a/text()').get()
            data['singer_id'] = singer_id
            data['singer_name'] = singer_name
            data['singer_classify'] = singer['singer_classify']
            data['singer_classify_id'] = singer['singer_classify_id']
            data['singer_img'] = singer_img
            # print(song_id)
            data['download_url'] = f"http://music.163.com/song/media/outer/url?id={song_id}"
            url=f"https://music.163.com/song?id={song_id}"
            data['_id'] = song_id
            # print("------------")

            # request = scrapy.Request(url=url, callback=self.parse_song, encoding="utf-8", meta={'flag': False,'dont_merge_cookies':True},
            #                          errback=self.err_song,
            #                cb_kwargs={'data':data})
            yield SeleniumRequest(url=url, callback=self.parse_song, encoding="utf-8", meta={'flag': False,'dont_merge_cookies':True},
                                     errback=self.err_song,
                           cb_kwargs={'data':data})


    def parse_song(self,response,data):
        # data = response.meta['data']
        data['song_img'] = response.xpath('//img[@class="j-img"]/@data-src').get()
        data['album']   = response.xpath('//div[@class="m-lycifo"]//p[@class="des s-fc4"][2]/a[@class="s-fc7"]/text()').get()
        # print(main_url)
        # print(data['singer'])
        # print(data['song_name'])
        # print(data['_id'])
        print(data)
        # print("----------")
        yield data

    def err_song(self, failure):
        print(failure.request.cb_kwargs['data'])
        # yield dict(
        #     main_url=failure.request.cb_kwargs['main_url'],
        # )

    def err_singer(self, failure):
        print(failure.request.cb_kwargs['data'])