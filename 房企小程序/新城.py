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

Db = pymongo.MongoClient(host='127.0.0.1', port=27017)['新城']['info']

city_Map = 'https://apps1.xincheng.com/brokerService/rest/city/list'


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

headers = {
    'Host': 'apps1.xincheng.com',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
    'content-type': 'application/json',
    'miniprogram': 'wechat',
    'xxj-authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblVzZXJJZCI6IjRmOWMwNTZmMTc4ZDQyZjhiYTg5ZjFiN2Q4NjQ2NWJhIiwidXNlckxvZ2luVHlwZSI6IjIiLCJ0b2tlblR5cGUiOiJhdXRoZW50aWNhdGUiLCJleHAiOjE2MDUwMTI3ODUsImlhdCI6MTYwNDk5ODM4NX0.0g_UX_usj0wg_BSPssSB4nWdUtkWOBm_efQ0SHBPefk',
    'xxj-refresh-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblVzZXJJZCI6IjRmOWMwNTZmMTc4ZDQyZjhiYTg5ZjFiN2Q4NjQ2NWJhIiwidXNlckxvZ2luVHlwZSI6IjIiLCJ0b2tlblR5cGUiOiJyZWZyZXNoLXRva2VuIiwiZXhwIjoxNjA1MjU3NTg1LCJpYXQiOjE2MDQ5OTgzODV9.SWAKR5MlABmn1H3x0PsBeK25C_wCdIiPTZ8FApBE1OE',
    'Referer': 'https://servicewechat.com/wx8d3bd4ba7f82fe1e/12/page-frame.html',
    'Accept-Encoding': 'gzip,deflate,br',
}

def statis_output(title, rowlist, database) -> object:
    csvfile = open('{}'.format(title), 'w+', newline='', encoding='utf-8')
    res_writer = csv.writer(csvfile, dialect='excel')
    res_writer.writerow(rowlist)
    for item in database.find():
        res_writer.writerow(list(item.values())[1:])

def get_cityMap(url,headers):

    resp = requests.get(url=url,headers=headers)
    name = jsonpath(resp.json(),'$..name')
    code = jsonpath(resp.json(),'$..code')[1:]
    for i in range(len(name)):
        item = {}
        item['code'] = code[i]
        item['城市'] = name[i]
        QueryFormats = 'https://apps1.xincheng.com/brokerService/rest/city/queryProject?areaCode={}&format=0&pageIndex=1&pageSize=10'.format(item['code'])
        time.sleep(random.randint(10, 15) * 0.1 * 3)
        get_cityList(QueryFormats,headers,item)

def get_cityList(url,headers,item):
    try:
        resp = requests.get(url=url,headers=headers)
    except:
        print('wating....')
        time.sleep(20)
        resp = requests.get(url=url,headers=headers)
    total = jsonpath(resp.json(),'$.data.total')
    if int(total[0]) > 10:
        print('出现巨量，重写代码')

    items = jsonpath(resp.json(),'$.data.items')[0]
    for i in items:
        try:
            item['projectFormatsGuid'] = i['projectFormatsGuid']
            item['标题'] = i['name']
            item['区县'] = i['areaName']+i['districtName']
            item['标签'] = str(i['tags'])
            item['总价'] = i['totalPrice']
            item['建面'] = i['roomAreaMin'] + '-' + i['roomAreaMax']
            item['longitude'] = i['longitude']
            item['latitude'] = i['latitude']
            simple_info = 'https://apps1.xincheng.com/brokerService/rest/building/queryProjectMoreDetail?projectFormatsGuid={}'.format(item['projectFormatsGuid'])
            time.sleep(random.randint(10, 15) * 0.1 * 3)
            get_proBaseInfo(simple_info,headers,item)
        except:
            pass

def get_proBaseInfo(url,headers,item):
    try:
        resp = requests.get(url=url,headers=headers)
    except:
        print('wating....')
        time.sleep(20)
        resp = requests.get(url=url,headers=headers)
    item['_id'] = ObjectId()
    dictTitle_list = jsonpath(resp.json(),'$..dictTitle')
    dictValue_list = jsonpath(resp.json(),'$..dictValue')
    datas = dict(zip(dictTitle_list,dictValue_list))
    try:
        item['地址'] = datas['售卖地址']
        item['户型'] = datas['售卖户型']
        item['开盘时间'] = datas['最新开盘']
        item['装修'] = datas['装修标准']
        item['开发商'] = datas['开发商']
        item['容积率'] = datas['容积率']
        item['建筑面积'] = datas['小区建筑面积']
        item['绿化率'] = datas['绿化率']
        item['物业费'] = datas['物业费用']
        item['楼栋总数'] = datas['规划楼栋']
        item['总户数'] = datas['规划户数']
        print(item)
        Db.insert_one(item)
    except:
        pass


# get_cityMap(city_Map,headers)
statis_output('新城_全国_{}_房产信息.csv'.format(time.strftime("%Y-%m-%d", time.localtime())),
              ['code','城市','uuid', '标题','区县','标签','总价','建面','longitude','latitude','地址','户型','开盘时间','装修','开发商','容积率','建筑面积','绿化率','物业费','楼栋总数','总户数'], Db)
