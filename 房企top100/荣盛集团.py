import requests
import time
import pymongo
import re
import json
from lxml import etree
from urllib import parse
from multiprocessing import Process, Pool

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
    retryWrites="false")['房企top100']['荣盛集团_数据_202109']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['房企top100']['荣盛集团_去重_202109']
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
}

def get_proxy():
    try:
            return requests.get('http://demo.spiderpy.cn/get/').json().get('proxy')
            # return '111.202.83.35:80'
    except:
        num = 3
        while num:
            try:
                return requests.get('http://demo.spiderpy.cn/get/').json().get('proxy')
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
        print('geturl错误', url, e)
        time.sleep(2)
        return get_html(url)


def getDetailInfo(city,data):
    url = 'https://www.risesun.cn/service_urban_housing/'+ data['id'] +'.html'
    has_spider_urllist = []
    for has_spider_url in has_spider.find():
        has_spider_urllist.append(has_spider_url['标题url'])
    if url in has_spider_urllist:
        print('该页数据已爬取，下一页')
        return
    item = {}
    item['城市'] = city['title']
    try:
        item['区县'] = data['area'].split('市')[1]
    except:
        item['区县'] = data['area']
    item['标题'] = data['title']
    item['标题url'] = url
    item['销售情况'] = ''
    try:
        item['分类'] = data['building_cate']
    except:
        item['分类'] = ''
    try:
        item['装修'] = ''
    except:
        item['装修'] = ''

    item['户型'] = ''
    try:
        item['单价'] =''
    except:
        item['单价'] = ''
    item['总价'] = ''
    item['建面'] = ''
    try:
        item['最小建面'] = ''
        item['最大建面'] = ''
    except:
        item['最小建面'] = ''
        item['最大建面'] = ''
    try:
        item['容积率'] = ''
    except:
        item['容积率'] = ''
    try:
        item['绿化率'] = ''
    except:
        item['绿化率'] = ''
    item['楼栋户数'] = ''
    try:
        item['总户数'] = ''
    except:
        item['总户数'] = ''
    try:
        item['建筑面积'] = ''
    except:
        item['建筑面积'] = ''
    item['地址'] = data['address']
    # # tags =
    # # tag = ''
    # # for i in tags:
    # #     tag = tag + ' ' + i.strip()
    item['标签'] = data['tag']
    try:
        item['开盘时间'] = ''
    except:
        item['开盘时间'] = ''
    try:
        item['物业费'] = ''
    except:
        item['物业费'] = ''
    item['latitude'] = data['lat']
    item['longitude'] = data['long']
    item['抓取年份'] = year
    item['抓取月份'] = month
    item['数据来源'] = '荣盛集团'
    item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    item['抓取年份'] = year
    item['抓取月份'] = month
    item['抓取日期'] = day
    info_base.insert_one(item)
    has_spider.insert_one({'标题url': url})
    print(item)


def getlist(city,page=1,list=[]):
    url='https://www.risesun.cn/Home/Form/getHousing?position_id='+city['id']+'&business_id=0&sale_status_id=0&title=&p=' + str(page)
    res = get_html(url)
    res.encoding = 'utf8'
    # print(res.json())
    for i in res.json()['list']:
        list.append(i)
    if res.json()['nowpage'] < res.json()['maxpage']:
        return getlist(city,res.json()['nowpage']+1,list)
    return list

def getcity():
    url='https://www.risesun.cn/Form/getForm/id/72'
    res=get_html(url)
    res.encoding='utf8'
    # print(res.json()['list'][:-1])
    return res.json()['list'][:-1]



if __name__ == '__main__':
    year = 2021
    month = 9
    day = 27
    citylist=getcity()
for city in citylist:
    list=getlist(city,page=1,list=[])
    for data in list:
        getDetailInfo(city,data)

