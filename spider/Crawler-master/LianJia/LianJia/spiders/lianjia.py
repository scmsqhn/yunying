# -*- coding: utf-8 -*-
import scrapy
import requests
import re
import time
from lxml import etree
from ..items import LianjiaItem
from ..items import MyscrapyItemcd
from scrapy_redis.spiders import RedisSpider
from scrapy.conf import settings 
import random
import logging
class LianjiaSpider(RedisSpider):
    name = 'lianjiaspider'
    redis_key = 'lianjiaspider:urls'
    start_urls = ('http://cd.lianjia.com/ershoufang/')
    allowed_domains = ["lianjia.com"]

#http://cd.lianjia.com/
    def start_requests(self):
        self.logger.info('istart_requests') 
#        user_agent = random.choice(settings['AGENTS'])
#        headers = {'User-Agent': user_agent}
        self.logger.info(self.start_urls) 
#        self.logger.info(headers) 
        yield scrapy.Request(url=self.start_urls, method='GET', callback=self.parse)

    def parse(self, response):
        self.logger.info(response)
        user_agent = random.choice(settings['AGENTS'])
        headers = {'User-Agent': user_agent}
        lists = response.body.decode('utf-8')
        selector = etree.HTML(lists)
        area_list = selector.xpath('/html/body/div[3]/div[1]/dl[2]/dd/div[1]/div/a')
        for area in area_list:
#            #try:
                area_han = area.xpath('text()').pop()    # 地点
                area_pin = area.xpath('@href').pop().split('/')[2]   # 拼音
                area_url = 'http://cd.lianjia.com/ershoufang/{}/'.format(area_pin)
                print(area_url)
                user_agent = random.choice(settings['AGENTS'])
                headers = {'User-Agent': user_agent}
                px = "http://%s" % random.choice(settings['PROXYS'])['ip_port']
                self.logger.info(px) 
                self.logger.info(area_url) 
                yield scrapy.Request(url=area_url, headers=headers, callback=self.detail_url, meta={"id1":area_han,"id2":area_pin, "proxy":str(px)})
            #except Exception:
                #pass

    def get_latitude(self,url):  # 进入每个房源链接抓经纬度
        p = requests.get(url)
        contents = etree.HTML(p.content.decode('utf-8'))
        latitude = contents.xpath('/ html / body / script[19]/text()').pop()
        time.sleep(random.randint(3,120))
        regex = '''resblockPosition(.+)'''
        items = re.search(regex, latitude)
        content = items.group()[:-1]  # 经纬度
        longitude_latitude = content.split(':')[1]
        self.logger.info(longitude_latitude)
        return longitude_latitude[1:-1]

    def detail_url(self,response):
        self.logger.info(response)
        'http://cd.lianjia.com/ershoufang/dongcheng/pg2/'
        for i in range(1,101):
                url = 'http://cd.lianjia.com/ershoufang/{}/pg{}/'.format(response.meta["id2"],str(i))
                time.sleep(random.randint(3,120))
            ##try:
                contents = requests.get(url)
                contents = etree.HTML(contents.content.decode('utf-8'))
                houselist = contents.xpath('/html/body/div[4]/div[1]/ul/li')
                for house in houselist:
                    #try:
                        item = MyscrapyItemcd()
                        item['title'] = house.xpath('div[1]/div[1]/a/text()').pop()
                        item['community'] = house.xpath('div[1]/div[2]/div/a/text()').pop()
                        item['model'] = house.xpath('div[1]/div[2]/div/text()').pop().split('|')[1]
                        item['area'] = house.xpath('div[1]/div[2]/div/text()').pop().split('|')[2]
                        item['focus_num'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[0]
                        item['watch_num'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[1]
                        item['time'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[2]
                        item['price'] = house.xpath('div[1]/div[6]/div[1]/span/text()').pop()
                        item['average_price'] = house.xpath('div[1]/div[6]/div[2]/span/text()').pop()
                        item['link'] = house.xpath('div[1]/div[1]/a/@href').pop()
                        item['city'] = response.meta["id1"]
                        self.url_detail = house.xpath('div[1]/div[1]/a/@href').pop()
                        item['Latitude'] = self.get_latitude(self.url_detail)
                    #/except Exception:
                        #pass
                        yield item
            #except Exception:
                #pass
