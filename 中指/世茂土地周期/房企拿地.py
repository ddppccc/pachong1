#coding:utf-8
import os
import random
import time
import datetime
import json
import urllib.parse

import arrow
import pandas as pd
import requests

from config import cookie


class Urlchuli():

    def __init__(self, can, mazhi='utf-8'):
        self.can = can
        self.mazhi = mazhi

    def url_bm(self):
        """url_bm() 将传入的中文实参转为Urlencode编码"""
        quma = str(self.can).encode(self.mazhi)
        bianma = urllib.parse.quote(quma)
        return bianma

    def url_jm(self):
        """url_jm() 将传入的url进行解码成中文"""
        quma = str(self.can)
        jiema = urllib.parse.unquote(quma, self.mazhi)
        return jiema


def saveData(df, name):
    path = 'data/房企拿地/'
    os.path.exists(path) or os.makedirs(path)
    fileName = os.path.join(path, "%s.xlsx" % name)
    # 选择需要的字段
    df = df[["年","月","周","房企","地块名称","城市","编号","受让单位","规划用途","占地面积(万㎡)","规划建筑面积(万㎡)","总成交金额(亿元)","平均楼面价(元/㎡)","平均溢价率(%)","土地权益(%)","权益金额(亿元)","权益规划建筑面积(万㎡)","拿地时间","城市能级","房企排名"]]
    try:
        df.to_excel(fileName, index=False,)
    except:
        print('保存失败')


# 获取每个公司的城市分布
def get_company_city_distribution(company, companyID):
    url = 'https://creis.fang.com/enterprise/Dictionaries/GetCitysByCompanyID'
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": cookie,
        "origin": "https://creis.fang.com",
        "pragma": "no-cache",
        # "referer": "https://creis.fang.com/enterprise/Detail/EnterpriseParcelList?sCompanyID=7cbea25f-26dc-47b6-b8c8-d58dd681b6d2",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",

    }
    data = {
        "sCompanyID": companyID,
        "type": 1
    }
    params = { 'rd':4097.720646026488,}

    # print(data)
    res = requests.post(url, headers=headers, data=data,params=params)
    # print(res.text)
    res = res.json()
    cityLevel = dict( zip([cityDict['scity'] for cityDict in res['Table']],[cityDict['slevel'] for cityDict in res['Table']] ))
    cityIDStr = ",".join([str(cityDict['sCityID']) for cityDict in res['Table']])
    # print(cityIDStr)
    print('公司: {}, \t 发展城市数量: {}'.format(company,len(res['Table'])))
    return cityLevel, cityIDStr


headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        # "content-length": "2137",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": cookie,
        "origin": "https://creis.fang.com",
        "pragma": "no-cache",
        "referer": "https://creis.fang.com/enterprise/Detail/EnterpriseParcelList?iMarketLevel=0",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }
url = 'https://creis.fang.com/enterprise/Detail/GetCompanyCityNewParcelListSearch'

# 第一次请求,
# 房企拿地,  获取总共的数目条数
def get_first_number(companyID, startDate, endDate, cityIDStr):
    astr = '{"sCompanyID":"%s","sBeginDate":"%s","sEndDate":"%s","sCities":"%s","sParcelConformings":"住宅用地,商业/办公用地,工业用地,其它用地","sParcelName":"","sBeginClosingCost":"","sEndClosingCost":"","sBeginfParcelBuildArea":"","sEndfParcelBuildArea":"","sBeginfParcelArea":"","sEndfParcelArea":"","sBeginfFloorPrice":"","sEndfFloorPrice":"","sBeginsOverPricePercent":"","sEndsOverPricePercent":"","iPageIndex":1,"iPageSize":"15","sOrderIndex":"sCity","sOrderType":"asc","bIsDown":"0","iMarketLevel":"0"}'%(companyID, startDate, endDate, cityIDStr)
    data = {
        "jsonParameters": Urlchuli(astr, 'utf-8').url_bm()
    }
    res = requests.post(url, data=data, headers=headers).json()
    number = res['Table1'][0]['num']
    print('第一次请求, 获取到的数据量为i: ', number)
    return number


