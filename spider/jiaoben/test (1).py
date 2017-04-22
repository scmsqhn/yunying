#-*- utf-8 -*-
import sys
from lxml import etree
import codecs
import json
import time
import random
import place2wgs
import sqlitetool


reload(sys)
sys.setdefaultencoding('utf-8')


from selenium import webdriver

# FLAG
DEBUG = False#True


#URL
home_url = u'http://cd.lianjia.com/'
ershou_url = u'http://cd.lianjia.com/ershoufang/'

auth_url = u'https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fcd.lianjia.com%2F'
chengjiao_url = u'http://cd.lianjia.com/chengjiao/'

#CHILD_URL
jinjiang = 'http://cd.lianjia.com/ershoufang/jinjiang'
jinniu   = 'http://cd.lianjia.com/ershoufang/jinniu'  
gaoxin7  = 'http://cd.lianjia.com/ershoufang/gaoxin7' 
chenghua = 'http://cd.lianjia.com/ershoufang/chenghua'
wuhou    = 'http://cd.lianjia.com/ershoufang/wuhou'   
tianfuxinqu='http://cd,lianjia.com/ershoufang/tianfuxinqu'
shuangliu= 'http://cd.lianjia.com/ershoufang/shuangliu'
wenjiang = 'http://cd.lianjia.com/ershoufang/wenjiang'
pidou    = 'http://cd.lianjia.com/ershoufang/pidou'   
longquanyi='http://cd.lianjia.com/ershoufang/longquanyi'
xindou   = 'http://cd.lianjia.com/ershoufang/xindou'

urls_dic={'jj':jinjiang,\
          'wh':wuhou,\
          'wj':wenjiang,\
          'tfxq':tianfuxinqu,\
          }

#wenjiang tianfuxinqu
#gaoxin7
#jinniu
def _getpage(xp):

    selector.xpath(xp)

def _initlxml(html):

    selector=stree.HTML(html)
    return selector


def _savepage(url):

    driver = webdriver.PhantomJS()
    driver.get(url)
    data = driver.page_source
    if DEBUG:
        f=open("./temp.html",'a+')
        f.write(data)
        f.close()
    print data
    driver.quit()
    return data

def _handlearea(sel): 

    cons=sel.xpath('/html/body/div[4]/div[1]/div[7]/div[2]/div')
#    page_num=cons.xpath('page-data()'["totalPage"a)]    
    for i in range[1, 1]:#page_num]:
        _handlepage()
        if(i<page_bum):
            _pressnextpage()


def _handlepage():
    _picdata()
    _savedata()
    pass


def _pressnextpage():

    pass


def _get_data_30_page(j):    
        title = driver.find_elements_by_xpath("/html/body/div[4]/div[1]/ul/li[%d]/div[1]/div[1]/a" % j)
        for i in title:
            title = i.text
            jsonobj = json.dumps(title, ensure_ascii=False)+'\n'

        house = driver.find_elements_by_xpath('/html/body/div[4]/div[1]/ul/li[%d]/div[1]/div[2]/div' % j)
        for i in house:
            house = i.text
            jsonobj = json.dumps(house, ensure_ascii=False)+'\n'

        build = driver.find_elements_by_xpath('/html/body/div[4]/div[1]/ul/li[%d]/div[1]/div[3]/div' % j)
        for i in build:
            build = i.text
            jsonobj = json.dumps(build, ensure_ascii=False)+'\n'

        price = driver.find_elements_by_xpath('/html/body/div[4]/div[1]/ul/li[%d]/div[1]/div[6]/div[1]/span' % j)
        for i in price:
            price = i.text
            jsonobj = json.dumps(price, ensure_ascii=False)+'\n'

        mipri = driver.find_elements_by_xpath('/html/body/div[4]/div[1]/ul/li[%d]/div[1]/div[6]/div[2]/span' % j)
        for i in mipri:
            mipri = i.text
            jsonobj = json.dumps(mipri, ensure_ascii=False)+'\n'

        buyer = driver.find_elements_by_xpath('/html/body/div[4]/div[1]/ul/li[%d]/div[1]/div[4]' % j)
        for i in buyer:
            buyer = i.text
            jsonobj = json.dumps(buyer, ensure_ascii=False)+'\n'

        info = {"title":title, \
                 "house":house, \
                 "build":build, \
                 "price":price, \
                 "mipri":mipri, \
                 "buyer":buyer,}
        return dict(info)
        


if __name__=="__main__":
    print("START main")
    fout = codecs.open('cdesf0228.json', 'a+', encoding='utf-8')
    
    #log in
    '''
    driver.get(logurl)
    time.sleep(10)
    driver.find_elements_by_xpath('').send_keys('13678028750')
    time.sleep(5)
    driver.find_elements_by_xpath('').send_keys('lianjia333333$')

    time.sleep(5)
    driver.find_elements_by_xpath('').click()
    time.sleep(5)
    cookie= [item["name"]+"="+item["value"]for item in driver.get_cookies()]
    '''



    #get url
    for quyui in urls_dic.values():
        driver = webdriver.PhantomJS()
        print quyui
        time.sleep(random.randint(0,0))
        driver.get(quyui)
        data = driver.page_source
        
        pagenum=driver.find_elements_by_xpath('/html/body/div[4]/div[1]/div[7]/div[2]/div')
        fpnum=1
        for i in pagenum: 
            pnum=i.get_attribute('page-data')
            fpnum=eval(pnum)["totalPage"]
            print fpnum
        for i in range(1,fpnum):
            print('is a new page')
            url=('%s/pg%d/' % (quyui, i))
            time.sleep(random.randint(0,0))
            driver.get(url)
            print url
            pagedata = driver.page_source
            if DEBUG:
                ftemp=open("./temp.html",'a+')
                ftemp.write(pagedata)
                ftemp.close()
                print pagedata
            for j in range(1,30):
                print('is a new house')
                try:  
                    dictobj=_get_data_30_page(j)
                    jsonobj = json.dumps(dictobj, ensure_ascii=False)+'\n'
                    print(jsonobj)
                    fout.write(jsonobj)
                except:   
                    print('sth. is wrong in writing page')
        driver.quit()
        fout.flush()
    fout.close()
    
