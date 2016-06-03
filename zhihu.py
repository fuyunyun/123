#coding=utf-8

import  requests
from lxml import etree
import sys
import time
from selenium import webdriver

account=""
password=""

browser=webdriver.Firefox()
url='https://www.zhihu.com/people/XXXXXX'
browser.get(url)
time.sleep(2)

browser.find_element_by_class_name("switch-to-login").click()
time.sleep(3)
"""
@输入用户名和密码
"""
browser.find_element_by_xpath('//input[@aria-label="手机号或邮箱" and @name="account"]').send_keys(account)
browser.find_element_by_xpath('//input[@placeholder="密码" and  @aria-label="密码"]').send_keys(password)
"""
@看页面要不要输入验证码，要求输入就去掉注释
"""
#captcha=raw_input()
#browser.find_element_by_xpath('//form[@method="POST"]/div[@class="input-wrapper captcha-module"]//input[@id="captcha" and @name="captcha"]').send_keys(captcha)
browser.find_element_by_xpath('//input[@value="登录" and @class="submit zg-btn-blue"]').submit()
time.sleep(3)
expands=browser.find_elements_by_xpath('//div[@class="zm-item-rich-text expandable js-collapse-body"]')
titles=browser.find_elements_by_xpath('//div[@class="zm-profile-section-main zm-profile-section-activity-main zm-profile-activity-page-item-main"]/a[@class="question_link" and @target="_blank"]')
for i in range(len(expands)):
    u=expands[i].get_attribute("data-entry-url")
    url="http://www.zhihu.com"+u
    print "赞同回答的title:",titles[i].text
    contentbr=webdriver.Firefox()
    contentbr.get(url)
    time.sleep(2)
    """
    @打开问题页
    """
    content=contentbr.find_element_by_xpath('//div[@class="zm-editable-content clearfix"]')
    print "赞同回答的内容: ",content.text,"\n"
    contentbr.quit()
browser.quit()

