#coding:utf-8
#Destroyer IgnaleoG for civil use
#驱逐舰伊格那雷奥G型民用版本
#MIT License
#Python 3.6 or 3.7
#More examples will be added in the future

#Thank Chtholly Nota Seniorious for encouraging me to build Ignaleo destroyers

import asyncio,gevent
from gevent import monkey
monkey.patch_all()

import functools,os,time,gc,random,re

portList=tuple([i for i in range(55568,55569)])#本服务器监听端口

#超时设置
request_timeout=80
captcha_timeout=80

import tornado.ioloop
import tornado.web
from tornado.platform.asyncio import AsyncIOMainLoop
#from concurrent.futures import ThreadPoolExecutor
import requests

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
def genHeaders():
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

#worker_loop=tornado.ioloop.IOLoop.instance()
worker_loop=asyncio.get_event_loop()
class MainHandler(tornado.web.RequestHandler):
    #@tornado.concurrent.run_on_executor
    def get(self, *args, **kwargs):
        self.write("Destroyer IgnaleoG is ready!")
        #gevent.spawn(a function with socket operations)

    #@tornado.concurrent.run_on_executor
    def post(self):
        #gevent.spawn(a function with socket operations)

def run_proc(port):
    AsyncIOMainLoop().install()
    app=tornado.web.Application([
        (r'/',MainHandler),
    ])
    app.listen(port)
    print('DestroyerIgnaleoG@localhost:%d'%(port))
    worker_loop.run_forever()

if __name__ == '__main__':
    from multiprocessing import Process
    length=len(portList)
    for port in range(length-1):
        p=Process(target=run_proc, args=(portList[port],))
        p.start()
    run_proc(portList[length-1])
