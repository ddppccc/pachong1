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

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
null = None
Db = pymongo.MongoClient(host='127.0.0.1', port=27017)['华润']['info']
headers = {
    'Host': 'imapi.ideamake.cn',
    'Connection': 'keep-alive',
    'IM-TOKEN': 'ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6STFOaUo5LmV5SjFibWx2Ymtsa0lqb2lJaXdpY0hKdmFtVmpkRU52WkdVaU9pSm9jbXAwTVRreElpd2liM0JsYmtsa0lqb2liemxrZFRRMVpIYzJXREZqTW5sQ2NYSkpNVk0zUkZWU1oxWk5SU0lzSW1Gd2NFbGtJam9pZDNnNU5EaGxaams0TlRobU1EUm1ObVU1SWl3aWFYTlZjMlZ5SWpvd0xDSmxlSEFpT2pFMk1EWXlPVEEwTVRZc0luVjFhV1FpT2lJaUxDSm5jbTkxY0VOdlpHVWlPaUpvY21wMEluMC5tU2Raa3NQUVpfcElxbm5KNjR5dDg3ZTRCaTExcDAxeHBFWVZvbGJwY1Vj',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
    'appId': 'wx948ef9858f04f6e9',
    'content-type': 'application/x-www-form-urlencoded',
    'Referer': 'https://servicewechat.com/wx948ef9858f04f6e9/27/page-frame.html',
    'Accept-Encoding': 'gzip, deflate, br',
}


def statis_output(title, rowlist, database) -> object:
    csvfile = open('{}'.format(title), 'w+', newline='', encoding='utf-8')
    res_writer = csv.writer(csvfile, dialect='excel')
    res_writer.writerow(rowlist)
    for item in database.find():
        res_writer.writerow(list(item.values())[1:])


def total_pageInfo():
    for i in range(1,30):
        time.sleep(random.randint(10, 15) * 0.1 * 3)
        resp = requests.get(url='https://imapi.ideamake.cn/exhibition-huarun/project/v1?isPrecise=1&page={}'.format(i),headers=headers)
        data_list = jsonpath(resp.json(),'$..list')[0]
        if data_list is None:
            print('wating。。。')
            time.sleep(20)
            resp = requests.get(
                url='https://imapi.ideamake.cn/exhibition-huarun/project/v1?isPrecise=1&page={}'.format(i),
                headers=headers)
            data_list = jsonpath(resp.json(), '$..list')[0]
        for info in data_list:
            item = {}
            item['_id'] = ObjectId()
            item['标题'] = info['projectName']
            item['标签'] = str(info['tags'])
            item['浏览人数'] = info['lookingNum']
            item['单价'] = info['averagePrice']
            item['projectCode'] = info['projectCode']
            try:
                item['latitude'] = info['latitudeAndLongitude'].split(',')[0]
                item['longitude'] = info['latitudeAndLongitude'].split(',')[1]
            except:
                item['latitude'] = None
                item['longitude'] = None
            item['地址'] = info['detailAddress']
            get_detailInfo(url='https://imapi.ideamake.cn/exhibition-huarun/project/detail/{}'.format(item['projectCode']),item=item)


def get_detailInfo(url,item):
    time.sleep(random.randint(10, 15) * 0.1 * 3)
    resp = requests.get(url=url,headers=headers)

    data = jsonpath(resp.json(),'$.data')[0]
    if data is None:
        print('wating。。。')
        time.sleep(20)
        resp = requests.get(url=url, headers=headers)
        data = jsonpath(resp.json(), '$.data')[0]
        if data is None:
            return
    try:
        item['开盘时间'] = data['basicInfo']['startSaleTime']
    except:
        item['开盘时间'] = None
    try:
        item['建面'] = data['saleInfo'][3]['value']
    except:
        item['建面'] = None
    try:
        item['户型'] = data['basicInfo']['mainHouse']
    except:
        item['户型'] = None
    try:
        item['建筑面积'] = data['basicInfo']['buildArea']
    except:
        item['建筑面积'] = None
    try:
        item['城市'] = data['basicInfo']['area']['city']['name']
    except:
        item['城市'] = None
    try:
        item['区县'] = data['basicInfo']['area']['district']['name']
    except:
        item['区县'] = None
    try:
        item['销售情况'] = data['saleInfo'][0]['value']
    except:
        item['销售情况'] = None
    try:
        item['绿化率'] = data['overviewInfo'][2]['value']
    except:
        item['绿化率'] = None
    try:
        item['容积率'] = data['overviewInfo'][3]['value']
    except:
        item['容积率'] = None
    try:
        item['物业费'] = data['overviewInfo'][6]['value']
    except:
        item['物业费'] = None
    print(item)
    Db.insert_one(item)

total_pageInfo()
statis_output('华润_全国_{}_房产信息.csv'.format(time.strftime("%Y-%m-%d", time.localtime())),
              ['标题', '标签', '浏览人数', '单价','projectCode','latitude', 'longitude', '地址', '开盘时间','建面',
               '户型', '建筑面积', '城市', '区县', '销售情况', '绿化率', '容积率', '物业费'], Db)
