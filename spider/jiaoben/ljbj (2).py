# -*- coding: utf-8 -*-
import scrapy


class LjbjSpider(scrapy.Spider):
    name = "ljbj"
    allowed_domains = ["crawl"]
    start_urls = ['http://crawl/']

    def parse(self, response):
        pass
