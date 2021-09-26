import requests
import time
import pymongo
import re
import json
from lxml import etree
from urllib import parse
from multiprocessing import Process,Pool
import warnings
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
            retryWrites="false")['房企top100']['金地集团_数据_202108']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['房企top100']['金地集团_去重_202108']
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    'Host':'online.gemdale.com',
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
        response = requests.get(url, headers=headers,verify=False,timeout=(10, 10))
        # response = requests.get(url, headers=headers,verify=False,proxies = {"https": get_proxy()},timeout=(10, 10))

        # encod = response.apparent_encoding
        # if encod.upper() in ['GB2312', 'WINDOWS-1254']:
        #     encod = 'gbk'
        # response.encoding = encod
        return response
    except Exception as e:
        print('geturl错误',url, e)
        time.sleep(2)
        return get_html(url)
def getCityList():
    url='https://online.gemdale.com/list'
    # res=requests.get(url,headers=headers,proxies = {"https": get_proxy()},verify=False,timeout=10)
    res=requests.get(url,headers=headers,verify=False,timeout=10)
    res.encoding='utf8'
    # print(res.text)
    html=etree.HTML(res.text)[0]
    cityList=html.xpath('/html/body/div[1]/div/div/li/a')
    citydict={}
    for i in cityList:
        city=i.xpath('./text()')[0]
        urlcode=i.xpath('./@href')[0]
        citydict[city]=urlcode
    return citydict
def getInfo(city,code):
    url = 'https://online.gemdale.com'+code
    listurl='https://online.gemdale.com/list'
    # headers['Cookie']='bt_route=a1836aad7f47f3a6ca76d65fa3eb2f1a; PHPSESSID=vau2jq9rbodu7i5p0q4uf4kgvl; acw_tc=0bcf7c4616194252656401174e8aebbc811a561e2595a8727a7ce881ec64ad; XSRF-TOKEN=eyJpdiI6Img5Umk0MWNuUDVOaTBDNmxadlwvV0NBPT0iLCJ2YWx1ZSI6InFmdVBWYWNYcE5iUDVRWjRoaThmQ2xGSDN5cGNaSkVzeHdkclVrZFlBNW1aNThpK0szUjUxZ3NNbDJzelh5dFgiLCJtYWMiOiIwODU4ZjIwNWNjMDFmMzkzOTQzMjRmNDFlMGViN2QyYmQ0M2NhNWFmNTY5MWM5YzkzMWExMWNmYTRkNWI4ODdlIn0%3D; laravel_session=eyJpdiI6IlJYcWduaGhQanA1Wkx0YUVDZExSVVE9PSIsInZhbHVlIjoiS0sxUTFHNjlZUlpiU1hFODJrQTVLajBcL1BCenpVb2ZSUG1Qc0pHSmZRUXVZSXA2cSswUzdyWGtjNWpuUU9QUjkiLCJtYWMiOiIwNDMyOTJhMzBkOTNlMGFmNDcwYzY3NGJhMDZiZTFjMDI4ZGFjMTljZjljMmE5NmJmYTU4NGMwNjc2ZTU2N2EzIn0%3D'
    session = requests.session()
    # print(url)
    session.get(url,headers=headers,verify=False,timeout=10)
    res=session.get(listurl,verify=False)
    res.encoding='utf8'
    html=etree.HTML(res.text)
    tables=html.xpath('/html/body/div[5]/div')[1:]
    # print('tables',len(tables),tables)
    datalist=[]
    for i in tables:
        data = {}
        data['城市']=city
        data['标题']=i.xpath('./a/div[2]/span/text()')[0].strip()
        data['标题url']='https://online.gemdale.com'+i.xpath('./a/@href')[0]
        data['地址']=i.xpath('string(./a/div[2]/p[1])').strip()
        data['户型']=i.xpath('string(./a/div[2]/p[2])').replace('户型：','').strip()
        data['开盘时间']=i.xpath('string(./a/div[2]/p[3])').strip()
        data['单价']=i.xpath('string(./a/div[2]/div[1])').strip()
        datalist.append(data)
    # print(datalist)
    return datalist
def getDetailInfo(data):
    url =data['标题url']
    has_spider_urllist = []
    for has_spider_url in has_spider.find():
        has_spider_urllist.append(has_spider_url['标题url'])
    if url in has_spider_urllist:
        print('该页数据已爬取，下一页')
        return
    res=get_html(url)
    res.encoding='utf8'
    if res.status_code == 502:
        print(url,'页面打开失败')
        return 
    html=etree.HTML(res.text)
    # print(res.text)
    item = {}
    item['城市'] =data['城市']
    item['区县'] =''
    item['标题'] =data['标题']
    item['标题url'] = url
    item['销售情况'] = ''
    item['分类'] = html.xpath('//div[@style="float: left;width: 50%;"]/li[3]/p/text()')[0]
    try:
        item['装修'] =html.xpath('//div[@style="float: left;width: 50%;"]/li[4]/p/text()')[0]
    except:
        item['装修'] = ''
    item['户型'] =data['户型']
    item['单价'] =data['单价']
    item['总价'] =''
    item['建面'] = ''
    item['最小建面'] = ''
    item['最大建面'] = ''
    try:
        item['容积率'] =''
    except:
        item['容积率'] = ''
    try:
        item['绿化率'] =''
    except:
        item['绿化率'] = ''
    item['楼栋户数'] =html.xpath('//div[@style="float:right;width: 50%;"]/li[3]/p/text()')[0]
    item['总户数'] =''
    item['建筑面积'] =html.xpath('//div[@style="float:right;width: 50%;"]/li[2]/p/text()')[0]
    item['地址'] =data['地址']
    tags=html.xpath('.//div[@class="detail_banner_code_tag_bottom_tags"]/span/text()')
    tag=''
    for i in tags:
        tag=tag+' '+i.strip()
    item['标签'] =tag
    try:
        item['开盘时间'] =data['开盘时间']
    except:
        item['开盘时间'] = ''
    item['物业费'] =html.xpath('//div[@style="float: left;width: 50%;"]/li[6]/p/text()')[0]
    item['latitude'] =''
    item['longitude'] =''
    item['抓取年份'] = year
    item['抓取月份'] = month
    item['数据来源'] = '金地集团'
    item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    item['抓取年份'] = year
    item['抓取月份'] = month
    item['抓取日期'] = day
    info_base.insert_one(item)
    has_spider.insert_one({'标题url': url})
    print(item)
if __name__ == '__main__':
    year = 2021
    month = 8
    day = 31
    citydict=getCityList()
    print(citydict)
    for city,urlcode in citydict.items():
        datalist=getInfo(city,urlcode)
        for data in datalist:
            getDetailInfo(data)
            # time.sleep(2)
            