# 第二次请求, 获取全部的数据
def get_second_data(company, companyID, startDate, endDate, number, cityIDStr, cityLevel, dataList, TOP):
    print("company: %s ,all data number: %s" % (company, number))
    data = {
        "jsonParameters": '{"sCompanyID":"%s","sBeginDate":"%s","sEndDate":"%s","sCities":"%s","sParcelConformings":"住宅用地,商业/办公用地,工业用地,其它用地","sParcelName":"","sBeginClosingCost":"","sEndClosingCost":"","sBeginfParcelBuildArea":"","sEndfParcelBuildArea":"","sBeginfParcelArea":"","sEndfParcelArea":"","sBeginfFloorPrice":"","sEndfFloorPrice":"","sBeginsOverPricePercent":"","sEndsOverPricePercent":"","iPageIndex":1,"iPageSize":%s,"sOrderIndex":"sCity","sOrderType":"asc","bIsDown":"1","iMarketLevel":"0"}' % (companyID, startDate, endDate, cityIDStr, number),
    }
    while True:
        try:
            res = requests.post(url=url, data=data, headers=headers)
            res = res.json()
            break
        except:
            time.sleep(5)
            continue

    for i in res['Table']:
        items = {}
        items['城市'] = i['sCity']
        items['城市能级'] = cityLevel[i['sCity']]
        items['房企'] = company
        items['房企排名'] = TOP
        items['年'] = datetime.datetime.strptime(i['sParcelDate'],'%Y-%m-%d').year
        items['月'] = datetime.datetime.strptime(i['sParcelDate'],'%Y-%m-%d').month
        items['周'] = datetime.datetime.strptime(i['sParcelDate'],'%Y-%m-%d').isocalendar()[1]
        items['地块名称'] = i['sParcelName']
        items['编号'] = i['sParcelSN']
        items['受让单位'] = i['sTransferee']
        items['规划用途'] = i['sParcelConforming']
        items['占地面积(万㎡)'] = i['fParcelArea']
        items['规划建筑面积(万㎡)'] = i['fPlanningArea']
        items['总成交金额(亿元)'] = i['fClosingCost']
        items['平均楼面价(元/㎡)'] = i['sFloorAvgPrice']
        items['平均溢价率(%)'] = i['sOverPricePercent']
        items['土地权益(%)'] = i['dShareValue']
        items['权益金额(亿元)'] = i['fShareClosingCostNew']
        items['权益规划建筑面积(万㎡)'] = i['fSharePlanningArea']
        items['拿地时间'] = i['sParcelDate']
        items['地块ID'] = i['sParcelID']
        dataList.append(items)
    print('')


if __name__ == '__main__':
    # TODO 修改时间
    # TODO 开始时间向上推一个月左右吧, 截止时间为上周日
    startDate = '2020-12-20'
    endDate = '2021-01-10'    # 结束时间为上周周日
    print(startDate, endDate)

    with open("Top30_企业_ID.json", 'r', encoding='utf-8') as fp:
        TOP30 = json.load(fp)
    with open("Top30_50_企业_ID.json", 'r', encoding='utf-8') as fp:
        TOP30_50 = json.load(fp)

    data = []
    # TOP30
    for company, companyID in TOP30.items():
        print('30强公司')
        # 获取每个公司的发展城市
        time.sleep(random.random() + 1.5)
        cityLevel, cityIDStr = get_company_city_distribution(company, companyID)

        # # 获取列表数量
        time.sleep(random.random() + 0.5)
        while True:
            try:
                number = get_first_number(companyID, startDate, endDate, cityIDStr)
                break
            except:
                print('出错......, 等待5秒,')
                time.sleep(5)
                continue

        # # 获取并下载全部数据
        time.sleep(random.random())
        while True:
            try:
                get_second_data(company, companyID, startDate, endDate, number, cityIDStr, cityLevel, data, TOP='TOP30')
                break
            except:
                print('下载出错......, 等待5秒,')
                time.sleep(5)
                continue


    # # TOP30_50
    for company, companyID in TOP30_50.items():
        # 获取每个公司的发展城市
        print('TOP30-50')
        time.sleep(random.random() + 2)
        cityLevel, cityIDStr = get_company_city_distribution(company, companyID)

        # # 获取列表数量
        time.sleep(random.random() + 0.5)
        number = get_first_number(companyID, startDate, endDate, cityIDStr)

        # # 获取并下载全部数据
        time.sleep(random.random())
        get_second_data(company,companyID, startDate, endDate, number, cityIDStr, cityLevel, data, TOP='TOP30-50')

    # 保存数据
    df = pd.DataFrame(data)
    saveData(df, name='房企拿地')
