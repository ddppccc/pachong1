# encoding=utf-8
import requests
import time
import datetime
from dateutil.relativedelta import relativedelta
import pymongo
from urllib import parse
import warnings
from gethash import gethash,getdriver
warnings.filterwarnings("ignore")
MONGODB_CONFIG = {
    "host": "192.168.1.28",
    "port": "27017",
    "user": "admin",
    "password": '123123',
}
page_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['土地市场网招拍挂']['供地结果_列表_202204']
info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['土地市场网招拍挂']['供地结果_详情_202204']
headers={

    'Host': 'api.landchina.com',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'Origin': 'https://www.landchina.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.landchina.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': "'zh-CN,zh;q=0.9'",
}
def get_proxy():
    return 'http://H041YJYT015P8T3D:0B6839D706F30F56@http-dyn.abuyun.com:9020'
    try:
        return requests.get('http://1.116.204.248:5454/proxy2').text
        # return requests.get('http://1.116.204.248:5000/proxy').text
    except:
        num = 3
        while num:
            try:
                return requests.get('http://1.116.204.248:5000/proxy').text
            except:
                print('暂无ip，等待20秒')
                time.sleep(20)
                num -= 1
        print('暂无ip')

def getdata(data):
    # if info_base.find_one({'gdGuid':data['gdGuid']}):
    #     print(data['gdGuid'],'已存在..')
    #     return
    proxy = get_proxy()
    proxies = {
        "https": proxy,
        "http": proxy,
    }
    for i in range(10):
        url='https://api.landchina.com/tGdxm/result/detail'
        postdata={'gdGuid': data['gdGuid']}
        time.sleep(1)
        keys = headers['User-Agent'] + str(datetime.datetime.now().day) + 'list'
        headers['Hash'] = gethash(keys)
        try:
            res=requests.post(url,headers=headers,proxies=proxies,json=postdata,verify=False)
        except:
            continue
        res.encoding='utf8'
        if res.status_code != 200:
            continue
        if res.json()['code'] == 500:
            # time.sleep(5)
            continue

        item={}
        item['gdGuid'] = data['gdGuid']
        print(res.json())
        item['项目名称'] = res.json()['data']['xmMc']
        item['行政区'] = res.json()['data']['xzqFullName']
        item['项目位置'] = res.json()['data']['tdZl']
        try:
            item['面积'] = res.json()['relate'][0]['mj']
        except:
            item['面积'] =None
        item['土地来源'] = res.json()['data']['tdLy']
        try:
            item['土地用途'] = res.json()['data']['tdYt']
        except:
            item['土地用途'] = ''
        item['供地方式'] = res.json()['data']['gyFs']
        try:
            item['土地使用年限'] = res.json()['data']['crNx']
        except:
            item['土地使用年限'] =None
        item['行业分类'] = res.json()['data']['hyFl']
        item['土地级别'] = res.json()['data']['tdJb']
        try:
            item['成交价格'] = res.json()['data']['je']
        except:
            item['成交价格'] = ''
        try:
            item['土地使用权人'] = res.json()['data']['srr']
        except:
            item['土地使用权人'] =None
        try:
            item['容积率下限'] = res.json()['data']['minRjl']
        except:
            item['容积率下限'] = ''
        try:
            item['容积率上限'] = res.json()['data']['maxRjl']
        except:
            item['容积率上限'] = ''
        try:
            item['约定交地时间'] = time.strftime("%Y-%m-%d %H:%M:%S",  time.localtime(int(int(res.json()['data']['jdSj'])/1000)))
        except:
            try:
                item['约定交地时间'] = res.json()['data']['jdSj']
            except:
                item['约定交地时间'] = '--'
        try:
            item['合同签订日期'] = time.strftime("%Y-%m-%d %H:%M:%S",  time.localtime(int(int(res.json()['data']['qdRq'])/1000)))
        except:
            try:
                item['合同签订日期'] = res.json()['data']['qdRq']
            except:
                item['合同签订日期'] = '--'
        try:
            item['约定开工时间'] = time.strftime("%Y-%m-%d %H:%M:%S",  time.localtime(int(int(res.json()['data']['dgSj'])/1000)))
        except:
            try:
                item['约定开工时间'] = res.json()['data']['dgSj']
            except:
                item['约定开工时间'] = '--'
        try:
            item['约定竣工时间'] = time.strftime("%Y-%m-%d %H:%M:%S",  time.localtime(int(int(res.json()['data']['jgSj'])/1000)))
        except:
            try:
                item['约定竣工时间'] = res.json()['data']['jgSj']
            except:
                item['约定竣工时间'] = '--'
        item['实际开工时间']= '--'
        item['实际竣工时间']= '--'
        try:
            item['批准单位'] = res.json()['data']['pzJg']
        except:
            item['批准单位']='--'
        if item['项目位置'] != data['tdZl']:
            continue
        try:
            # print('-----------------')
            # print('-----------------')
            # print(data)
            print(item)
        except:
            pass
        try:
            info_base.insert_one(item)
        except:
            pass
        break

if __name__ == '__main__':
    with open('详情页去重.txt', encoding='utf8') as f:
        bj = f.readlines()
    # driver=getdriver()
    for d in page_base.find():
        # ###################################
        if d['gdGuid']+'\n' in bj:
            continue
        # print(d)
        getdata(d)
        bj.append(d['gdGuid']+'\n')
        with open('详情页去重.txt', 'a', encoding='utf8') as f:
            f.write(d['gdGuid']+'\n')

