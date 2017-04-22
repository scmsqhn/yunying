#encoding=utf-8
import time

from selenium import webdriver  
LOGIN=True

#flags
LOGIN=True
FABU=True


if(LOGIN):
  username = u'qhn614'
  password = u'taobao161230@@'

  driver = webdriver.PhantomJS()
  #driver = webdriver.Firefox()  
  t0=time.time()
                   
    
  driver.get("https://login.taobao.com/member/login.jhtml")
  print 'driver get'
  t1=time.time()
  print 't1=time.time()'
  time.sleep(5)
    
  driver.find_element_by_id("J_LoginBox").click()  
  time.sleep(5)
  print 'time.sleep()'

  driver.find_element_by_id("TPL_username_1").clear()  
  driver.find_element_by_id("TPL_password_1").clear()  
  driver.find_element_by_id("TPL_username_1").send_keys(username)  
  driver.find_element_by_id("TPL_password_1").send_keys(password)  
  driver.find_element_by_id("J_SubmitStatic").click()  

  #driver.get_cookies()取得cookie  
  cookie = "; ".join([item["name"] + "=" + item["value"] +"\n" for item in driver.get_cookies()])  
  print cookie  
  #然后带上cookie登录后的页面去请求页面  

if(FABU):
    pass


