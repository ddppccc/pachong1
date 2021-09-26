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
    retryWrites="false")['房企top100']['蓝光发展_数据_202108']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['房企top100']['蓝光发展_去重_202108']
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
    url = 'https://www.brc.com.cn/'+ data['标题url']
    has_spider_urllist = []
    for has_spider_url in has_spider.find():
        has_spider_urllist.append(has_spider_url['标题url'])
    if url in has_spider_urllist:
        print('该页数据已爬取，下一页')
        return
    res=get_html(url)
    res.encoding='urf8'
    html=etree.HTML(res.text)
    item = {}
    title=html.xpath('.//div[@class="pinner clearfix"]/dl[1]/dd[@class="overLeft"]/span/text()')
    info=html.xpath('.//div[@class="pinner clearfix"]/dl[1]/dd[@class="overLeft"]/text()')[1:-1]
    # print(title)
    # print(info)
    dict={}
    try:
        title.remove('交房时间：')
    except:pass
    for k in range(len(title)):
        for v in range(len(info)):
            if k != v:continue
            key=title[k].strip()[:-1]
            value=info[v].strip()
            # print(key,value)
            dict[key]=value
    # print(dict)
    item['城市'] = city
    try:
        item['区县'] = ''
    except:
        item['区县'] = ''
    item['标题'] = data['标题']
    item['标题url'] = url
    item['销售情况'] = ''
    try:
        item['分类'] = dict['物业形态']
    except:
        item['分类'] = ''
    try:
        item['装修'] = ''
    except:
        item['装修'] = ''

    try:
        item['户型'] = dict['主要户型']
    except:
        item['户型'] = ''
    try:
        item['单价'] = dict['项目均价']
    except:
        item['单价'] = ''
    item['总价'] = ''
    try:
        item['建面'] = dict['面积范围']
    except:
        item['建面'] = ''
    try:
        item['最小建面'] = '' #re.findall('(\d+).*?\d+',dict['面积范围'])[0]
        item['最大建面'] = '' #re.findall('\d+.*?(\d+)',dict['面积范围'])[0]
    except:
        item['最小建面'] = ''
        item['最大建面'] = ''
    try:
        item['容积率'] = dict['容积率']
    except:
        item['容积率'] = ''
    try:
        item['绿化率'] = dict['绿化率']
    except:
        item['绿化率'] = ''
    item['楼栋户数'] = ''
    try:
        item['总户数'] = dict['项目户数']
    except:
        item['总户数'] = ''
    try:
        item['建筑面积'] = dict['建筑面积']
    except:
        item['建筑面积'] = ''
    try:
        item['地址'] = html.xpath('//div[@class="pinner clearfix"]/dl[2]/dd/p[3]/span/text()')[0]
    except:
        item['地址'] = ''
    # # tags =
    # # tag = ''
    # # for i in tags:
    # #     tag = tag + ' ' + i.strip()
    item['标签'] = ''
    try:
        item['开盘时间'] = dict['开盘时间']
    except:
        item['开盘时间'] = ''
    try:
        item['物业费'] = ''
    except:
        item['物业费'] = ''
    item['latitude'] = ''
    item['longitude'] = ''
    item['抓取年份'] = year
    item['抓取月份'] = month
    item['数据来源'] = '蓝光发展'
    item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    item['抓取年份'] = year
    item['抓取月份'] = month
    item['抓取日期'] = day
    info_base.insert_one(item)
    has_spider.insert_one({'标题url': url})
    print(item)

def getcity():
    url='https://www.brc.com.cn/realestateworks.aspx?t=46'
    res=get_html(url)
    res.encoding='utf8'
    html=etree.HTML(res.text)
    data={}
    tables=html.xpath('//select[@class="selectYear"]/option')[1:]
    for i in tables:
        city=i.xpath('./text()')[0]
        cityurl=i.xpath('./@value')[0]
        data[city]=cityurl
    return data
def getlist(code,list=[]):
    url='https://www.brc.com.cn/'+code
    res=get_html(url)
    res.encoding='utf8'
    html=etree.HTML(res.text)
    tables=html.xpath('//div[@class="prodctArea-ul clearfix"]/ul/li')
    for i in tables:
        data={}
        data['标题']=i.xpath('./div/div[2]/text()')[0]
        data['标题url']=i.xpath('./div/div[1]/a/@href')[0]
        list.append(data)
    # print(list)
    # print(len(list))
    try:
        nexturl=html.xpath('//div[@id="ctl00_ContentID_Pager"]/a')[-1].xpath('./@href')[0]
        return getlist(nexturl,list)
    except:
        return list
if __name__ == '__main__':
    year = 2021
    month = 8
    day = 31
    citylist=getcity()

    for city,code in citylist.items():
        list=getlist(code,list=[])
        for data in list:
            getDetailInfo(city,data)


