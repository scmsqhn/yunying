# -*- coding: utf-8 -*-


import urllib
import urllib2
import json
import cookielib
import re
import zlib
import time
import random



#获取Cookiejar对象（存在本机的cookie消息）
cookie = cookielib.CookieJar()
#print('======cookie')
#print(cookie)
#自定义opener,并将opener跟CookieJar对象绑定

#使用代理IP地址
proxies=[
"119.5.0.77:808",
"110.72.40.235:8123",
"125.118.72.239:808",
"113.123.76.14:808",
"119.5.0.77:808",
"110.72.40.235:8123",
"125.118.72.239:808",
"113.123.76.14:808",
"121.204.165.170:8118",
"106.46.136.66:808",
"182.244.96.89:8998",
]
#random_proxy = random.choice(proxies) 
#proxy_support = urllib2.ProxyHandler({"http":random_proxy})  
#opener = urllib2.build_opener(proxy_support)  

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
#print('======opener')
#print(opener)
#安装opener,此后调用urlopen()时都会使用安装过的opener对象

urllib2.install_opener(opener)

home_url = 'http://cd.lianjia.com/'
auth_url = 'https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fcd.lianjia.com%2F'
chengjiao_url = 'http://cd.lianjia.com/chengjiao/'

def delay():
  time.sleep(random.randint(30,100))

header1 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'passport.lianjia.com',
    'Origin': 'https://passport.lianjia.com',
    'Pragma': 'no-cache',
    'Referer':'https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fcd.lianjia.com%2F',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'X-Requested-With': 'XMLHttpRequest',
}

headers={
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate, sdch, br',
'Accept-Language': 'zh-CN,zh;q=0.8',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Content-Type': 'text/html; charset=utf-8',
'Host': 'passport.lianjia.com',
'Origin': 'https://passport.lianjia.com',
'Pragma': 'no-cache',
'Referer':'https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fcd.lianjia.com%2F',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest',
}
#https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fcd.lianjia.com%2F 
 
''' 
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'passport.lianjia.com',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
}
'''
# 获取lianjia_uuid
delay()

req = urllib2.Request('http://cd.lianjia.com/')
#print('======req')
#print(req)
delay()
opener.open(req)
# 初始化表单
delay()
#print('======auth_url')
#print(auth_url)
#print('======headers')
#print(headers)

req = urllib2.Request(auth_url, headers=headers)
delay()
result = opener.open(req)
#print('======result')
#print(result)


# 获取cookie和lt值
pattern = re.compile(r'JSESSIONID=(.*)')
jsessionid = pattern.findall(result.info().getheader('Set-Cookie').split(';')[0])[0]
#print('======pattern')
#print(pattern)
#print('======jsessionid')
#print(jsessionid)
html_content = result.read()
#print('======html_content')
#print(html_content)

gzipped = result.info().getheader('Content-Encoding')
#print('======gzipped')
#print(gzipped)

if gzipped:
    html_content = zlib.decompress(html_content, 16+zlib.MAX_WBITS)
pattern = re.compile(r'value=\"(LT-.*)\"')
#print('======pattern')
#print(pattern)
lt = pattern.findall(html_content)[0]
#print('======lt')
#print(lt)
pattern = re.compile(r'name="execution" value="(.*)"')
#print('======pattern')
#print(pattern)
execution = pattern.findall(html_content)[0]
#print('======execution')
#print(execution)
 

# data
data = {
    'username': '13678028750', #替换为自己账户的用户名
    'password': 'lianjia333333$' , #替换为自己账户的密码
    'execution': execution,
    '_eventId': 'submit',
    'lt': lt,
    'verifyCode': '',
    'redirect': '',
}
#print(data)

# urllib进行编码
delay()
post_data=urllib.urlencode(data)
#print('======post_data')
#print(post_data)



req = urllib2.Request(auth_url, post_data, headers)
#print('======auth_url')
#print(auth_url)
#print('======post_data')
#print(post_data)
#print('======headers')
#print(headers)
#print('======req')
#print(req)

try:
    delay()
    result = opener.open(req)
except urllib2.HTTPError, e:
    #print('======getcode')
    #print e.getcode()  
    #print('======reason')
    #print e.reason  
    #print('======geturl')
    #print e.geturl()  
    #print('======info')
    #print e.info()
    delay()
    req = urllib2.Request(e.geturl())
    result = opener.open(req)
    delay()
    req = urllib2.Request(chengjiao_url)
    result = opener.open(req).read()
    #print result