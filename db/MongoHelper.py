# -*- coding: utf-8 -*-

import pymongo
from config import DB_CONFIG, DEFAULT_SCORE

from ISqlHelper import ISqlHelper
import traceback
import json
import codecs
import chardet

class MongoHelper(ISqlHelper):
    '''''初始化MongoHelper
    '''
    def __init__(self):
      self.connection = pymongo.MongoClient('localhost:27017', connect=False)
      self.db=self.connection.db_def
      self.collection=self.db.collection_def
      print(self.connection)
      print(self.db)
      print(self.collection)

    '''''初始化MongoHelper 数据库
    '''
    def init_db(self,db):
      self.db=db
      print(self.db)

    '''''初始化 数据库内 集合
    '''
    def select_colletion(self,arg0):
      if arg0==("ip_addr"):
        self.collection=self.db.ip_addr
        print(self.collection)
      elif arg0==("ip_addr_req"):
        self.collection=self.db.ip_addr_req
        print(self.collection)
      else:
        pass

    '''''丢弃 数据库内 集合
    '''
    def drop_db(self,arg0):
        self.connection.drop_database(arg0)

    '''''插入 数据
    '''
    def insert(self, value=None):
      if value:
        try:
          self.collection.insert(value)
          print(value)
        except:
          traceback.print_exc()
          time.sleep(3)
          pass

    '''''删除 数据
    '''
    def delete(self, conditions=None):
      if conditions:
        self.proxys.remove(conditions)
        return ('deleteNum', 'ok')
      else:
        return ('deleteNum', 'None')

    def update(self, conditions=None, value=None):
        # update({"UserName":"libing"},{"$set":{"Email":"libing@126.com","Password":"123"}})
        if conditions and value:
            self.proxys.update(conditions, {"$set": value})
            return {'updateNum': 'ok'}
        else:
            return {'updateNum': 'fail'}

    def select(self, count=None, conditions=None):
        if count:
            count = int(count)
        else:
            count = 0
        if conditions:
            conditions = dict(conditions)
            conditions_name = ['types', 'protocol']
            for condition_name in conditions_name:
                value = conditions.get(condition_name, None)
                if value:
                    conditions[condition_name] = int(value)
        else:
            conditions = {}
        items = self.proxys.find(conditions, limit=count).sort(
            [("speed", pymongo.ASCENDING), ("score", pymongo.DESCENDING)])
        results = []
        for item in items:
            result = (item['ip'], item['port'], item['score'])
            results.append(result)
        return results
        
        
    ''''' 查询table中，每项所占比例
    '''
    def cal_per_of_items(self):
#      print(self.collection.find_one())
      projection = {'start':0,'stop':0}
      total_dict=self.collection.find()
      total_count=self.collection.find().count()
      dict_count={}
      for item in total_dict:
        country=item['country']
        prov=item['prov']
        city=item['city']
        net=item['net']
        if country in dict_count:
          dict_count[country]+=1
        else:
          dict_count[country]=1
        if prov in dict_count:
          dict_count[prov]+=1
        else:
          dict_count[prov]=1
        if city in dict_count:
          dict_count[city]+=1
        else:
          dict_count[city]=1
        if net in dict_count:
          dict_count[net]+=1
        else:
          dict_count[net]=1
#          print(dict_count)
      f=codecs.open('./cal_per_of_items.txt','a+','utf8')
      for item in json.dumps(dict_count,ensure_ascii=False).split(','):
        f.write(item)
        f.write('\r\n')
        print(item)
      f.flush()
      f.close()      

      '''''      
      n = 4  
      matrix = [None]*n  
      for i in range(len(matrix)):  
      matrix[i] = [0]*3  
      print(matrix)  
      '''
      
    ''''' 讲file内容录入数据库,file为ip地址与物理地址对应关系
    '''    
    def  insert_File(str):
      with open(str,'r') as f:
        lines=f.readlines()
        for line in lines:
          wds=line.split(',')
          dict={}
          dict['req_ip']=wds[0]
          dict['start']=wds[1]
          dict['stop']=wds[2]
          dict['country']=wds[3]
          dict['prov']=wds[4]
          dict['city']=wds[5]
          dict['net']=wds[6]
          mongohelper.insert(dict)

if __name__ == '__main__':
  mongohelper=MongoHelper()
  mongohelper.select_colletion('ip_addr_req')
  mongohelper.cal_per_of_items()


