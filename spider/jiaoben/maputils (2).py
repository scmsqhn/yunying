#!/usr/bin/python
# coding:utf-8
# sqlitetool.py
import sqlite3
import sys
import sys
import place2wgs
import xlrd
import xlwt
import chardet 
import time
import re
from pymongo import *
import vincent



reload(sys)
sys.setdefaultencoding('utf8')

DATABASE = 'musql3-lj.db'
TABLE = 'bj_lj_esf_demo'

      
class mongotool:

    def __init__(self):

        client = MongoClient('localhost', 27017)
        client = MongoClient('mongodb://localhost:27017')

        self.db = client.test_db
        self.collection = self.db.test_collection
        self.wgscol = self.db.wgscol
        self.paoya = self.db.paoya  
        self.area_paoya = self.db.area_paoya  

    def insertlist(self):
        
        fin=open('ljcd2.json', 'r')
        lines=fin.readlines()
        count=1
        mglist=[]
        for line in lines:
            it=eval(line)
            item = [count, str(it['title']), str(it['house']),\
                    str(it['price']), str(it['build']), \
                    str(it['buyer']), str(it['mipri'])]

            mgcell={'_id':item[0], "title":item[1], 'house':item[2], \
                    'price': item[3] ,'build':item[4], 'buyer':item[5],\
                    'mipri': item[6]}

            mglist.append(mgcell)
            count=count+1
            print count
            self.db.test_collection.insert(mgcell)
       # self.db.collection.insert_many(mglist)

    def selectitem(self):
        for i in self.collection.find({'_id':1}):           
             print i



    def match_address(self, dicts):
          area =dicts["build"]
          area =area.split('-')
          area =area[1].strip()#.decode('utf8')

          house=dicts["house"]
          house=house.split('|')
          house=house[0].strip()#.decode('utf8')

          pro = (u'四川') 
          city= (u'成都') 

          addrstr=(pro+city+area+'\n')
          #print chardet.detect(addrstr)
          return addrstr
           
    def insertlist_wgs(self):
        
        fin=open('ljcd_wgs.txt', 'r')
        lines=fin.readlines()
        count=1
        mglist=[]
        count=0
        for line in lines:
            line = line.split(',')
            addt   =line[0]
            wgsj   =re.search('\d+',line[1])
            wgsw   =re.search('\d+',line[1])
            price  =line[2]
            print addt
            print wgsj
            print wgsw
            print price


#            li.strip().encode('utf8')
            item = {'_id':count, \
                    'addr':line[1],\
                    'wgsj':line[2],\
                    'wgsw':line[3],\
                    'price':line[4]
                   }
            self.wgscol.insert(item)
            count=count+1

    def insertlist_py(self):
        self.paoya.remove()
        
        fin=open('paoya.txt', 'r')
        lines=fin.readlines()
        count=1
        mglist=[]
        count=0
        for line in lines:
            line = line.split(',')
            print line
            if line=='':
                break
            addr =line[0]
            wgsj =re.search('\d{2,3}\.\d{11,15}',line[1])
            wgsw =re.search('\d{2,3}\.\d{11,15}',line[2])
            print(type(wgsw))
            wgsj=wgsj.group(0).decode('ascii')
            wgsw=wgsw.group(0).decode('ascii')
            price=line[3]
            item = {'_id':count,  'addr':addr, 'wgsj':wgsj, 'wgsw':wgsw, 'price':price}
            self.paoya.insert(item)
            count=count+1
        fin.close()

    def selectitem(self):
        for i in self.collection.find({'_id':1}):           
             print i

         
if __name__ == '__main__':
  reload(sys)
  sys.setdefaultencoding('utf8')
  f = mongotool()
  f.db.wgscol.ensure_index([('_id',ASCENDING),('addr',ASCENDING)])

  flag = 7 
  if flag==7:
      for i in range(1,18000):
          items=f.db.area_paoya.find_one({'_id':i})
          for j in items:
              print items[j]


  if flag==6:
      fin = open('paoya.txt','r')
      lines = fin.readlines()
      count = 1
      for line in lines:
          line = line.split(',')
          item = {'_id':count,\
                  'addr':line[0],\
                  'price':line[1]
                 }
          print line[0]
          print line[1]
          f.db.area_paoya.insert(item) 
          count=count+1


  if flag==5:
    f.insertlist_py()


  if flag==4:
      print 'flag==4'
      for i in range(13000,14000):
          items=f.db.test_collection.find_one({'_id':i})
          print i
          for item in items:
              print items[item]
              pass
        
  if flag==3:
    f.wgscol.remove()
    f.insertlist_wgs()

  if flag==1:
    fout = open('paoya.txt', 'w')
    count=0
    addrstr=''
    price=-1
    addrlist=[]
    for i in range(1,18000):
        items=f.db.test_collection.find_one({'_id':i})
        try:
            addrstr = f.match_address(items).strip()
        except:
            continue
        if addrstr in addrlist:
            print 'addrstrs is already handled'
            continue
        print i 
        price = float(items['price'])
        for j in range(1,18000):
            try:
                items=f.db.test_collection.find_one({'_id':j})
                if addrstr == f.match_address(items).strip():
                    price = price+int(items['price'])
            except:
                continue
        fout.write(('%s, %d\n') % (addrstr, price))
        print(('%s, %d\n') % (addrstr, price))
        addrlist.append(addrstr)
        print(addrstr)
        print(price)
    fout.close()

  if flag==2:
    reload(sys)
    sys.setdefaultencoding('utf8')

    for i in f.wgscol.find():
        for j in i:
            print i['addr'] 
        break
#        print i
    

