# -*- codeing=utf-8 -*-
import os
import sys
import re
print('start')
fin = open(r'H:\basestr.json')
fout = open(r'H:\outstr.txt', 'w')
while (fin.next):
  line = fin.readline()
  if len(line)==0:
      break
#  print(line)
  obj = re.search(u'http.*html', line, re.M|re.I)
  if obj:
    fout.writelines(obj.group(0)+'\n')
print('end')
fin.close()
fout.close()    
  