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
    retryWrites="false")['房企top100_5月数据']['zhengrongjituan_cjy']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['房企top100_5月数据']['zhengrongjituan_has_spider']
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
    url = 'http://www.zhenrodc.com/project/'+data['标题url']
    # url='http://www.zhenrodc.com/project/details-business-61.html'
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
    html=etree.HTML(res.text)
    item = {}
    item['城市'] =city
    item['区县'] =''
    item['标题'] =data['标题']
    item['标题url'] = url
    info=html.xpath('//*[@id="s1"]//div[@class="area_25 tcenter mo_margintop10"]')
    infodict={}
    if url == 'http://www.zhenrodc.com/project/details-business-61.html':
        infodict['项目地址'] = html.xpath('string(.//*[@id="s1"]/section[1]/div/div[1]/div[1])').strip()[5:].replace('\r\n',                                                                                                         '').strip()
        infodict['建筑类型'] = html.xpath('string(.//*[@id="s1"]/section[1]/div/div[2]/div[1])').replace('建筑类型：', '').strip()
        infodict['开盘时间'] = html.xpath('string(.//*[@id="s1"]/section[1]/div/div[3]/div[1])').replace('开盘时间：', '').strip()
        infodict['项目状态'] = html.xpath('string(.//*[@id="s1"]/section[1]/div/div[4]/div[1])').replace('项目状态：', '').strip()
        infodict['建筑装修'] = html.xpath('string(.//*[@id="s1"]/section[1]/div/div[2]/div[2])').replace('建筑装修：', '').strip()
        infodict['建筑面积'] = html.xpath('string(.//*[@id="s1"]/section[1]/div/div[3]/div[2])').replace('建筑面积：', '').strip()
        infodict['主力户型'] = html.xpath('string(.//*[@id="s1"]/section[1]/div/div[4]/div[2])').replace('主力户型：', '').strip()   
    else:
        infodict['项目地址'] = html.xpath('string(.//*[@id="s1"]/section[2]/div[@aos="fade-zoom-in"]/div[1]/div[1])').strip()[5:].replace('\r\n','').strip()
        infodict['建筑类型'] = html.xpath('string(.//*[@id="s1"]/section[2]/div[@aos="fade-zoom-in"]/div[2]/div[1])').replace('建筑类型：','').strip()
        infodict['开盘时间'] = html.xpath('string(.//*[@id="s1"]/section[2]/div[@aos="fade-zoom-in"]/div[3]/div[1])').replace('开盘时间：','').strip()
        infodict['项目状态'] = html.xpath('string(.//*[@id="s1"]/section[2]/div[@aos="fade-zoom-in"]/div[4]/div[1])').replace('项目状态：','').strip()
        infodict['建筑装修'] = html.xpath('string(.//*[@id="s1"]/section[2]/div[@aos="fade-zoom-in"]/div[2]/div[2])').replace('建筑装修：','').strip()
        infodict['建筑面积'] = html.xpath('string(.//*[@id="s1"]/section[2]/div[@aos="fade-zoom-in"]/div[3]/div[2])').replace('建筑面积：','').strip()
        infodict['主力户型'] = html.xpath('string(.//*[@id="s1"]/section[2]/div[@aos="fade-zoom-in"]/div[4]/div[2])').replace('主力户型：','').strip()
    # print(infodict['项目地址'])
    # print(infodict['建筑类型'])
    # print(infodict['开盘时间'])
    # print(infodict['项目状态'])
    # print(infodict['建筑装修'])
    # print(infodict['建筑面积'])
    # print(infodict['主力户型'])
    for i in info:
        key=i.xpath('./p/text()')[0].strip()
        value=i.xpath('string(./div/h3/text())').strip()
        infodict[key]=value
    item['销售情况'] =infodict['项目状态']
    try:
        item['分类'] =infodict['建筑类型']
    except:
        item['分类'] = ''
    try:
        item['装修'] =infodict['建筑装修']
    except:
        item['装修'] = ''

    item['户型'] =infodict['主力户型']
    try:
        item['单价'] =''
    except:
        item['单价'] = ''
    item['总价'] = ''
    item['建面'] =''
    try:
        item['最小建面'] =''
        item['最大建面'] =''
    except:
        item['最小建面'] = ''
        item['最大建面'] = ''
    try:
        item['容积率'] =infodict['容积率']
    except:
        item['容积率'] = ''
    try:
        item['绿化率'] =infodict['绿化率']
    except:
        item['绿化率'] = ''
    item['楼栋户数'] =''
    try:
        item['总户数'] =''
    except:
        item['总户数'] = ''
    try:
        item['建筑面积'] =infodict['建筑面积']
    except:
        item['建筑面积'] = ''
    try:
        infodict['项目地址']=html.xpath('/html/body/div[1]/article/section[2]/div/div/div[2]/div[2]/div[2]/a/text()')[0]
    except:
        pass
    item['地址'] = infodict['项目地址']
    # tags =
    # tag = ''
    # for i in tags:
    #     tag = tag + ' ' + i.strip()
    item['标签'] = data['标签']
    try:
        item['开盘时间'] =infodict['开盘时间']
    except:
        item['开盘时间'] = ''
    try:
        item['物业费'] =''
    except:
        item['物业费'] =''
    item['latitude'] =''
    item['longitude'] =''
    item['抓取年份'] = year
    item['抓取月份'] = month
    item['数据来源'] = '正荣集团'
    item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    item['抓取年份'] = year
    item['抓取月份'] = month
    item['抓取日期'] = day
    info_base.insert_one(item)
    has_spider.insert_one({'标题url': url})
    print(item)
def getcitylist():
    url = 'http://www.zhenrodc.com/project/index.aspx?hasCity=1'
    res = get_html(url)
    res.encoding = 'utf8'
    print(res.json())
    return res.json()
def getlist(code):
    url='http://www.zhenrodc.com/project/city-'+str(code)+'.html'
    res=get_html(url)
    res.encoding='utf8'
    html=etree.HTML(res.text)
    tables=html.xpath('/html/body/div[2]/article/section[5]/div/div')
    list=[]
    for house in tables:
        data={}
        data['标题']=house.xpath('.//h3/text()')[0]
        data['标题url']=house.xpath('.//@href')[0]
        tags=house.xpath('.//h6/span')[1:]
        tag=''
        for i in tags:
            s=i.xpath('./text()')[0].strip()
            tag=tag+s+','
        data['标签']=tag
        list.append(data)
    return list
if __name__ == '__main__':
    year = 2021
    month = 5
    day = 23
    # cilist=getcitylist()
    # for i in cilist:
    #     city=i['name']
    #     datalist=getlist(i['id'])
    #     for data in datalist:
    #         getDetailInfo(city, data)
    
    
    '''
    原链接已失效，新网页无数据
    '''
   
