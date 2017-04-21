import pymongo

from config import DB_CONFIG, DEFAULT_SCORE

from ISqlHelper import ISqlHelper
from MongoHelper import MongoHelper
from RedisHelper import RedisHelper
import re
import json

class DBHandler():

  def __init__(self):
    self.redishelper=RedisHelper()
    self.mongohelper=MongoHelper()

if __name__ == '__main__':
  dbhandler=DBHandler()
  for key in dbhandler.redishelper.get_all_keys():
    string=str(dbhandler.redishelper.get(key))
    string=re.sub("b'","'",string)
    string=re.sub("'",'"',string)
    string=re.sub(r"\\x",r"\\\\x",string)
    string=re.sub('""','" "',string)
    try:
      string=json.loads(string)
      print(string)
      dbhandler.mongohelper.insert(string)
    except:
      continue

