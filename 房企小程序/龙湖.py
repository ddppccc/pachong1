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
url = 'https://uapi.longfor.com/uhome-mzapi-prod/web/api/project/searchProjectList'

Db = pymongo.MongoClient(host='127.0.0.1', port=27017)['龙湖']['info']

headers = {
    'Host': 'uapi.longfor.com',
    'Connection': 'keep-alive',
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                  '/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv'
                  '/Windows WindowsWechat',
    'X-Gaia-Api-Key': '58e2d904-7f66-42a0-9bb4-e5134d7c1f43',
    'X-Tingyun-Id': '6So13D7TU2k;r=79436702',
    'apiversion': '2.1',
    'appversion': '1.0',
    'content-type': 'application/json;charset=UTF-8',
    'dxdeviceid': '5fab46a98BHtZIz6FUdhncBRWs4FO0tl02AooQN4',
    'openid': 'oVvTl5aWDrJ1sneqU24yBNc0-MY8',
    'refer': 'xcx',
    'user-source-channel': '{"mediaId":"","actionId":"source1","channelId":5,"customId":"","campaignId":"",'
                           '"serviceId":"0","serviceType":"5Z+O5biC6aaW6aG1","clickId":"","areaId":"","projectId":"",'
                           '"posterId":"","posterOwner":"","posterOwnerId":"","channelProjectId":""}',
    'x-authentication-id': '3a113db1-0ce2-4a6c-a4b2-c72532e058c4',
    'x-authentication-token': 'dc2e0a19838543563971e373b409b6eb48b4e4fa7e8b7771b5f467bed0be8069f7c908d9761fa6aa1c4a5a'
                              'f1ed441076400163a9b0d6fe3b6e7bb2085063637bdabfad230a82b010619301a531609a50b1c481fbd532'
                              'fa4b5dbe628481a386e08ac16d0e8384880876e849ad9c854ad637e80e89a87eb31a6b353673030a760fca'
                              '6c2a191569f0d8e829c173995a45497a81e30ada369344ec9bf0bd2491cadd69931455dc864d889bcc0f4a'
                              '1a86ce2450f1df5d635e7231c61a7ba5455216dd081f6ed03cada9e35c95393d32d00c55768f7770f27b10'
                              '10bf760db6f8a5dd42057c9e82eda24d93f30e91c5a76cfe52f34be3ab9c111411b7e83163c0de788b29df'
                              'b8fbff90398d904e014bff30a2815c604564c2bfcdd9215c252320efeb79',
    'Referer': 'https://servicewechat.com/wx2afa3f76abf7bd29/289/page-frame.html',
    'Accept-Encoding': 'gzip, deflate, br',
}


def statis_output(title, rowlist, database) -> object:
    csvfile = open('{}'.format(title), 'w+', newline='', encoding='utf-8')
    res_writer = csv.writer(csvfile, dialect='excel')
    res_writer.writerow(rowlist)
    for item in database.find():
        res_writer.writerow(list(item.values())[1:])


def get_totalContury(url):
    detil_url = 'https://uapi.longfor.com/uhome-mzapi-prod/web/api/project/selectNewProjectInfo'
    for x in range(1, 27):
        # time.sleep(random.randint(10, 15) * 0.1 * 3)
        try:
            resp = requests.post(url, headers=headers,
                                 json={"areaid": "0", "salesstatus": 0, "projectname": "", "areaIdArr": null,
                                       "districtidArr": null, "priceType": 1, "minprice": "", "maxprice": "",
                                       "housetype": null, "arearanges": null, "projectTypeList": null, "projectsort": 0,
                                       "pageFlag": 1, "pagesize": 10, "pageindex": x, "pageindexRecommend": 1,
                                       "pagesizeRecommend": 10, "purchaseLimit": "", "query": "", "newArearanges": null,
                                       "newProjectTypeList": null, "areaName": "全国", "pageType": 1})
        except:
            print('wating....')
            time.sleep(20)
            resp = requests.post(url, headers=headers,
                                 json={"areaid": "0", "salesstatus": 0, "projectname": "", "areaIdArr": null,
                                       "districtidArr": null, "priceType": 1, "minprice": "", "maxprice": "",
                                       "housetype": null, "arearanges": null, "projectTypeList": null, "projectsort": 0,
                                       "pageFlag": 1, "pagesize": 10, "pageindex": x, "pageindexRecommend": 1,
                                       "pagesizeRecommend": 10, "purchaseLimit": "", "query": "", "newArearanges": null,
                                       "newProjectTypeList": null, "areaName": "全国", "pageType": 1})
        data_list = jsonpath(resp.json(), '$..list')[0]
        # print(data_list)
        for i in data_list:
            item = {}
            item['_id'] = ObjectId()
            item['标题'] = i['ProjectName']
            item['城市'] = i['city']
            item['区县'] = i['district']
            item['浏览人数'] = i['lookers']
            item['latitude'] = i['sellHouseLatitude']
            item['longitude'] = i['sellHouseLongitude']
            item['标签'] = str(i['newTagNames'])
            item['单价'] = i['rPrice']
            item['ProjectID'] = i['ProjectID']
            item['areaID'] = i['areaID']

            get_detail(detil_url, {"projectid": item['ProjectID'], "pageindex": "1", "pagesize": "20",
                                           "userid": "3a113db1-0ce2-4a6c-a4b2-c72532e058c4",
                                           "landingstate": "26c2db3d-6e14-4518-a60e-799312bcd005", "type": "0",
                                           "matchpageindex": "1", "matchpagesize": "20", "qrCodeID": "",
                                           "sqFlag": 0},item)



