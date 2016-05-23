
#coding=utf-8
import requests
from lxml import etree
from PIL import Image
session=requests.session()


class Spider():
    def __init__(self,user_agent):
        self.headers={'User-Agent':user_agent}


    def get_html(self,method,url,cookies=None,proxies=None,data=None,params=None):
        if method=="post":
            html=session.post(url=url,headers=self.headers,cookies=cookies,data=data,params=params,proxies=proxies)
        else:
            html=session.get(url=url,headers=self.headers,cookies=cookies,data=data,params=params,proxies=proxies)
        page=html.content
        return html,page

    def captcha_input(self,captcha_page):
        with open('captcha.jpg', "wb") as output:
            output.write(captcha_page)
        Image.open('captcha.jpg').show()
        captcha = raw_input("enter captcha：")
        return captcha


    def get_info(self,page,postion):#存放位置公司名，注册日期，注册号，行业代码，注册资本，所属门类，登记机关，企业类型)，必要时调整位置
        def if_null(list):
            if list==[]:
                list.append("无")
                return list
            else:
                return list
        tree = etree.HTML(page)
        entname = if_null(tree.xpath('//div[@class="tbShadow1"]/table/tr[1]/td[1]//text()'))
        regno=if_null(tree.xpath('//div[@class="tbShadow1"]/table/tr[1]/td[2]//text()'))
        cotype=if_null(tree.xpath('//div[@class="tbShadow1"]/table/tr[2]/td[1]//text()'))
        estdate=if_null(tree.xpath('//div[@class="tbShadow1"]/table/tr[2]/td[2]//text()'))
        localorg=if_null(tree.xpath('//div[@class="tbShadow1"]/table/tr[3]/td[1]//text()'))
        industryphy=if_null(tree.xpath('//div[@class="tbShadow1"]/table/tr[3]/td[2]//text()'))
        wdhy=if_null(tree.xpath('//div[@class="tbShadow1"]/table/tr[4]/td[1]//text()'))
        regcep=if_null(tree.xpath('//div[@class="tbShadow1"]/table/tr[4]/td[2]//text()'))
        param=(entname[0],estdate[0],regno[0],wdhy[0],regcep[0],industryphy[0],localorg[0],cotype[0])
        return param

    def get_pagecount(self,page,xpathStr):
        tree=etree.HTML(page)
        pagenumber=tree.xpath(xpathStr)
        for i in pagenumber:
            import math
            totalpage=filter(str.isdigit,str(i))
            #totalrecord=filter(str.isdigit,str(i))
            #totalpage=int(math.ceil(int(totalrecord)/10))
            return totalpage

    def save(self,sqlStr,param):
        import dbutil
        mysql=dbutil.Mysql()
        mysql.insertOne(sqlStr,param)
        mysql.dispose()

#天津微小企业爬虫举例
import time
import json
user_agent='Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'
spider=Spider(user_agent)



captchaUrl='http://www.tjcredit.gov.cn/xwqy/randomCode/generate?time='+str(time) #param={'time'；str(time)},get
captcha_html,captcha_page=spider.get_html("get",captchaUrl,params={'time':str(time)})
captcha=spider.captcha_input(captcha_page)

verifyUrl='http://www.tjcredit.gov.cn/xwqy/randomCode/validCode?c='+str(captcha)#+str(captcha) #data={'c':captcha},post
verify_html,verify_page=spider.get_html("post",verifyUrl,data={'c':captcha},cookies=captcha_html.cookies)
print verify_page

for pageno in range(1,2):
    searchUrl='http://www.tjcredit.gov.cn/xwqy/enterprise/search'# data={'entname':'天津','pageSize':;10','pageIndex':str(pageno)},post
    search_html,search_page=spider.get_html("post",searchUrl,data={'entname':'天津','pageSize':'10','pageIndex':str(pageno)},cookies=captcha_html.cookies)
    tree=etree.HTML(search_page)
    details=tree.xpath('//a[@onclick]//@onclick')
    for detail in details:
        print detail
        entid=(str(detail).split("'"))[1]
        detailUrl='http://www.tjcredit.gov.cn/xwqy/enterprise/detail'#params={'entId':entid} ,post
        detail_html,detail_page=spider.get_html("post",detailUrl,params={'entId':entid},cookies=captcha_html.cookies)
        info=spider.get_info(detail_page,None)
        print info

