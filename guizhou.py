
#coding=utf-8
import urllib
import urllib2
import re
import sys
import time
import requests
from lxml import etree
#from pytesser import *
from PIL import Image
import math
import dbutil
reload(sys)
sys.setdefaultencoding('utf-8')
time=int(time.time())
location=['贵阳','六盘水','遵义','安顺','毕节','铜仁','黔西','黔东','黔南']
session=requests.session()
user_agent='Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'
headers={'User-Agent':user_agent,'Host':'gsxt.gzgs.gov.cn:8080'}

captchaUrl='http://gsxt.gzgs.gov.cn:8080/xwqyweb/app/code'
captchahtml=session.get(captchaUrl,headers=headers)
captchacontent=captchahtml.content
with open('captcha.jpg', "wb") as output:
            output.write(captchacontent)
Image.open('captcha.jpg').show()
captcha = raw_input("enter captcha：")
print captcha

def if_null(list):
    if list==[]:
        list.append("无")
        return list
    else:
        return list

mysql=dbutil.Mysql()
for dest in location:
    url='http://gsxt.gzgs.gov.cn:8080/xwqyweb/app/xwqyjbxx/list'
    postdata={'act':'/xwqyweb/app/xwqyjbxx/list','page':'1','key':str(dest),'textfield2':'2'}
    html=session.post(url=url,data=postdata,cookies=captchahtml.cookies,headers=headers )
    content=html.content
    tree=etree.HTML(content)
    recordcount=tree.xpath('//p[@id="page"]/span/text()')
    for i in recordcount:
        count=(int(filter(str.isdigit,str(i))))/10
        pagecount=int(math.ceil(count/10.0))
        for pageno in range(1,pagecount+1):
            postdata={'act':'/xwqyweb/app/xwqyjbxx/list','page':str(pageno),'key':str(dest),'textfield2':'2'}
            url='http://gsxt.gzgs.gov.cn:8080/xwqyweb/app/xwqyjbxx/list'
            html=session.post(url=url,headers=headers,data=postdata,cookies=captchahtml.cookies)
            infor=(html.content)
            tree = etree.HTML(infor)
            mom=tree.xpath('//table[@class="tbList1"]/tr/td[@nowrap="nowrap"]/text()')
            r_url=tree.xpath('//table[@class="tbList1"]/tr/td/a/@href')
            reg=[]
            for i in mom:
                reg.append(i)
            for i in r_url:
                url= 'http://gsxt.gzgs.gov.cn:8080'+str(i)
                print url
                page=session.get(url=url,headers=headers)
                print page.content
                tree = etree.HTML(page.content)
                entname =if_null(tree.xpath('//div[@class="tbShadow1"]/table/tr[1]/td[1]//text()'))
                regno=if_null(tree.xpath('//div[@class="tbShadow1"]/table/tr[1]/td[2]//text()'))
                cotype=if_null(tree.xpath('//div[@class="tbShadow1"]/table/tr[2]/td[1]//text()'))
                estdate=if_null(tree.xpath('//div[@class="tbShadow1"]/table/tr[2]/td[2]//text()'))
                localorg=if_null(tree.xpath('//div[@class="tbShadow1"]/table/tr[3]/td[1]//text()'))
                industryphy=if_null(tree.xpath('//div[@class="tbShadow1"]/table/tr[3]/td[2]//text()'))
                wdhy=if_null(tree.xpath('//div[@class="tbShadow1"]/table/tr[4]/td[1]//text()'))
                regcep=if_null(reg)
                insert_sql='INSERT INTO xw.贵州 VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
                #这里输出全是乱码！！！！！！！！！！！！！！！！！
                param=(str(entname[0]),str(estdate[0]),str(regno[0]),str(wdhy[0]),str(regcep[0]),str(industryphy[0]),str(localorg[0]),str(cotype[0]))
                #mysql.insertOne(insert_sql,param)
                print "data....................",pagecount,pageno,dest
                del reg[0]

mysql.dispose()