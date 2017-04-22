#coding:utf-8

from selenium import webdriver  
import urllib

DEBUG=True
FABU=False

if(DEBUG):
  print('DEBUG')
  try:
      driver = webdriver.PhantomJS()
      driver.get("https://movie.douban.com/tv/#!type=tv&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0")
  except:
      print('except')
      pass
  print('driver get')
  
  fout=open(r'/scrapyredis/selephan/mvtxt.txt', 'a+')
  print('fout.open')

  xpaths    = r'//*[@id="gaia"]/div[4]/div/a//div/img'
  txtxpaths = r'//*[@id="gaia"]/div[4]/div/a//p'
  print('txtxpaths')

  for element in driver.find_elements_by_xpath(xpaths):
      print(element)
      img_url = element.get_attribute('src')
      print(img_url)
      if img_url != None:
          print(img_url)
          filename=str(img_url).split('/')[7]
          print(filename)
          data=urllib.urlopen(img_url).read()
          f = open('./img_'+filename, 'ab')
          f.write(data)
          f.close()
                
#(status, output)=commands.getstatusoutput('cat/proc/cpuinfo')    


