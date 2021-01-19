import datetime
import json
import os
import time
import requests
import pandas as pd
import numpy as np

from lxml import etree


def get_proxy():
    # return requests.get("http://192.168.88.51:5010/get/").json().get('proxy')
    return requests.get("http://127.0.0.1:5010/get/").json().get('proxy')


def delete_proxy(proxy):
    # html = requests.get("http://192.168.88.51:5010/delete/?proxy={}".format(proxy))
    html = requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
    return html.text


# 生成城市映射
def get_city_map():
    url = "http://piaofang.maoyan.com/citypage"
    params = {'t': 10}
    headers = {"Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Cookie": "_lxsdk_cuid=16cf51faf76c8-0d37207e0600ff-e343166-144000-16cf51faf77c8; _lxsdk=9DBCACD0CE0F11E9899D6B628470FE8D290909417DEB4377B74FF7A32839FC64; __mta=142506893.1567490207554.1567490261983.1567490263283.6; isid=E2536D19061DB1B0574DF5B232E883CE; token=9d-SQ-9WhEi_4vDSuMeQo_irdY4AAAAA-QgAAKxq6aqZD4_d0wH6_wMT_Yfc45KlzXtxynyc8aJsiEmy1Gz1cDZQYHfUOW1Rq81raw; __mta=142506893.1567490207554.1567490263283.1567490442613.7; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=16cf5b26ed1-0ec-8d-ca3%7C%7C71",
    "Host": "piaofang.maoyan.com",
    "Pragma": "no-cache",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://piaofang.maoyan.com/company/invest",
    "Token": "9d-SQ-9WhEi_4vDSuMeQo_irdY4AAAAA-QgAAKxq6aqZD4_d0wH6_wMT_Yfc45KlzXtxynyc8aJsiEmy1Gz1cDZQYHfUOW1Rq81raw",
    "Uid": "acd6daadb0e492422e8791617551c0a8b62d86d4",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    }

    res = requests.get(url, params=params, headers=headers)
    tree = etree.HTML(res.text)

    city_code = tree.xpath("//div[@class='abc']/ul/li/a/@data-cityid")
    city_name = tree.xpath("//div[@class='abc']/ul/li/a/text()")
    city_map = dict(zip(city_code,city_name))
    with open("city_map.json", 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(city_map, ensure_ascii=False))


# 生成时间序列
def get_data_range(start):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    date_list = pd.date_range(start, date)
    date_list= [str(date).split(" ")[0] for date in date_list]
    return date_list


# 城市映射表
with open("city_map.json", 'r', encoding='utf-8') as fp:
    city_codes = json.load(fp)


if __name__ == '__main__':

    # 生成城市映射表
    # get_city_map()

    # 生成时间序列
    data_list = get_data_range()
    print(data_list)











