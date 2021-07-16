import requests
import time
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
            retryWrites="false")['房企top100']['万科_数据_202106']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['房企top100']['万科_去重_202106']
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
def getCityInfo():
    url = 'https://zhikebiz.vanke.com/api/sys/cities/list'
    res = get_html(url)
    res.encoding = 'utf8'
    list = res.json()['data']
    # for data in list:
    #     print('abbreviation', data['abbreviation'])
    #     print('cityCode', data['cityCode'])
    #     print('cityName', data['cityName'])
    #     print('regionCode', data['regionCode'])
    #     print('regionName', data['regionName'])
    #     print('sapId', data['sapId'])
    return list
def getList(city,citycode):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json;charset=UTF-8',
        'referer': 'https://life.vanke.com/search?sort=',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        'useraccessinfo': '{"domain":"zxj-web","traceId":1619153523487}'
    }
    url = 'https://zhikebiz.vanke.com/api/product/list'
    data = {
        'keyword': "",
        'pageNo': '1',
        'pageSize': '100',
        'productTypeCode': "1",
        'showAppCode': "zxj",
        'showCityCode': citycode,
        'sort': "sort",
        'tag': "",
    }
    res = requests.post(url, headers=headers, json=data)
    res.encoding = 'utf8'
    print(city)
    if not res.json()['data']['list']:
        return
    list=res.json()['data']['list']
    for data in list:
        getInfo(data, data['proCode'])
        # print('address',data['address'])
        # print('avgPrice',data['avgPrice'])
        # print('features',data['features'])
        # print('mapJson',data['mapJson'])
        # print('maxArea',data['maxArea'])
        # print('name',data['name'])
        # print('proCode',data['proCode'])
        # print('minArea',data['minArea'])
        # print('showCity',data['showCity'])
        # print('showCountry',data['showCountry'])
        # print('showCountryCode',data['showCountryCode'])
        # print('spotLightJson',data['spotLightJson'])
        
    # print(res.json()['data']['list'])
    # print('pageNo',res.json()['data']['pageNo'])
    # print('pageSize',res.json()['data']['pageSize'])
    # print('total',res.json()['data']['total'])

def getInfo(data,proCode):
    has_spider_proCodelist = []
    for has_spider_proCode in has_spider.find():
        has_spider_proCodelist.append(has_spider_proCode['proCode'])
    if data['proCode'] in has_spider_proCodelist:
        print('该页数据已爬取，下一页')
        return 
    dict={}
    url='https://life.vanke.com/estate?proCode='+str(proCode)
    apiurl='https://zhikebiz.vanke.com/api/product/detail/'+str(proCode)
    res=get_html(apiurl)
    res.encoding='utf8'
    detaildata=res.json()['data']
    try:
        detailJson = json.loads(detaildata['detailJson'])
    except:
        print('没有detailJson数据')
    try:
        mapjson=json.loads(data['mapJson'])
    except:
        print('没有mapJson数据')
    dict['城市']=data['showCity']
    dict['区县']=data['showCountry']
    dict['标题']=data['name']
    dict['标题url'] =url
    dict['销售情况']=''
    dict['分类']=''
    try:
        dict['装修']=detailJson['decorationStandard']
    except:
        dict['装修'] =''
    dict['户型']=detaildata['estateMarket']
    dict['单价']=data['avgPrice']
    dict['总价']=''
    dict['建面']=''
    dict['最小建面']=data['minArea']
    dict['最大建面']=data['maxArea']
    try:
        dict['容积率']=detailJson['plotRatio']
    except:
        dict['容积率'] =''
    try:
        dict['绿化率']=detailJson['greeningRate']
    except:
        dict['绿化率'] =''
    dict['楼栋户数']=''
    try:
        dict['规划户数']=detailJson['planFamilies']
    except:
        dict['规划户数'] =''
    try:
        dict['占地总面积']=detailJson['locationArea']
    except:
        dict['占地总面积'] =''
    dict['地址']=data['address']
    dict['标签']=data['features']
    dict['开盘时间']=data['openDate']
    try:
        dict['物业费']=detailJson['propertyFee']
    except:
        dict['物业费'] =''
    try:
        dict['latitude']=mapjson['latitude']
        dict['longitude']=mapjson['longitude']
    except:
        dict['latitude'] = ''
        dict['longitude'] = ''
    dict['数据来源']='万科'
    dict['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    dict['抓取年份'] = year
    dict['抓取月份'] = month
    dict['抓取日期'] = day
    print(dict)
    sum.append(1)
    print(len(sum))
    info_base.insert_one(dict)
    has_spider.insert_one({'proCode': proCode})

def mian():
    list=getCityInfo()
    for data in list:
        # print('cityCode', data['cityCode'])
        citycode=data['cityCode']
        city=data['cityName']
        # print(city)
        getList(city,citycode)
if __name__ == '__main__':
    year = 2021
    month = 6
    day = 9
    sum=[]
    mian()


# getList('重庆',500000)
# res=requests.get('https://zhikebiz.vanke.com/api/product/detail/1547884951063P')
# res.encoding='utf8'
# print(res.json()['data']['detailJson'])
# detailJson=json.loads(res.json()['data']['detailJson'])
# # print(x['plotRatio'])
