# encoding=utf-8
import requests
import time
import datetime
from dateutil.relativedelta import relativedelta
import pymongo
from urllib import parse
MONGODB_CONFIG = {
   "host": "8.135.119.198",
   "port": "27017",
   "user": "hladmin",
   "password": parse.quote("Hlxkd3,dk3*3@"),
   "db": "dianping",
   "collections": "dianping_collections",
}
info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['土地市场网招拍挂']['出让公告_列表_202110']
def get_time_range_list(startdate, enddate):
    """
        切分时间段
    """
    date_range_list = []
    startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
    while 1:
        tempdate = startdate + datetime.timedelta(days=1)
        if tempdate > enddate:
            date_range_list.append((str(startdate.date()), str(enddate.date())))
            break
        date_range_list.append((str(startdate.date()), str((tempdate - datetime.timedelta(days=1)).date())))
        startdate = tempdate
    return date_range_list
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
def getdata(start,end,page=1):
    for i in range(5):
        url='https://api.landchina.com/tGygg/transfer/list'
        postdata={"pageNum":page,
                  "pageSize":10,
                  "startDate":f"{start} 00:00:00",
                  "endDate":f"{end} 23:59:59"}
        time.sleep(1)
        res=requests.post(url,headers=headers,json=postdata)
        res.encoding='utf8'
        if res.json()['code'] == 500:
            time.sleep(5)
            continue
        print(res.json()['data']['list'])
        info_base.insert_many(res.json()['data']['list'])
        print('当前页',page)
        print('总页数',res.json()['data']['pages'])
        if page<res.json()['data']['pages']:
            page += 1
            return getdata(start, end, page)


        break



if __name__ == '__main__':
    start='2021-09-23'                    #0923-1027共60000页 已完成1-726
    end='2021-10-27'
    getdata(start,end)
    # list=get_time_range_list(start, end)
    # print(list)