import csv
import time

import pymongo
import requests
from jsonpath import jsonpath

Db = pymongo.MongoClient(host='127.0.0.1', port=27017)['祥生']['info']
page_IndexUrl = 'https://tt.leju.com/addons/ren_wechat/interface/mobile/page_index_new.php'
detail_url = 'https://tt.leju.com/addons/ren_wechat/interface/mobile/detail_new.php'
headers = {
    'Host': 'tt.leju.com',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
    'content-type': 'application/x-www-form-urlencoded',
    'Referer': 'https://servicewechat.com/wxbfcc312eb1827cff/7/page-frame.html',
    'Accept-Encoding': 'gzip, deflate, br',
}

data = {
    'city':'',
    'is_openid':'yes',
    'openid': 'oecue4i7PPe6B_o2Tbdw9wIPcR44',
    'brand': 'xiangsheng',
    'nickname':'ButterCat',
    'headimgurl':'https://thirdwx.qlogo.cn/mmopen/vi_32/ajNVdqHZLLDYicvFn7MQTrOkC1n7uMkXW4rXEXQGWlCgg8oAO3Q6KLia7vB3n9Kulic8cFayQ5DMyJUiaz5Djhicj5g/132',
    'gender':'1',
}

city_list = [
    ["nanchang", "江西"],
    ["shaoxing", "绍兴"],
    ["wuxi", "泰州"],
    ["nantong", "盐城"],
    ["chagnsha", "湖南"],
    ["shanghai", "衢州"],
    ["nanjing", "滁州"],
    ["suzhou", "苏州"],
    ["ningbo", "宁波"],
    ["hangzhou", "诸暨"],
    ["fuzhou", "福建"]
]

def statis_output(title, rowlist, database) -> object:
    csvfile = open('{}'.format(title), 'w+', newline='', encoding='utf-8')
    res_writer = csv.writer(csvfile, dialect='excel')
    res_writer.writerow(rowlist)
    for item in database.find():
        res_writer.writerow(list(item.values())[1:])

def get_page_Index(city, url, headers):
    data['city'] = city
    resp = requests.post(url=url, headers=headers, data=data)
    resp.encoding = 'utf-8'
    house_list = jsonpath(resp.json(),'$.house_list')[0]
    for detail in house_list:
        item = {}
        hid = detail['hid']
        site = detail['site']
        item['城市'] = city
        item['标题'] = detail['name']
        item['销售情况'] = detail['salestate']
        item['单价'] = detail['price_display']
        item['标签'] = detail['tags_id']
        item['浏览人数'] = detail['onlookers_num']
        item['longitude'] = detail['coordy2']
        item['latitude'] = detail['coordx2']
        get_detail(hid,city,site,detail_url,headers,item)


def get_detail(hid,city,site,detail_url,headers,item):
    data = {
        'hid':hid,
        'city':city,
        'site':site,
        'brand':'xiangsheng',
        'openid':'oecue4i7PPe6B_o2Tbdw9wIPcR44',
    }
    resp = requests.post(url=detail_url,headers=headers,data=data)
    resp.encoding = 'utf-8'
    house_info = jsonpath(resp.json(),'$.house')[0]
    item['容积率'] = house_info['plotratio']
    item['绿化率'] = house_info['greenratio']
    item['开盘时间'] = house_info['opentime_desc']
    item['户型'] = house_info['main_housetype']
    item['装修'] = house_info['fitment_standard']
    item['物业费'] = house_info['property_fee']
    item['地址'] = house_info['address']
    item['分类'] = house_info['hometype_name']
    print(item)
    Db.insert_one(item)
if __name__ == '__main__':
    for city in city_list:
        get_page_Index(city[0],page_IndexUrl, headers)
    statis_output('祥生_全国_{}_房产信息.csv'.format(time.strftime("%Y-%m-%d", time.localtime())),
                  ['城市','标题','销售情况','单价','标签','浏览人数','longitude','latitude','容积率','绿化率','开盘时间','户型','装修','物业费','地址','分类'], Db)
