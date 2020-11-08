import scrapy
from selenium import webdriver
from scrapy.http import HtmlResponse

from scrapy_selenium import SeleniumRequest

class CustormMiddlewares(object):
    def __init__(self):
        self.proxies = []


    def process_request(self,request,spider):
        '''
        请求中间,是否使用代理
        '''
        if 'flag' in request.meta and not request.meta['flag']:
            print(request)
            '''
            用selenium
            '''
            return None
            # return HtmlResponse(url=request.url, body=html_str, encoding='utf-8', request=request)
        # return None 表示用下载器下载。
        return None