def get_detail(url, json, item):
    deep_url = 'https://uapi.longfor.com/uhome-mzapi-prod/web/api/project/selectNewProjectMoreInfo'
    time.sleep(random.randint(10, 15) * 0.1 * 3)
    try:
        resp = requests.post(url=url, headers=headers, json=json)
    except:
        print('wating....')
        time.sleep(20)
        resp = requests.post(url=url, headers=headers, json=json)
    data_item = jsonpath(resp.json(),'$..projectTypeList')[0]

    decoration_list = []
    totalPrice_list = []
    dictName_list = []
    area_list = []
    for i in data_item:
        if i['decorationStandard']:
            decoration_list.append(i['decorationStandard'])
        if i['Price']:
            totalPrice_list.append(i['Price'])
        if i['dictName']:
            dictName_list.append(i['dictName'])

            area_list.append(i['minPropertyArea'] + '-' + i['maxPropertyArea'])
    item['开盘时间'] = i['openingTime']
    item['装修'] = str(decoration_list)
    item['分类'] = str(dictName_list)
    item['总价'] = str(totalPrice_list)
    item['建面'] = str(area_list)

    get_deep_detailInfo(deep_url,{"ispublish": 1, "projectid": item['ProjectID'], "pageindex": 1, "pagesize": 99},
                        item)


def get_deep_detailInfo(url, json, item):
    time.sleep(random.randint(10, 15) * 0.1 * 3)
    headers = {
        'Host': 'uapi.longfor.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                      '/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv'
                      '/Windows WindowsWechat',
        'X-Gaia-Api-Key': '58e2d904-7f66-42a0-9bb4-e5134d7c1f43',
        'X-Tingyun-Id': '6So13D7TU2k;r=79436702',
        'apiversion': '2.0',
        'appversion': '1.0',
        'content-type': 'application/json;charset=UTF-8',
        'dxdeviceid': '5fab46a98BHtZIz6FUdhncBRWs4FO0tl02AooQN4',
        'openid': 'oVvTl5aWDrJ1sneqU24yBNc0-MY8',
        'refer': 'xcx',
        'user-source-channel': '{"mediaId":"","actionId":"source1","channelId":5,"customId":"","campaignId":"",'
                               '"serviceId":"0","serviceType":"5Z+O5biC6aaW6aG1","clickId":"","areaId":"","projectId":"",'
                               '"posterId":"","posterOwner":"","posterOwnerId":"","channelProjectId":""}',
        'x-authentication-id': '3a113db1-0ce2-4a6c-a4b2-c72532e058c4',
        'x-authentication-token': 'dc2e0a19838543563971e373b409b6eb48b4e4fa7e8b7771b5f467bed0be8069f7c908d9761fa6aa1c4a5a'
                                  'f1ed441076400163a9b0d6fe3b6e7bb2085063637bdabfad230a82b010619301a531609a50b1c481fbd532'
                                  'fa4b5dbe628481a386e08ac16d0e8384880876e849ad9c854ad637e80e89a87eb31a6b353673030a760fca'
                                  '6c2a191569f0d8e829c173995a45497a81e30ada369344ec9bf0bd2491cadd69931455dc864d889bcc0f4a'
                                  '1a86ce2450f1df5d635e7231c61a7ba5455216dd081f6ed03cada9e35c95393d32d00c55768f7770f27b10'
                                  '10bf760db6f8a5dd42057c9e82eda24d93f30e91c5a76cfe52f34be3ab9c111411b7e83163c0de788b29df'
                                  'b8fbff90398d904e014bff30a2815c604564c2bfcdd9215c252320efeb79',
        'Referer': 'https://servicewechat.com/wx2afa3f76abf7bd29/289/page-frame.html',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    try:
        resp = requests.post(url=url, headers=headers, json=json)
    except:
        print('wating....')
        time.sleep(20)
        resp = requests.post(url=url, headers=headers, json=json)
    print(resp.text)
    item['物业费'] = jsonpath(resp.json(), '$..propertyMoney')[0]
    item['总价'] = jsonpath(resp.json(), '$..unitPrice')[0]
    item['容积率'] = jsonpath(resp.json(), '$..capaCity')[0]
    item['绿化率'] = jsonpath(resp.json(), '$..greening')[0]
    item['总户数'] = jsonpath(resp.json(), '$..houseHoldNum')[0]
    item['建筑面积'] = jsonpath(resp.json(), '$..area')[0]
    item['地址'] = jsonpath(resp.json(), '$..projectAddress')[0]
    print(item)
    Db.insert_one(item)


# get_totalContury(url=url)
statis_output('龙湖_全国_{}_房产信息.csv'.format(time.strftime("%Y-%m-%d", time.localtime())),
              ['标题', '城市', '区县', '浏览人数', 'latitude', 'longitude', '标签', '单价','ProjectID',
               'areaID', '开盘时间', '装修', '分类', '物业费', '建筑面积', '物业费', '容积率', '绿化率', '总户数', '建筑面积',
               '地址'], Db)
