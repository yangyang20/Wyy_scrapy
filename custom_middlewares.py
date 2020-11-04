import scrapy
from fake_useragent import UserAgent
import fake_useragent
class CustormMiddlewares(object):
    def __init__(self):
        self.proxies = []


    def process_request(self,request,spider):
        '''
        请求中间,是否使用代理
        '''
        if 'flag' in request.meta and not request.meta['flag']:
            # print("111111111")
            # ua = UserAgent().random
            # print(ua)
            # request.headers.setdefault('User-Agent',ua)
            return None
        # return None 表示用下载器下载。
        return None







