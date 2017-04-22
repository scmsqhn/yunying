# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from .items import LianjiaItem
from .items import MyscrapyItemcd
import codecs
import json



class LianjiaPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        db_name = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host,port=port)
        tdb = client[db_name]
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        if isinstance(item,LianjiaItem):
            try:
                info = dict(item)
                if self.post.insert(info):
                    print('bingo')
            except Exception:
                pass
        return item

class MyscrapyPipeline(object):

    def __init__(self):
        print('json write __init__!')
        self.f = codecs.open('tempdat.json', 'w', encoding='utf-8')
        self.f2 = codecs.open('tempdat2.json', 'w', encoding='utf-8')
   
    def process_item(self, item, spider):

        if(isinstance(item, MyscrapyItemcd)):
            print('process_item_cd')
            dictobj = dict(item)
            jsobj = json.dumps(dictobj, ensure_ascii=False) + "\n"
            self.f2.write(jsobj)
            spider.logger.info('+++++++Pipeline_process_item_write+++++++++++++++++++')

        elif(isinstance(item, MyscrapyItem)):
            print('process_item_bj')
            dictobj = dict(item)
            jsobj = json.dumps(dictobj, ensure_ascii=False) + "\n"
            self.f.write(jsobj)
            spider.logger.info('+++++++Pipeline_process_item_write+++++++++++++++++++')

    def spider_closed(self, spider):
        print('spider_closed!')
        self.f.close()
        self.f2.close()
