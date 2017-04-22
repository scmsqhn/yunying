#!/usr/bin/python
#coding:utf-8

import xlrd
import xlwt
import requests
import urllib
import math
import re

pattern_x=re.compile(r'"x":(".+?")')
pattern_y=re.compile(r'"y":(".+?")')

def mercator2wgs84(mercator):
  print "INFO============mercator2wgs84 start"
  #key1=mercator.keys()[0]
  #key2=mercator.keys()[1]
  point_x=mercator[0]
  point_y=mercator[1]
  x=point_x/20037508.3427892*180
  y=point_y/20037508.3427892*180
  y=180/math.pi*(2*math.atan(math.exp(y*math.pi/180))-math.pi/2)
  print "INFO============mercator2wgs84 succ"
#  x,y = x-0.01185,y-0.00328
  return (x,y)

def get_mercator(addr):
  print "INFO============get_mercator start"
  quote_addr=urllib.quote(addr.encode(u'utf8'))
  city=urllib.quote(u'成都市'.encode(u'utf8'))
  province=urllib.quote(u'四川'.encode(u'utf8'))
  if False:#quote_addr.startswith(city) or quote_addr.startswith(province):
    print "INFO============mercator2wgs84 succ"
    pass
  else:
    print "INFO============getposition start"
    quote_addr=city+quote_addr
    s=urllib.quote(u'成都市'.encode(u'utf8'))
    api_addr="http://api.map.baidu.com/?qt=gc&wd=%s&cn=%s&ie=utf-8&oue=1&fromproduct=jsapi&res=api&callback=BMap._rd._cbk62300"%(quote_addr,s)
    req=requests.get(api_addr)
    content=req.content
    print content
    x=re.findall(pattern_x,content)
    y=re.findall(pattern_y,content)
    print "INFO============getposition handle data"
    if x:
      x=x[0]
      y=y[0]
      x=x[1:-1]
      y=y[1:-1]
      x=float(x)
      y=float(y)
      location=(x,y)
    else:
      print "INFO============getposition lost"
      location=()
    print "INFO============getposition return data"
    return location

def run():
  data=xlrd.open_workbook('G:\ProgramData\Anaconda2\usr\Book2.xls')
  print "INFO============open file Book2.xls"
  rtable=data.sheets()[0]
  nrows=rtable.nrows
  values=rtable.col_values(3)
  workbook=xlwt.Workbook()
  fout = open(r'G:\ProgramData\Anaconda2\usr\cd-db-17-wgs.txt', 'a+')
  datahead = u'wgsdata=[\n'.encode('utf-8')
  fout.write(datahead) #保存入结果文件
#  wtable=workbook.add_sheet(u'data',cell_overwrite_ok=True)
  row=0
  valuebase = u''
  dataitembase = u''
  for value in values[82696:]:
    if value == valuebase:
      fout.write(dataitembase) #保存入结果文件
      continue
    print "INFO===========values",value
    mercator=get_mercator(value)
    if mercator:
      print "INFO===========mercator2wgs84"
      wgs=mercator2wgs84(mercator)
    else:
      wgs=(u'NotFound','NotFound')
      continue
    print"%s,%s,%s"%(value,wgs[0],wgs[1])
    dataitem = '  (%s, %f, %f),\n' % (value, wgs[0], wgs[1])
    dataitem = dataitem.encode('UTF-8')
    print dataitem
    fout.write(dataitem) #保存入结果文件
    print "INFO============write ok "
    valuebase = value
    dataitembase = dataitem
  dataend = u']\n'.encode('utf-8')
  fout.write(dataend) #保存入结果文件
  print "INFO============save data.xls"
  
  def formatwgs():
    fin = open(r'G:\ProgramData\Anaconda2\usr\cd-db-17-wgs.txt', 'a+')
    
    
  
if __name__=='__main__':
  print "INFO===========START WORK"
  run()
  formatwgs()