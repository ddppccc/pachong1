import json
import random
import re
import time
import uuid
from urllib import parse

import pandas as pd
import pymongo
import requests

from lxml import etree
from concurrent.futures.thread import ThreadPoolExecutor
from sqlalchemy import create_engine
from requests.adapters import HTTPAdapter

MONGODB_CONFIG = {
    "host": "8.135.119.198",
    "port": "27017",
    "user": "hladmin",
    "password": parse.quote("Hlxkd3,dk3*3@"),
    "db": "dianping",
    "collections": "dianping_collections",
}

# 建立连接
info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['安居客商铺']['西安_数据_202109']

url = 'https://xa.sydc.anjuke.com/sp-shou/'
header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    # cookie: sessid=33763AAB-F7EC-48E0-AA55-E35252BD65D2; aQQ_ajkguid=5EE7F0EB-DF6B-4B2B-80A9-50401C396C6A; id58=e87rkGBtTqZF51K+EqHJAg==; 58tj_uuid=b20c504d-d269-4c78-8c25-f4c099dd68af; _ga=GA1.2.22727802.1617776650; als=0; isp=true; seo_source_type=0; cmctid=523; ajk-appVersion=; twe=2; new_uv=71; obtain_by=1; xxzl_cid=2b465dc24cfa41f998e0aeaae8556857; xzuid=01e24b14-a4a2-47a0-b2ae-3f09df4dfbc2; lps=https%3A%2F%2Fxa.sydc.anjuke.com%2Fsp-shou%2F%7Cnull; ctid=31; fzq_h=5cd00eae5327d396d1f9c3426dd042cd_1631513630783_6805ea4ec459403daf0138c3fe1a74e7_241886715; wmda_uuid=98472b7f7076ccf46af9012a32b137d8; wmda_new_uuid=1; wmda_session_id_6289197098934=1631513630614-ee9717d0-6739-2dae; wmda_visited_projects=%3B6289197098934; __xsptplus8=8.7.1631513630.1631513807.18%234%7C%7C%7C%7C%7C%23%23JumRHN0Ctf_H4H0wUu-0BLDvMHdHRtQ3%23; JSESSIONID=5E8E91503912A5012085A4EB3A0885FF; fzq_js_anjuke_business_fang_pc=7b513e7b4b810926a6d374c5d3820bda_1631514008455_25; __xsptplusUT_8=1
    'referer': 'https://xa.sydc.anjuke.com/sp-shou/xagx-p7/?listFilterCount=73',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}


# response = requests.get(url, headers=header)
# text = response.text
# print(text)


def get_proxy():
    while True:
        try:
            return requests.get('http://1.116.204.248:5000/proxy').text
        except:
            print('暂无ip，等待20秒')
            time.sleep(20)


def get_html(url):
    s = 0
    while True:
        try:
            proxy = get_proxy()
            proxies = {"https": proxy}
            response = requests.get(url, headers=header, proxies=proxies, timeout=(5, 10))
            encod = response.apparent_encoding
            if encod.upper() in ['GB2312', 'WINDOWS-1254']:
                encod = 'gbk'
            response.encoding = encod
            if '人机认证' in response.text:
                continue
            html = etree.HTML(response.text)
            if '登录' in ''.join(html.xpath('//head/title/text()')):
                continue
            if '访问验证-安居客' in ''.join(html.xpath('//head/title/text()')):
                continue
            if "访问过于频繁" in "".join(html.xpath("//h2[@class='item']/text()")):
                continue
            if '点击去完成' in "".join(html.xpath('//div[@class="verify-button"]//text()')):
                continue

            if response.status_code in [403]:
                continue
            if '请输入验证码' in ''.join(html.xpath('//head/title/text()')):
                continue
            return html
            # print(''.join(html.xpath('//head/title/text()')))

        except Exception as e:
            s += 1

            print('get_html错误', e)
            continue


