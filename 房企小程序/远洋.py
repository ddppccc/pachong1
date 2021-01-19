import csv
import random
import time
import urllib.parse
import pymongo
import requests
from jsonpath import jsonpath
from bson import ObjectId

Db = pymongo.MongoClient(host='127.0.0.1', port=27017)['远洋']['info']

headers = {
    'Host': 'etrading.sinooceangroup.com',
    'Connection': 'keep-alive',
    'Authorization': 'Bearer 8ee66b01c2753efe725c870fca5dbf8f',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
    'content-type': 'application/x-www-form-urlencoded',
    'Referer': 'https://servicewechat.com/wx389b61b4be61cf31/62/page-frame.html',
    'Accept-Encoding': 'gzip, deflate, br',
}

url = 'https://etrading.sinooceangroup.com/SWF/WeixinApi/city/index'

def statis_output(title, rowlist, database) -> object:
    csvfile = open('{}'.format(title), 'w+', newline='', encoding='utf-8')
    res_writer = csv.writer(csvfile, dialect='excel')
    res_writer.writerow(rowlist)
    for item in database.find():
        res_writer.writerow(list(item.values())[1:])


def getcityMap(url,headers):
    resp = requests.get(url,headers)
    cityList = jsonpath(resp.json(),'$.data.citys')
    for i in cityList[0]:
        cityMap = i['cityList']
        for i in cityMap:
            get_Projectsinfo(i['shortname'])
            time.sleep(random.randint(10, 15) * 0.1 * 3)


def get_Projectsinfo(cityName):
    data = {'cityName':cityName}
    data = urllib.parse.urlencode(data)
    url = 'https://etrading.sinooceangroup.com/SWF/WeixinApi/main/index?' + data
    resp = requests.get(url=url,headers=headers)
    projects_list = jsonpath(resp.json(),'$.data.Projects')[0]
    item = {}
    for i in projects_list:
        item['_id'] = ObjectId()
        item['code'] = i['Code']
        item['城市'] = i['ProjectBasicInfo']['City']
        item['标题'] = i['ProjectBasicInfo']['CaseName']
        item['销售情况'] = i['ProjectBasicInfo']['ProjectStatusDesc']
        house_list = i['HouseStyleDesc']
        item['户型'] = []
        for i in house_list:
            item['户型'].append(i)
        item['户型'] = str(item['户型']).replace('[','').replace(']','')
        get_Detailinfo(item)

def get_Detailinfo(item):
    url = 'https://etrading.sinooceangroup.com/SWF/WeixinApi/houses/detail?projectCode={}'.format(item['code'])
    resp = requests.get(url=url,headers=headers)
    detail_Info = jsonpath(resp.json(),'$.data.BasicInfo')[0]
    item['地址'] = detail_Info['ProjectAddress']
    item['开盘时间'] = detail_Info['OpenTime']
    item['latitude'] = detail_Info['Lat']
    item['longitude'] = detail_Info['Lng']
    item['标签'] = detail_Info['SellPoint']
    item['单价'] = detail_Info['AveragePrice']
    item['总价'] = detail_Info['TotalPrice']
    item['分类'] = detail_Info['PropertyTypeName']
    detail_Info = jsonpath(resp.json(),'$.data.DetailInfo')[0]
    item['总户数'] = detail_Info['PlanHouseNum']
    item['总建筑面积'] = detail_Info['ConstructionArea']
    item['绿化率'] = detail_Info['GreenRate']
    item['物业费'] = detail_Info['PropertyFee']
    item['容积率'] = detail_Info['VolumeRate']
    item['装修'] = detail_Info['DecorationNames']
    print(item)
    Db.insert_one(item)




# getcityMap(url,headers)
statis_output('远洋_全国_{}_房产信息.csv'.format(time.strftime("%Y-%m-%d", time.localtime())),
              ['code', '城市', '标题', '销售情况','户型','地址', '开盘时间', 'latitude', 'longitude','标签',
               '单价', '总价', '分类', '总户数', '总建筑面积', '绿化率', '物业费','容积率','装修'], Db)
