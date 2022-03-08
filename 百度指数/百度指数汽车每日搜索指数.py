import datetime
import os
import random
import time
from config import COOKIES, CITY_CODE2,KEYWORDS
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
            retryWrites="false")['百度指数']['汽车每日搜索指数_数据_202106']
if __name__ == "__main__":
    year = 2021
    month = 6
    day = 2
    # 百度关键词
    keywords = KEYWORDS
    start_date = '2020-12-04'
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    # x=info_base.delete_many({})
    # print(x.deleted_count,'个文档已删除')

    for keyword in keywords:     # TODO 每次递增
        keylist=[keyword]

        for city, city_code in CITY_CODE2.items():
            if info_base.find_one({'城市': city,'keyword': "[{'name': '%s', 'wordType': 1}]"%keyword}):
                print('该数据已抓取')
                continue
            cookie = random.choice(COOKIES)
            baidu_index = BaiduIndex(keywords=keylist, start_date=start_date,
                                     end_date=end_date,
                                     area=city_code, cookies=cookie)
            l=[]
            for index in baidu_index.get_index():
                index['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                index['城市'] = city
                index['抓取年份'] = year
                index['抓取月份'] = month
                index['抓取日期'] = day
                # print(index)
                l.append(index)
            print({'城市': city,'keyword': "[{'name': '%s', 'wordType': 1}]"%keyword})
            if info_base.find_one({'城市': city,'keyword': "[{'name': '%s', 'wordType': 1}]"%keyword}):
                print('数据已存在')
            else:
                info_base.insert_many(l)
                print(city,keyword,'数量',len(l))