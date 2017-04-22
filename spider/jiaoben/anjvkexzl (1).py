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


class AnjvkexzlSpider(scrapy.Spider):
    name = "anjvkexzl"
    allowed_domains = ["cd.xzl.anjuke.com"]
    start_urls = 'http://cd.xzl.anjuke.com/'
    handle_httpstatus_list = [111, 404, 500]    
    def dum(self):
        time.sleep(random.randint(1, 3))

    def start_requests(self):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 \
                         Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': user_agent}
        yield scrapy.Request(url=self.start_urls, headers=headers, method='GET', callback=self.parse)


    def parse(self, response):
	if response.status in self.handle_httpstatus_list:
            proxy = random.choice(proxys)
            agent = random.choice(agents)
            headers.setdefault('User-Agent', agent)
            metas = "http://%s" % proxy['ip_port']
            self.logger.info('=================START_parse_404===================')
            self.logger.info('Spider opened: %s, %s' % (spider.name,request.meta['proxy']))
            self.logger.info('request: %s, %s' % (request.url, exception))
            self.logger.info('=================END_parse_404===================')
            yield scrapy.Request(url=response.url, callback=self.parse, meta={"proxy":metas}, method='GET', dont_filter=True )

        else:
            scrapy.log.msg()
            lists = response.body.decode('utf-8')
            selector = etree.HTML(lists)
            area_list = selector.xpath('/html/body/div[5]/div[2]/div/div[1]/div/a')
            for area in range[2:len(area_list)]:
                area_url = iselector.xpath('//*[@id="list-content"]/div[%d]' % area)
                print(area_url)
                self.log(('Parse function called on %s', response.url),level=log.INFO)
      	        self.log(('Parse function called on %s', response.url),level=log.INFO)
                yield scrapy.Request(url=area_url, callback=self.detail_url, dont_filter=True )

    #'http://cd.lianjia.com/ershoufang/dongcheng/pg2/'
    def detail_url(self,response):
       for i in range(1, 101):
            self.dum()
            contents = etree.HTML(response.body.decode('utf-8'))
            col1 = contents.xpath('//*[@id="fy_info"]/ul[1]')
            col2 = contents.xpath('//*[@id="fy_info"]/ul[2]')
            cols[2] = [col1, col2]
            
            self.dum();
            for col in cols:
                for i in col:
                item = AnjvkexzlItem()
                item['zizujin'] = house.xpath('//*[@id="fy_info"]/ul[%d]/li[%d]/span[2]',(col, i)).pop()
                item['yuezujin'] = house.xpath('//*[@id="fy_info"]/ul[%d]/li[%d]/span[2]',(col, i)).pop()
                item['loupan'] = house.xpath('//*[@id="fy_info"]/ul[%d]/li[%d]/span[2]',(col, i)).pop()
                item['dizhi'] = house.xpath('//*[@id="fy_info"]/ul[%d]/li[%d]/span[2]',(col, i)).pop()
                item['ditie'] = house.xpath('//*[@id="fy_info"]/ul[%d]/li[%d]/span[2]',(col, i)).pop()
                item['jzmianji'] = house.xpath('//*[@id="fy_info"]/ul[%d]/li[%d]/span[2]',(col, i)).pop()
                item['louceng'] = house.xpath('//*[@id="fy_info"]/ul[%d]/li[%d]/span[2]',(col, i)).pop()
                item['gongweishu'] = house.xpath('//*[@id="fy_info"]/ul[%d]/li[%d]/span[2]',(col, i)).pop()
                item['wuye'] = house.xpath('//*[@id="fy_info"]/ul[%d]/li[%d]/span[2]',(col, i)).pop()
                item['pingjia'] = house.xpath('//*[@id="xzl_desc"]/div/text()')
                self.logger.info('item is %s' % item)
            latitude = contents.xpath('/html/body/script[11]/text()').pop()
            relat = '''lat: ".*'''
            relng = '''lng: ".*'''
            j = re.search(relat, latitude)
            w = re.search(relng, latitude)
            j = j.split(':')[1]
            w = w.split(':')[1]
            item['jwd'] = jwd[j,w]
            yield item

