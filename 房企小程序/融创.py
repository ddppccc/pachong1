# -*- coding:utf-8 -*-
import csv
import random
import sys
import io
import time

from bson import ObjectId
import requests
import pymongo
from jsonpath import jsonpath

Info_url = 'https://msales.sunac.com.cn/open/api/pro/pro/proBaseInfo/all'
# {"data":{"uuid":"P0302"}}
city_url = 'https://msales.sunac.com.cn/open/api/sys/city/queryCityList'
# {"data":{"cityName":""}}
prolist_url = 'https://msales.sunac.com.cn/open/api/pro/pro/map/proListNew'
# {"data":{"geoCityUuid":"110100","proType":1}}
Db = pymongo.MongoClient(host='127.0.0.1', port=27017)['融创']['info']

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

headers = {
    'Host': 'msales.sunac.com.cn',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
    'UserAccessInfo': '{"loginId":"","versionNum":"1.6.0","domain":"group-applet","timestamp":"1604978472","signature":"0625e2b3835be1ac03a9946288efaff21a88ab54"}',
    'accept': '*/*',
    'content-type': 'application/json',
    'Referer': 'https://servicewechat.com/wx0c971d77a629b471/70/page-frame.html',
    'Accept-Encoding': 'gzip,deflate,br',
}

def statis_output(title, rowlist, database) -> object:
    csvfile = open('{}'.format(title), 'w+', newline='', encoding='utf-8')
    res_writer = csv.writer(csvfile, dialect='excel')
    res_writer.writerow(rowlist)
    for item in database.find():
        res_writer.writerow(list(item.values())[1:])

def get_cityMap(url,headers,json):

    resp = requests.post(url=url,headers=headers,json=json)
    data = jsonpath(resp.json(),'$.data')[0]
    for i in data:
        time.sleep(random.randint(10, 15) * 0.1 * 3)
        list = jsonpath(i,'$.list')[0]
        for j in list:
            time.sleep(random.randint(10, 15) * 0.1 * 3)
            item = {}
            item['geoCityUuid'] = j['cid']
            item['城市'] = j['cname']
            get_cityList(prolist_url,headers,{"data":{"geoCityUuid":item['geoCityUuid']},"proType":1},item)

def get_cityList(url,headers,json,item):
    try:
        resp = requests.post(url=url,headers=headers,json=json)
    except:
        print('wating....')
        time.sleep(20)
        resp = requests.post(url=url,headers=headers,json=json)
    data = jsonpath(resp.json(),'$.data')[0]
    for i in data:
        time.sleep(random.randint(10, 15) * 0.1 * 3)
        item['uuid'] = i['uuid']
        item['标题'] = i['name']
        item['单价_out'] = i['price']
        item['建面'] = i['areaInterval']
        item['latitude'] = i['dimension']
        item['longitude'] = i['longitude']
        get_proBaseInfo(Info_url,headers,{"data":{"uuid":item['uuid']}},item)



def get_proBaseInfo(url,headers,json,item):
    try:
        resp = requests.post(url=url,headers=headers,json=json)
    except:
        print('wating....')
        time.sleep(20)
        resp = requests.post(url=url,headers=headers,json=json)
    item['_id'] = ObjectId()
    item['区县'] = jsonpath(resp.json(),'$.data.geoAreaName')[0]
    item['地址'] = jsonpath(resp.json(),'$.data.buldAddr')[0]
    item['项目名'] = jsonpath(resp.json(),'$.data.name')[0]
    item['户型'] = jsonpath(resp.json(),'$.data.mainHuxingName')[0]+jsonpath(resp.json(),'$.data.areaInterval')[0]
    item['开盘时间'] = jsonpath(resp.json(),'$.data.openTime')[0]
    item['标签'] = jsonpath(resp.json(),'$.data.tag')[0]
    item['单价'] = jsonpath(resp.json(),'$.data.price')[0]
    item['装修'] = jsonpath(resp.json(),'$.data.decorate')[0]
    item['开发商'] = jsonpath(resp.json(),'$.data.buldDeveloper')[0]
    item['容积率'] = jsonpath(resp.json(),'$.data.volumeRate')[0]
    item['建筑面积'] = jsonpath(resp.json(),'$.data.totalAre')[0]
    item['绿化率'] = jsonpath(resp.json(),'$.data.greenRate')[0]
    item['物业费'] = jsonpath(resp.json(),'$.data.propertyFee')[0]
    item['总户数'] = jsonpath(resp.json(),'$.data.totalUsers')[0]
    print(item)
    Db.insert_one(item)


# city_data = {"data":{"cityName":""}}
# get_cityMap(city_url,headers,city_data)

statis_output('融创_全国_{}_房产信息.csv'.format(time.strftime("%Y-%m-%d", time.localtime())),
              ['120100','城市','uuid', '标题','单价—out','建面','latitude','longitude','区县','地址','项目名','户型','开盘时间','标签','单价','装修','开发商','容积率','建筑面积','绿化率','物业费','总户数'], Db)
