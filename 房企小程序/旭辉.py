# -*- coding:utf-8 -*-
import csv
import random
import sys
import io
import time

import requests
import pymongo
from jsonpath import jsonpath

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
null = None
Db = pymongo.MongoClient(host='127.0.0.1', port=27017)['旭辉']['info']

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
    'content-type':	'application/json',
    'openid':'o--0F5q_qzBrPyMGL4k3CjqQzSOo',
    'referer':'https://servicewechat.com/wxe4bf124e97c87ebd/78/page-frame.html',
    'accept-encoding':	'gzip, deflate, br',
}

url = 'https://scrm-api.cifi.com.cn/broker/broker/getCitys?brokerAccount=16601716505'


def statis_output(title, rowlist, database) -> object:
    csvfile = open('{}'.format(title), 'w+', newline='', encoding='utf-8')
    res_writer = csv.writer(csvfile, dialect='excel')
    res_writer.writerow(rowlist)
    for item in database.find():
        res_writer.writerow(list(item.values())[1:])


def getcityMap(url,headers):
    resp = requests.get(url,headers)
    cityMap = jsonpath(resp.json(),'$..allCity')[0]
    for i in cityMap:
        get_buildBooklist('https://scrm-api.cifi.com.cn/broker/broker/getBuildBookList',headers,{"cityName":i['CityName'],"buildBookName":"","pageNum":1,"pageSize":99})
        time.sleep(random.randint(10, 15) * 0.1 * 3)

def get_buildBooklist(url,headers,json):
    resp = requests.post(url,headers=headers,json=json)
    for info in jsonpath(resp.json(),'$..list')[0]:
        item = {}
        item['_id'] = info['id']
        id_list = []
        for i in Db.find():
            id_list.append(i['_id'])
        if item['_id'] in id_list:
            continue
        item['projectID'] = info['projectID']
        item['城市'] = info['cityName']
        item['标题'] = info['projectName']
        item['标签'] = info['buildLabel']
        item['地址'] = info['address']
        item['单价'] = info['unitPrice']
        item['建筑面积'] = info['buildSapce']
        item['浏览人数'] = info['weiguanTotal']
        data = {
            'buildBookId': item['_id'],
            'projectId': item['projectID'],
        }
        print(data)
        get_deepdetailbuildBook('https://scrm-api.cifi.com.cn/broker/broker/getBuildBookDetail',headers,data,item)
        time.sleep(random.randint(10, 15) * 0.1 * 3)

def get_deepdetailbuildBook(url,headers,data,item):
    resp = requests.get(url=url,headers=headers,params=data)
    data = jsonpath(resp.json(),'$.data')[0]
    item['装修'] = data['buildInfo']['DecorationLevel']
    item['容积率'] = data['buildInfo']['PlotRatio']
    item['绿化率'] = data['buildInfo']['GreenRate']
    try:
        item['开盘时间'] = time.strftime('%Y-%m-%d',time.localtime(int(str(data['buildInfo']['OpenTime'])[:-3])))
    except:
        item['开盘时间'] = None
    item['物业费'] = data['buildInfo']['PropertyFee']
    item['latitude'] = data['buildInfo']['Latitude']
    item['longitude'] = data['buildInfo']['Longitude']
    item['户型'] = []
    item['建面'] = []
    for single in data['buildhouseType']:
        item['户型'].append(single['HouseType'])
        item['建面'].append(single['HouseArea'])
    item['户型'] = str(item['户型']).replace('[','').replace(']','')
    item['建面'] = str(item['建面']).replace('[','').replace(']','')
    Db.insert_one(item)


# getcityMap(url,headers)
statis_output('旭辉_全国_{}_房产信息.csv'.format(time.strftime("%Y-%m-%d", time.localtime())),
              ['Project_Id', '城市', '标题', '标签','地址','单价', '建筑面积', '浏览人数', '装修','容积率',
               '绿化率', '开盘时间', '物业费', 'latitude', 'longitude', '户型', '建面'], Db)
