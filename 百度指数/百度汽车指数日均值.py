import datetime
import os
import random
import time

import pandas as pd
import requests

from config import COOKIES, CITY_CODE2
from get_index import BaiduIndex
import pymongo
from urllib import parse
from multiprocessing import Process,Pool
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
            retryWrites="false")['百度指数']['汽车指数日均值_数据_202106']
headers = {
    'Host': 'index.baidu.com',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
}
if __name__ == "__main__":
    year = 2021
    month = 6
    day = 2
    # 百度关键词
    headers['Cookie']=random.choice(COOKIES)
    keywords = ['特斯拉',"阿尔法罗米欧",'阿斯顿马丁','奥迪','宝马','宾利','奔驰','布加迪','别克','凯迪拉克','雪佛兰','克莱斯勒',
                '雪铁龙','大宇','大发','道奇','法拉利','菲亚特','福特','本田','悍马','现代','五十铃','捷豹','吉普','起亚','兰博基尼',
                '蓝旗亚','路虎','雷克萨斯','林肯','玛莎拉蒂','迈巴赫','马自达','梅赛德斯-奔驰','雷诺','劳斯莱斯','萨博','桑塔纳','土星',
                '西雅特','斯柯达','精灵','双龙','斯巴鲁','铃木','丰田','沃克斯豪尔','大众','沃尔沃','昌河铃木','比亚迪','广汽传祺','Wey',
                '长安汽车','奇瑞','长城','哈弗','吉利','五菱','保时捷','日产']
    start_date = "2020-12-04"
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    url='https://index.baidu.com/api/SearchApi/index'
    for city,citycode in CITY_CODE2.items():
        for keyword in keywords:
            word=[[{"name": keyword, "wordType": 1}]]
            data={
                "area": citycode,
                "word": str(word).replace("'", '"'),
                "startDate": start_date,
                "endDate": end_date,
            }
            res=requests.get(url,params=data,headers=headers)
            # print(res.json()['data']['generalRatio'][0])
            # print(res.json()['data']['generalRatio'][0]['all']['avg'])
            # print(res.json()['data']['generalRatio'][0]['wise']['avg'])
            item={}
            item['城市']=city
            item['关键词']=keyword
            item['整体日均值']=res.json()['data']['generalRatio'][0]['all']['avg']
            item['移动日均值']=res.json()['data']['generalRatio'][0]['wise']['avg']
            item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            item['抓取年份'] = year
            item['抓取月份'] = month
            item['抓取日期'] = day
            # print(item)
            if info_base.find_one({'城市':city,'关键词':keyword}):
                print('该条数据已存在')
            else:
                info_base.insert_one(item)
                print(item)
            # time.sleep(1)
