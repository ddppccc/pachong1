import time
import jsonpath
import pymongo
import requests
from Base_info_spider import statis_output

info_data = pymongo.MongoClient(host='127.0.0.1', port=27017)['Beike']['info_new']
Beike_second = pymongo.MongoClient(host='127.0.0.1', port=27017)['Beike']['beike_second']
city_map = pymongo.MongoClient(host='127.0.0.1', port=27017)['Beike']['city_map']

pass_year = '2019' + '年'
this_year = '2020' + '年'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'cookie': 'lianjia_ssid=38c77e0b-d46b-402f-917e-174595d13f1e; lianjia_uuid=e204ed92-d42b-4a6a-8fbd-6ef869d3886a; _smt_uid=5f8804cd.25b2ced1; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221752b52c1b53b6-03d9ed69788878-5b123211-2073600-1752b52c1b665f%22%2C%22%24device_id%22%3A%221752b52c1b53b6-03d9ed69788878-5b123211-2073600-1752b52c1b665f%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; select_city=340100; crosSdkDT2019DeviceId=-xf4acz-b283ki-nnhg81z5q0tllkp-e9qmx2qla; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiZjgyY2EwYjIwOWNlMjAwODYwNjE5ZmRlOTM4ZWNlNGJiYzYyYmJiMWE1NjRhNTc0NGVhZWZkZTg1NTgwMjhlM2I0YmNmMzBiZDNhNTA1OWVhMThhNjcxNGM2YzQ3OTM5MTYzYzMzZDZhOGU0OWEzOTdiNjFjYjU0N2ZmMjQ2MjExYWM3OTU2Y2M2YWM0YTRlZDRkMzFhM2JhMzUxYmVmMTE5ZGVhNzYzNDE2ZGVjOGEzMjY2NWQ3YTE5MTA5MDdiOGExYzRlNjJmNDQ4OWZiZmYzZWMwNWZhOTIzYmQwZTIwMmIxY2VhYjJlMWMxOGYwM2JmYzViYjViYzhiYWJkMGRhYjc0MTBlZjc5NDg1NmQxMzIxZjljYmE5MTkxZjFjYTZmNjlhNzFlOTBjNTRkNjdmZmJjYjEzNmJlMzY2Mzc2NGExY2JjYmRmOWQ3MzE2MDVlMTk0Yzg4NWJjMDY3ZFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJlZWFjZWVmYVwifSIsInIiOiJodHRwczovL3d3dy5rZS5jb20vY2l0eS8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ=='
}

for info in info_data.find():
    city = info['tit']
    belong = info['belong']
    realm_name = city_map.find({'city': belong})
    for _ in realm_name:
        realm_name = _['url']
    region_id = info['region_id']
    region = 'district'
    url = 'https:{}/fangjia/priceTrend/?region={}&region_id={}&analysis=1'.format(realm_name, region, region_id)
    resp = requests.get(url=url, headers=headers)
    json_data = resp.json()
    if json_data:
        duration = jsonpath.jsonpath(json_data, '$..duration')  # 月份
        houseAmount = jsonpath.jsonpath(json_data, '$..houseAmount')  # 新增房源量
        showAmount = jsonpath.jsonpath(json_data, '$..showAmount')  # 带看次数
        duration, houseAmount, showAmount = duration[0], houseAmount[0], showAmount[0]
        duration_ex = [pass_year + i if duration.index(i) < duration.index('1月') else this_year + i for i in duration]
        print(duration_ex, houseAmount, showAmount)
        data = dict(zip(duration_ex, zip(houseAmount, showAmount)))
        for unit in data.keys():
            item = {}
            item['city'] = city
            item['duration'] = unit
            item['houseAmount'] = data[unit][0]
            item['showAmount'] = data[unit][1]
            item['belong'] = belong
            Beike_second.insert_one(item)
    else:
        region = 'city'
        url = 'https:{}/fangjia/priceTrend/?region={}&region_id={}&analysis=1'.format(realm_name, region, region_id)
        resp = requests.get(url=url, headers=headers)
        json_data = resp.json()
        if json_data:
            # 月份 新增房源量 带看次数
            duration = jsonpath.jsonpath(json_data, '$..duration')
            houseAmount = jsonpath.jsonpath(json_data, '$..houseAmount')
            showAmount = jsonpath.jsonpath(json_data, '$..showAmount')
            duration, houseAmount, showAmount = duration[0], houseAmount[0], showAmount[0]
            print(duration_ex, houseAmount, showAmount)
            duration_ex = [pass_year + i if duration.index(i) < duration.index('1月') else this_year + i for i in
                           duration]
            data = dict(zip(duration_ex, zip(houseAmount, showAmount)))
            for unit in data.keys():
                item = {}
                item['city'] = city
                item['duration'] = unit
                item['houseAmount'] = data[unit][0]
                item['showAmount'] = data[unit][1]
                item['belong'] = belong
                Beike_second.insert_one(item)
statis_output('贝壳二手房_全国_{}_贝壳二手房供需走势.csv'.format(time.strftime("%Y-%m-%d", time.localtime())),
              ['地区', '月份', '新增房源量', '带看次数', '从属'], Beike_second)
