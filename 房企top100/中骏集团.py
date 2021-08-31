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
    retryWrites="false")['房企top100']['中骏集团_数据_202107']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['房企top100']['中骏集团_去重_202107']
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
    url = 'https://www.sce-re.com/'+ data['标题url']
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
    item['城市'] = city
    try:
        item['区县'] = ''
    except:
        item['区县'] = ''
    item['标题'] = data['标题']
    item['标题url'] = url
    item['销售情况'] = ''
    try:
        item['分类'] = html.xpath('/html/body/div[3]/div[1]/div/div[2]/p/text()')[0].replace('项目业态：','')
    except:
        item['分类'] = ''
    try:
        item['装修'] = ''
    except:
        item['装修'] = ''

    try:
        item['户型'] = ''
    except:
        item['户型'] = ''
    try:
        item['单价'] = ''
    except:
        item['单价'] = ''
    item['总价'] = ''
    try:
        item['建面'] = ''
    except:
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
    try:
        item['地址'] = html.xpath('/html/body/div[3]/div[1]/div/div[2]/div[1]/p/text()')[0].replace('项目地址：','')
    except:
        item['地址'] = ''
    # # tags =
    # # tag = ''
    # # for i in tags:
    # #     tag = tag + ' ' + i.strip()
    item['标签'] = ''
    try:
        item['开盘时间'] = ''
    except:
        item['开盘时间'] = ''
    try:
        item['物业费'] = ''
    except:
        item['物业费'] = ''
    item['latitude'] = ''
    item['longitude'] = ''
    item['数据来源'] = '中骏集团'
    item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    item['抓取年份'] = year
    item['抓取月份'] = month
    item['抓取日期'] = day
    info_base.insert_one(item)
    has_spider.insert_one({'标题url': url})
    print(item)


def getlist(code):
    url='https://www.sce-re.com/WebUserControl/product/GetNewsList1.ashx'
    form={
        'pageIndex': 1,
        'pageSize': 200,
        'TypeID': code,
        'TypeID2': 0
    }
    res=requests.post(url,data=form,headers=headers)
    res.encoding='utf8'
    data=json.loads(res.text)['list']
    list=data.split('<li')[1:]
    datalist=[]
    for i in list:
        data={}
        url=re.findall('href=\"(.*?)\">',i)[0]
        title=re.findall('<h1>(.*?)<\/h1>',i)[0].replace('&#183;','·')
        data['标题']=title
        data['标题url']=url
        datalist.append(data)
    return datalist

def getcity():
    url='https://www.sce-re.com/product.aspx?type=15&cityid=551&estateid='
    res=get_html(url)
    res.encoding='utf8'
    html=etree.HTML(res.text)
    tables=html.xpath('//*[@id="city"]/li')
    citycode={}
    for i in tables:
        uid=i.xpath('./@value')[0]
        city=i.xpath('./text()')[0]
        citycode[city]=uid
    return citycode


if __name__ == '__main__':
    year = 2021
    month = 7
    day = 15
    citycode=getcity()
    # print(citycode)
    for city,code in citycode.items():
        datalist=getlist(code)
        # print(datalist)
        for data in datalist:
            getDetailInfo(city,data)
