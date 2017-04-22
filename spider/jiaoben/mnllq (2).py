#coding=utf-8
from selenium import webdriver

driver = webdriver.PhantomJS(executable_path=u'/root/anaconda2/lib/python2.7/site-packages/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
driver.get("http://duckduckgo.com/")
driver.find_element_by_id('search_form_input_homepage').send_keys("Nirvana")
driver.find_element_by_id("search_button_homepage").click()
print driver.current_url
driver.quit()

#===============================================================
#coding=utf-8
'''from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
import time
import sys

driver = webdriver.PhantomJS(executable_path='C:\Users\Gentlyguitar\Desktop\phantomjs-1.9.7-windows\phantomjs.exe')
driver.get("http://www.zhihu.com/#signin")
#driver.find_element_by_name('email').send_keys('your email')
driver.find_element_by_xpath('//input[@name="password"]').send_keys('your password')
#driver.find_element_by_xpath('//input[@name="password"]').send_keys(Keys.RETURN)
time.sleep(2)
driver.get_screenshot_as_file('show.png')
#driver.find_element_by_xpath('//button[@class="sign-button"]').click()
driver.find_element_by_xpath('//form[@class="zu-side-login-box"]').submit()

try:
    dr=WebDriverWait(driver,5)
    dr.until(lambda the_driver:the_driver.find_element_by_xpath('//a[@class="zu-top-nav-userinfo "]').is_displayed())
except:
    print '登录失败'
    sys.exit(0)
driver.get_screenshot_as_file('show.png')
#user=driver.find_element_by_class_name('zu-top-nav-userinfo ')
#webdriver.ActionChains(driver).move_to_element(user).perform() #移动鼠标到我的用户名
loadmore=driver.find_element_by_xpath('//a[@id="zh-load-more"]')
actions = ActionChains(driver)
actions.move_to_element(loadmore)
actions.click(loadmore)
actions.perform()
time.sleep(2)
driver.get_screenshot_as_file('show.png')
print driver.current_url
print driver.page_source
driver.quit()'''