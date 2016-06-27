#coding=utf-8

import requests
from lxml import  etree
import time
import socket
socket.setdefaulttimeout(2)
class getAddress():
    def __init__(self):
        self.pageno=1
        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        self.url='http://www.xicidaili.com/nn/'+str(self.pageno)
#postdata={'cnzz_eid':'2109631214-1462333134-','h':'1','id':'1256960793','lg':'zh-cn','ntime':str(time.time()),'r':'http://www.xicidaili.com/nn/','rnd':'1594815936','showp':'1920x1080','t':'国内高匿免费HTTP代理IP__第'+str(pageno)+'页国内高匿'}
    def run(self):
        session=requests.session()
        html=session.get(url=self.url,headers=self.headers)
        return html.text
    def getAddr(self,page):
        tree=etree.HTML(page)
        lists=tree.xpath('//table[@id="ip_list"]/tr[@class]')
        address=[]
        for i in range(1,len(lists)+1):
            ip=tree.xpath('//table[@id="ip_list"]/tr[@class]['+str(i)+']/td[2]/text()')
            port=tree.xpath('//table[@id="ip_list"]/tr[@class]['+str(i)+']/td[3]/text()')
            http=tree.xpath('//table[@id="ip_list"]/tr[@class]['+str(i)+']/td[6]/text()')
            address.append('{"'+http[0].strip().lower()+'":"'+http[0].strip().lower()+'://'+ip[0].strip()+':'+port[0].strip()+'"}')
        return address
    def chooseAddr(self,testUrl,address):
        chooseAddr=[]
        session=requests.session()
        for addr in address:
            try:
                html=session.get(url=testUrl,proxies=eval(addr))
                chooseAddr.append(addr)
            except Exception,e:
                print e
                print addr
        return chooseAddr
testUrl='http://gsxt.scaic.gov.cn/xxcx.do?method=ycmlIndex&random='+str(int(time.time()))+'&cxyzm=no&entnameold=&djjg=&maent.entname=&page.currentPageNo=1&yzm='
getADDR=getAddress()
address=getADDR.getAddr(getADDR.run())
chooseAddr=getADDR.chooseAddr(testUrl=testUrl,address=address)
print chooseAddr
#print address







