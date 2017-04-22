import os
import sys
import re

def geturllist():
  print("start2")
  fin = open('H:\outstr.txt', 'r')
  print("open")
  while fin.next:
    print("open")
    line = fin.readline()
    if (len(line)==0):
      print("read over")
      break
    print(line)
    urllist.append(str(line))

def passrept(inurl):
    for i in urllist:
      print(i)
      obj = re.search(inurl, i,  re.M|re.I)
      if obj:
        print("catch it")
        return False
    print("download it")
    return False

if __name__ == '__main__':
  urllist = []
  geturllist()
  passrept()
