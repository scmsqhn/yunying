#coding:utf-8
#获取电影天堂全站电影资源的迅雷下载地址
#获取的迅雷地址，暂时无法解码成base64 -d
#使用迅雷批量下载
import base64
import os
from subprocess import call
from selenium import webdriver  
import urllib
import re
import sys
import commands

reload(sys)
sys.setdefaultencoding('utf8')

DEBUG=True
FABU=False

base_url=r'http://www.dytt8.net'
index_url=r'http://www.dytt8.net/index.htm'
#base_url=r'http://www.dytt8.net/html/gndy/dyzz/20170305/53401.html'
  
def get_driver(url):
    print('get_driver')
    driver = webdriver.PhantomJS()
    driver.get(url)
    return driver

def search_html_final(driver, html):
   # fout=open(r'/scrapyredis/selephan/dytt_mv_url.txt', 'a+')
    print('search_html') 
    restrs = ('<a href="(.*?)">')
    resurl = ('/html(.*?)html')
    lines = html.encode('utf8').split('\n')
    for line in lines:
            results = re.search(restrs, line.strip())
            if results is None:
                continue
            for result in results.groups():
                urls = re.search(resurl, result.strip())
                if urls is None:
                    continue
                for url in urls.groups():
                     url = '/html%shtml\n' % url
                     if repeatcheck(url, fout):
                         fout.write(url)

def search_html(driver, html):
   # fout=open(r'/scrapyredis/selephan/dytt_mv_url.txt', 'a+')
    print('search_html') 
    restrs = ('<a href="(.*?)">')
    resurl = ('/html(.*?)html')
    lines = html.encode('utf8').split('\n')
    for line in lines:
        #print(line) 
#        try:
            results = re.search(restrs, line.strip())
            if results is None:
                continue
            for result in results.groups():
                urls = re.search(resurl, result.strip())
                if urls is None:
                    continue
                for url in urls.groups():
                     url = '/html%shtml\n' % url
                     if repeatcheck(url, fout):
                         fout.write(url)
                         prepare_data_final(base_url+url)
#        except:
#            pass
#        try:
#            driver.close()
#        except:
#            pass

def repeatcheck(url, file):
    file.seek(0)
    #print url 
    #print file
    lines=file.readlines()
    for line in lines:
        #print line 
        #print url 
        if url.strip()==line.strip():
            #print 'REPEAT'
            return False
    print ('UNREPEAT')
    print (url) 
    return True 

def prepare_data_final(url):
    print('main') 
    driver = get_driver(url)
    html = driver.page_source
    search_html_final(driver, html)

def prepare_data(url):
#    fout=open(r'/scrapyredis/selephan/dytt_mv_url.txt', 'a+')
    print('main') 
    driver = get_driver(url)
 #   time.sleep(10)
    html = driver.page_source
    search_html(driver, html)
 #   fout.flush()
  #  fout.close()

def download_data():
    xpath = ('//*[@id="Zoom"]/span/table/tbody/tr/td/a')
    print('download_data') 
    fout=open(r'/scrapyredis/selephan/dytt_mv_url.txt', 'r')
    fsave=open(r'/scrapyredis/selephan/dytt_mv_url_save.txt', 'a+')
    print('open data') 
    lines = fout.readlines()
    print(lines) 
    for line in lines:
        url = base_url+line
        if 'index' in url:
            continue
        driver = get_driver(url)
        elements = driver.find_elements_by_xpath(xpath)
        if elements is not None:
            for element in elements:
                try:
                    strsele = str(element)
                    print ('call[]')
                    thunder = element.get_attribute('wmwalovz')
                    href    = element.get_attribute('href')
#                    call("echo | %s | base64 -d | echo" % thunder, shell=True)
#                    call("echo | %s | base64 -d | echo" % href, shell=True)
                    text = element.text
                    print ('text=%s' % text)
                    print ('thunder=%s' % thunder)
                    print ('href=%s' % href)
                except:
                    print ('except: ')
                    pass
    fout.close()
    fsave.close()

def download_data_2():
    print('download_data') 
    fout=open(r'/scrapyredis/selephan/temp_url.txt', 'r')
    fsave=open(r'/scrapyredis/selephan/temp_thunder.txt', 'a+')
    print('open data') 
    lines = fout.readlines()
    print(lines) 
    pat=('thunder://(.*?)">')
    for line in lines:
       try:
#          url = base_url+line
          url = line[:-1]
          if 'index' in url:
              continue
          print ('downurl='+url)
          driver = get_driver(url)
          html = driver.page_source
          lines = html.split('\n')
          for line in lines:
              print ('line='+line)
              urls = re.search(pat, line, flags=0)
              if urls is not None:
                  try:
                      for url in urls.groups():
                          fsave.write('thunder://'+url+'\n')
                          print ('thunder://'+url+'\n')
                  except:
                      print('except 9')
                      pass
       except:
          print('except key')
          pass
    fout.close()
    fsave.close()
    driver.close()
    
def get_all_html_addr():   
    global fout
    fout=open(r'/scrapyredis/selephan/dytt_mv_url.txt', 'a+')

    prepare_data(base_url)
#    download_data_2()
    fout.flush()
    fout.close()

def get_all_thunder_addr():   
    prepare_data(base_url)
    download_data_2()

def get_all_rar_cont():
    print('get_all_rar_cont')
    fsave=open(r'/scrapyredis/selephan/dytt_mv_url_save.txt', 'r')
    lines=fsave.readlines()
    for line in lines:
        line = line[10:-1]
        b64c = base64.b64decode(line)
        b64c = b64c[2:-2]
        print (b64c)
        b64c = commands.getoutput(r'axel -n 10 -o ./ %s' % b64c)
        print (b64c)

if __name__=="__main__":
#    get_all_rar_cont()
#    try:
#        get_all_html_addr()
        download_data_2()
#    except: 
#        print ('except')
#        pass






