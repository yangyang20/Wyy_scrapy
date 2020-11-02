import scrapy
import re
from wangyiyun.items import WangyiyunItem

class WangYiYunSpider(scrapy.Spider):
    name = "wyy_spider"

    start_urls = []
    # start_urls = ["https://music.163.com/discover/artist/cat?id=1001"]

    def start_requests(self):
        for i in ['1001','1002','1003','2001','2002','2003','6001','6003','7001','7002','7003']:
            url = f"https://music.163.com/discover/artist/cat?id={i}"
            yield scrapy.Request(url, callback=self.parse,encoding="utf-8",meta={'flag':False})

    def parse(self, response):
        # print(response.xpath('//html').get())
        list = response.xpath('//ul[@id="m-artist-box"]/li')
        singClassify = response.xpath('//a[contains(@class,"z-slt")]/text()').get()
        request_url = response.request.url
        singClassifyId = re.findall(r'id=(\d+)',request_url)[0]
        # print(list)
        for item in list :
            # print(item.get())
            data = WangyiyunItem()
            # data['img'] = item.xpath('.//img/@src').get()
            href = item.xpath('.//a[@class="msk"]/@href').get()
            data['singer'] = item.xpath('.//a[contains(@class,"nm")]/text()').get()
            data['singer_id']= re.findall('id=(\d+)',href)[0]
            data['singer_classify'] = singClassify
            data['singer_classify_id'] = singClassifyId
            # data['title'] = item.xpath('.//a[@class="nm nm-icn f-thide s-fc0"]/@title').get()
            # print(data)
            url = f"https://music.163.com/artist?id={data['singer_id']}"
            # print("--------------------------")
            yield scrapy.Request(url,callback=self.parse_singer,encoding="utf-8",meta={'flag':True,'data':data})
        # print(list)

    def parse_singer(self,response):
        data = response.meta['data']
        singer_img = response.xpath('//div[contains(@class,"n-artist")]/img/@src').get()
        list = response.xpath('//div[@id="song-list-pre-cache"]/ul[@class="f-hide"]/li')
        # print(list)
        # print("1111111")
        for item in list:
            # print("----------------")
            # print(item.get())
            data['song_name'] = item.xpath('.//a/text()').get()
            href = item.xpath('.//a/@href').get()
            song_id = re.findall(r'id=(\d+)',href)[0]
            data['download_url'] = f"http://music.163.com/song/media/outer/url?id={song_id}"
            url=f"https://music.163.com/song?id={song_id}"
            data['_id'] = song_id
            # print("------------")
            yield scrapy.Request(url=url,callback=self.parse_song,encoding="utf-8",meta={'flag':True,'data':data})


    def parse_song(self,response):
        data = response.meta['data']
        data['song_img'] = response.xpath('//img[@class="j-img"]/@data-src').get()
        data['album']   = response.xpath('//div[@class="m-lycifo"]//p[@class="des s-fc4"][2]/a[@class="s-fc7"]/text()').get()
        print(data)
        item = data
        # print(data)
        # print("----------")
        yield item