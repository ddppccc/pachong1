import json
import time
import pandas as pd
import requests

from config import cookie

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'cache-control': 'no-cache',
# 'content-length': '179',
'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
'cookie': cookie,
'origin': 'https://creis.fang.com',
'pragma': 'no-cache',
'referer': 'https://creis.fang.com/enterprise/Detail/FinancingData?sCompanyID=247b1aa6-9d78-4aad-ad86-daea8a6bca19',
'sec-fetch-mode': 'cors',
'sec-fetch-site': 'same-origin',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
'x-requested-with': 'XMLHttpRequest'
}

# TODO 这个直接运行即可

def down(data, company, item):
    url = 'https://creis.fang.com/enterprise/Detail/GetFinancingData/'
    while True:
        try:
            res = requests.post(url=url,  data=data, headers=headers).json()
            break
        except:
            print('戳错重试中....')
            time.sleep(5)
            continue
    for i in res['Table']:
        items = {}
        items['房企'] = company
        items['时间'] = i['dFinancingDate']
        items['金额(亿元)'] = i['fFinancingPrice']
        items['融资类型'] = i['sFinancingTypeName']
        items['融资内容'] = i['sDes']
        item.append(items)


with open("Top30_企业_ID.json", 'r', encoding='utf-8') as fp:
    TOP30 = json.load(fp)
with open("Top30_50_企业_ID.json", 'r', encoding='utf-8') as fp:
    TOP30_50 = json.load(fp)


item = []
for company, companyID in TOP30.items():
    time.sleep(2)
    print("TOP30", company)
    data = {
        "jsonParameters": '{"sCompanyID":"%s","sOrderColumn":"date","sOrderType":"desc","rd":0.436301013272375}' % companyID,
        "v": "0.3734663275532917"
    }
    down(data, company, item)


for company, companyID in TOP30_50.items():
    time.sleep(2)
    print("TOP30_50",company)
    data = {
        "jsonParameters": '{"sCompanyID":"%s","sOrderColumn":"date","sOrderType":"desc","rd":0.436301013272375}' % companyID,
        "v": "0.3734663275532917"
    }
    down(data, company, item)


df = pd.DataFrame(item)
df = df[["房企", "时间", "金额(亿元)", "融资类型", "融资内容"]]
df.to_excel('data/房企拿地/房企融资.xlsx', index=False)



