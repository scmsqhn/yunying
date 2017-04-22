#coding=utf-8
#from selenium import webdriver
#http://www.cnblogs.com/fnng/p/6431484.html
import sys
import pickle
sys.path
sys.path.append(u'/root/anaconda2/envs/py34/lib/python3.4/site-packages')
from selenium import webdriver
import time


def get_driver():
    executable_path = 'phantomjs'
    service_log_path = './ghostdriver.log'
    driver = webdriver.PhantomJS()
#    driver = webdriver.PhantomJS(executable_path=executable_path, service_log_path=service_log_path)
    try:
        cookies= driver.get_cookies()
        cookies = pickle.load(open('/cookie.txt', 'rb'))
        for cookie in cookies:
            print(cookie)
            print('\n')
            if(cookie["domain"]=='.taobao.com'):
                driver.add_cookie(cookie)
        return driver
    except Exception,e:
        return driver

def login_taobao():
#    driver = webdriver.Chrome("D:\\python\\chromedriver_win32\\chromedriver.exe")
 #   try:
    executable_path = 'phantomjs'
    service_log_path = './ghostdriver.log'
    driver = webdriver.PhantomJS(executable_path=executable_path, service_log_path=service_log_path)
#    driver.delete_all_cookies()
    driver.get("https://login.taobao.com/member/login.jhtml")
    time.sleep(5)
#    print(driver.page_source)
    driver.find_element_by_xpath("//*[@id='J_Quick2Static']").click()
    print('click to name pw 1')
    username=driver.find_element_by_name("TPL_username")
    time.sleep(5)
    if not username.is_displayed:
        print('click to name pw 2')
        time.sleep(10)
        driver.find_element_by_xpath("//*[@id='J_Quick2Static']").click()
    time.sleep(5)
    username.clear()
    username.send_keys("qhn614")
    print('send qhn614')
    driver.find_element_by_name("TPL_password").clear()
    driver.find_element_by_name("TPL_password").send_keys("taobao161230@@")
    print('send pw')
    driver.find_element_by_xpath("//*[@id='J_SubmitStatic']").click()
    print('submit to')
    time.sleep(5)
    print(driver.page_source)
    #以下是获得cookie代码
#    cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
#    cookiestr = ';'.join(item for item in cookie)
#    f = open("./cookie.txt",'w')
#    f.write(cookiestr)
#    f.close()
    pickle.dump(driver.get_cookies(), open('/cookie.txt', 'wb'))
    return driver
    
def upload_baobei(driver):
    print('uploaded')
    driver.get("https://upload.taobao.com/auction/publish/publish.htm")
    print(type(driver.page_source))
    print(driver.page_source.encode("utf-8"), open('./pages.html','w'))
    print('uploaded wait 10')
    time.sleep(10)
    login_taobao_half(driver)
    driver.find_element_by_xpath(ur'//*[@id="TitleID"]').clear()
    driver.find_element_by_xpath('//*[@id="TitleID"]').send_keys('脚本服务订制')
    driver.find_element_by_xpath('//*[@id="buynow"]').clear().send_keys('20')
    driver.find_element_by_xpath('//*[@id="quantityId"]').clear().send_keys('1000')
    driver.find_element_by_xpath('//*[@id="J_Internal"]').click()
    driver.find_element_by_xpath('//*[@id="keyword"]').clear().send_keys('caihong.jpg')
    driver.find_element_by_xpath('//*[@id="search-btn"]').click()
    driver.find_element_by_xpath('/html/body/div/div/div[2]/div[1]/div[2]/div[2]/ul/li[1]/a').click()
    driver.find_element_by_xpath('//*[@id="newEditorContainer"]/div[1]/div[2]/iframe').clear().send_keys('脚本订制服务。需求明确，定期交付')
    driver.find_element_by_xpath('//*[@id="btn-generate-detail"]').click()
    driver.find_element_by_xpath('//*[@id="J_deliverTemplate"]/option[2]').click()
    driver.find_element_by_xpath('//*[@id="event_submit_do_publish"]').click()
    
def close_driver(driver):
    driver.close()
    driver.quit()

def login_taobao_half(driver):
    driver.find_element_by_xpath("//*[@id='J_Quick2Static']").click()
    print('click to name pw 1')
    username=driver.find_element_by_name("TPL_username")
    time.sleep(5)
    if not username.is_displayed:
        print('click to name pw 2')
        time.sleep(10)
        driver.find_element_by_xpath("//*[@id='J_Quick2Static']").click()
    time.sleep(5)
    username.clear()
    username.send_keys("qhn614")
    print('send qhn614')
    driver.find_element_by_name("TPL_password").clear()
    driver.find_element_by_name("TPL_password").send_keys("taobao161230@@")
    print('send pw')
    driver.find_element_by_xpath("//*[@id='J_SubmitStatic']").click()
    print('submit to')
    time.sleep(5)
    print(driver.page_source, open('/source.html' ,'w'))

if __name__=='__main__':
#    close_driver(driver)
#    driver = login_taobao()
    upload_baobei(get_driver())
#    upload_baobei(driver)





