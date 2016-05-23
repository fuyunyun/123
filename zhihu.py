

#coding=utf-8

import  requests
from lxml import etree
import sys


session=requests.session()
user_agent='Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'
headers={'User-Agent':user_agent}
cookies={"q_c1":"246888bd2fea485bbdebabd05607db21|1462268201000|1462268201000", "cap_id":"ZTllOWMxNmU2ZjFkNDcxNDhlYzBhNjQ3OGY4MTZjNzc=|1462949620|5fbc109ac2a65bfaf24e9b89a06108629e6011e9", "l_cap_id":"MjNlOTFkMGZhYWMxNGI2YjgxMTEyMTUzYjUwYzJhZDI=|1462949620|04cf2878133c72ff25919a9e76e7cd890739f5ae", "d_c0":"ACBA0y2S3QmPTqhJZF8-N6gKF5uHYIO8XiA=|1462268201"," __utma":"51854390.1317056880.1463734913.1463964952.1463974221.5"," __utmz":"51854390.1463734913.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic"," _za":"e822b14a-3315-4be1-8131-c2a9053694e4"," _zap":"b88578af-0a1a-4f72-ac90-0052ff16c903"," login":"NzcyZDVjNTYxMDljNGM0MGE1MGZlNDFlNDhiMTQ2ZGU=|1462949638|c8b379981ad7399b03bdb154806f3e006595ced5"," _xsrf":"93023797fadbaf9eaac0bc4ad5a1c86e"," z_c0":"Mi4wQUtCQW5BSU8xQWNBSUVEVExaTGRDUmNBQUFCaEFsVk5CbVJhVndBUFNBSnZCU29jN0ppZUgyNHZNUUNjcTEtZDdB|1462949638|b440e8bf35a2cd7cbe3bb48285cf540ae4e50000"," __utmv":"51854390.100--|2=registration_date=20150325=1^3=entry_date=20150325=1"," __utmc":"51854390", "__utmb":"51854390.7.9.1463982013240"," __utmt":"1"}
url="https://www.zhihu.com/people/XXX"
html=session.get(url=url,headers=headers,cookies=cookies)
page=html.content
tree=etree.HTML(page)
items=tree.xpath('//div[@class="zm-profile-section-main zm-profile-section-activity-main zm-profile-activity-page-item-main"]/a[@class="question_link"]/text()')
urls=tree.xpath('//div[@class="zm-profile-section-main zm-profile-section-activity-main zm-profile-activity-page-item-main"]/a[@class="question_link"]/@href')
for i in range(len(items)):
    print items[i]
    url="http://www.zhihu.com"+str(urls[i])
    html=session.get(url=url,cookies=cookies,headers=headers)
    page=html.content
    ans=etree.HTML(page)
    content=ans.xpath('//meta[@property="og:description"]/@content')
    for i in content:
        print i

