#-*-coding:utf8-*-

import urllib2
import re
import threading
import time
import requests
rawProxyList = []
checkedProxyList = []
#抓取代理网站
targets=[]
for i in range(1,3):
    target = r"http://www.xici.net.co/nn/%d" % i
    targets.append(target)
    #print target

#正则
p = re.compile(r'''<tr class=".+?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>.+?(\d{2,4})</td>.+?<td>(.{4,5})</td>''',re.DOTALL)
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
#获取代理的类
class ProxyGet(threading.Thread):
    def __init__(self,target):
        threading.Thread.__init__(self)
        self.target = target

    def getProxy(self):
        print "目标网站："+self.target
        session=requests.session()
        req=session.get(url=self.target,headers=headers)
        result=req.text
        matchs = p.findall(result)
        for row in matchs:
            ip = row[0]
            port = row[1]
            agent = row[2]
            addr=agent+'://'+ip+':'+port
            proxy = [ip,port,addr]
            rawProxyList.append(proxy)

    def run(self):
        self.getProxy()

#检验代理类
class ProxyCheck(threading.Thread):
    def __init__(self,proxyList):
        threading.Thread.__init__(self)
        self.proxyList = proxyList
        self.timeout=5
        self.data={'entNameOrRegNo':'浙江','pagination.currentPage':1,'pagination.pageSize':'10'}
        self.testUrl = "http://gsxt.zjaic.gov.cn/small/doReadSmallEntDirInfoListJSON.do"
        self.testStr = "pages"

    def checkProxy(self):
        session=requests.session()
        for proxy in self.proxyList:
            t1 = time.time()
            proxies={"http" : r'http://%s:%s' %(proxy[0],proxy[1])}
            try:
                req=session.get(url=self.testUrl,proxies=proxies,headers=headers,timeout=self.timeout,data=self.data)
                #req = opener.open(self.testUrl,timeout=self.timeout)
                #result=req.read()
                result=req.text
                timeused = time.time()-t1
                #pos = result.find(self.testStr)
                #print pos
                #if pos > 1:
                if "200" in str(req):
                    checkedProxyList.append((proxy[0],proxy[1],proxy[2],timeused))
                else:
                    continue
            except Exception,e:
                continue

    def run(self):
        self.checkProxy()

if __name__ == "__main__":
    getThreads=[]
    checkThreads=[]

#对每个目标网站开启一个线程负责抓取代理
for i in range(len(targets)):
    t = ProxyGet(targets[i])
    getThreads.append(t)
for i in range(len(getThreads)):
    getThreads[i].start()

for i in range(len(getThreads)):
    getThreads[i].join()

print '.'*10+"总共抓取了%s个代理" %len(rawProxyList) +'.'*10

#开启20个线程负责校验，将抓取到的代理分成20份，每个线程校验一份
for i in range(20):
    t = ProxyCheck(rawProxyList[((len(rawProxyList)+19)/20) * i:((len(rawProxyList)+19)/20) * (i+1)])
    checkThreads.append(t)

for i in range(len(checkThreads)):
    checkThreads[i].start()

for i in range(len(checkThreads)):
    checkThreads[i].join()

print '.'*10+"总共有%s个代理通过校验" %len(checkedProxyList) +'.'*10
proxiesF="{"
#持久化
for i in range(len(checkedProxyList)):
    proxy0=checkedProxyList[i][0]
    proxy1=checkedProxyList[i][1]
    if i==len(checkedProxyList)-1:
        proxiesF=proxiesF+'"http": "http://%s:%s"' %(proxy0,proxy1)
    else:
        proxiesF=proxiesF+'"http":"http://%s:%s",' %(proxy0,proxy1)
proxiesF=proxiesF+"}"
print proxiesF
f= open("proxy_list.txt",'w+')
f.write(str(proxiesF))
f.close()
