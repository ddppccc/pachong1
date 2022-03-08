# encoding=utf8
import requests
import time
import random
from config import get_proxy,headers
e = ['a', 'b', 'c', 'd', 'e', 'f']
n = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
s = ['a', 'b', 'c', 'd', 'e', 'f', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
cuid1 = '179e'
for i in range(8):
    cuid1 += random.choice(s)
cuid2 = '0'
for i in range(13):
    cuid2 += random.choice(s)
cuid3 = 'f'
for i in range(6):
    cuid3 += random.choice(s)
cuid4 = '1fa400'
cuid5 = cuid1
cuid = cuid1 + '-' + cuid2 + '-' + cuid3 + '-' + cuid4 + '-' + cuid5
def rans(num):
    x=''
    for i in range(num):
        x += random.choice(s)
    return x

def getheaders():
    s = ['a', 'b', 'c', 'd', 'e', 'f', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    cuid1 = '179e'
    for i in range(8):
        cuid1 += random.choice(s)
    cuid2 = '0'
    for i in range(13):
        cuid2 += random.choice(s)
    cuid3 = 'f'
    for i in range(6):
        cuid3 += random.choice(s)
    cuid4 = '1fa400'
    cuid5 = cuid1
    cuid = cuid1 + '-' + cuid2 + '-' + cuid3 + '-' + cuid4 + '-' + cuid5
    headers = {
        'Connection': 'keep-alive',
        'Cookie': f'_lxsdk_cuid={cuid}; _lxsdk=179e9{rans(5)}91-06ce{rans(10)}-68151f7a-1fa400-179e{rans(7)}c8; _hc.v=f50464d5-{rans(4)}-07d4-fad0-7f7d{rans(5)}c25.{str(int(time.time()))}; Hm_lvt_602b80cf8079ae659{rans(10)}940e7={str(int(time.time()))}; Hm_lpvt_602b80cf8079ae65{rans(10)}3940e7={str(int(time.time()))}; _lxsdk_s=179ea{rans(6)}-7a0-{rans(3)}-68c%7C%7C3',
        'Host': 'www.dianping.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    }
    return headers
def getscore(shopId,cityId,mainCategoryId):
    # print('正在获取评分')
    url = 'http://www.dianping.com/ajax/json/shopDynamic/reviewAndStar'
    data2 = {
        'shopId':shopId ,
        'cityId': cityId,
        'mainCategoryId': mainCategoryId,
        'platform': '1',
        'partner': '150',
        'optimusCode': '10',
        'originUrl': 'http://www.dianping.com/shop/'+shopId,
    }
    for i in range(100):
        try:
            proxy=get_proxy()
            proxies = {
                "http": proxy,
                "https": proxy
            }
            r = requests.get(url, params=data2,proxies=proxies, headers=getheaders(),timeout=2)
            # r = requests.get(url, params=data2, headers=headers,timeout=2)
            if not r.status_code in [200]:continue
            key=r.json()['shopScoreTitleList']
            valvue=r.json()['shopRefinedScoreValueList']
            try:
                fiveScore=r.json()['fiveScore']
                print('获取成功')
            except:
                fiveScore=''
            print('获取评分成功')
            return key,valvue,fiveScore
        except Exception as e:
            continue
    print('获取评分错误次数过多')
    return '',''


if __name__ == '__main__':
    headers = {
        'Connection': 'keep-alive',
        'Cookie': f'_lxsdk_cuid={cuid}; _lxsdk=179e9{rans(5)}91-06ce{rans(10)}-68151f7a-1fa400-179e{rans(7)}c8; _hc.v=f50464d5-{rans(4)}-07d4-fad0-7f7d{rans(5)}c25.{str(int(time.time()))}; Hm_lvt_602b80cf8079ae659{rans(10)}940e7={str(int(time.time()))}; Hm_lpvt_602b80cf8079ae65{rans(10)}3940e7={str(int(time.time()))}; _lxsdk_s=179ea{rans(6)}-7a0-{rans(3)}-68c%7C%7C3',
        'Host': 'www.dianping.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    }
    url = 'http://www.dianping.com/ajax/json/shopDynamic/reviewAndStar'
    proxies = {"https": get_proxy()}
    data = {
        'shopId': 'l9ZCNMdT6rTzUzZF',
        'cityId': '2',
        'mainCategoryId': '64867',
        'platform': '1',
        'partner': '150',
        'optimusCode': '10',
        'originUrl': 'http://www.dianping.com/shop/l9ZCNMdT6rTzUzZF',
    }
    r = requests.get(url, params=data,proxies=proxies, headers=headers,timeout=2)
    print(r.json()['shopScoreTitleList'])