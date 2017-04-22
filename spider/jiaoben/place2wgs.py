#!/usr/bin/python
#coding:utf-8
#/scrapyredis/selenium/place2wgs.py

import xlrd
import xlwt
import requests
import urllib
import math
import re

pattern_x=re.compile(r'"x":(".+?")')
pattern_y=re.compile(r'"y":(".+?")')

class place2wgs:

    def __init__(self):
        pass

    def addres2wgs(self, pro, city, addr):
      loca=self.get_mercator(pro, city, addr) 
      return self.mercator2wgs84(loca)

    def mercator2wgs84(self, mercator):
      print "INFO============mercator2wgs84 start"
      #key1=mercator.keys()[0]
      #key2=mercator.keys()[1]
      point_x=mercator[0]
      point_y=mercator[1]
      x=point_x/20037508.3427892*180
      y=point_y/20037508.3427892*180
      y=180/math.pi*(2*math.atan(math.exp(y*math.pi/180))-math.pi/2)
      print "INFO============mercator2wgs84 succ"
      return (x,y)

    def throws(self, e):
        raise RuntimeError('this is the error message %s' % e)
    
    def get_mercator(self, pro, city, addr):
        location=(-1,-1)
        addr=urllib.quote(addr.encode('utf8'))
        city=urllib.quote(city.encode('utf8'))
        pro =urllib.quote(pro.encode('utf8'))
        quote_addr=pro+city+addr
        s=urllib.quote(city.encode('utf8'))
        api_addr="http://api.map.baidu.com/?qt=gc&wd=%s&cn=%s&ie=utf-8&oue=1&fromproduct=jsapi&res=api&callback=BMap._rd._cbk62300"%(quote_addr,s)
        try:
            req=requests.get(api_addr)
        except Exception, e:
            self.throws(e)
        print(req)
        content=req.content
        x=re.findall(pattern_x,content)
        y=re.findall(pattern_y,content)
        if x:
            x=x[0]
            y=y[0]
            x=x[1:-1]
            y=y[1:-1]
            x=float(x)
            y=float(y)
            print('%f, %f'% (x,y))
            location=(x,y)
        else:
            location=()
        return location


    #===================    
    #input file : xls
    #datasheet : 0
    #col : 0
    #-------------------    
    def run(filepath):
      data=xlrd.open_workbook(filepath)
      print "INFO============open file Book2.xls"
      rtable=data.sheets()[0]
      nrows=rtable.nrows
      values=rtable.col_values(0)
      workbook=xlwt.Workbook()
      wtable=workbook.add_sheet('data',cell_overwrite_ok=True)
      row=0
      for value in values:
        print "INFO===========values",value
        mercator=get_mercator(value)
        if mercator:
          wgs=mercator2wgs84(mercator)
        else:
          wgs=('NotFound','NotFound')
        print"%s,%s,%s"%(value,wgs[0],wgs[1])
        wtable.write(row,0,value)
        wtable.write(row,1,wgs[0])
        wtable.write(row,2,wgs[1])
        row=row+1
        print "INFO============save data.xls"
        workbook.save('data.xls')
    
    if __name__=='__main__':
      print "INFO===========START WORK"
      run()
