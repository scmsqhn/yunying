# -*- coding: utf-8 -*-
"""
@author: qin haining
@date: 2017/02/25
"""
import chardet
import re
import urllib2  
import sqlite3
import random
import threading
from bs4 import BeautifulSoup
import time
import sys
import random
reload(sys)
sys.setdefaultencoding("utf-8")
reload(sys)
import urllib
import re
import urllib
import urllib2
import json
import cookielib
import re
import zlib
import time
import random


#switch
LOG_EN = False#True#
PROXY_EN = True#False#
COOKIE_EN = True


xqurlsdict = {}

#print sys.getfilesystemencoding()  
reload(sys)
sys.setdefaultencoding('utf-8')
def GetHtml( url):  
    page = urllib.urlopen(url)  
    contex = page.read()  
    return contex  
    
#home_url = u'http://domz.org/'
    
home_url = u'http://cd.lianjia.com/'
auth_url = u'https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fcd.lianjia.com%2F'
chengjiao_url = u'http://cd.lianjia.com/chengjiao/'
xiaoqu1 = u"http://cd.lianjia.com/xiaoqu/pg2rs%E9%AB%98%E6%96%B0/"
quyu = u"http://cd.lianjia.com/xiaoqu/rs"

#print 'Html is encoding by : %',chardet.detect(GetHtml(home_url))  
#登录，不登录不能爬取三个月之内的数据,代码参考博客[1]


if LOG_EN:
  import LianJiaLogIn
else:
  pass
  
#使用代理IP地址
proxies=[
"106.46.136.21:808",
"123.169.89.38:808",
"106.46.136.79:808",
"27.159.124.121:8118",
"106.46.136.127:808",
"106.46.136.144	808",
"60.165.191.179	81",
"182.44.33.71	8998",
"124.88.67.14	80",
"60.179.40.16	808",
"106.46.136.232	808",
]


#  PROXY
random_proxy = random.choice(proxies) 
proxy_handler = urllib2.ProxyHandler({"http" : 'http://%s' % random_proxy})
null_proxy_handler = urllib2.ProxyHandler({})
if PROXY_EN:
    opener = urllib2.build_opener(proxy_handler)
else:
    opener = urllib2.build_opener(null_proxy_handler)
urllib2.install_opener(opener)

if COOKIE_EN:
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
else:
    pass



#Some User Agents
hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]


regions=[u"郫县"]
lock = threading.Lock()


class SQLiteWraper(object):
    """
    数据库的一个小封装，更好的处理多线程写入
    """
    def __init__(self,path,command='',*args,**kwargs):  
        #print(u'====__init__')

        self.lock = threading.RLock() #锁  
        self.path = path #数据库连接参数  

        if command!='':
            conn=self.get_conn()
            cu=conn.cursor()
            cu.execute(command)

    def get_conn(self):  
        #print(u'====get_conn')

        conn = sqlite3.connect(self.path)#,check_same_thread=False)  
        conn.text_factory=str
        return conn   

    def conn_close(self,conn=None):  
        #print(u'====conn_close')

        conn.close()  

    def conn_trans(func):  
        #print(u'====conn_trans')

        def connection(self,*args,**kwargs):  
            #print(u'====conn_trans.connection')


            self.lock.acquire()  
            conn = self.get_conn()  
            kwargs['conn'] = conn  
            rs = func(self,*args,**kwargs)  
            self.conn_close(conn)  
            self.lock.release()  
            #print(rs)

            return rs  
        return connection  

    @conn_trans    
    def execute(self,command,method_flag=0,conn=None):  
        #print(u'====execute')
        cu = conn.cursor()
        try:
            if not method_flag:
                #print(command)

                cu.execute(command)
            else:
                #print(command[0])
                #print(command[1])

                cu.execute(command[0],command[1])
            conn.commit()
        except sqlite3.IntegrityError,e:
            #print(u'====execute excep 1')

            ##print e
            return -1
        except Exception, e:
            #print(u'====execute excep 2')

            #print e
            return -2
        return 0

    @conn_trans
    def fetchall(self,command="select name from xiaoqu",conn=None):
        #print(u'====fetchall')
        cu=conn.cursor()
        lists=[]
        try:
            cu.execute(command)
            lists=cu.fetchall()
            #print(lists)
        except Exception,e:
            #print(u'====execute fetchall 2')

            #print e
            pass
        return lists

def delay():
  time.sleep(random.randint(10,30))

