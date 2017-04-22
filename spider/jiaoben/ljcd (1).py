# -*- coding: utf-8 -*-
import scrapy
import re
import time
from lxml import etree
from scrapy import log
import random
import requests

from myscrapy.items import MyscrapyItemcd

import logging
'''
1. logging.CRITICAL - for critical errors (highest severity) 致命错误
2. logging.ERROR - for regular errors 一般错误
3. logging.WARNING - for warning messages 警告＋错误
4. logging.INFO - for informational messages 消息＋警告＋错误
5. logging.DEBUG - for debugging messages (lowest severity) 低级别
'''
  
logging.warning("This is a warning")

logging.log(logging.WARNING,"This is a warning")
from myscrapy.middlewares import agents
from myscrapy.middlewares import proxys 


class LjcdSpider(scrapy.Spider):
    name = "ljcd"
    allowed_domains = ["lianjia.com"]
    area = 'wuhou' 
    start_urls = 'http://cd.lianjia.com/ershoufang/%s/' % area
    base_urls =start_urls 
    handle_httpstatus_list = [111, 404, 500, 302, 110, 301]    

    urllist = []
   
    def geturllist():
      print("start2")
      fin = open('/myscrapy/myscrapy/outstr.txt', 'r')
      print("open")
      while fin.next:
        print("open")
        line = fin.readline()
        if (len(line)==0):
          print("read over")
          break
        print(line)
        self.urllist.append(str(line))

    def passrept(inurl):
        for i in self.urllist:
          print(i)
          obj = re.search(inurl, i,  re.M|re.I)
          if obj:
            print("catch it")
            return False
        print("download it")
        return  True



    def dum(self):
        time.sleep(random.randint(1, 1))


    def randomproxy(self):
        d1 = random.randint(1, 255)
        d2 = random.randint(1, 255)
        d3 = random.randint(1, 255)
        d4 = random.randint(1, 255)
        d5 = random.randint(1, 9999)
        ip = ("http://%s.%s.%s.%s:%s" % (str(d1), str(d2), str(d3), str(d4), str(d5)))
        self.logger.info("+++++++++++++++++++, %s" % ip)
        return ip

    def start_requests(self):
       # self.geturllist()
        self.logger.info('=================START_request===================\n')
        user_agent = random.choice(agents)
        headers = {'User-Agent': user_agent}
#        yield scrapy.Request(url=self.start_urls, headers=headers,  method='GET', callback=self.parse)
        yield scrapy.Request(url=self.start_urls, headers=headers,  method='GET', callback=self.detail_url)

    def parse(self, response):
        self.logger.info('===response.status: %d' % response.status)
        self.dum()
        self.logger.info(response)
      	if (response.status in self.handle_httpstatus_list or (re.search(r'http://captcha.lianjia.com', response.url, re.M|re.I))):
            self.logger.info('response is %s' % response)
            self.logger.info('===response.status: %d' % response.status)
            proxy = random.choice(proxys)
            agent = random.choice(agents)
            headers = {'User-Agent', agent}
            metas = "http://%s" % proxy['ip_port']
           # meta = {"proxy":metas}
           # metas = self.randomproxy()
            self.logger.info('=================START_parse_404===================\n')
            self.logger.info('proxy:url %s, %s' % (metas, response.url))
            self.logger.info('=================END_parse_404===================\n')
       #     yield scrapy.Request(url=self.base_urls, callback=self.parse, meta={"proxy":metas}, method='GET', dont_filter=True)
           # if not passrept(inurl):
           #     self.logger.info('=================break URL==================\n')
           #     return None
            yield scrapy.Request(url=self.base_urls, method='GET', meta={"proxy":metas}, dont_filter=True)


        else:
            self.logger.info('=================START_parse_OK===================\n')
            self.logger.info('proxy:url %s' % response.url)
            self.logger.info('=================END_parse_ok===================\n')
            lists = response.body.decode('utf-8')
            selector = etree.HTML(lists)
            area_list = selector.xpath('/html/body/div[3]/div[1]/dl[2]/dd/div[1]/div/a')
            for area in area_list:
                area_han = area.xpath('text()').pop()    # 地点
                area_pin = area.xpath('@href').pop().split('/')[2]   # 拼音
                area_url = 'http://cd.lianjia.com/ershoufang/{}/'.format(area_pin)
                print(area_url)
                self.log(('Parse function called on %s', response.url),level=log.INFO)
      	        self.log(('Parse function called on %s', response.url),level=log.INFO)
           #     if not passrept(inurl):
           #         self.logger.info('=================break URL==================\n')
           #         return None
                yield scrapy.Request(url=area_url, callback=self.detail_url, meta={"id1":area_han,"id2":area_pin}, dont_filter=True )


    def get_latitude(self, url):  # 进入每个房源链接抓经纬度
        self.logger.info('=================START_parse_OK:%s\n' % url)
        p = requests.get(url)
        contents = etree.HTML(p.content.decode('utf-8'))
        latitude = contents.xpath('/ html / body / script[19]/text()').pop()
        self.dum()
        regex = '''resblockPosition(.+)'''
        items = re.search(regex, latitude)
        content = items.group()[:-1]  # 经纬度
        longitude_latitude = content.split(':')[1]
        self.base_urls = url
        fin = open('/myscrapy/myscrapy/outstr.txt', 'a')
        print("===========insert file===========")
        fin.writelines(url+'\n')
        return longitude_latitude[1:-1]

    #'http://cd.lianjia.com/ershoufang/dongcheng/pg2/'
    def detail_url(self,response):
      self.logger.info('=================response:%s' % response.url)
      self.logger.info(response)
      if (response.status in self.handle_httpstatus_list or (re.search(r'http://captcha.lianjia.com', response.url, re.M|re.I))):
        proxy = random.choice(proxys)
        agent = random.choice(agents)
        headers = {'User-Agent', agent}
        metas = "http://%s" % proxy['ip_port']
        # meta = {"proxy":metas}
        # metas = self.randomproxy()
        self.logger.info('=================START_parse_404===================\n')
        self.logger.info('proxy:url %s, %s' % (metas, response.url))
        self.logger.info('=================END_parse_404===================\n')
       #     yield scrapy.Request(url=self.base_urls, callback=self.parse, meta={"proxy":metas}, method='GET', dont_filter=True)
           # if not passrept(inurl):
           #     self.logger.info('=================break URL==================\n')
           #     return None
        yield scrapy.Request(url=self.base_urls, method='GET', meta={"proxy":metas}, dont_filter=True)
      else:      
         self.logger.info('=================detail_url:%s\n' % response.url)
         for i in range(1, 101):
              url = 'http://cd.lianjia.com/ershoufang/{}/pg{}/'.format(self.area, str(i))#response.meta["id2"], str(i))
              self.dum()
              contents = requests.get(url)
             # contents = response.body.decode('utf-8'))
              contents = etree.HTML(contents.content.decode('utf-8'))
              houselist = contents.xpath('/html/body/div[4]/div[1]/ul/li')
              for house in houselist:
                  try:
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
                    self.logger.info('item is %s' % item)
                    yield item
                  except:
                      pass
