import requests
import time
import re
import pymongo
from urllib import parse
from lxml import etree
import json
from multiprocessing import Process,Pool
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
            retryWrites="false")['融创中国']['info']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['融创中国']['has_spider']
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
}
year=2021
month=4
def get_proxy():
    try:
            return requests.get('http://47.106.223.4:50002/get/').json().get('proxy')
            # return '111.202.83.35:80'
    except:
        num = 3
        while num:
            try:
                return requests.get('http://47.106.223.4:50002/get/').json().get('proxy')
            except:
                print('暂无ip，等待20秒')
                time.sleep(20)

                num -= 1
        print('暂无ip')
def get_html(url):
    try:
        proxies = {"https": get_proxy()}
        response = requests.get(url, headers=headers,timeout=(10, 10))
        # encod = response.apparent_encoding
        # if encod.upper() in ['GB2312', 'WINDOWS-1254']:
        #     encod = 'gbk'
        # response.encoding = encod
        return response
    except Exception as e:
        print('geturl错误',url, e)
        return get_html(url)


def getUrl():
    url = 'https://www.sunac.com.cn/Ajax/More.ashx'
    data = {
        'method': 'GetEstateMore',
        'pageIndex': 1,
        'pageSize': 500,
        'typeId': '14',
        'pid': '0'
    }
    res = requests.post(url, data=data, headers=headers)
    res.encoding = 'utf8'
    # print(res.json()['List'])
    # name = re.findall('<h4>(.*?)<', res.json()['List'])
    # pid = re.findall('type=14&tag=512&pid=(\d+)', res.json()['List'])
    # print(name)
    # print(len(name))
    # print(pid)
    # print(len(pid))
    html=etree.HTML(res.json()['List'])
    url=html.xpath('//@href')
    print(url)
    print(len(url))
getlist()
  
