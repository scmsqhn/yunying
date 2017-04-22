# -*- coding: utf-8 -*-
import urllib2,urllib,time,socket,random,Proxy_ip,Useragent


def Visitpage(proxyip,url):
    socket.setdefaulttimeout(6)
    proxy_support = urllib2.ProxyHandler({'http':proxyip})
    user_agent = random.choice(Useragent.user_agents)
    opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    try:
        request = urllib2.Request(url)
        request.add_header('Referer','http://www.baidu.com')
        request.add_header('User-Agent',user_agent)
        html = urllib2.urlopen(request).read()
        print html
        time.sleep(random.randint(60,180))
    except urllib2.URLError,e:
        print 'URLError! The bad proxy is %s' %proxyip
    except urllib2.HTTPError,e:
        print 'HTTPError! The bad proxy is %s' %proxyip
    except:
        print 'Unknown Errors! The bad proxy is %s ' %proxyip


def Clicklikebutton(proxyip,url,data):
    socket.setdefaulttimeout(6)
    proxy_support = urllib2.ProxyHandler({'http':proxyip})
    user_agent = random.choice(Useragent.user_agents)
    opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
    try:
        request = urllib2.Request(url)
        request.add_header('Referer','http://www.baidu.com')
        request.add_header('User-Agent',user_agent)
        data = urllib.urlencode(data)
        resp = opener.open(request, data)
        print resp.read()
        time.sleep(random.randint(60,180))
    except urllib2.URLError,e:
        print 'URLError! The bad proxy is %s' %proxyip
    except urllib2.HTTPError,e:
        print 'HTTPError! The bad proxy is %s' %proxyip
    except:
        print 'Unknown Errors! The bad proxy is %s ' %proxyip

def main():
    for i in range(len(Proxy_ip.iplist)):
        proxyip = Proxy_ip.iplist[i]
        i += 1
        print proxyip
        for m in range(random.randint(2,4)):
            Visitpage(proxyip,u'你的get请求url地址')54         
            Clicklikebutton(proxyip,u'你的post请求地址',{你的post请求参数})

if __name__ == "__main__":
    main()