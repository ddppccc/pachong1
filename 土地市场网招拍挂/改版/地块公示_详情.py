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
            retryWrites="false")['土地市场网招拍挂']['地块公示_列表_202110']
info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['土地市场网招拍挂']['地块公示_数据_202110']
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
    if info_base.find_one({'cjgsGuid':data['cjgsGuid']}):
        print('已存在..')
        return
    for i in range(5):
        url='https://api.landchina.com/tCjgs/deal/detail'
        postdata={'cjgsGuid': data['cjgsGuid']}
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
            item['cjgsGuid'] = data['cjgsGuid']
            item['标题'] = data['gsbt']
            item['省份'] = res.json()['data']['gsbt']
            item['城市'] = res.json()['data']['city']
            item['成交日期'] = data['fbSj']
            item['标题url'] = f'https://www.landchina.com/landSupplyDetail?id={data["cjgsGuid"]}&type=%E5%9C%B0%E5%9D%97%E5%85%AC%E7%A4%BA&path=0'
            item['地块编号'] = i['zdBh']
            item['土地面积'] = i['mj']
            item['地块位置'] = i['zdZl']
            try:
                item['土地用途'] = i['tdYt']
            except:
                item['土地用途'] =''
            item['明细用途'] = ''
            item['受让单位'] = i['srDw']
            item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print(item)
            info_base.insert_one(item)
        break






if __name__ == '__main__':
    for d in page_base.find():
        print(d)
        getdata(d)
