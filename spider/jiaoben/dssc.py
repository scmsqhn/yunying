#coding:utf-8
#定期上传下载好的文件
import base64
import os
from subprocess import call
from selenium import webdriver  
import urllib
import re
import sys
import commands
import time 

reload(sys)
sys.setdefaultencoding('utf8')

DEBUG=True
FABU=False

base_url=r'http://www.dytt8.net'
index_url=r'http://www.dytt8.net/index.htm'
base_url=r'http://www.dytt8.net/html/gndy/dyzz/20170305/53401.html'

def time_delay(t):   
    print('delayed')
    time.sleep(t)

def upload():
    print('upload')
    ans=commands.getoutput(r'bypy upload .*')
    print(ans)

def redytt():
    print('redytt')
    ans=commands.getoutput(r'python dytt.py')
    print(ans)

if __name__=="__main__":
    while True:
        time_delay(1800)
        upload()
        time_delay(1800)
        redytt()