# # html, proxieslist = get_html(url, [])
# response = requests.get(url, headers=header)
# encod = response.apparent_encoding
# html = etree.HTML(response.text)
# lis = html.xpath('//div[@class="list-item"]/a')
# for li in lis:
#     item = {}
#     item['title'] = ''.join(li.xpath('./div[@class="item-info"]/div[@class="item-title"]/span/text()'))
#     lists = ''.join(li.xpath('./div[@class="item-info"]/p[1]//text()')).replace(' ', '').replace('\n', '').split('|')
#     item['地址'] = lists[0]
#     item['状态'] = lists[1]
#     item['类型'] = ''.join(li.xpath('./div[@class="item-info"]/p[2]/span[@class="mr5"]/text()'))
#     item['楼层'] = ''.join(li.xpath('./div[@class="item-info"]/p[2]/span/text()')).replace(item['类型'], '')
#     item['标签'] = '|'.join(li.xpath('./div[@class="item-info"]/p[@class="item-tag"]//text()')).replace(' ', '').replace('\n', '').replace('||', '|')
#     item['建筑面积'] = ''.join(li.xpath('./div[@class="item-area"]/p/span/text()'))
#     item['总价'] = ''.join(li.xpath('./div[@class="item-price"]/div[@class="price-monthly"]/span/text()'))
#     item['单价'] = ''.join(li.xpath('./div[@class="item-price"]/div[@class="price-daily"]/span/text()')).replace('单价', '')
#     # item['title'] = ''.join(li.xpath('./div[@class="item-title"]/span/text()'))
#     # item['title'] = ''.join(li.xpath('./div[@class="item-title"]/span/text()'))
#
#     print(item)
def get_zb(url, item):
    # text = requests.get(url, headers=headers, proxies=proxies, timeout=(5, 10)).text
    tree = get_html(url)
    var = ''.join(tree.xpath('//head/script[4]/text()'))
    # var中包含了百度的坐标，没有高德的坐标
    # item['lat'] = re.findall("lat: (\d+\.\d+),", var)[0]
    # item['lng'] = re.findall("lng: (\d+\.\d+),", var)[0]
    id = re.findall("loupanID: '(\d+)',", var)[0]
    if id == '0':
        item['坐标'] = {}
        return item
    item['坐标'] = get_zb1(id)
    return item


def get_zb1(id):
    headers = {
        'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        # 'cookie': 'aQQ_ajkguid=8ee69264-9310-4805-a310-14b4e7d76565; sessid=9a03123f-787e-4cba-98fd-0fcea10ec525; lps=https%3A%2F%2Fxa.sydc.anjuke.com%2Fsp-shou%2F%7Cnull; ctid=31; fzq_h=eab1d9afc53bb70398c1a930c2a318a8_1632372362723_ebc3cdf0b4654a208b6b4ab7ffd629e4_241886870; id58=CpQBZWFMBouP78WIDfweAg==; id58=CocIQ2FMBourHz7JD2X7Ag==; wmda_uuid=7133274a4a343bf78385bc5078fa35b3; wmda_new_uuid=1; wmda_visited_projects=%3B6289197098934; wmda_session_id_6289197098934=1632374889571-d705cf0d-bd49-bf9d; __xsptplus8=8.2.1632374891.1632374891.1%234%7C%7C%7C%7C%7C%23%236ebt6EmfjiX6x-sefUSKLJ_dnOnAZYv8%23; JSESSIONID=4381CF5F67A7489A3AC612B96EB79021; fzq_js_anjuke_business_fang_pc=eb3be957934049403d495fe5b1c3400e_1632375337593_23',
        'referer': 'https://xa.sydc.anjuke.com/sp-shou/5945006479/?legoHuiDu=1&legoAdClickUrl=aHR0cHM6Ly9sZWdvLWNsaWNrLmFuanVrZS5jb20vanVtcD90YXJnZXQ9cFp3WTBabmxzenRkcmFPV1V2WUt1YVkxUDFtdnJBUmJ1aVkzcnlFM3NId2hQMUVWcnluenJpWVFuMS1iUDFQaG5XdWJuajlLUEhFUVAxMDNuSERrcmpOZHJIREtUSGNRUEg5M3JIVFlQam1ZbldiUXJqMEtuSG1MbmpUS25IbUxualRLbmlrUVBFRFlyam5LbkhtMW5XbkxuV252blcwelBURFFUWHlBaFh5Vi1TcC1mYTQtLW1VR2JlQ1ZPbVhsT2xYeE9tWGxPdWk4T21CZ2wyQUNscEFkVEhES25FREtzSERLVEhEWW4xYmRuSG52ckhiMVAxOXpQMUUxbmpFS1A5N2ttZ0Y2VWduem5qbmxuQmtLbkVEelBIRVFtdm1rbXpkNm5obWtzSHdickhjVm1oTjFQYVlkbWhQV3Jqd0J1am1RUEFuS25IRTFySE5RbjEwa25IVDNySE5kbmpuMVA5RFFQam5PUEhEMVAxVGtySGNRUDE5em5XMHpURURLVEVES3NFREtURURLbkhFOG5IVHZzV2MxbmEzUVBIVEtzSERLblRES25pa1FQRTdleEVEUW5qVDFQa0RRbmpUem5XOXZUeXVXUDFOem1oRXpzSE5rdXljVlBqRUxQYWQ2UFc5THN5TnZQaHdockhiTG55Tkxua0RLUFRES1RIVEtQajkxc2pOT25XbV9uMW5ZbkhjS25FNzhJeVFfVEg5elAxbnZtSERMbldUWW52d0JuV0U%3D&houseid=2158890446429187&pt=2&zhidingLegoHuiDu=0&legoTid=fc752bd2-50eb-4474-a687-e66df9971e73&uniqid=9c6479dda6e942f7b87264a61f515066&gpos=1&',
        'sec-ch-ua': '"Microsoft Edge";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52',
        'x-requested-with': 'XMLHttpRequest',
    }
    while True:
        try:
            proxy = get_proxy()
            proxies = {"https": proxy}
            return requests.get('https://xa.sydc.anjuke.com/shangban/loupan/lhbg/detail/' + id, headers=headers,
                                proxies=proxies,
                                timeout=(5, 10)).json()['data']['gisInfo']
        except Exception as e:
            print(e)
            continue


