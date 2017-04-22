#!/usr/bin/python
# coding:utf-8
# sqlitetool.py
import sqlite3
import sys
import sys
import place2wgs
import xlrd
import xlwt
import time




reload(sys)
#sys.setdefaultencoding('utf8')

DATABASE = 'musql3-lj.db'
TABLE = 'bj_lj_esf_demo'

      
class sql3tool:

  def __init__(self):
      self.conn = sqlite3.connect(DATABASE)
      self.cursor = self.conn.cursor()
      self.count = 0
      self.conn.commit()
      xlrd.open_workbook('./data.xls')

  def createtb(self):
    self.cursor.execute('CREATE TABLE IF NOT EXISTS bj_lj_esf_demo'
      '(ID INT PRIMARY KEY    NOT NULL,'
       'city           TEXT   NOT NULL,'
       'title          TEXT   NOT NULL,'
       'focusnum       TEXT   NOT NULL,'
       'price          TEXT   NOT NULL,'
       'area           TEXT   NOT NULL,'
       'community      TEXT   NOT NULL,'
       'watchnum       TEXT   NOT NULL,'
       'link           TEXT   NOT NULL,'
       'time           TEXT   NOT NULL,'
       'model          TEXT   NOT NULL,'
       'averageprice   TEXT   NOT NULL);')
    print "Table created successfully";

  def select(self, db):
    curs.execute("SELECT * from bj_lj_esf_demo;")
    for row in cursor:
      print "city = ", row[0]
      print "title = ", row[1]
      print "focus_num = ", row[2]
      print "price = ", row[3]
      print "area = ", row[4]
      print "community = ", row[5]
      print "watch_num = ", row[6]
      print "link = ", row[7]
      print "time = ", row[8]
      print "model = ", row[9]
      print "average_price = ", row[10]

  def txt2item(self, line, curs, count):
    print line
    line.decode('utf-8')
    dict = eval(line)
    print 'count= %d' % count
    dataitem = (count, str(dict['city']), str(dict['title']), str(dict['focus_num']), str(dict['price']), str(dict['area']), str(dict['community']), str(dict['watch_num']), str(dict['link']), str(dict['time']), str(dict['model']), str(dict['average_price']))
    print dataitem
    curs.execute('INSERT INTO bj_lj_esf_demo VALUES("%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % dataitem)
    print 'insert'
    
    def rdtxtwr():
      f = open('bj-lj-esf-demo.txt', 'rb')                   #以读方式打开文件  
      result = list()  
      for line in f.readlines():                          #依次读取每行  
        line = line.strip()                             #去掉每行头尾空白  
        if not len(line) or line.startswith('#'):       #判断是否是空行或注释行  
          continue                                    #是的话，跳过不处理  
        result.append(line)                             #保存  
      result.sort()                                       #排序结果  
      print result  
      open('cdays-4-result.txt', 'w').write('?' % '\n'.join(result)) #保存入结果文件    

  def savetxt2db(self, curs):
      print 'savatxt2db'
      f = open(r'G:\ProgramData\Anaconda2\usr\bj-lj-esf-demo.txt', 'r')    #以读方式打开文件  
      print 'open file'
      for line in f.readlines():                          #依次读取每行  
        print 'line in'
        line = line.strip()#.encode('mbcs')                             #去掉每行头尾空白 
        print 'del space'
        if not len(line) or line.startswith('#'):       #判断是否是空行或注释行  
          print 'no need'
          continue                                    #是的话，跳过不处理  
        self.count = self.count+1
        print 'count: %d' % self.count
        self.txt2item(line, curs, self.count)    
        print 'txt2item ok'
      print "save succ"  

  def _import_lianjia_cd_data(self, file):
      fin=open(file,'r')
      ls = fin.readlines()
      count=0
      for l in ls:
          l = eval(l)
          print(l)
          print(type(l.values()))
          self._insert_data('cdljesf', count, l.values())
          count=count+1

  def _create_tb_cdlj(self):
    self.cursor.execute('CREATE TABLE IF NOT EXISTS cdljesf'
      '(ID INT PRIMARY KEY    NOT NULL,'
       'title          TEXT   NOT NULL,'
       'house          TEXT   NOT NULL,'
       'price          TEXT   NOT NULL,'
       'build          TEXT   NOT NULL,'
       'buyer          TEXT   NOT NULL,'
       'mipri          TEXT   NOT NULL);')
    self.conn.commit()
    print "Table created successfully";
      
  def _insert_data(self, tb, _id, data): 
      self.cursor.execute('INSERT INTO %s VALUES("%d", "%s", "%s", "%s", "%s", "%s", "%s")' % (tb, _id, data[0], data[1],data[2],data[3],data[4],data[5]))


  def _get_alldata(self, tb):
    print("select * from %s"% tb)
    self.cursor=self.conn.execute("SELECT * FROM %s"% tb) 
    self.conn.commit()
    print("get all data")
    print(type(self.cursor))
    for rows in self.cursor:
        for i in rows:
            print(i)
        print('tt hs bd pr mp by=======')
      
  def _paoya_calcu(self):
      pass

  def _sqladdress_name_2wgs(self):
      self.cursor=self.conn.execute("select house ,build from cdljesf") 
      self.conn.commit()
      addnam=''
      areaname=''
      for rows in self.cursor:
          for row in rows:
              pp = row.split('|')
              addnam=pp[0].strip()
          for row in rows[:0:-1]:
              pp = row.split('-')
              areaname=pp[1].strip()
              print(areaname)

          fullname=u"四川成都"+areaname+addnam    
          fullname=fullname.strip()
          wgsmanager=place2wgs.place2wgs()
          wgs=wgsmanager.addres2wgs(u'四川',u'成都', areaname, addnam)
          print(fullname)
          print(wgs)

      pass

  def _fileaddress_name_2wgs(selfi, rowbase):
      fin = open(u'ljcd.json', 'r')
      lines = fin.readlines()
      row=rowbase
      fout=open('wgs.txt', 'a+')
      for line in lines[rowbase:]:
          t1=time.time()
          print('start for wrap')
          dicts=eval(line)

          house=dicts["house"]
          house=house.split('|')
          house=house[0].strip().decode('utf8')

          pro = ('四川'.decode('utf8')) 
          city= ('成都'.decode('utf8')) 
          print('prepare data')

          try:
              wgsmanager=place2wgs.place2wgs()
              wgs=wgsmanager.addres2wgs(pro, city, house)
          except:    
              print('catch')
              row=row-1
              continue

          print(wgs)
          strsout=('%d, %s, %s\n')% (row, (pro+city+house).encode('utf8'), wgs)
          fout.write(strsout)
          print(strsout)
          row=row+1
          t2=time.time()
          t=((t2-t1)/1)*3
          time.sleep(t)

if __name__ == '__main__':
  print '__name__ == __main__ exec'
  f = sql3tool()   
#  f.cursor.execute('drop table if exists cdljesf')
#  f._create_tb_cdlj()
#  f._import_lianjia_cd_data('./ljcd.json') 
#  f._get_alldata('cdljesf')
  f._fileaddress_name_2wgs(1)
  f.conn.close()



