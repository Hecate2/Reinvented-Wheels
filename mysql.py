#coding:utf-8
#使用gevent使requests异步化
import asyncio,gevent,time

from gevent import monkey
monkey.patch_all()

import functools,os,time,gc,random,re
repattern=re.compile('voting_token" value="(.*?)"')

portList=tuple([i for i in range(55568,55569)])#本服务器监听端口

#超时设置
request_timeout=80
captcha_timeout=80

import tornado.ioloop
import tornado.web
from tornado.platform.asyncio import AsyncIOMainLoop
#from concurrent.futures import ThreadPoolExecutor
import requests,cfscrape

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from fake_useragent import UserAgent
uaGen = UserAgent(
    fallback="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
    )
acceptLanguage=(
    'zh-cn,zh;q=0.8,zh-tw;q=0.7,zh-hk;q=0.5,en-us;q=0.3',
    'zh-cn,zh;q=0.8,zh-tw;q=0.7,zh-hk;q=0.5',
    )
indexLanguage=len(acceptLanguage) - 1
def genHeaders():#aiohttp会自动生成大部分header
    headers = {
        'User-Agent': uaGen.random,
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'Referer': "https://www.internationalsaimoe.com/voting/",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': acceptLanguage[random.randint(0, indexLanguage)],
        #'cache-control': "no-cache",
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1',
    }
    return headers
localsession=requests.Session()

RequestExceptions=(
    requests.RequestException,
    requests.ConnectionError,
    requests.HTTPError,
    requests.Timeout,
    )

from retryapi import retry,RetryExhausted

import MySQLdb

from sqlalchemyOps import QueryConn

import pymysql

#worker_loop=tornado.ioloop.IOLoop.instance()
worker_loop=asyncio.get_event_loop()
class MainHandler(tornado.web.RequestHandler):
    #@tornado.concurrent.run_on_executor
    def get(self, *args, **kwargs):
        self.write("Destroyer IgnaleoG is ready!<br><br>")
        tries=1000

        '''MySQLdb + gevent'''
        db=MySQLdb.connect(host='localhost',port=3306,user='root',passwd='a',db='mysql')
        c=db.cursor()
        startTime=time.time()
        gevent.joinall([gevent.spawn(c.execute,'SELECT * FROM `sys`.`sys_config` LIMIT 0, 1000') for i in range(tries)])
        endTime=time.time()
        self.write('%d MySQLdb concurrent tries with gevent<br>'%(tries)+
            'Time elapsed: '+str(endTime-startTime)+' seconds<br><br>')

        time.sleep(0.2)

        '''MySQLdb'''
        db=MySQLdb.connect(host='localhost',port=3306,user='root',passwd='a',db='mysql')
        c=db.cursor()
        startTime=time.time()
        for i in range(tries):
            result = c.execute('SELECT * FROM `sys`.`sys_config` LIMIT 0, 1000')
            #self.write(str(result.fetchone()))
            #self.write('<br>')
        endTime=time.time()
        self.write('%d MySQLdb sequential tries<br>'%(tries)+
            'Time elapsed: '+str(endTime-startTime)+' seconds<br><br>')

        time.sleep(0.2)

        '''pymysql + gevent'''
        pydb = pymysql.connect(host = 'localhost', user = 'root', passwd = 'a', db= 'mysql')
        pycursor = db.cursor()
        startTime=time.time()
        gevent.joinall([gevent.spawn(pycursor.execute,'SELECT * FROM `sys`.`sys_config` LIMIT 0, 1000') for i in range(tries)])
        endTime=time.time()
        self.write('%d pymysql concurrent tries with gevent<br>'%(tries)+
            'Time elapsed: '+str(endTime-startTime)+' seconds<br><br>')

        time.sleep(0.2)

        '''pymysql'''
        pydb = pymysql.connect(host = 'localhost', user = 'root', passwd = 'a', db= 'mysql')
        pycursor = db.cursor()
        startTime=time.time()
        for i in range(tries):
            result = pycursor.execute('SELECT * FROM `sys`.`sys_config` LIMIT 0, 1000')
        endTime=time.time()
        self.write('%d pymysql sequential tries<br>'%(tries)+
            'Time elapsed: '+str(endTime-startTime)+' seconds<br><br>')

        time.sleep(0.2)

        '''sqlalchemy (pymysql)'''
        q=QueryConn()
        connection=q.connect()
        startTime=time.time()
        for i in range(tries):
            result = connection.execute('SELECT * FROM `sys`.`sys_config` LIMIT 0, 1000')
        endTime=time.time()
        self.write('%d sqlalchemy (pymysql) sequential tries<br>'%(tries)+
            'Time elapsed: '+str(endTime-startTime)+' seconds<br><br>')

        time.sleep(0.2)

    #@tornado.concurrent.run_on_executor
    def post(self):
        pass

def run_proc(port):
    AsyncIOMainLoop().install()
    app=tornado.web.Application([
        (r'/',MainHandler),
    ])
    app.listen(port)
    print('DestroyerIgnaleoG@localhost:%d'%(port))
    worker_loop.run_forever()

if __name__ == '__main__':
    print("本服务器测试MySQL的异步连接")
    from multiprocessing import Process
    length=len(portList)
    for port in range(length-1):
        p=Process(target=run_proc, args=(portList[port],))
        p.start()
    run_proc(portList[length-1])
