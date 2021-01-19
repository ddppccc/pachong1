import json
import random, time
import pandas as pd
import os
import math
import requests
from selenium import webdriver

from config import cookie


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



def down_load_json(bs, pages, beginDate, endDate, city_code, data_all):
    print(f'当前页数: {pages}, 时间: {beginDate[:4]}')
    time.sleep(random.random() + random.randint(5, 10))
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        # "content-length": "510",
        "content-type": "application/json",
        "cookie": cookie,
        "origin": "https://creis.fang.com",
        "referer": "https://creis.fang.com/city/2.0/statistics/project",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        # "x-csrf-token-creis-city": "OnF2TVwAMRKt-hOXv-684fKN",
        "x-csrf-token-creis-city": "ciA_wXrxiWs6L01Ld8Gq9O8Q",
        "x-requested-with": "XMLHttpRequest",
    }
    url = 'https://creis.fang.com/city/2.0/proxy/cm_s_creis/city/getProjectStatisData?referer=&request_transaction={}'.format(
        99999 * random.random())
    payload = {"cityId": city_code, "beginDate": beginDate, "endDate": endDate,
               "dealPriceBegin": "", "dealPriceEnd": "", "orderIndex": "成交套数", "orderType": "desc", "pageNum": pages,
               "pageSize": 2000, "projectName": "", "roomAmountBegin": "", "roomAmountEnd": "", "roomAreaBegin": "",
               "roomAreaEnd": "", "typeName": "成交情况", "floorBegin": "", "floorEnd": "", "boardIdList": [],
               "districtIdList": [], "propertyTypeIdList": [2],
               "zoneIdList": [], "roomTypeIdList": [], "fixStatusTypeList": []}
    while True:
        res = requests.post(url, json=payload, headers=headers).json()
        print(res)
        try:
            timestamp = res.get('meta').get('timestamp')
            data = res['data']
        except:
            print(f'重试... 页数: {pages}')
            print(res)
            time.sleep(random.random() + random.randint(4, 7))
            continue
        break

    code_json = decrypt(bs, timestamp, data)

    body = code_json.get('tableData').get('body')
    print("数量body: ", len(body))
    for b in body:
        item = b.get('values')
        data_all.append(item)

    # 总条数
    totalCount = code_json.get('tableData').get('totalCount')
    print("总条数: ",totalCount)
    # total_pages = math.ceil(totalCount/100)
    # if pages < total_pages:
    #     page = pages + 1
    #     print(f'总页数: {total_pages}, 下一页第 {page} 页, \n')
    #     down_load_json(bs, page, beginDate, endDate, city_code, data_all)
    # else:
    #     print(f'当前城市, 运行结束 \n\n')
    #     return


