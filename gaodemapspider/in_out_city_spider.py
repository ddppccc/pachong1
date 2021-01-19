# -*- coding: utf-8 -*-
import json
import time

import jsonpath
import requests
from logsitc import *
import pymongo
import xlsxwriter

# 连接数据库
in_city_info = pymongo.MongoClient(host='127.0.0.1', port=27017)['migrate_data']['city_migrate_in_data_test']
out_city_info = pymongo.MongoClient(host='127.0.0.1', port=27017)['migrate_data']['city_migrate_out_data_test']

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://trp.autonavi.com/migrate/index.do',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'cookie': '_uab_collina=159797962670973574646665; UM_distinctid=1740f02100412c-0060d7142d7eea-6701b35-144000-1740f021005beb; __session:0.7035764361253245:state=111; user_unique_id=a184b07b741f1e0501741f8dd73906a9; SESSION=79dbebec-2361-40ea-8bc3-4676325b292b; CNZZDATA1256662931=1103843308-1597977235-https%253A%252F%252Ftrp.autonavi.com%252F%7C1598319841; user_unique_id=a187b9ae741f1d360174237a1d1070bf'
}


def get_proxy():
    return requests.get("http://192.168.88.51:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://192.168.88.51:5010/delete/?proxy={}".format(proxy))


def getHtml(url):
    retry_count = 5
    proxy = get_proxy().get("proxy")
    proxies = {
        "http": "http://{}".format(proxy),
        "https": "https://{}".format(proxy)
    }
    if "!" in proxy:
        print('没有代理，等待2分钟')
        time.sleep(60 * 2)
    while retry_count > 0:
        try:
            html = requests.get(url, proxies=proxies, headers=headers)
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
    # 出错5次, 删除代理池中代理
    delete_proxy(proxy)
    print(retry_count)
    # getHtml(url)
    return None


#
def get_in_data(url):
    # response = getHtml(url)
    try:
        response = requests.get(url, headers=headers)
        time.sleep(2)

        while response is None:
            time.sleep(10)
            response = requests.get(url, headers=headers)
            # response = getHtml(url)
        data = response.json()
        return data
    except:
        # 数据出错，延长至10s获取一次内容
        time.sleep(10)
        return get_in_data(url)


def parse_in_data(data):
    in_city = jsonpath.jsonpath(data, '$..name')
    in_willIdx = jsonpath.jsonpath(data, '$..willIdx')
    in_realIdx = jsonpath.jsonpath(data, '$..realIdx')
    return in_city, in_willIdx, in_realIdx


def get_out_data(url):
    # response = getHtml(url)
    try:
        response = requests.get(url, headers=headers)
        time.sleep(2)
        while response is None:
            time.sleep(10)
            response = requests.get(url, headers=headers)
            # response = getHtml(url)
        data = response.json()

        return data
    except:
        time.sleep(10)
        return get_out_data(url)


def parse_out_data(data):
    out_city = jsonpath.jsonpath(data, '$..name')
    out_willIdx = jsonpath.jsonpath(data, '$..willIdx')
    out_realIdx = jsonpath.jsonpath(data, '$..realIdx')
    return out_city, out_willIdx, out_realIdx


for adcode in adcode_list:
    for dt in data_time_range:
        in_url = 'https://trp.autonavi.com/cityTravel/inAndOutCity.do?adcode={}&dt={}&willReal=WILL&inOut=IN&size=200'.format(
            adcode, dt)
        out_url = 'https://trp.autonavi.com/cityTravel/inAndOutCity.do?adcode={}&dt={}&willReal=WILL&inOut=OUT&size=200'.format(
            adcode, dt)
        in_data = get_in_data(in_url)
        out_data = get_out_data(out_url)
        in_city, in_willIdx, in_realIdx = parse_in_data(in_data)
        out_city, out_willIdx, out_realIdx = parse_out_data(out_data)
        print('迁入城市：', in_city, '\n', '迁出城市：', out_city, '\n', '迁入意愿指数:', in_willIdx, '\n', '迁出意愿指数', out_willIdx, '\n',
              '实际迁入指数', in_realIdx, '\n', '实际迁出指数', out_realIdx, '\n', '时间', dt)
        # print(in_city)
        if in_city is False or in_willIdx is False or in_realIdx is False:
            print('存在False')
            time.sleep(10)
            get_in_data(in_url)
        if out_city is False or out_willIdx is False or out_realIdx is False:
            print('存在False')
            time.sleep(10)
            get_out_data(out_url)
        while len(in_city) > 0:
            in_item = {}
            in_item['area'] = area_dict[adcode]
            in_item['city'] = in_city.pop(0)
            in_item['date_time'] = dt
            in_item['in_willIdx'] = in_willIdx.pop(0)
            in_item['in_realIdx'] = in_realIdx.pop(0)
            in_city_info.insert_one(in_item)
        # 迁出数据
        while len(out_city) > 0:
            out_item = {}
            out_item['area'] = area_dict[adcode]
            out_item['city'] = out_city.pop(0)
            out_item['in_willIdx'] = out_willIdx.pop(0)
            out_item['in_realIdx'] = out_realIdx.pop(0)
            out_item['date_time'] = dt
            out_city_info.insert_one(out_item)
