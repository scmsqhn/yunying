#!/usr/bin/env python
# coding=utf-8

import re
import sys
import time 
import traceback
import codecs
import json


reload(sys)
sys.setdefaultencoding('utf-8')

direct_set=set()

def readfile_2_set():
    f=codecs.open('./cdesf.json','r','utf8')
    lines=f.readlines()
    for line in lines:
 #       print(type(line))
        line=json.loads(line)
        a=line['house'].split('|')[0].strip()
        if a not in direct_set:
            direct_set.add(a)
#            print('add')
        else:
            pass
#            print('no_add')
#        print(a.encode('utf8'))
#        print('noadd')

readfile_2_set()      

dicts_sell_vs_buyers={}

def add_sell_with_direct():
    g=codecs.open('./output.txt','a+','utf8')
    f=codecs.open('./cdesf.json','r','utf8')
    lines=f.readlines()
    for set in direct_set:
#        print(set.encode('utf8'))
        finalprice=0
        finaleyeson=0
        finalvisit=0
        finalmipri=0
        findlarea=""
        findlfloor=0
        findlyear=0
        count=0
        for line in lines:
            if set in line:
               line=json.loads(line)
               finalprice=finalprice+float(line['price'])
               visit=line['buyer'].split('/')[0]
               visit=re.sub('\D','',visit)
               finalvisit=finalvisit+int(visit)
               eyeson=line['buyer'].split('/')[1]
               eyeson=re.sub('\D','',eyeson)
               finaleyeson=finaleyeson+int(eyeson)
               mipri=line['mipri']
               #print(mipri.encode('utf8'))
               mipri=re.sub('\D','',mipri)
               finalmipri=finalmipri+int(mipri)
               count= count+1
              # print(count)
              # print(finalmipri)
               finalarea=line['build'].split('-')[1].strip()
               try:
                 floor=line['build'].split('-')[0].split(')')[0].strip()
                 finalfloor=re.sub('\D','',floor)
                 year=line['build'].split('-')[0].split(')')[1].strip()
                 finalyear=re.sub('\D','',year)
               except:
                 finalfloor=""
                 year=line['build'].split('-')[0].strip()
                 finalyear=re.sub('\D','',year)
  #               print(finalyear)
  #               print(finalfloor)
  #               time.sleep(10)

#               print(finalarea.encode('utf8'))

        finalmipri= finalmipri/count
#        print(finalmipri)
 #       print(finalmipri)
      # print(set.encode('utf8'),finalprice,int(finalvisit),int(finaleyeson))
        final_list=[set,str(finalprice),str(finaleyeson),str(finalvisit),str(finalmipri),str(finalfloor),str(finalyear),str(count),finalarea]
        g.write(','.join(final_list))
        g.write('\r\n')

          
add_sell_with_direct()








