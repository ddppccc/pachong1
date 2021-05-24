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
            retryWrites="false")['房企top100_5月数据']['longhujituan_cjy']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['房企top100_5月数据']['longhujituan_has_spider']
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
def getList():
    url='https://mzapi.longfor.com/web/api/project/selecthottestproject'
    headers = {
                'Accept':'application/json,text/plain,*/*',
                'Accept-Encoding':'gzip,deflate,br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'apiversion':'2.1',
                'appversion':'1.0',
                'Connection':'keep-alive',
                'Content-Length':'128',
                'Content-Type':'application/json;charset=UTF-8',
                'Host':'mzapi.longfor.com',
                'Origin':'https://u.longfor.com',
                'refer':'pc',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
                'user-source-channel':'{"mediaId":"","actionId":"source1","channelId":"5","customId":"","serviceId":"","serviceType":"Lw=="}',
                'X-Gaia-Api-Key':'58e2d904-7f66-42a0-9bb4-e5134d7c1f43',
    }
    data={
        'areaid':'0',
        'pageFlag':1,
        'pageindex':1,
        'pagesize':300,
        'projectTypeList':[],
        'projectname':"",
        'projecttype':"",
        'salesstatus':"0"
    }
    res=requests.post(url,json=data,headers=headers)
    list=res.json()['data']['list']
    print(len(list))
    return list
def getHouseType(pid):
    headers = {
        'Accept':'application/json,text/plain,*/*',
        'Accept-Encoding':'gzip,deflate,br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'apiversion':'2.1',
        'appversion':'1.0',
        'Connection':'keep-alive',
        'Content-Length':'35',
        'Content-Type':'application/json;charset=UTF-8',
        'Host':'mzapi.longfor.com',
        'Origin':'https://u.longfor.com',
        'refer':'h5-pc',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
        'user-source-channel':'{"mediaId":"","actionId":"source1","channelId":"5","customId":"","serviceId":"","serviceType":"Lw=="}',
        'X-Gaia-Api-Key':'58e2d904-7f66-42a0-9bb4-e5134d7c1f43',
    }
    url='https://mzapi.longfor.com/web/api/project/selectHouseTypeList'
    data={'projectId':pid,'pageIndex':1,'pageSize':99}
    res=requests.post(url,json=data,headers=headers)
    res.encoding='utf8'
    list=res.json()['data']
    houtype=''
    for i in list:
        for j in i['names']:
            houtype =houtype +' ' +str(j['name'])
    return houtype
def getInfo(data):
    url ='https://u.longfor.com/home/projectInfo/city/'+data['AreaID']+'/project/'+data['ProjectID']+'?cid='+data['AreaID']
    has_spider_urllist = []
    for has_spider_url in has_spider.find():
        has_spider_urllist.append(has_spider_url['标题url'])
    if url in has_spider_urllist:
        print('该页数据已爬取，下一页')
        return
    headers = {
        'Accept':'application/json, text/plain, */*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'apiversion':'1.1',
        'appversion':'1.0',
        'Connection':'keep-alive',
        'Content-Length':'35',
        'Content-Type':'application/json;charset=UTF-8',
        'Host':'mzapi.longfor.com',
        'Origin':'https://u.longfor.com',
        'refer':'h5-pc',
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile':'?0',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-site',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
        'user-source-channel':'{"mediaId":"","actionId":"source1","channelId":"5","customId":"","serviceId":"","serviceType":"Lw=="}',
        'X-Gaia-Api-Key':'58e2d904-7f66-42a0-9bb4-e5134d7c1f43',
    }
    item = {}
    api='https://mzapi.longfor.com/web/api/project/projectlistinfodetailsselect'
    form={'ispublish':"1",'projectid':data['ProjectID']}
    res = requests.post(api, json=form, headers=headers)
    res.encoding = 'utf8'
    # print(res)
    # return
    detaildata = res.json()['data']
    # print(detaildata)
    item['城市'] =data['city']
    item['区县'] =data['district']
    item['标题'] =data['ProjectName']
    item['标题url'] = url
    item['销售情况'] = ''
    item['分类'] = ''
    try:
        item['装修'] =detaildata['Decoration']
    except:
        item['装修'] = ''
    item['户型'] =getHouseType(data['ProjectID'])
    if data['unitType'] == '单价':
        item['单价'] =data['Price']
        item['总价'] =''
    if data['unitType'] == '总价':
        item['单价'] =''
        item['总价'] =data['Price']
    item['建面'] = ''
    item['最小建面'] = ''
    item['最大建面'] = ''
    try:
        item['容积率'] =detaildata['Capacity']
    except:
        item['容积率'] = ''
    try:
        item['绿化率'] =detaildata['Greening']
    except:
        item['绿化率'] = ''
    item['楼栋户数'] =''
    item['总户数'] = detaildata['HouseholdNum']
    item['建筑面积'] = detaildata['BuildArea']
    item['地址'] =data['ProjectAddress']
    tags=''
    for tag in data['TagNames']:
        tags=tags+' '+tag['TagName']
    item['标签'] =tags
    try:
        item['开盘时间'] =detaildata['OpeningTime']
    except:
        item['开盘时间'] = ''
    item['物业费'] = detaildata['PropertyMoney']
    item['latitude'] =data['sellHouseLatitude']
    item['longitude'] =data['sellHouseLongitude']
    item['数据来源'] = '龙湖集团'
    item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    item['抓取年份'] = year
    item['抓取月份'] = month
    item['抓取日期'] = day
    info_base.insert_one(item)
    has_spider.insert_one({'标题url': url})
    print(item)
def main():
    datalist = getList()
    print('datalist获取成功')
    for data in datalist:
        getInfo(data)
if __name__ == '__main__':
    year = 2021
    month = 5
    day = 23
    main()