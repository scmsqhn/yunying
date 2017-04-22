# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

class MyscrapyPipeline(object):

    def __init__(self):
        print('json write __init__!')
        self.f = codecs.open('tempdat.json', 'w', encoding='utf-8')  
    
    def process_item(self, item, spider):
        print('process_item')
        dictobj = dict(item) 
        jsobj = json.dumps(dictobj, ensure_ascii=False) + "\n"  
        self.f.write(jsobj)
        spider.logger.info('+++++++Pipeline_process_item_write+++++++++++++++++++')

    def spider_closed(self, spider):
        print('spider_closed!')
        self.f.close()

