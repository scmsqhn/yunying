#-*-coding:utf8-*-
import pymongo

connection = pymongo.MongoClient()
lj = connection.lianjia
post_info = lj.ershoufang

jike = {'name':u'极客', 'age':'5', 'skill': 'Python'}
god = {'name': u'玉皇大帝', 'age': 36000, 'skill': 'creatanything', 'other': u'王母娘娘不是他的老婆'}
godslaver = {'name': u'月老', 'age': 'unknown', 'other': u'他的老婆叫孟婆'}

f = open(u"H:\金牛二手房")
while f.hasnext:
  line = fin.readline()
  if len(line)==0:
      break
      print(line)
      post_info.insert(line)

#f = open(u"H:\武侯二手房")
#f = open(u"H:\锦江二手房")

print u'操作数据库完成！'