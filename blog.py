#conding='utf-8'
import requests
from lxml import etree
import dbutil
import sys
import threading
import Queue

reload(sys)
sys.setdefaultencoding('utf-8')
session=requests.session()
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'}
cookies={'bdshare_firstime':'1462339277944','uuid_tt_dd':'-154572344638092054_20160504','_message_m':'wxhmbjtim3qwwyszep3s3051','_gat':'1','aliyungf_tc':'AQAAAF4U21sgHwAAuoRe2nkdUuR4X+HO','__utmt':'1','FirstBlog':'XLiUJv7fl6URZSDS6RDTqA%3d%3d','_ga':'GA1.2.1546434951.1467267771','UserName':'fuyunkaka','UserInfo':'R3Ffo%2BiBaH7o06CKPernw1pvvBmFh1OU8xmMNx9j3%2FPPuW7xnZkVtsZ3B9ZBTs7ypLe2IJbP%2FJJOGoj5UUx59R%2Fj4hvN7kU13M5RkgiKhHpzK2bzPRU%2FoXuf7xeLT9KCAz4jvqHVogHeu4QfcgAI2g%3D%3D','UserNick':'fuyunkaka','AU':'C53','UN':'fuyunkaka','UE':'"15951817767@163.com"', 'BT':'1467267818040','access-token':'9a4f1797-9506-4874-8134-fc21cf7d0d0e','__utma':'17226283.1546434951.1467267771.1467267785.1467267785.1', '__utmb':'17226283.5.10.1467267785','__utmc':'17226283','__utmz':'17226283.1467267785.1.1.utmcsr=passport.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/account/login','uuid':'65348c8d-9a8f-4201-b6c2-2cac26b97cca','dc_tos':'o9kn3g','dc_session_id':'1467267807956','__message_sys_msg_id':'0', '__message_gu_msg_id':'0','__message_cnel_msg_id':'0','__message_district_code':'320000', '__message_in_school':'0'}
queue=Queue.Queue()
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
        for i in detailUrls:
            queue.put('http://blog.csdn.net'+str(i))
            print i
		#return items

class detailBlog(threading.Thread):
    def __init__(self,url):
        threading.Thread.__init__(self)
        self.url=url
        self.headers=headers
        self.cookies=cookies
    def getDetail(self):
        html=session.get(url=self.url,headers=self.headers,cookies=self.cookies)
        page=html.text
        tree=etree.HTML(page)
        contents=tree.xpath('//div[@id="article_content"]/text()')
        for i in contents:
            contentBlog.append(i)
            print i


class myThreading(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.threadList=[]
    def runThread(self):
        msg=queue.get()

        self.threadList.append(detailBlog(msg))
        self.threadList[0].start()
        #print len(self.threadList)
        #for i in range(len(self.threadList)):
        #    self.threadList[i].start()
        #for i in range(len(self.threadList)):
        #    self.threadList[i].join()
    def run(self):
        self.runThread()

blog=myBlog()
blog.splitHtml()
myThread=myThreading()
myThread.run()



