import requests
import time
import pymongo
import re
import json
from lxml import etree
from urllib import parse
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
            retryWrites="false")['房企top100']['绿城中国_数据_202107']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['房企top100']['绿城中国_去重_202107']
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
        print('geturl错误',url, e)
        return get_html(url)

def getList(city):
    url='https://m.gtdreamlife.com/api/app/3.0/home/estate/list'
    data={
        'cityName': city,
        'pageCurrent': 1,
        'pageLimit': 100,
    }
    res=requests.post(url,data=data,headers=headers)
    res.encoding='utf8'
    datalist=res.json()['data']['pageListData']
    return datalist
def getCitylist():
    url = 'https://gtcloud-center.oss-cn-hangzhou.aliyuncs.com/h5AndHomeAreaListprod.js'
    res = requests.get(url, headers=headers)
    res.encoding = 'utf8'
    citylist=re.findall('"areaName":"(.*?)","id',res.text)
    return citylist
def getInfo(id,data):
    url='https://home.gtdreamlife.com/web/pages/buildDetail/buildDetail.html?estateId='+id
    has_spider_urllist = []
    for has_spider_url in has_spider.find():
        has_spider_urllist.append(has_spider_url['标题url'])
    if url in has_spider_urllist:
        print('该页数据已爬取，下一页')
        return
    item = {}
    api='https://m.gtdreamlife.com/api/app/3.0/building_front/buildNewList'
    form={'estateId':id}
    res=requests.post(api,data=form,headers=headers)
    res.encoding='utf8'
    infodata=res.json()['data']['data']
    # print(infodata)
    item['城市'] = data['cityName']
    item['区县'] = data['areaname']
    item['标题'] =data['estateName']
    item['标题url'] = url
    item['销售情况'] = ''
    item['分类'] =''
    try:
        item['装修'] = infodata['decorationtype']
    except:
        item['装修'] = ''
    item['户型'] =data['admProjectHousePicDTOList']
    item['单价'] = data['price']
    item['总价'] = data['totalprice']
    item['建面'] = ''
    item['最小建面'] = ''
    item['最大建面'] = ''
    try:
        item['容积率'] = infodata['arearate']
    except:
        item['容积率'] = ''
    try:
        item['绿化率'] = infodata['greenrate']
    except:
        item['绿化率'] =''
    item['规划户数'] = infodata['totalroomnum']
    item['总户数'] = ''
    item['建筑面积'] =''
    item['地址'] =data['projectAddress']
    item['标签'] =data['labels']
    try:
        item['最新开盘'] = data['openDate']
    except:
        item['最新开盘'] =''
    item['物业费'] = ''
    item['latitude'] = data['addressy']
    item['longitude'] = data['addressx']
    item['抓取年份'] = year
    item['抓取月份'] = month
    item['数据来源'] = '绿城中国'
    item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    item['抓取年份'] = year
    item['抓取月份'] = month
    item['抓取日期'] = day
    info_base.insert_one(item)
    has_spider.insert_one({'标题url': url})
    print(item)
def main():
    citylist=getCitylist()
    for city in citylist:
        datalist = getList(city)
        for data in datalist:
            getInfo(data['id'], data)

if __name__ == '__main__':
    year = 2021
    month = 7
    day = 15
    main()
    