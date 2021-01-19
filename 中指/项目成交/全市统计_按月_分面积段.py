# -*- encoding: utf-8 -*-
"""
@Time    : 2020/12/26 16:56
@Software: PyCharm
@Description：
"""
import json
import random, time
import pandas as pd
import os
import requests
from selenium import webdriver

from Cookie import cookie, city_id_df

headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json",
        "cookie": cookie,
        "origin": "https://creis.fang.com",
        "referer": "https://creis.fang.com/city/2.0/statistics/project",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        "x-csrf-token-creis-city": "fR7b3xh2nNEbmSypMb4LLmP3",  # TODO
        "x-requested-with": "XMLHttpRequest",
    }


def selenium_bs():
    driver = webdriver.Chrome()
    driver.get('http://127.0.0.1:5000')
    return driver


def decrypt(bs, timestamp, data):
    ti = bs.find_element_by_id('time')
    ti.clear()
    ti.send_keys(timestamp)
    time.sleep(0.5)

    t = bs.find_element_by_id('code')
    t.clear()
    js = f"element = document.getElementById('code'); element.value = '{data}';"
    bs.execute_script(js)

    de = bs.find_element_by_id('de')
    de.click()
    time.sleep(0.5)

    de = bs.find_element_by_id('decode')
    code = de.text
    code_json = json.loads(code)
    return code_json


def get_params_id(cityId):
    url = 'https://creis.fang.com/city/2.0/proxy/cm_s_creis/city/getCityDealRangeData'
    params = {
        'cityId': cityId,
        'ownerId': 'creis',
        'referer': '',
        # 'request_transaction': '33691.033847379316',
        'request_transaction': 99999 * random.random()
    }

    while True:

        # print(res)
        try:
            res = requests.get(url, params=params, headers=headers).json()
            timestamp = res.get('meta').get('timestamp')
            data = res['data']
            if 'springframework' in res.get('meta').get('error', ''):
                print('没有数据')
                return
        except: # 米兰的小铁建
            # print('获取条件', res)
            time.sleep(random.random() + random.randint(4, 7))
            continue
        break
    # print('time, data: ', timestamp, data)
    code_json = decrypt(bs, timestamp, data)
    id = [i['id'] for i in [code['propertyTypeList'] for code in code_json if code['dealTableSource'] == 'month'][0] if i['name'] in ['普通住宅', '别墅']]
    romeTypeList = [i['id'] for i in [code['roomTypeList'] for code in code_json if code['dealTableSource'] == 'month'][0] ]
    buildTypeList = [i['buildTypeValue'] for i in [code['buildTypeList'] for code in code_json if code['dealTableSource'] == 'month'][0]]
    propertyTypeSource = [code['propertyTypeSource'] for code in code_json if code['dealTableSource'] == 'month'][0][0]
    roomTypeSource = [code['roomTypeSource'] for code in code_json if code['dealTableSource'] == 'month'][0][0]
    return id, romeTypeList, buildTypeList, propertyTypeSource, roomTypeSource


