#coding=utf-8
import requests
from lxml import etree
import dbutil
import sys
import threading
import random
import math
import time
reload(sys)
sys.setdefaultencoding('utf-8')
user_agent=random.choice(['Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0'])
headers={'User-Agent':user_agent}
randomNum=int(time.time())
def if_null(list):
    if list==[]:
        list.append("无")
        return list
    else:
        return list
"""
@山西异常企业信息抓取
"""
session=requests.session()
"""获取总页数 """
def getpages():
    url='http://gsxt.fc12319.com/exceptionInfoSelect.jspx'
    html=session.get(url=url,headers=headers)
    tree=etree.HTML(html.text)
    totalrecord=tree.xpath('//li[@style="padding-left:10px;color:#666666; font-size:14px;"]/text()')
    for i in totalrecord:
        print i
        count=(int(filter(str.isdigit,str(i))))
        pagecount=int(math.ceil(count/10.0))
    return pagecount
proxies={'http':'http://113.107.57.76:8101'}#113.107.57.76:8101
"""获取每一页每一个公司的特定值"""


"""
@工商公示-登记信息,变更信息,股东信息
"""
def get_basicInfo(page):
    tree=etree.HTML(page)
    """登记信息"""
    regno=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[2]/td[1]/text()'))  #注册号
    entname=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[2]/td[2]/text()'))#名称
    companytype=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[3]/td[1]/text()'))#类型
    responsibler=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[3]/td[2]/text()'))#负责人、经营者

    if"注册" in (if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[4]/th[1]/text()')))[0]:#判断是否有注册资本的字段
        destination=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[5]/td[1]/text()'))#营业场所
        datefrom=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[6]/td[1]/text()'))#营业期限自
        dateto=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[6]/td[2]/text()'))#营业期限至
        businessscope=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[7]/td[1]/text()'))#经营范围
        localorg=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[8]/td[1]/text()'))#登记机关
        approvedate=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[8]/td[2]/text()'))#核准日期
        establishdate=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[4]/td[2]/text()'))#成立日期
        regcep=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[4]/td[1]/text()'))#注册资本
        status=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[9]/td[1]/text()'))#登记状态
        wdhy=["无"]
        industryphy=["无"]
        compositeform=["无"]
        suspensiondate=["无"]
        registerdate=["无"]
    elif "个体工商户" in companytype[0]:
        destination=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[4]/td[1]/text()'))
        compositeform=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[5]/td[1]/text()'))
        registerdate=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[5]/td[2]/text()'))
        businessscope=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[6]/td[1]/text()'))
        localorg=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[7]/td[1]/text()'))
        approvedate=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[7]/td[2]/text()'))
        status=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[8]/td[1]/text()'))
        datefrom=["无"]
        dateto=["无"]
        establishdate=["无"]
        regcep=["无"]
        wdhy=["无"]
        industryphy=["无"]
        suspensiondate=["无"]
    elif companytype[0]=="个人独资企业" :
        destination=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[4]/td[1]/text()'))
        businessscope=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[5]/td[1]/text()'))
        localorg=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[6]/td[1]/text()'))
        approvedate=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[6]/td[2]/text()'))
        establishdate=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[7]/td[1]/text()'))
        status=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[7]/td[2]/text()'))
        wdhy=["无"]
        industryphy=["无"]
        regcep=["无"]
        datefrom=["无"]
        dateto=["无"]
        suspensiondate=["无"]
        registerdate=["无"]
        compositeform=["无"]
    elif companytype[0]=="农民专业合作社分支机构":
        destination=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[4]/td[1]/text()'))
        businessscope=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[5]/td[1]/text()'))
        localorg=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[6]/td[1]/text()'))
        approvedate=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[6]/td[2]/text()'))
        establishdate=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[7]/td[1]/text()'))
        status=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"]/tr[7][1]/td[2]/text()'))
        wdhy=["无"]
        industryphy=["无"]
        regcep=["无"]
        datefrom=["无"]
        dateto=["无"]
        suspensiondate=["无"]
        registerdate=["无"]
        compositeform=["无"]
    elif "外国" in companytype[0]:
        destination=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[5]/td[1]/text()'))#营业场所
        datefrom=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[6]/td[1]/text()'))#营业期限自
        dateto=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[6]/td[2]/text()'))#营业期限至
        businessscope=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/th[9]/text()'))#经营范围
        localorg=["无"]#登记机关
        approvedate=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[7]/td[2]/text()'))#核准日期
        establishdate=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[4]/td[2]/text()'))#成立日期
        status=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[7]/td[1]/text()'))#登记状态
        regcep=["无"]
        wdhy=["无"]
        industryphy=["无"]
        compositeform=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[4]/td[1]/text()'))#首席代表
        registerdate=["无"]
        suspensiondate=["无"]
    elif  companytype[0]=="农民专业合作经济组织" or companytype[0]=="农民专业合作社":
        destination=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[4]/td[1]/text()'))#营业场所
        regcep=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[5]/td[1]/text()'))#注册资本
        establishdate=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[5]/td[2]/text()'))#成立日期
        businessscope=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[6]/td[1]/text()'))#经营范围
        localorg=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[7]/td[1]/text()'))#登记机关
        approvedate=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[7]/td[2]/text()'))#核准日期
        status=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[8]/td[1]/text()'))#登记状态
        datefrom=["无"]
        dateto=["无"]
        wdhy=["无"]
        industryphy=["无"]
        compositeform=["无"]
        suspensiondate=["无"]
        registerdate=["无"]
    elif companytype[0]=="集体所有制" or companytype[0]=="全民所有制" or companytype[0]=="股份合作制" or companytype[0]=="内资企业法人" or companytype[0]=="股份制" or companytype[0]=="联营" or '国有事业单位营业' in companytype[0] or '事业单位营业' in companytype[0]:
        destination=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[4]/td[1]/text()'))#营业场所
        if tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[5]/th[1]/text()')[0]=="营业期限自":
            datefrom=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[5]/td[1]/text()'))
            dateto=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[5]/td[2]/text()'))
            businessscope=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[6]/td[1]/text()'))
            localorg=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[7]/td[1]/text()'))
            approvedate=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[7]/td[2]/text()'))
            establishdate=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[8]/td[1]/text()'))
            status=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[8]/td[2]/text()'))
            regcep=["无"]
        else:
            regcep=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[5]/td[1]/text()'))#注册资本
            establishdate=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[5]/td[2]/text()'))#成立日期
            datefrom=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[6]/td[1]/text()'))#经营范围
            dateto=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[6]/td[2]/text()'))
            businessscope=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[7]/td[1]/text()'))
            localorg=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[8]/td[1]/text()'))#登记机关
            approvedate=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[8]/td[2]/text()'))#核准日期
            status=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[9]/td[1]/text()'))#登记状态
        wdhy=["无"]
        industryphy=["无"]
        compositeform=["无"]
        suspensiondate=["无"]
        registerdate=["无"]
    else:
        destination=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[4]/td[1]/text()'))#营业场所
        datefrom=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[5]/td[1]/text()'))#营业期限自
        dateto=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[5]/td[2]/text()'))#营业期限至
        businessscope=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[6]/td[1]/text()'))#经营范围
        localorg=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[7]/td[1]/text()'))#登记机关
        approvedate=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[7]/td[2]/text()'))#核准日期
        establishdate=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[8]/td[1]/text()'))#成立日期
        status=if_null(tree.xpath('//div[@id="jibenxinxi"]/table[@class="detailsList"][1]/tr[8]/td[2]/text()'))#登记状态
        regcep=["无"]
        wdhy=["无"]
        industryphy=["无"]
        compositeform=["无"]
        registerdate=["无"]
        suspensiondate=["无"]
    return regno,entname,companytype,regcep,responsibler,destination,datefrom,dateto,businessscope,localorg,approvedate,establishdate,status,wdhy,industryphy,compositeform,registerdate,suspensiondate

"""有多项变更事项记录"""
def get_changeInfo(page):
    tree=etree.HTML(page)
    bgxx=tree.xpath('//div[@id="altDiv"]/table[@id="altTab"]/tr')
    bginfo=[]
    if tree.xpath('//div[@id="altDiv"]/table[@id="altTab"]/tr')==[]:
        pass
    else:
        for i in range(1,len(bgxx)+1):
            changeitem=if_null(tree.xpath('//div[@id="altDiv"]/table[@id="altTab"]/tr['+str(i)+']/td[1]/text()'))[0]
            changebefore=if_null(tree.xpath('//div[@id="altDiv"]/table[@id="altTab"]/tr['+str(i)+']/td[2]/text()'))[0]
            changeafter=if_null(tree.xpath('//div[@id="altDiv"]/table[@id="altTab"]/tr['+str(i)+']/td[3]/text()'))[0]
            changedate=if_null(tree.xpath('//div[@id="altDiv"]/table[@id="altTab"]/tr['+str(i)+']/td[4]/text()'))[0]
            bginfo.append([changeitem,changebefore,changeafter,changedate])
    return bginfo

""" 股东信息"""
def get_holderInfo(page):
    tree=etree.HTML(page)
    gdxx=(tree.xpath('//div[@id="invDiv"]/table[@class="detailsList"]/tr'))
    gdinfo=[]
    if (tree.xpath('//div[@id="invDiv"]/table[@class="detailsList"]/tr'))==[]:
        pass
    else:
      for i in range(1,len(gdxx)+1):
            holder=if_null(tree.xpath('//div[@id="invDiv"]/table[@class="detailsList"]/tr['+str(i)+']/td[1]/text()'))[0]
            passporttype=if_null(tree.xpath('//div[@id="invDiv"]/table[@class="detailsList"]/tr['+str(i)+']/td[2]/text()'))[0]
            passportid=if_null(tree.xpath('//div[@id="invDiv"]/table[@class="detailsList"]/tr['+str(i)+']/td[3]/text()'))[0]
            holdertype=if_null(tree.xpath('//div[@id="invDiv"]/table[@class="detailsList"]/tr['+str(i)+']/td[4]/text()'))[0]
            gdinfo.append([holder,passporttype,passportid,holdertype])
    return gdinfo
"""
@工商公示-经营异常信息
"""
def get_jyycInfo(page):
    tree=etree.HTML(page)
    jyyc=tree.xpath('//div[@id="jingyingyichangminglu"]/div[@id="excDiv"]/table[@id="excTab"]/tr')
    jyycinfo=[]
    if tree.xpath('//div[@id="jingyingyichangminglu"]/div[@id="excDiv"]/table[@id="excTab"]/tr')==[]:
        pass
    else:
        for i in range(1,len(jyyc)+1):
            number=if_null(tree.xpath('//div[@id="jingyingyichangminglu"]/div[@id="excDiv"]/table[@id="excTab"]/tr['+str(i)+']/td[1]/text()'))[0]
            inclusionreason=if_null(tree.xpath('//div[@id="jingyingyichangminglu"]/div[@id="excDiv"]/table[@id="excTab"]/tr['+str(i)+']/td[2]/text()'))[0]
            inclusiondate=if_null(tree.xpath('//div[@id="jingyingyichangminglu"]/div[@id="excDiv"]/table[@id="excTab"]/tr['+str(i)+']/td[3]/text()'))[0]
            movereason=if_null(tree.xpath('//div[@id="jingyingyichangminglu"]/div[@id="excDiv"]/table[@id="excTab"]/tr['+str(i)+']/td[4]/text()'))[0]
            movedate=if_null(tree.xpath('//div[@id="jingyingyichangminglu"]/div[@id="excDiv"]/table[@id="excTab"]/tr['+str(i)+']/td[5]/text()'))[0]
            organ=if_null(tree.xpath('//div[@id="jingyingyichangminglu"]/div[@id="excDiv"]/table[@id="excTab"]/tr['+str(i)+']/td[6]/text()'))[0]
            jyycinfo.append([number,inclusionreason,inclusiondate,movereason,movedate,organ])
    return jyycinfo

"""
@工商公示-抽查检查信息
"""
def get_ccjcInfo(page):
    tree=etree.HTML(page)
    ccjc=tree.xpath('//div[@id="chouchaxinxi"]/div[@id="spotCheckDiv"]/table[@class="detailsList"]/tr')
    ccjcinfo=[]
    if tree.xpath('//div[@id="chouchaxinxi"]/div[@id="spotCheckDiv"]/table[@class="detailsList"]/tr')==[]:
        pass
    else:
        for i in range(1,len(ccjc)+1):
            number=if_null(tree.xpath('//div[@id="chouchaxinxi"]/div[@id="spotCheckDiv"]/table[@class="detailsList"]/tr['+str(i)+']/td[1]/text()'))[0]
            inspectorgan=if_null(tree.xpath('//div[@id="chouchaxinxi"]/div[@id="spotCheckDiv"]/table[@class="detailsList"]/tr['+str(i)+']/td[2]/text()'))[0]
            inspecttype=if_null(tree.xpath('//div[@id="chouchaxinxi"]/div[@id="spotCheckDiv"]/table[@class="detailsList"]/tr['+str(i)+']/td[3]/text()'))[0]
            inspectdate=if_null(tree.xpath('//div[@id="chouchaxinxi"]/div[@id="spotCheckDiv"]/table[@class="detailsList"]/tr['+str(i)+']/td[4]/text()'))[0]
            inspectresult=if_null(tree.xpath('//div[@id="chouchaxinxi"]/div[@id="spotCheckDiv"]/table[@class="detailsList"]/tr['+str(i)+']/td[5]/text()'))[0]
            ccjcinfo.append([number,inspectorgan,inspecttype,inspectdate,inspectresult])
    return ccjcinfo

def control_database(regno,entname,companytype,regcep,responsibler,destination,datefrom,dateto,businessscope,localorg,approvedate,establishdate,status,wdhy,industryphy,compositeform,registerdate,suspensiondate,changeinfo,holderinfo,jyycinfo,ccjcinfo):
    """
    数据库操作
    """
    base_selectStr='select * from gsinfo.shanxi1_baseinfo where regNo=%s'
    base_insertStr='insert into gsinfo.shanxi1_baseinfo values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    bg_insertStr='insert into gsinfo.shanxi1_changeinfo values (%s,%s,%s,%s,%s,%s,%s)'
    gd_insertStr='insert into gsinfo.shanxi1_holderinfo values (%s,%s,%s,%s,%s,%s,%s)'
    ccjc_insertStr='insert into gsinfo.shanxi1_ccjcinfo values (%s,%s,%s,%s,%s,%s,%s,%s)'
    jyyc_insertStr='insert into gsinfo.shanxi1_jyycinfo values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    mysql=dbutil.Mysql()
    if mysql.getOne(base_selectStr,regno)==False:
        print "data is inserting ..........",regno
        mysql.insertOne(base_insertStr,(entname[0],establishdate[0],regno[0],wdhy[0],regcep[0],industryphy[0],localorg[0],companytype[0],responsibler[0],destination[0],datefrom[0],dateto[0],businessscope[0],approvedate[0],status[0],compositeform[0],suspensiondate[0],registerdate[0]))
        """ 变更信息"""
        if changeinfo==[]:
            pass
        else:
            for i in changeinfo:
                mysql.insertOne(bg_insertStr,("",entname[0],regno[0],i[0],i[1],i[2],i[3]))
        """股东信息 """
        if holderinfo==[]:
            pass
        else:
            for i in holderinfo:
                mysql.insertOne(gd_insertStr,("",entname[0],regno[0],i[3],i[0],i[1],i[2])) #holder,passporttype,passportid,holdertype
        """ 抽查检查信息"""
        if ccjcinfo==[]:
            pass
        else:
            for i in  ccjcinfo:
                mysql.insertOne(ccjc_insertStr,("",entname[0],regno[0],i[0],i[1],i[2],i[3],i[4]))

        """ 经营异常信息"""
        if jyycinfo==[]:
            pass
        else:
            for i in jyycinfo:
                mysql.insertOne(jyyc_insertStr,("",entname[0],regno[0],i[0],i[1],i[2],i[3],i[4],i[5]))
    else:
        print "it is existed..............",regno
        pass

class get_info(threading.Thread):
  def __init__(self,href):
      threading.Thread.__init__(self)
      self.href=href
      self.user_agent=random.choice(['Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0'])
      self.headers={'User-Agent':user_agent}
  def get_infopage(self):
    t=random.choice([1,2,0,0.1,0,1.7,0.8,0.2])
    time.sleep(t)
    html=session.get(url=self.href,headers=headers,proxies=proxies)
    page=html.text
    regno,entname,companytype,regcep,responsibler,destination,datefrom,dateto,businessscope,localorg,approvedate,establishdate,status,wdhy,industryphy,compositeform,registerdate,suspensiondate=get_basicInfo(page)
    changeinfo=get_changeInfo(page)
    holderinfo=get_holderInfo(page)
    ccjcinfo=get_ccjcInfo(page)
    jyycinfo=get_jyycInfo(page)
    control_database(regno,entname,companytype,regcep,responsibler,destination,datefrom,dateto,businessscope,localorg,approvedate,establishdate,status,wdhy,industryphy,compositeform,registerdate,suspensiondate,changeinfo,holderinfo,jyycinfo,ccjcinfo)
  def run(self):
    self.get_infopage()

global hrefs
hrefs=[]
class get_list(threading.Thread):
    def __init__(self,pageno):
        threading.Thread.__init__(self)
        self.user_agent=random.choice(['Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0'])
        self.headers={'User-Agent':user_agent}
        self.pageno=pageno
    def get_detailpage(self):
            print "获取hrefs中........................",str(self.pageno)+"页",proxies
            params={"pageNo":str(self.pageno),"gjz":""}
            url='http://gsxt.fc12319.com/exceptionInfoSelect.jspx'
            html=session.get(url=url,headers=headers,params=params,proxies=proxies)
            t=random.choice([1,2,0,5,0,7,1.2,0.8,0.2])
            time.sleep(t)
            tree=etree.HTML(html.text)
            click=tree.xpath('//li[@class="tb-a1"]/a[@href]/@href')
            for i in click:
                href="http://gsxt.fc12319.com"+str(i)
                hrefs.append(href)
            return hrefs
    def run(self):
        self.get_detailpage()

class myThreading(threading.Thread):
    def __init__(self,urls):
        threading.Thread.__init__(self)
        self.threadList=[]
        self.urls=urls
    def runThread(self):
        for url in self.urls:
            self.threadList.append(get_info(url))
        for i in range(len(self.threadList)):
                self.threadList[i].start()
        for i in range(len(self.threadList)):
                self.threadList[i].join()
    def run(self):
        self.runThread()

class listThreading(threading.Thread):
    def __init__(self,startpage,endpage):
        threading.Thread.__init__(self)
        self.threadList=[]
        self.sp=startpage
        self.ep=endpage
    def runThread(self):
        for pageno in range(self.sp,self.ep+1):
            self.threadList.append(get_list(pageno))
        for i in range(len(self.threadList)):
                self.threadList[i].start()
        for i in range(len(self.threadList)):
                self.threadList[i].join()
    def run(self):
        self.runThread()
mysql=dbutil.Mysql()
#pages=getpages()
#pages=24565
#for i in range(5390,24565):
for i in range(5730,24565,10):
    listThread=listThreading(startpage=i,endpage=i+10)
    listThread.run()
    print len(hrefs),"len........"
    mythread=myThreading(hrefs)
    mythread.run()

mysql.dispose()


