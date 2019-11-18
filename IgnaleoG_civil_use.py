#coding:utf-8
portList=[port for port in range(55568,55569)]

#使用gevent使requests等socket操作异步化
import asyncio,gevent
from gevent import monkey
monkey.patch_all()

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

RequestExceptions=(
    requests.RequestException,
    requests.ConnectionError,
    requests.HTTPError,
    requests.Timeout,
    )

from retryapi import retry,RetryExhausted
import gc

#worker_loop=tornado.ioloop.IOLoop.instance()
worker_loop=asyncio.get_event_loop()
class MainHandler(tornado.web.RequestHandler):
    #executor = ThreadPoolExecutor(30)

    class VoterMT:
        def __init__(self,proxy,loop,localsession,id=0):
            self.proxy=proxy
            self.loop=loop
            self.session=requests.Session()
            self.localsession=localsession
            #self.executor=executor
            self.id=id #用于标记这次投票是第几次

        @retry(exceptions=RequestExceptions,tries=2,logger=None)
        def _get(self,url,timeout=request_timeout):
            with self.session.get(url,timeout=timeout,proxies={"http":self.proxy,"https":self.proxy},verify=False) as response:
                if (response.status_code<400):
                    if 'text' in response.headers['content-type']:
                        #f=open('./tmp.txt','a',encoding='utf-8')
                        #f.write(text)
                        #f.close()
                        return response.text
                    #if 'image' in response.content_type:
                    else:
                        #fb=open('./tmp.png','wb')
                        #fb.write(body)
                        #fb.close()
                        return response.content
                #if (response.status==503):
                    #pass
                    #处理cloudflare防火墙
                else:
                    #print(response.status_code)
                    return response.raise_for_status()

        @retry(exceptions=RequestExceptions,tries=2,logger=None)
        def _localget(self,url,timeout=request_timeout):
            with self.session.get(url,timeout=timeout) as response:
                if (response.status_code<400):
                    if 'text' in response.headers['content-type']:
                        #f=open('./tmp.txt','a',encoding='utf-8')
                        #f.write(text)
                        #f.close()
                        return response.text
                    #if 'image' in response.content_type:
                    else:
                        #fb=open('./tmp.png','wb')
                        #fb.write(body)
                        #fb.close()
                        return response.content
                #if (response.status==503):
                    #pass
                    #处理cloudflare防火墙
                else:
                    return response.raise_for_status()
                
        @retry(exceptions=RequestExceptions,tries=2,logger=None)
        def _post(self,url,data,timeout=request_timeout):
            with self.session.post(url,data=data,timeout=timeout,proxies={"http":self.proxy,"https":self.proxy},headers={'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'},verify=False) as response:
                if (response.status_code<400):
                    return response.text
                else:
                    return response.raise_for_status()
        
        @retry(exceptions=RequestExceptions,tries=2,logger=None)
        def _localpost(self,url,data,timeout=request_timeout):
            with self.localsession.post(url,data=data,timeout=timeout,verify=False) as response:
                if (response.status_code<400):
                    return response.text
                else:
                    return response.raise_for_status()

    #@tornado.concurrent.run_on_executor
    def get(self, *args, **kwargs):
        gc.collect()
        self.write('Ignaleo: 清理内存')
        print('Ignaleo: 清理内存')
        
    #@tornado.concurrent.run_on_executor
    def post(self):
        #gc.collect()
        proxies=self.request.body.decode(encoding='utf-8').split('\r\n')
        self.write('收到POST')
        print('Ignaleo: 收到POST')
        #print('收到POST\n',proxies)
        for proxy in proxies:
            pass
            #gevent.spawn(a function with socket I/O, e.g. HTTP requests, database operations)

def run_proc(port):
    AsyncIOMainLoop().install()
    app=tornado.web.Application([
        (r'/',MainHandler),
    ])
    app.listen(port)
    print('DestroyerIgnaleoG@localhost:%d'%(port))
    #worker_loop.start()
    worker_loop.run_forever()

if __name__ == '__main__':
    from multiprocessing import Process
    length=len(portList)
    for port in range(length-1):
        p=Process(target=run_proc, args=(portList[port],))
        p.start()
    run_proc(portList[length-1])
