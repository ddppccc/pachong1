# encoding=utf-8
from selenium import webdriver
import time
from flask import Flask,request
import threading
import json
from gevent import pywsgi
from flask import Flask, request, send_from_directory
import base64
import upload_image
import pymongo
from urllib import parse
from multiprocessing import Process,Pool
import selenium
from sendsms import sendsms
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
            retryWrites="false")['大众点评']['cookie数据']
caps = {
    'browserName': 'chrome',
    'loggingPrefs': {
        'browser': 'ALL',
        'driver': 'ALL',
        'performance': 'ALL',
    },
    'goog:chromeOptions': {
        'perfLoggingPrefs': {
            'enableNetwork': True,
        },
        'w3c': False,
    },
}
def getcode():
    option = webdriver.ChromeOptions()
    option.add_argument("--disable-blink-features")
    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(desired_capabilities=caps)
    # driver = webdriver.Chrome(options=option)
    while 1:
        time.sleep(1)
        if not info_base.find_one({'getcode':1}):continue
        driver.get("https://account.dianping.com/account/iframeLogin?callback=EasyLogin_frame_callback0&wide=false&protocol=https:&redir=http%3A%2F%2Fwww.dianping.com%2F")
        print('窗口打开成功')
        time.sleep(1)
        try:
            img = driver.find_element_by_xpath('/html/body/div/div[2]/div[3]/img')
        except:
            print('失败')
        time.sleep(1)
        img.screenshot('static/1.png')
        print('成功')
        upload_image.upload()
        cookiedata = info_base.find_one()
        info_base.update_one(cookiedata, {"$set": {'upload': 1}})
        i=0
        while 1:
            time.sleep(1)
            i += 1

            if driver.find_element_by_xpath('//div[@class="success-side"]').get_attribute('style') == 'display: block;':
                print('扫描成功')
            else:
                if i<120:
                    continue
            time.sleep(15)
            driver.get("http://www.dianping.com/chongqing/ch80")
            datalist=[]
            try:
                for log in driver.get_log('performance'):
                    if all(i in str(json.loads(log['message'])['message']['params']) for i in
                           ('requestHeaders', 'User-Agent')):
                        print(json.loads(log['message'])['message']['params']['response']['requestHeaders'])
                        print('')
                        datalist.append(json.loads(log['message'])['message']['params']['response']['requestHeaders'])
            except:
                sendsms('【广信奥海】 登录出错，请更换账号')
                print('登录出错')
                cookiedata = info_base.find_one()
                info_base.update_one(cookiedata, {"$set": {'getcode': 0, 'upload': 0}})
                time.sleep(10)
                driver.close()
                return getcode()
            time.sleep(1)
            driver.execute_script("document.write(document.cookie)")
            time.sleep(1)
            cookie = driver.find_elements_by_xpath('/html/body')[0].text
            time.sleep(1)
            driver.close()
            print(cookie)
            cookiedata = info_base.find_one()
            info_base.update_one(cookiedata, {"$set": {'Cookie': datalist[-1]['Cookie'],'status':1,'opend':0,'getcode':0,'upload':0}})
            print('cookie更新成功')
            break
        break
if __name__ == '__main__':
    print('running...')
    while 1:
        time.sleep(3)
        if info_base.find_one({'status':0}):
            sendsms('【广信奥海】 大众点评cookie失效，请关注公众号禾略回复"获取二维码扫码"更新cookie')
            print('cookie失效')
            getcode()
