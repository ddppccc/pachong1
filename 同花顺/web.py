from selenium import webdriver
from config import gainiandict,bankuaidict
import re
import pymongo
from urllib import parse
import time
MONGODB_CONFIG = {
   "host": "8.135.119.198",
   "port": "27017",
   "user": "hladmin",
   "password": parse.quote("Hlxkd3,dk3*3@"),
   "db": "dianping",
   "collections": "dianping_collections",
}

info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['同花顺']['概念行业板块_数据_202108']

def getcookie(url):
    option = webdriver.ChromeOptions()
    # 无界面模式：
    # option.headless = True
    # option.add_argument('--headless')
    option.add_argument("--disable-blink-features")
    option.add_argument("--disable-blink-features=AutomationControlled")
    # option.add_argument("--proxy-server=%s"%IP)
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument("--disable-blink-features=AutomationControlled")
    # login = webdriver.Chrome(options=option)
    # # login.implicitly_wait(10)
    # login.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     "source": """
    #     Object.defineProperty(navigator, 'webdriver', {
    #       get: () => undefined
    #     })
    #   """
    # })
    driver=webdriver.Chrome(options=option)
    driver.get(url)
    # data='Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1628473097; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1628473097;'
    # time.sleep(2)
    # cookie=driver.get_cookies()
    # print(cookie[-1]['value'])
    # data=data+cookie[-1]['value']
    time.sleep(1)
    try:
        driver.execute_script("document.write(document.cookie)")
        time.sleep(1)
        data = driver.find_elements_by_xpath('/html/body')[0].text
        time.sleep(1)
    except:
        driver.close()
        return getcookie(url)
    with open('cookie.txt','w') as f:
        f.write(data)
    print(data)
    driver.close()
    # time.sleep(1000)
if __name__ == '__main__':
    getcookie('https://q.10jqka.com.cn/gn/detail/field/264648/order/desc/page/3/ajax/1/code/300018')
