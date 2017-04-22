# -*- coding: utf-8 -*-
COOKIES_ENABLES=False
# Scrapy settings for LianJia project
AGENTS = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "  
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",  
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "  
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",  
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "  
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",  
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "  
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",  
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "  
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",  
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "  
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",  
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "  
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",  
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",  
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",  
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "  
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",  
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "  
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",  
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "  
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"  

]


PROXYS = [
    {'ip_port': '115.204.28.138:808', 'user_pass': ''},
    {'ip_port': '217.146.214.206:8080', 'user_pass': ''},
    {'ip_port': '58.251.227.240:9797', 'user_pass': ''},
    {'ip_port': '119.40.106.33:8081', 'user_pass': ''},
    {'ip_port': '82.206.132.118:80', 'user_pass': ''},
    {'ip_port': '46.0.196.220:8081', 'user_pass': ''},
    {'ip_port': '163.125.193.168:9797', 'user_pass': ''},
    {'ip_port': '162.105.80.111:3128', 'user_pass': ''},
    {'ip_port': '200.229.193.182:8080', 'user_pass': ''},
    {'ip_port': '163.172.28.61:8080', 'user_pass': ''},
    {'ip_port': '103.5.173.153:8080', 'user_pass': ''},
    {'ip_port': '125.121.122.165:808', 'user_pass': ''},
    {'ip_port': '191.242.113.1:8080', 'user_pass': ''},
    {'ip_port': '185.112.180.249:8080', 'user_pass': ''},
    {'ip_port': '36.66.203.139:3128', 'user_pass': ''},
    {'ip_port': '203.76.222.198:8080', 'user_pass': ''},
    {'ip_port': '200.84.233.81:8080', 'user_pass': ''},
    {'ip_port': '138.68.88.61:3128', 'user_pass': ''},
    {'ip_port': '160.202.42.58:8080', 'user_pass': ''},

]


BOT_NAME = 'LianJia'

SPIDER_MODULES = ['LianJia.spiders']
NEWSPIDER_MODULE = 'LianJia.spiders'


ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 3

SCHEDULER = "scrapy_redis.scheduler.Scheduler"    #调度
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"  #去重
SCHEDULER_PERSIST = True       #不清理Redis队列
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"    #队列

ITEM_PIPELINES = {
   'LianJia.pipelines.MyscrapyPipeline': 300,
}

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = "lianjia"
MONGODB_DOCNAME = "saveinfo_5"