def run(bs):
    for city, city_code in {
        "北京": '6679b8fe-0231-4c3e-95e2-1afa9e3fea5f',
        "上海": '52907f4c-7222-4b38-b50a-3d5346852b53', "成都": 'e83875a9-79cb-40c6-9508-df6fd2ac31a3',
        "重庆": 'efce77a3-d836-4847-897f-9930e58ef0af', "广州": '2890d08e-d072-450f-a34d-9f56cc980106',
        "杭州": '3146b167-dcc5-4be2-9db2-47f2a6bda5b6', "深圳": 'c159b923-46aa-4be5-91ba-e9e3561141b1',
        "苏州": '23d61d94-7967-44af-8268-be7a7b440437', "武汉": '83a1fc91-183a-4007-8383-f224df858304',
        "南京": 'b1dc179a-4fde-4d3b-b4af-c88ddf7c1a28', "天津": '94024b0a-7615-45bb-afb9-07a19f5d626a',
        "西安": '926123c5-6fc4-495e-8f9d-149c201ed933',
        "青岛": '00402edb-0ac6-48d5-b448-bd385f0c527c', "东莞": '8a89e25d-86cf-486c-8d2f-7cb4e565315d',
        "郑州": '14197f14-2b22-47b4-b1df-9764775d1668', "宁波": '95bf06ba-8b21-4d63-ad47-9f449625a29d',
        "佛山": '57ce4c93-9774-4055-bbe2-a4bb110c58fb', "昆明": 'e993035c-1209-4a86-8cee-ea0e80a35f74',

        "温州": 'cfb424de-5744-4845-af9e-a210c8c2d7ee', "无锡": '3aaa9a25-fe54-4c40-aa24-af695cb3f907',
        "长沙": 'f43974e7-32a4-45df-8ae8-a7eb142fd5df', "沈阳": 'feb9b146-709b-430d-815e-e2e54d67fe13',
        "福州": '4225b4c8-7ad3-4776-9062-755bd8d8bd17', "大连": 'f97442b7-1c7d-4ba7-ada9-e356ce3f9b4a',
        "哈尔滨": 'a36db81d-c97d-4916-a57b-21561d581e3a', "合肥": 'ec224a51-6810-4885-8852-caaae0aee0f8',
        "济南": 'd8186a41-8bf5-49fd-a9ec-c1b86561ec76', "厦门": '03c15b7a-6ec0-49ff-ba3e-1f6c15cb1197',
        "金华": 'ff46ecc3-2964-416d-b210-5716a1378242', "嘉兴": '12dbfe72-d57c-499d-bedb-036270e24cc9',
        "绍兴": 'ac242bc5-2e7e-4721-b462-925043e8c073', "潍坊": '8cd0cbbe-b687-4645-aa73-8c47b2f59d5b',
        "石家庄": '9a08213a-fce3-455a-8787-f13392c09f61', "常州": '8a515f4c-919a-4754-bf1d-0ee49aea728b',
        "烟台": '23ae58cc-d401-483c-8f1c-127b97a6c775', "太原": 'd85083ca-b50e-4560-bae3-8c148b87be14'
    }.items():
        if city in [i.split('.')[0] for i in os.listdir(r'data')]:
            continue
        # if city == '潍坊': continue  # 没有 15-17年数据
        if city != '成都': continue  # 没有 15年数据
        print(f'当前城市: {city}, {city_code}')

        name = f'data/{city}.xlsx'
        writer = pd.ExcelWriter(name)
        # for j in [('2015-01-01', '2015-12-31'), ('2015-01-01', '2015-12-31')]:
        for j in [ ('2020-01-01', '2015-12-31')]:
            pages = 1
            beginDate = j[0]
            endDate = j[1]
            data_all = []

            down_load_json(bs, pages, beginDate, endDate, city_code, data_all)

            df = pd.DataFrame(data=data_all, columns=['项目名称', '区县', '板块', '所属企业', '成交套数', '成交面积', '成交价格', '成交金额', '套均总价', '套均面积'])
            df.to_excel(writer, sheet_name=f'{beginDate[:4]}-{endDate[:4]}', index=False)
        writer.save()
        writer.close()


if __name__ == '__main__':
    bs = selenium_bs()
    # bs = ''
    run(bs=bs)

    # 合并
#     path_name = '综合_36城_项目成交数据_2015.xlsx'
#     writer = pd.ExcelWriter(path_name)
#     d = []
#     d1 = []
#     for i in os.listdir('data'):
#         print(i)
#         city = i.split('.')[0]
#         path = os.path.join('data', i)
#         try:
#             df1 = pd.read_excel(path, sheet_name='2015-2015')
#         except:
#             df1 = pd.DataFrame()
#         df2 = pd.read_excel(path, sheet_name='2015-2015')
#         if city == '潍坊':
#             pass
#         else:
#             df1['城市'] = city
#
#         print(city)
#         df2['城市'] = city
#         d.append(df1)
#         d1.append(df2)
#     df1 = pd.concat(d)
#     df2 = pd.concat(d1)
#     df1.to_excel(writer, sheet_name='2015-2018', index=False)
#     df2.to_excel(writer, sheet_name='2015-2015', index=False)
# # chengdu
#     writer.save()
#     writer.close()







