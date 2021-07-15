import requests
import time
import pymongo
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
            retryWrites="false")['房企top100']['碧桂园_数据_202106']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['房企top100']['碧桂园_去重_202106']
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
}
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
        #
        # response.encoding = encod
        return response
    except Exception as e:
        print('geturl错误',url, e)
        return get_html(url)
def getCityMap(cityList=[]):
    url='https://xs6.bgy.com.cn/XCXhfy/Handler/FHYPcOfficialHandler.ashx?act=getCitiesList'
    response = get_html(url).json()
    cl = response['items']
    for i in response['items']:
        l = i['cities']
        for j in l:
            # print(j)
            cityList.append(j['name'])
    # print(cl['cities'])
    return cityList


def getInfo(areaList):
    for area in areaList:
        has_spider_areaList = []
        for has_spider_area in has_spider.find():
            has_spider_areaList.append(has_spider_area['areaId'])
        if area['areaId'] in has_spider_areaList:
            print('该页数据已爬取，下一页')
            continue
        dict={}
        dict['标题']=area['areaName']
        dict['url']='https://fhy.bgy.com.cn/#/property/detail?areaId='+area['areaId']
        dict['城市']=area['City']
        # dict['省市']=area['Province']
        dict['户型']=area['ApartmentInterval']
        dict['单价']=area['AveragePriceJson']
        dict['总价']=area['consultPriceJson']
        dict['建面']=area['AreaIntervalJson']
        dict['最小建面']=area['AreaInterval']
        dict['最大建面']=area['AreaIntervalEnd']
        dict['地址']=area['Address']
        dict['标签']=area['Lables']
        dict['开盘时间']=area['KaiPanTime']
        dict['latitude']=area['Lat']
        dict['longitude']=area['Lng']
        dict['数据来源']='碧桂园'
        dict['销售情况'] = ''
        dict['装修'] = ''
        dict['容积率'] = ''
        dict['绿化率'] = ''
        dict['楼栋总数'] = ''
        dict['总户数'] = ''
        dict['建筑面积'] = ''
        dict['物业费'] = ''
        getDetailInfo(dict, area['areaId'])
def getDetailInfo(dict,areaId):   #获取详细信息
    url='https://xs6.bgy.com.cn/XCXhfy/Handler/FHYPcOfficialHandler.ashx?act=getPropertyDetail&areaId='+areaId
    try:
        res=get_html(url).json()
        data=res['data'][0]
        # print(data)
        dict['区县'] = data['Region']
        dict['分类'] = data['ProductType']
    except:
        dict['区县'] = ''
        dict['分类'] = ''
    dict['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    dict['抓取年份'] = year
    dict['抓取月份'] = month
    dict['抓取日期'] = day
    print(dict)
    info_base.insert_one(dict)
    has_spider.insert_one({'areaId': areaId})
    sum.append(1)
    print(len(sum))

def getallid():
    idlist=[]
    for page in range(1,95):
        url = 'https://xs6.bgy.com.cn/XCXhfy/Handler/FHYPcOfficialHandler.ashx?act=getPropertyList&pageNum=' + str(page) + '&pageSize=20&sortType=&keyword=&group=&city=&isHome='
        print(url)
        response = get_html(url).json()
        list = response['data']['list']
        getInfo(list)


if __name__ == '__main__':
    year = 2021
    month = 6
    day = 9
    sum=[]
    t1 = time.time()
    getallid()
    print('运行结束,耗时',int(time.time()-t1))






