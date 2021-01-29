import time
import os
import re
import requests
import json
import pandas as pd

from lxml import etree


# 获取小区面积
def get_community_area(url, title):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    }
    while True:
        try:
            res = requests.get(url=url, headers=headers, timeout=(2, 5))
            res.encoding = 'gbk'
            tree = etree.HTML(res.text)
            break
        except Exception as e:
            print('新房详情中...', e, url)
            time.sleep(2)
            continue
    item, data = [], {}

    # 销售信息
    sales_message = tree.xpath("//div[@class='main-item']/h3[contains(text(), '销售信息')]/../ul/li")
    for sales in sales_message:
        txt = re.sub('\s', '', sales.xpath('string(.)')).split('：')
        item.append(dict(zip(txt[0::2], txt[1::2])))

    # 小区规划
    Community_planning = tree.xpath('//ul[@class="clearfix list"]//li')
    for plan in Community_planning:
        txt = re.sub('\s', '', plan.xpath('string(.)')).split('：')
        item.append(dict(zip(txt[0::2], txt[1::2])))
    [data.update(i) for i in item]
    return data


# 楼盘详情页url
def get_detail_url(url, title, dataDict, data):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",

    }
    while True:
        try:
            res = requests.get(url=url, headers=headers, timeout=(2, 7))
            res.encoding = res.apparent_encoding
            tree = etree.HTML(res.text)
            break
        except Exception as e:
            print("get_detail_url error: ", e)
            continue

    # 楼盘详情url
    try:
        durl = tree.xpath('//*[@id="orginalNaviBox"]/a[contains(text(), "楼盘详情") or contains(text(), "详细信息")]/@href')[0]
        detail_url = "https:" + durl if 'http' not in durl else durl
        if 'ld.newhouse' in durl:
            print('出现: ld.newhouse', durl)
            Infodata = dict()
        else:
            Infodata = get_community_area(detail_url, title)
    except:
        print('get_detail_url函数中, 详情错误')
        Infodata = dict()
    dataDict['销售状态'] = Infodata.get('销售状态', '')
    dataDict['开盘时间'] = Infodata.get('开盘时间', '')
    dataDict['主力户型'] = Infodata.get('主力户型', '')
    dataDict['占地面积'] = Infodata.get('占地面积', '')
    dataDict['建筑面积'] = Infodata.get('建筑面积', '')
    dataDict['容积率'] = Infodata.get('容积率', '')
    dataDict['绿化率'] = Infodata.get('绿化率', '')
    dataDict['停车位'] = Infodata.get('停车位', '')
    dataDict['楼栋总数'] = Infodata.get('楼栋总数', '')
    dataDict['总户数'] = Infodata.get('总户数', '')
    dataDict['物业费'] = Infodata.get('物业费', '')
    dataDict['楼层状况'] = Infodata.get('楼层状况', '')

    print(dataDict)
    data.append(dataDict)


if __name__ == '__main__':
    title_url = 'https://yunshijiehe.fang.com/?ctm=1.jn.xf_search.lplist.5'
    title = '测试'
    data = get_detail_url(title_url, title)
    print(data)
