#encoding=utf8
import urllib2
from bs4 import BeautifulSoup
import urllib
import socket
 
User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
header = {}
header['User-Agent'] = User_Agent
 
'''
获取所有代理IP地址
'''
def getProxyIp():
 proxy = []
 for i in range(1,2):
  try:
   url = 'http://www.xicidaili.com/nn/'+str(i)
   req = urllib2.Request(url,headers=header)
   res = urllib2.urlopen(req).read()
   soup = BeautifulSoup(res)
   ips = soup.findAll('tr')
   for x in range(1,len(ips)):
    ip = ips[x]
    tds = ip.findAll("td")
    ip_temp = tds[1].contents[0]+"\t"+tds[2].contents[0]
    proxy.append(ip_temp)
  except:
   continue
 return proxy
  
'''
验证获得的代理IP地址是否可用
'''
def validateIp(proxy):
 url = "http://ip.chinaz.com/getip.aspx"
 socket.setdefaulttimeout(3)
 f = open("H:\ip.txt","a+")
 for i in range(0,len(proxy)):
  try:
   ip = proxy[i].strip().split("\t")
   proxy_host = "http://"+ip[0]+":"+ip[1]
   proxy_temp = {"http":proxy_host}
   res = urllib.urlopen(url,proxies=proxy_temp).read()
   ip_compile= re.search(r'<td>(\d+\.\d+\.\d+\.\d+)</td>',proxy[i])
   port_compile = re.search(r'<td>(\d+)</td>',proxy[i])
   str = ("'%s:%s'," % ip_compile, port_compile)
   f.write(str+'\n')
   print str
  except Exception,e:
   continue
 f.close()
 
    
if __name__ == '__main__':
 proxy = getProxyIp()
 validateIp(proxy)