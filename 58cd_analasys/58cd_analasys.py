#!/usr/bin/env python
# coding=utf-8

#58cd_analasys.py

import re
import sys
import time 
import traceback
import codecs
import json
import chardet

reload(sys)
sys.setdefaultencoding("utf-8")

items_list=[]

def readfile_2_list():
    g=codecs.open('./output.txt','w','utf8')
    f=codecs.open('./58data.txt','r','utf8')
    lines=f.readlines()
    for line in lines:
        line=line.encode('utf8')
        house_item=[]
        outstr=""
        words=line.split(',')
        house_item.append(str(words[0]))
        house_item.append(str(words[-1]))
        for word in words:
            word=str(word).encode('utf8')
            if '(\d+)m' in word:
                house_item.append(word)
            if '地铁站' in word:
                house_item.append(word)
            if '\d室' in word:
                house_item.append(word)
        line=re.sub(",","",line)
        house_item.append(line.encode('utf8'))
        outstr=",".join(house_item)
        outstr=re.sub("\r\n","",outstr)
        print(outstr.encode('utf8'))
        g.write(outstr.encode('utf8'))
        g.write("\r\n")

readfile_2_list()      