def get_data(url):
    print('当前url:', url)
    html = get_html(url)
    lis = html.xpath('//div[@class="list-item"]/a')
    for li in lis:
        item = {}
        item['url'] = ''.join(re.findall('(https://xa.sydc.anjuke.com/sp-shou/\d+/)', ''.join(li.xpath('./@href'))))
        if info_base.count({'url': item['url']}):
            print('当前商铺已爬取')
            continue
        item = get_zb(item['url'], item)
        item['title'] = ''.join(li.xpath('./div[@class="item-info"]/div[@class="item-title"]/span/text()'))
        lists = ''.join(li.xpath('./div[@class="item-info"]/p[1]//text()')).replace(' ', '').replace('\n', '').split(
            '|')
        item['地址'] = lists[0]
        try:
            item['状态'] = lists[1]
        except:
            item['状态'] = ''
        item['类型'] = ''.join(li.xpath('./div[@class="item-info"]/p[2]/span[@class="mr5"]/text()'))
        item['楼层'] = ''.join(li.xpath('./div[@class="item-info"]/p[2]/span/text()')).replace(item['类型'], '')
        item['标签'] = '|'.join(li.xpath('./div[@class="item-info"]/p[@class="item-tag"]//text()')).replace(' ',
                                                                                                          '').replace(
            '\n', '').replace('||', '|')
        item['建筑面积'] = ''.join(li.xpath('./div[@class="item-area"]/p/span/text()'))
        item['总价'] = ''.join(li.xpath('./div[@class="item-price"]/div[@class="price-monthly"]/span/text()'))
        item['单价'] = ''.join(li.xpath('./div[@class="item-price"]/div[@class="price-daily"]/span/text()')).replace('单价',
                                                                                                                   '')
        print(item)
        info_base.insert_one(item)

    # next_url = ''.join(html.xpath('//a[@class="aNxt"]/@href'))
    # if next_url == '':
    #     return
    # get_data(next_url)


if __name__ == '__main__':
    # info_base.delete_many({})
    url = 'https://xa.sydc.anjuke.com/sp-shou/'
    pool = ThreadPoolExecutor()
    l = []
    for pg in range(0, 85):
        url1 = 'https://xa.sydc.anjuke.com/sp-shou/p%s/' % str(pg)
        l.append(pool.submit(get_data, url1))
    [obj.result() for obj in l]
