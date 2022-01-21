# encoding=utf-8
import requests
import time
import datetime
from dateutil.relativedelta import relativedelta
import pymongo
from urllib import parse
import warnings
warnings.filterwarnings("ignore")
MONGODB_CONFIG = {
   "host": "8.135.119.198",
   "port": "27017",
   "user": "hladmin",
   "password": parse.quote("Hlxkd3,dk3*3@"),
   "db": "dianping",
   "collections": "dianping_collections",
}
page_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['土地市场网招拍挂']['出让公告_列表_202111']
info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['土地市场网招拍挂']['出让公告_数据_202111']
headers={

    'Host': 'api.landchina.com',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'Origin': 'https://www.landchina.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.landchina.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': "'zh-CN,zh;q=0.9'",


}
def getdata(data):
    if info_base.find_one({'gyggGuid':data['gyggGuid']}):
        print('已存在..')
        return
    for i in range(5):
        url='https://api.landchina.com/tGygg/transfer/detail'
        postdata={'gyggGuid': data['gyggGuid']}
        time.sleep(1)
        res=requests.post(url,headers=headers,json=postdata,verify=False)
        res.encoding='utf8'
        if res.json()['code'] == 500:
            time.sleep(5)
            continue
        for i in res.json()['relate']:
            # print(i)
            item={}
            item['行政区'] = data['xzqFullName']
            item['gyggGuid'] = data['gyggGuid']
            item['标题'] = data['gyggBt']
            item['省份'] = res.json()['data']['province']
            item['城市'] = res.json()['data']['city']
            item['成交日期'] = data['fbSj']
            item['标题url'] = f'https://www.landchina.com/landSupplyDetail?id={data["gyggGuid"]}&type=%E5%87%BA%E8%AE%A9%E5%85%AC%E5%91%8A&path=0'
            try:
                item['宗地编号'] = i['zdBh']
            except:
                item['宗地编号'] = ''
            try:
                item['宗地总面积'] = i['mj']
            except:
                item['宗地总面积'] = ''
            try:
                item['地块位置'] = i['zdZl']
            except:
                item['地块位置'] = ''
            try:
                item['土地用途'] = i['tdYt']
            except:
                item['土地用途'] =''
            try:
                item['挂牌开始时间'] =time.strftime("%Y-%m-%d %H:%M:%S",  time.localtime(int(int(i['gpSjS'])/1000)))
                item['挂牌截至时间'] =time.strftime("%Y-%m-%d %H:%M:%S",  time.localtime(int(int(i['gpSjE'])/1000)))
            except:
                item['挂牌开始时间'] = ''
                item['挂牌截至时间'] = ''
            item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print(item)
            info_base.insert_one(item)
        break






if __name__ == '__main__':
    for d in page_base.find():
        print(d)
        # getdata(d)
