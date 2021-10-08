import requests
import time
import pymongo
import re
import json
from lxml import etree
from urllib import parse
from multiprocessing import Process, Pool
import warnings
from selenium import webdriver
from selenium.webdriver.support.ui import Select
warnings.filterwarnings("ignore")
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
    retryWrites="false")['房企top100']['阳光城_数据_202109']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['房企top100']['阳光城_去重_202109']
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
    url = 'https://fangbao.yango.com.cn/LouPanDetail.html?lpId='+data['lpId']
    has_spider_urllist = []
    for has_spider_url in has_spider.find():
        has_spider_urllist.append(has_spider_url['标题url'])
    if url in has_spider_urllist:
        print('该页数据已爬取，下一页')
        return
    dataurl='https://fb.yango.com.cn/fbapi/project/lp/detail?lpId='+data['lpId']
    res = get_html(dataurl)
    res.encoding = 'utf8'
    if res.status_code == 502:
        print(url, '页面打开失败')
        return
    detaildata=res.json()['data']
    item = {}
    item['城市'] =city
    item['区县'] = detaildata['countyName']
    item['标题'] =data['lpName']
    item['标题url'] = url
    item['销售情况'] = '在售' if detaildata['salesStatus'] == 1 else '待售'
    try:
        item['分类'] =''
    except:
        item['分类'] = ''
    try:
        item['装修'] =detaildata['zhuangxiu']
    except:
        item['装修'] = ''
    type=''
    huxing=detaildata['huxingtuTypeObj']
    try:
        for i in huxing:
            type=type+' '+i['name']
    except:pass
    item['户型'] =type
    try:
        item['单价'] =''
    except:
        item['单价'] = ''
    item['总价'] = ''
    item['建面'] = data['areaRange']
    try:
        item['最小建面'] = re.findall('(\d+).*?\d+',data['areaRange'])[0]
        item['最大建面'] = re.findall('\d+.*?(\d+)',data['areaRange'])[0]
    except:
        item['最小建面'] = ''
        item['最大建面'] = ''
    try:
        item['容积率'] =detaildata['rongjilv']
    except:
        item['容积率'] = ''
    try:
        item['绿化率'] =detaildata['lvhualv']
    except:
        item['绿化率'] = ''
    item['楼栋户数'] =''
    try:
        item['总户数'] =''
    except:
        item['总户数'] = ''
    try:
        item['建筑面积'] =detaildata['jianzhumj']
    except:
        item['建筑面积'] = ''
    item['地址'] =data['lpAddress']
    # tags =
    # tag = ''
    # for i in tags:
    #     tag = tag + ' ' + i.strip()
    item['标签'] = data['salePointsName']
    try:
        item['开盘时间'] =detaildata['kpDate']
    except:
        item['开盘时间'] = ''
    try:
        item['物业费'] =''
    except:
        item['物业费'] =''
    item['latitude'] =data['latitude']
    item['longitude'] = data['longitude']
    item['抓取年份'] = year
    item['抓取月份'] = month
    item['数据来源'] = '阳光城'
    item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    item['抓取年份'] = year
    item['抓取月份'] = month
    item['抓取日期'] = day
    info_base.insert_one(item)
    has_spider.insert_one({'标题url': url})
    print(item)
def getcitylist():
    url='https://fb.yango.com.cn/fbapi/project/lp/city/all'
    res=get_html(url)
    res.encoding='utf8'
    citycode={}
    for i in res.json()['data']:
        for city in i['cities']:
            citycode[city['name']]=city['code']
    print(citycode)
    return  citycode
def getlist(code):
    url='https://fb.yango.com.cn/fbapi/project/lp/hot?cityCode='+str(code)
    res=get_html(url)
    res.encoding='utf8'
    return res.json()['data']
if __name__ == '__main__':
    year = 2021
    month = 9
    day = 27
    citycode=getcitylist()
    for k,v in citycode.items():
        datalist=getlist(v)
        for data in datalist:
            getDetailInfo(k,data)