def gen_xiaoqu_insert_command(info_dict):
    #print(u'====gen_xiaoqu_insert_command')
    """
    生成小区数据库插入命令
    """
    info_list=[u'小区名称',u'大区域',u'小区域',u'小区户型',u'建造时间']
    t=[]
    for il in info_list:
        if il in info_dict:
            t.append(info_dict[il])
        else:
            t.append('')
    t=tuple(t)
    command=(r"insert into xiaoqu values(?,?,?,?,?)",t)
    l.writelines('insert into xiaoqu values')
    #print(command)
    return command


def gen_chengjiao_insert_command(info_dict):
    #print(u'====gen_chengjiao_insert_comman')

    """
    生成成交记录数据库插入命令
    """
    info_list=[u'链接',u'小区名称',u'户型',u'面积',u'朝向',u'楼层',u'建造时间',u'签约时间',u'签约单价',u'签约总价',u'房产类型',u'学区',u'地铁']
    t=[]
    for il in info_list:
        if il in info_dict:
            t.append(info_dict[il])
        else:
            t.append('')
    t=tuple(t)
    command=(r"insert into chengjiao values(?,?,?,?,?,?,?,?,?,?,?,?,?)",t)
    #print(command)
    return command


def xiaoqu_spider(db_xq,url_page=xiaoqu1):

    """
    爬取页面链接中的小区信息
    """
    try:
        delay()
        req = urllib2.Request(url_page,headers=hds[random.randint(0,len(hds)-1)])
        source_code = urllib2.urlopen(req,timeout=10).read()
        plain_text=unicode(source_code.decode('utf-8'))#,errors='ignore')   
        soup = BeautifulSoup((plain_text))
    except (urllib2.HTTPError, urllib2.URLError), e:
        print(u'====xiaoqu_spider except 1')
        print e
        exit(-1)
    except Exception,e:
        print(u'====xiaoqu_spider except 2')
        print e
        exit(-1)
    xiaoqu_list=soup.findAll('ul',{'class':'listContent'})
    for xq in xiaoqu_list:
        print(xq)
        info_dict={}
        info = xq.find('div', 'info')
        title = info.find('div', 'title')
        href = title.find('a')

        pt = u"[\u4E00-\u9FFF]"
        xqurl=re.search(pt, str(href))
          
        info_dict.update({u'小区名称':xqurl.group(0)})
        l.writelines(u'write in xiaoqu name lines=286\n ')
#        info_dict.update({u'小区名称':xq.find('a').text})
        content=unicode(xq.find('div',{'class':'info'}).renderContents().strip())
        l.writelines(u'%s\n' % content)
 
 #       pts0= '.+href="(.+)" title'
        pts= '.+=(.+)</a>.+=(.+)</a>.+=(.+)</a>.+=(.+)</a>.+=(.+)</a>'
        info=(re.match(pts),content)
        strslist=[]
        for i in info:
            _str = re.match('.+>(.+)', i.group(0)).group(0)
            strslist.append(_str)
            l.writelines(u'%s\n%s\n%s\n%s\n%s\n' % (strslist[0], strslist[1], strslist[2], strslist[3], strslist[4]))
        if info:
            info=info.groups()
            info_dict.update({u'大区域':info[3]})
            info_dict.update({u'小区域':info[4]})
            info_dict.update({u'小区户型':info[0]})
            info_dict.update({u'建造时间':info[1][:2]})
        command=gen_xiaoqu_insert_command(info_dict)
        db_xq.execute(command,1)
        l.writelines('xiaoqu info_dict %s \n' % str(info_dict))
        l.writelines('got the xiaoqu info in info_dict \n')
        print(u'got the xiaoqu info in info_dict \n')
        break

def do_xiaoqu_spider(db_xq,region=u"郫县"):
    delay()
    #print(u'====do_xiaoqu_spider')
    """
    爬取大区域中的所有小区信息
    """
    url=quyu+region+"/"
    #print(url)
    try:
        delay()
        req = urllib2.Request(url,headers=hds[random.randint(0,len(hds)-1)])
        source_code = urllib2.urlopen(req,timeout=5).read()
        plain_text=unicode(source_code.decode('utf-8'))#,errors='ignore')   
        soup = BeautifulSoup(plain_text)
    except (urllib2.HTTPError, urllib2.URLError), e:
        exit(-1)
    except Exception,e:
        exit(-1)
    page = soup.find('div',{'class':'page-box house-lst-page-box'})
    #print ('=====page')
    #print (page)
    pagedata = page.get('page-data')
    #print (pagedata)
    d="d="+pagedata
    #print (d)
    exec(d)
    total_pages=d['totalPage']

    threads=[]
    for i in range(total_pages):
        delay()
        url_page=u"http://cd.lianjia.com/xiaoqu/pg%drs%s/" % (i+1,region)
        l.writelines(u'url_page is %s' % url_page)
        t=threading.Thread(target=xiaoqu_spider,args=(db_xq,url_page))
        print (db_xq,url_page)
        threads.append(t)
        #print ('====url_page')
        #print (url_page)
        break
    for t in threads:
        t.start()
        #print ('t.start()')
    for t in threads:
        t.join()
        #print ('t.start()')


