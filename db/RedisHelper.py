# coding:utf-8
from __future__ import unicode_literals

#from redis import Redis
import redis
import config
from ISqlHelper import ISqlHelper
from SqlHelper import Proxy

import codecs
import chardet

class RedisHelper(ISqlHelper):
    def __init__(self, url=None):
        print('__init__')
#        self.index_names = ('start','stop','ctry','prov','area','net')
        self.redis_url = url or config.DB_CONFIG['DB_CONNECT_STRING']

    def get_proxy_name(self, ip=None, port=None, protocal=None, proxy=None):
        ip = ip or proxy.ip
        port = port or proxy.port
        protocal = protocal or proxy.protocol
        return "proxy::{}:{}:{}".format(ip, port, protocal)

    def get_index_name(self, index_name, value=None):
        if index_name == 'score':
            return 'index::score'
        return "index::{}:{}".format(index_name, value)

    def get_proxy_by_name(self, name):
        pd = self.redis.hgetall(name)
        if pd:
            return Proxy(**{k.decode('utf8'): v.decode('utf8') for k, v in pd.items()})

    def init_db(self, url=None):
        print('init_db_redis')
        self.redis = Redis.from_url(url or self.redis_url)
        print(self.redis)

    def drop_db(self):
        return self.redis.flushdb()

    def get_keys(self, conditions):
        select_keys = {self.get_index_name(key, conditions[key]) for key in conditions.keys() if
                       key in self.index_names}
        if 'ip' in conditions and 'port' in conditions:
            return self.redis.keys(self.get_proxy_name(conditions['ip'], conditions['port'], '*'))
        if select_keys:
            return [name.decode('utf8') for name in self.redis.sinter(keys=select_keys)]
        return []

    def insert(self, value):
        print('__insert__')
        proxy = Proxy(ip=value['ip'], port=value['port'], types=value['types'], protocol=value['protocol'],
                      country=value['country'], area=value['area'],
                      speed=value['speed'], score=value.get('score', config.DEFAULT_SCORE))
        mapping = proxy.__dict__
        for k in list(mapping.keys()):
            if k.startswith('_'):
                mapping.pop(k)
        object_name = self.get_proxy_name(proxy=proxy)
        # 存结构
        insert_num = self.redis.hmset(object_name, mapping)
        # 创建索引
        if insert_num > 0:
            for index_name in self.index_names:
                self.create_index(index_name, object_name, proxy)
        print('__insert__')
        return insert_num

    def insertIp2DB(self, key, count, value):
        print(type(key))
        print(type(count))
        print(type(value))
        return Redis.zadd('myset', "b2", 1)
#        return Redis.zadd(key, value, count)
        
    def create_index(self, index_name, object_name, proxy):
        redis_key = self.get_index_name(index_name, getattr(proxy,index_name))
        if index_name == 'score':
            return self.redis.zadd(redis_key, object_name, int(proxy.score))
        return self.redis.sadd(redis_key, object_name)

    def delete(self, conditions):
        proxy_keys = self.get_keys(conditions)
        index_keys = self.redis.keys(u"index::*")
        if not proxy_keys:
            return 0

        for iname in index_keys:
            if iname == b'index::score':
                self.redis.zrem(self.get_index_name('score'), *proxy_keys)
            else:
                self.redis.srem(iname, *proxy_keys)
        return self.redis.delete(*proxy_keys) if proxy_keys else 0

    def update(self, conditions, values):
        objects = self.get_keys(conditions)
        count = 0
        for name in objects:
            for k, v in values.items():
                if k == 'score':
                    self.redis.zrem(self.get_index_name('score'), [name])
                    self.redis.zadd(self.get_index_name('score'), name, int(v))
                self.redis.hset(name, key=k, value=v)
            count += 1
        return count

    def select(self, count=None, conditions=None):
        count = (count and int(count)) or 1000  # 最多返回1000条数据
        count = 1000 if count > 1000 else count

        querys = {k: v for k, v in conditions.items() if k in self.index_names} if conditions else None
        if querys:
            objects = list(self.get_keys(querys))[:count]
            redis_name = self.get_index_name('score')
            objects.sort(key=lambda x: int(self.redis.zscore(redis_name, x)))
        else:
            objects = list(
                self.redis.zrevrangebyscore(self.get_index_name("score"), '+inf', '-inf', start=0, num=count))

        result = []
        for name in objects:
            p = self.get_proxy_by_name(name)
            result.append((p.ip, p.port, p.score))
        return result

    def simple_show(self):
      sqlhelper = RedisHelper()
      sqlhelper.init_db('redis://localhost:6379/9')
      proxy = {'ip': '192.168.1.1', \
      'port': 80, \
      'type': 0, \
      'protocol': 0, \
      'country': u'中国','area': u'广州', \
      'speed': 11.123,\
      'types': 1}
      
      proxy2 = {'ip': 'localhost', \
      'port': 433, \
      'type': 1, \
      'protocol': 1,'country': u'中国','area': u'广州', \
      'speed': 123,\
      'types': 0, \
      'score': 100}
      assert sqlhelper.insert(proxy) == True
      assert sqlhelper.insert(proxy2) == True
      assert sqlhelper.get_keys({'types': 1}) == ['proxy::192.168.1.1:80:0', ],sqlhelper.get_keys({'types': 1})
      assert sqlhelper.select(conditions={'protocol': 0})==[('192.168.1.1', '80', '0')]
      assert sqlhelper.update({'types': 1}, {'score': 888}) == 1
      assert sqlhelper.select() == [('192.168.1.1', '80', '888'), ('localhost', '433', '100')]
      # assert sqlhelper.delete({'types': 1}) == 1
      # sqlhelper.drop_db()
      print('All pass.')

    

if __name__ == '__main__':
  r = redis.StrictRedis(host='localhost', port=6379, db=0)
  with codecs.open('./ip3.csv','r','raw-unicode-escape') as f:
#  with codecs.open('./src_ip3.txt','r','raw-unicode-escape') as f:
    lines=f.readlines()
    count=0
    print('===')
    for line in lines:
      llist = line.split(',')
      r.lpush('ip_start_addr_list', llist[0])
'''''    for line in lines:
      llist = line.split(',')
      r.hset('ip_start_'+llist[0],'start',llist[0])
      r.hset('ip_start_'+llist[0],'stop',llist[1])
      r.hset('ip_start_'+llist[0],'country',llist[2])
      r.hset('ip_start_'+llist[0],'prov',llist[3])
      r.hset('ip_start_'+llist[0],'area',llist[4])
      r.hset('ip_start_'+llist[0],'net',llist[5])
'''