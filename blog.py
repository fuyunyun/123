#conding='utf-8'
import requests
from lxml import etree
import dbutil
import sys
import threading
""" 多线程爬取"""
reload(sys)
sys.setdefaultencoding('utf-8')
session=requests.session()
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'}
"""
@设置cookie
cookies={}
"""
msg=[]
contentBlog=[]
class myBlog():
    def __init__(self):
        self.url='http://blog.csdn.net/fuyunkaka'
        self.headers=headers
        #self.data=data
        self.cookies=cookies

    def getPage(self):
        html=session.get(url=self.url,headers=self.headers,cookies=self.cookies)
        page=html.text
        return page

    def splitHtml(self):
        page=self.getPage()
        tree=etree.HTML(page)
        detailUrls=tree.xpath('//span[@class="link_title"]/a/@href')
        return detailUrls

class detailBlog(threading.Thread):
    def __init__(self,url):
        threading.Thread.__init__(self)
        self.url='http://blog.csdn.net'+url
        self.headers=headers
        self.cookies=cookies
    def getDetail(self):
        html=session.get(url=self.url,headers=self.headers,cookies=self.cookies)
        page=html.text
        print page
        tree=etree.HTML(page)
        contents=tree.xpath('//div[@id="article_content"]/text()')
        for i in contents:
            contentBlog.append(i)
            print i
    def run(self):
        self.getDetail()


class myThreading(threading.Thread):
    def __init__(self,urls):
        threading.Thread.__init__(self)
        self.threadList=[]
    def runThread(self):
        for url in urls:
            print url
            self.threadList.append(detailBlog(url))
        for i in range(len(self.threadList)):
                self.threadList[i].start()
        for i in range(len(self.threadList)):
                self.threadList[i].join()
    def run(self):
        self.runThread()

blog=myBlog()
urls=blog.splitHtml()
myThread=myThreading(urls)
myThread.run()