def down_load_json(bs, pages, beginDate, endDate, city_code, data_all, city):
    print(f'当前页数: {pages}, 时间: {beginDate[:4]}')
    time.sleep(random.random() + random.randint(5, 10))
    url = 'https://creis.fang.com/city/2.0/proxy/cm_s_creis/city/getCityStatisData?referer=&request_transaction={}'.format(
        99999 * random.random())
    propertyTypeIdList, romeTypeList, buildTypeList, propertyTypeSource, roomTypeSource = get_params_id(cityId=city_code)
    if not propertyTypeIdList:
        print('没有数据')
        return
    romeTypeList.append(-1)
    # buildTypeList.append(-1)
    payload = {"cityId": city_code, "cityName": city, "districtIdList": [],
               "boardIdList": [], "zoneIdList": [], "buyerNatureList": [], "limitedPriceHousing": "",
               "propertyTypeSource": propertyTypeSource, "propertyTypeIdList": propertyTypeIdList, "roomTypeSource": roomTypeSource,
               "roomTypeIdList": romeTypeList, "orderColIndexValue": "",
               "areaSectionList": ["0-60","60-70","70-80","80-90","90-100","100-110","110-120","120-130","130-140","140-150","150-160","160-170","170-180","180-190","190-200","200-220","220-240","240-260","260-280","280-300","300-999999999"],
               "amountSectionList": ["0-200", "200-300", "300-400", "400-500", "500-600", "600-700", "700-800",
                                     "800-900", "900-1000", "1000-1200", "1200-1400", "1400-1600", "1600-99999999",
                                     "-1"],
               "priceSectionList": ["0-10000", "10000-15000", "15000-20000", "20000-25000", "25000-30000",
                                    "30000-40000", "40000-50000", "50000-60000", "60000-70000", "70000-80000",
                                    "80000-99999999", "-1"], "buildingCategoryList": buildTypeList, "rowType": "面积段",
               "colType": "时间", "spreadType": "汇总", "orderType": "desc", "isTrusted": True, "dealTableSource": "month",
               "beginDate": beginDate, "endDate": endDate, "pageNum": 1, "pageSize": 100, "orderIndex": "面积段"}
    print(f"{payload}")

    while True:
        res = requests.post(url, json=payload, headers=headers).json()
        print(res)
        try:
            timestamp = res.get('meta').get('timestamp')
            data = res['data']
            if 'springframework' in res.get('meta').get('error', ''):
                print('没有数据')
                return
        except:
            print(f'重试... 页数: {pages}')
            # print(res)
            time.sleep(random.random() + random.randint(4, 7))
            continue
        break
    # print(f'{timestamp}, {data}')
    code_json = decrypt(bs, timestamp, data)
    print(code_json)
    try:
        body = code_json.get('tableData').get('body')
    except:
        return
    print("数量body: ", len(body))
    for b in body:
        item = []
        item.append(b.get('values')[3])
        item.append(b.get('row'))
        item.append(b.get('col'))
        data_all.append(item)


def run(bs):

    i = 0
    for city in city_id_df['cityName'].tolist():
        # if city not in ['北京']: continue
        print()
        city_code = city_id_df[city_id_df['cityName'] == city]['houseID'].values[0]
        i += 1
        print(city, city_code, i)
        if i > 200: return

        if city in [i.split('.')[0] for i in os.listdir(r'全市统计_月_面积')]:
            continue

        print(f'当前城市: {city}, {city_code}')

        name = f'全市统计_月_面积/{city}.xlsx'
        writer = pd.ExcelWriter(name)
        # for j in [('2015-01-01', '2019-12-31'), ('2020-01-01', '2020-12-31')]:
        data_all = []
        for j in [('2019-01-01', '2020-12-31')]:
            pages = 1
            beginDate = j[0]
            endDate = j[1]
            down_load_json(bs, pages, beginDate, endDate, city_code, data_all, city)

        df = pd.DataFrame(data=data_all,
                          columns=['成交金额(元)', '面积', '月份'])
        df['城市'] = city
        df.to_excel(writer, sheet_name=f'2016-2020', index=False)
        writer.save()
        writer.close()


if __name__ == '__main__':
    bs = selenium_bs()
    # bs = ''
    run(bs=bs)
    # print()

    # 合并
    path_name = '全市项目成交_月_面积.xlsx'
    writer = pd.ExcelWriter(path_name)
    d = []
    d1 = []
    for i in os.listdir('全市统计_月_面积'):
        print(i)
        city = i.split('.')[0]
        path = os.path.join('全市统计_月_面积', i)
        df1 = pd.read_excel(path, sheet_name='2016-2020')
        d.append(df1)

    df1 = pd.concat(d)
    df1.to_excel(writer, sheet_name='2019-2020', index=False)
    writer.save()
    writer.close()