def chengjiao_spider(db_cj, \
    url_page=u"http://cd.lianjia.com/chengjiao/pg1rs%E5%A4%A9%E9%82%91%E5%AE%8F%E5%BE%A1%E8%8A%B1%E5%9B%AD%E5%BE%A1%E8%8B%91/"):

    print (url_page)
    l.writelines(url_page)
    l.writelines('\n')
    """
    爬取页面链接中的成交记录
    """
    try:
        #print(req)
        delay()
        req = urllib2.Request(url_page,headers=hds[random.randint(0,len(hds)-1)])
        source_code = urllib2.urlopen(req,timeout=10).read()
        plain_text=unicode(source_code.decode('utf-8'))#,errors='ignore')   
        soup = BeautifulSoup((plain_text),"html.parser")
    except (urllib2.HTTPError, urllib2.URLError), e:
        #print e
        exception_write('chengjiao_spider',url_page)
        exit(-1)
    except Exception,e:
        #print e
        exception_write('chengjiao_spider',url_page)
        exit(-1)

    cj_list=soup.findAll('div',{'class':'info-panel'})
    for cj in cj_list:
        print (cj)
        l.writelines(cj)
        l.writelines('\n')
        info_dict={}
        href=cj.find('a')
        if not href:
            continue
        info_dict.update({u'链接':href.attrs['href']})
        content=cj.find('h2').text.split()
        if content:
            info_dict.update({u'小区名称':content[0]})
            info_dict.update({u'户型':content[1]})
            info_dict.update({u'面积':content[2]})
        content=unicode(cj.find('div',{'class':'con'}).renderContents().strip())
        content=content.split('/')
        if content:
            info_dict.update({u'朝向':content[0].strip()})
            info_dict.update({u'楼层':content[1].strip()})
            if len(content)>=3:
                content[2]=content[2].strip();
                info_dict.update({u'建造时间':content[2][:4]}) 
        content=cj.findAll('div',{'class':'div-cun'})
        if content:
            info_dict.update({u'签约时间':content[0].text})
            info_dict.update({u'签约单价':content[1].text})
            info_dict.update({u'签约总价':content[2].text})
        content=cj.find('div',{'class':'introduce'}).text.strip().split()
        if content:
            for c in content:
                if c.find(u'满')!=-1:
                    info_dict.update({u'房产类型':c})
                elif c.find(u'学')!=-1:
                    info_dict.update({u'学区':c})
                elif c.find(u'距')!=-1:
                    info_dict.update({u'地铁':c})
        l.writelines('gen_chengjiao_insert_command done total!!')
        l.writelines('\n')

        command=gen_chengjiao_insert_command(info_dict)
        db_cj.execute(command,1)


def xiaoqu_chengjiao_spider(db_cj,xq_name=u""):

    #print(u'====xiaoqu_chengjiao_spider')

    """
    爬取小区成交记录
    """
    
    url=u"http://cd.lianjia.com/chengjiao/rs"+urllib2.quote(xq_name)+"/"
    print(url)
    l.writelines(url)
    l.writelines('\n')
    #print(urllib2.quote(xq_name))
    try:
        delay()
        req = urllib2.Request(url,headers=hds[random.randint(0,len(hds)-1)])
        source_code = urllib2.urlopen(req,timeout=10).read()
        plain_text=unicode(source_code.decode('utf-8'))#,errors='ignore')   
        soup = BeautifulSoup((plain_text), "html.parser")
    except (urllib2.HTTPError, urllib2.URLError), e:
        #print(u'====xiaoqu_chengjiao_spider except')

        #print e
        exception_write('xiaoqu_chengjiao_spider',xq_name)
        return
    except Exception,e:
        #print(u'====xiaoqu_chengjiao_spider except')

        #print e
        exception_write('xiaoqu_chengjiao_spider',xq_name)
        return
    content=soup.find('div',{'class':'page-box house-lst-page-box'})
    total_pages=0
    if content:
        d="d="+content.get('page-data')
        exec(d)
        total_pages=d['totalPage']

    threads=[]
    for i in range(total_pages):
        delay()
        url_page=u"http://cd.lianjia.com/chengjiao/pg%drs%s/" % (i+1,urllib2.quote(xq_name))
        print(url_page)
        l.writelines(url_page)
        l.writelines('\n')
        t=threading.Thread(target=chengjiao_spider,args=(db_cj,url_page))
        threads.append(t)
    for t in threads:
        delay()
        #print(u'====xiaoqu_chengjiao_spider')

        t.start()
    for t in threads:
        delay()
        #print(u'====t')

        t.join()


