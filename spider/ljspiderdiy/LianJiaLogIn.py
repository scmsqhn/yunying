# -*- coding: utf-8 -*-
"""
@author: 冰蓝
@site: http://lanbing510.info
"""

import urllib
import urllib2
import json
import cookielib
import re
import zlib
from cookielib import Cookie, CookieJar
import Cookie


#获取Cookiejar对象（存在本机的cookie消息）
cookie = cookielib.CookieJar()
Cookie='lianjia_uuid=205d25a0-3fa2-4b8b-89d6-9bc268f11a55; gr_user_id=dba46ec7-3d71-452b-89aa-47e5c3769e45; Hm_lvt_678d9c31c57be1c528ad7f62e5123d56=1487292480; all-lj=007e0800fb44885aa2065c6dfaaa4029; Hm_lvt_efa595b768cc9dc7d7f9823368e795f1=1486726371,1487292481,1488013426; Hm_lpvt_efa595b768cc9dc7d7f9823368e795f1=1488013426; Hm_lvt_660aa6a6cb0f1e8dd21b9a17f866726d=1487987111,1487998799,1487998878,1487998894; Hm_lpvt_660aa6a6cb0f1e8dd21b9a17f866726d=1488024890; _smt_uid=589d8429.404337d7; CNZZDATA1253492306=676618900-1486715611-http%253A%252F%252Fcn.bing.com%252F%7C1488021670; CNZZDATA1254525948=208011574-1486714296-http%253A%252F%252Fcn.bing.com%252F%7C1488021183; CNZZDATA1255633284=1067758961-1486715301-http%253A%252F%252Fcn.bing.com%252F%7C1488022596; CNZZDATA1255604082=435151434-1486716209-http%253A%252F%252Fcn.bing.com%252F%7C1488019770; _ga=GA1.2.1413369539.1486717997; gr_session_id_a1a50f141657a94e=cd746b33-1513-4ff3-9cc7-55877f30753d; select_city=110000; lianjia_token=2.0058b830d0224728c4491519e1353a413d; lianjia_ssid=7235edd6-6171-e796-d406-78b18c3df6fc'
cookie.set_cookie(Cookie)

#自定义opener,并将opener跟CookieJar对象绑定
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
#安装opener,此后调用urlopen()时都会使用安装过的opener对象
urllib2.install_opener(opener)

 
def build_opener_with_cookie_str(cookie_str, domain, path='/'):
    simple_cookie = Cookie.SimpleCookie(cookie_str)    # Parse Cookie from str
    cookiejar = cookielib.CookieJar()    # No cookies stored yet
 
    for c in simple_cookie:
        cookie_item = cookielib.Cookie(
            version=0, name=c, value=str(simple_cookie[c].value),
                     port=None, port_specified=None,
                     domain=domain, domain_specified=None, domain_initial_dot=None,
                     path=path, path_specified=None,
                     secure=None,
                     expires=None,
                     discard=None,
                     comment=None,
                     comment_url=None,
                     rest=None,
                     rfc2109=False,
            )
        cookiejar.set_cookie(cookie_item)    # Apply each cookie_item to cookiejar
    return urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))    # Return opener
 
cookie_str = ck#'tLargeScreenP=1; Authorization=Basic%20HereIsMySecret; subType=pcSub; TPLoginTimes=2'
opener = build_opener_with_cookie_str(cookie_str, domain= authurl)
	
home_url = 'http://cd.lianjia.com/'
#auth_url = 'https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fcd.lianjia.com%2F'
auth_url = 'https://m.lianjia.com/my/login?redirect=/my/index'
#auth_url = 'https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fcd.lianjia.com%2F&renew=1'
#auth_url = 'https://passport.lianjia.com/cas/login?service=http://cd.lianjia.com/&renew=1'
chengjiao_url = 'http://cd.lianjia.com/chengjiao/'
 
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
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
}
'''
headers = {
    'Accept': 'image/webp,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'image/x-icon',
#    'Host': 'passport.lianjia.com',
    'Host': 'https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fcd.lianjia.com%2F',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
}

# 获取lianjia_uuid
req = urllib2.Request('http://cd.lianjia.com/')
opener.open(req)
# 初始化表单
req = urllib2.Request(auth_url, headers=headers)
result = opener.open(req)


# 获取cookie和lt值
pattern = re.compile(r'JSESSIONID=(.*)')
jsessionid = pattern.findall(result.info().getheader('Set-Cookie').split(';')[0])[0]

html_content = result.read()
gzipped = result.info().getheader('Content-Encoding')
if gzipped:
    html_content = zlib.decompress(html_content, 16+zlib.MAX_WBITS)
pattern = re.compile(r'value=\"(LT-.*)\"')
lt = pattern.findall(html_content)[0]
pattern = re.compile(r'name="execution" value="(.*)"')
execution = pattern.findall(html_content)[0]
 

# data
data = {
    'username': '13678028750', #替换为自己账户的用户名
    'password': 'lianjia333333$', #替换为自己账户的密码
    'execution': execution,
    '_eventId': 'submit',
    'lt': lt,
    'verifyCode': '',
    'redirect': '',
}
print data

# urllib进行编码
post_data=urllib.urlencode(data)
req = urllib2.Request(auth_url, post_data, headers)

try:
    result = opener.open(req)
except urllib2.HTTPError, e:
    print e.getcode()  
    print e.reason  
    print e.geturl()  
    print e.info()
#    被禁掉后，不再次登录，一面被列入黑名单；
#    req = urllib2.Request(e.geturl())
#    result = opener.open(req)
#    req = urllib2.Request(chengjiao_url)
#    result = opener.open(req).read()
    #print result


