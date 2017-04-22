# -*- coding: UTF-8 -*-
import MySQLdb as mdb
import time

start=time.time()
def createTrain():
    try:
        #将con设定为全局连接
        con = mdb.connect('localhost', 'root', 'zean', 'mydb',charset='utf8');#
        with con:
            #获取连接的cursor，
            cur = con.cursor()
            #创建一个数据表 writers(id,name)
            #cur.execute("DROP TABLE IF EXISTS mydb")
            cur.execute("CREATE TABLE a (\
            uid varchar(255) NOT NULL,\
            mid varchar(255) NOT NULL,\
            time date NOT NULL,\
            ) ENGINE=MyISAM DEFAULT CHARSET=utf8;")
            #cur.execute("set names 'utf8'")
            input = open('a.txt')
            for line in input:
                linelist = line.split('\t')
                cur.execute("INSERT INTO a(uid, mid, time, content)\
                VALUES(%s,%s, %s)", [linelist[0], linelist[1], linelist[2]])
    except mdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        con.close()
createTrain()
print time.time()-start
print 'done'