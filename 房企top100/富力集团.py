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
    retryWrites="false")['房企top100']['fulijituan_cjy']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['房企top100']['fulijituan_has_spider']
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
}
year = 2021
month = 4


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
        response = requests.get(url, headers=headers, verify=False,timeout=(10, 10))
        # encod = response.apparent_encoding
        # if encod.upper() in ['GB2312', 'WINDOWS-1254']:
        #     encod = 'gbk'
        # response.encoding = encod
        return response
    except Exception as e:
        print('geturl错误', url, e)
        time.sleep(2)
        return get_html(url)


def getDetailInfo(data):
    url = 'https://www.rfchina.com/' + data['标题url']
    has_spider_urllist = []
    for has_spider_url in has_spider.find():
        has_spider_urllist.append(has_spider_url['标题url'])
    if url in has_spider_urllist:
        print('该页数据已爬取，下一页')
        return
    res = get_html(url)
    res.encoding = 'utf8'
    if res.status_code == 502:
        print(url, '页面打开失败')
        return
    # print(res.text)
    html = etree.HTML(res.text)
    item = {}
    item['城市'] = data['城市']
    item['区县'] = ''
    item['标题'] = data['标题']
    item['标题url'] = url
    infos=html.xpath('string(.//div[@class="box2"]/div[@class="left"]/div)').split('\r\n')
    item['销售情况'] = infos[5].replace('销售状态：','').strip()
    try:
        item['分类'] = infos[4].replace('所属业态：','').strip()
    except:
        item['分类'] = ''
    try:
        item['装修'] = ''
    except:
        item['装修'] = ''

    item['户型'] = ''
    try:
        item['单价'] = html.xpath('string(.//div[@class="box1"]/div/div/p[1])').replace('价格：','')
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
    item['地址'] = infos[2].replace('项目地址：','').strip()
    # # tags =
    # # tag = ''
    # # for i in tags:
    # #     tag = tag + ' ' + i.strip()
    item['标签'] = html.xpath('string(.//div[@class="box1"]/div/p[2])').replace('\r\n','').strip()
    try:
        item['开盘时间'] = infos[6].replace('开盘时间：','').strip()
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
    item['数据来源'] = '旭辉集团'
    item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    info_base.insert_one(item)
    has_spider.insert_one({'标题url': url})
    print(item)


def getlist(city,code):
    url = 'https://www.rfchina.com/Ajax/More.ashx'
    form={
        'method': 'GetEstateMore',
        'pageIndex': 1,
        'pageSize': 150,
        'typeId': 14,
        'gid': 1,
        'ptype': 0,
        'cid':code
    }
    res = requests.post(url,data=form,headers=headers,verify=False)
    res.encoding = 'utf8'
    list=[]
    tables=str(res.json()).split('<li>')[1:]
    for i in tables:
        data={}
        data['标题'] = re.findall('<h3>(.*?)</h3>', i)[0]
        data['城市']=city
        data['标题url'] = re.findall('<a href="(.*?)">', i)[0]
        list.append(data)
    return list
def getprovince():
    url='https://www.rfchina.com/product.aspx?type=14&gid=1'
    res=get_html(url)
    res.encoding='utf8'
    html=etree.HTML(res.text)
    tables=html.xpath('//*[@id="province"]/li')
    list=[]
    for i in tables:
        data={}
        province=i.xpath('./text()')[0]
        code=i.xpath('./@data-pid')[0]
        data[province]=code
        list.append(code)
    # print(list)
    return list
def getcity(provincelist):
    url = 'https://www.rfchina.com/product.aspx?type=14&gid=1'
    res = get_html(url)
    res.encoding = 'utf8'
    html = etree.HTML(res.text)
    tables=html.xpath('//*[@id="city"]/li')
    data = {}
    for i in tables:
        province=i.xpath('./@data-pid')[0]
        if province not in provincelist:
            continue

        citycode=i.xpath('./@data-cid')[0]
        city=i.xpath('./text()')[0]
        data[city]=citycode
    return data
if __name__ == '__main__':
    provincelist=getprovince()
    citydict=getcity(provincelist)
    # print(citydict)
    for city,code in citydict.items():
        list=getlist(city,code)
        for data in list:
            getDetailInfo(data)