def do_xiaoqu_chengjiao_spider(db_xq,db_cj):
    #print(u'====do_xiaoqu_chengjiao_spider')
    """
    批量爬取小区成交记录
    """
    l.writelines('do_xiaoqu_chengjiao_spider  lines=505')
    count=0
    xq_list=db_xq.fetchall()
    for xq in xq_list:
        l.writelines('do_xiaoqu_chengjiao_spider\n')
        l.writelines('xq=%s' % str(xq))
        delay()
        #print(u'====xq')

        xiaoqu_chengjiao_spider(db_cj,xq[0])
        count+=1
        #print 'have spidered %d xiaoqu' % count
    #print 'done'


def exception_write(fun_name,url):

    delay()
    #print(u'====exception_write')

    """
    写入异常信息到日志
    """
    lock.acquire()
    f = open(r'H:\log.txt','a')
    #print 'done'
    line="%s %s\n" % (fun_name,url)
    #print (line)
    l.write(line)
    f.close()
    lock.release()


def exception_read():
    delay()
    #print(u'====exception_read')

    """
    从日志中读取异常信息
    """
    lock.acquire()
    f=open(r'H:\log.txt','r')
    lines=f.readlines()
    f.close()
    f=open(r'H:\log.txt','w')
    f.truncate()
    f.close()
    lock.release()
    return lines


def exception_spider(db_cj):
    delay()
    #print(u'====exception_spider')

    """
    重新爬取爬取异常的链接
    """
    count=0
    excep_list=exception_read()
    while excep_list:
        #print(u'====excep_list except')

        for excep in excep_list:
            excep=excep.strip()
            if excep=="":
                continue
            excep_name,url=excep.split(" ",1)
            if excep_name=="chengjiao_spider":
                chengjiao_spider(db_cj,url)
                count+=1
            elif excep_name=="xiaoqu_chengjiao_spider":
                xiaoqu_chengjiao_spider(db_cj,url)
                count+=1
            else:
                pass
                #print "wrong format"
            #print "have spidered %d exception url" % count
        excep_list=exception_read()
    #print 'all done ^_^'

def  sorthanzi(file):
    pts2= '.+href="(.+)" title'
    pts0= '.+=(.+)</a>.+=(.+)</a>.+=(.+)</a>.+=(.+)</a>.+=(.+)</a>'
    pts1 = '[\u4E00-\u9FFF]'
    f = open(file,'r')
    lines = f.readlines()
    bsline=''
    for line in lines:
        bsline=bsline+line.strip()
    bsline=bsline.strip()
    info = re.match(pts0, bsline)
    print(bsline)
    print ('=============')
    print ('=============')
    print ('=============')
    if info:
        print (info.group(1).decode('utf8')+'\n')
        print (info.group(2).decode('utf8')+'\n')
        print (info.group(3).decode('utf8')+'\n')
        print (info.group(4).decode('utf8')+'\n')
        print (info.group(5).decode('utf8')+'\n')
    else:
        print ('match loss')


if __name__=="__main__":
#    sorthanzi('H:\logfile.txt')

    #print(u'main')
    command="create table if not exists xiaoqu (name TEXT primary key UNIQUE, regionb TEXT, regions TEXT, style TEXT, year TEXT)"
#    #print(command)
    db_xq=SQLiteWraper('lianjia-xq.db',command)

    command="create table if not exists chengjiao (href TEXT primary key UNIQUE, name TEXT, style TEXT, area TEXT, orientation TEXT, floor TEXT, year TEXT, sign_time TEXT, unit_price TEXT, total_price TEXT,fangchan_class TEXT, school TEXT, subway TEXT)"
    db_cj=SQLiteWraper('lianjia-cj.db',command)
#    #print(command)
    #爬下所有的小区信息'''
    

    xiaoqu_spider(db_xq,url_page=xiaoqu1)
    
    '''for region in regions:
        #print(region)
        #print(regions)

        do_xiaoqu_spider(db_xq,region)

    #爬下所有小区里的成交信息
#    do_xiaoqu_chengjiao_spider(db_xq,db_cj)

    #重新爬取爬取异常的链接
#    exception_spider(db_cj)'''
