import csv
import json
import random
import re
import sys
import io
import time

from bson import ObjectId
import requests
import pymongo
from jsonpath import jsonpath

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='ISO 8859-1')
null = None
Db = pymongo.MongoClient(host='127.0.0.1', port=27017)['富力地产']['info']

# url = 'https://tt.leju.com/addons/ren_wechat/interface/mobile/code.php'

headers = {

    'Host': 'tt.leju.com',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
    'content-type': 'application/x-www-form-urlencoded',
    'Referer': 'https://servicewechat.com/wx0ff38768679e13ff/23/page-frame.html',
    'Accept-Encoding': 'gzip, deflate, br',

}

city_list = [
    ["gz", "广州"],
    ["sg", "韶关"],
    ["mz", "梅州"],
    ["hb", "河源"],
    ["huizhou", "惠州"],
    ["fs", "佛山"],
    ["zhuhai", "珠海"],
    ["jl", "吉隆"],
    ["sw", "汕尾"],
    ["cq", "重庆"],
    ["sc", "成都"],
    ["zy", "资阳"],
    ["ls", "乐山"],
    ["ms", "眉山"],
    ["guizhou", "贵阳"],
    ["fj", "福州"],
    ["pt", "莆田"],
    ["sm", "三明"],
    ["lo", "龙岩"],
    ["xiamen", "厦门"],
    ["cs", "长沙"],
    ["wh", "鄂州"],
    ["nc", "南昌"],
    ["jj", "九江"],
    ["han", "海南"],
    ["tangshan", "唐山"],
    ["qhd", "秦皇岛"],
    ["sjz", "石家庄"],
    ["tj", "天津"],
    ["yt", "烟台"],
    ["qd", "青岛"],
    ["dy", "东营"],
    ["cp", "邹平"],
    ["eh", "菏泽"],
    ["zp", "淄博"],
    ["sy", "沈阳"],
    ["anshan", "鞍山"],
    ["tl", "铁岭"],
    ["heb", "哈尔滨"],
    ["sx", "西安"],
    ["ty", "太原"],
    ["dt", "大同"],
    ["bt", "包头"],
    ["xj", "乌鲁木齐"],
    ["hhht", "呼和浩特"],
    ["sh", "上海"],
    ["wx", "无锡"],
    ["nt", "南通"],
    ["nj", "滁州"],
    ["fy", "阜阳"],
    ["hbs", "淮北"],
    ["wz", "温州"],
    ["hangzhou", "杭州"],
    ["nb", "宁波"],
    ["wuhan", "武汉"],
    ["jinan", "济南"],
    ["nanj", "南京"],
    ["hefei", "合肥"]
]

def statis_output(title, rowlist, database) -> object:
    csvfile = open('{}'.format(title), 'w+', newline='', encoding='utf-8')
    res_writer = csv.writer(csvfile, dialect='excel')
    res_writer.writerow(rowlist)
    for item in database.find():
        res_writer.writerow(list(item.values())[1:])


def get_cityList(city_list):

    for _ in city_list:
        city = _[0]
        get_pageindex(city)


def get_pageindex(city):
    url = 'https://tt.leju.com/addons/ren_wechat/interface/mobile/page_index.php'
    # jsondata = {
    #     'brand': 'fuli',
    #     'city': city,
    #     'is_openid': 'yes',
    #     'openid': 'ohp235bP25y9ltnYEMJlZ3HWoZpk',
    #     'nickname': 'ButterCat',
    #     'headimgurl': 'https://thirdwx.qlogo.cn/mmopen/vi_32/ajNVdqHZLLDondgpDnm3vIfnJjNEic6WDd2JMPfKAIaxHezrMs7Swx5bgjQfhS1hCcW9sut65T6HrBDZXv9s5og/132',
    #     'gender': '1',
    # }
    jsondata = {
        'brand': 'fuli',
        'city': city,
        'is_openid': '',
        'openid': '',
        'nickname': '',
        'headimgurl': '',
        'gender': '',
    }
    resp = requests.post(url=url,headers=headers,data=jsondata)
    resp = resp.text.encode('raw_unicode_escape').decode()
    resp = eval(resp)
    house_list = resp['house_list']
    for info in house_list:
        item = {}
        for i in city_list:
            if info['site'] == i[0]:
                item['城市'] = i[1]
        item['标题'] = info['name']
        item['状态'] = info['salestate']
        item['地址'] = info['address']
        item['latitude'] = info['coordy2']
        item['longitude'] = info['coordx2']
        item['单价'] = info['price_display']
        item['标签'] = info['tags_id']
        site = info['site']
        hid = info['hid']
        # print(item)
        get_detail(hid,site,item)



def get_detail(hid,site,item):
    url = 'https://tt.leju.com/addons/ren_wechat/interface/mobile/detail_new.php'
    data = {
        'hid' : hid,
        'city' : site,
        'site' : site,
        'brand' : 'fuli',
        'openid' : 'ohp235bP25y9ltnYEMJlZ3HWoZpk',
    }
    resp = requests.post(url=url,headers=headers,data=data)
    resp = resp.text.encode('raw_unicode_escape').decode()
    resp = eval(resp)
    item['开盘时间'] = resp['house']['opentime_desc']
    item['容积率'] = resp['house']['plotratio']
    item['绿化率'] = resp['house']['greenratio']
    item['物业费'] = resp['house']['property_fee']
    try:
        zhulihuxing = resp['zhulihuxing'][0]['list']
        item['户型'] = []
        for i in zhulihuxing:
            item['户型'].append(i['rooms']+i['area'])
    except:
        item['户型'] = ''
    item['浏览人数'] = resp['onlookers_num']
    print(item)
    Db.insert_one(item)





# get_cityList(city_list)
statis_output('富力地产_全国_{}_房产信息.csv'.format(time.strftime("%Y-%m-%d", time.localtime())),
              ['城市', '标题','状态','地址','latitude','longitude','单价','标签','开盘时间','容积率','绿化率','物业化','户型','浏览人数'], Db)
