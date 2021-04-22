import datetime
import os
import random

import pandas as pd

from config import COOKIES, CITY_CODE
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
            retryWrites="false")['百度指数']['info']

if __name__ == "__main__":

    # 百度关键词
    keywords = ['招聘', '招工', '房价', '股票', '失业金', '买房', '卖房', '租房']
    start_date = '2021-01-01'
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")


    for number in [22, 23]:     # TODO 每次递增
        for city, city_code in CITY_CODE.items():
            data = random.sample(CITY_CODE.items(), 1)
            city, city_code = data[0][0], data[0][1]
            name = '%s_%s.xlsx' % (city, number)
            # if name in os.listdir('原始数据'):
            #     print(name, '存在')
            #     continue

            data = []
            print('城市: ', city)
            cookie = random.choice(COOKIES)
            # print(cookie)

            baidu_index = BaiduIndex(keywords=keywords, start_date=start_date,
                                     end_date=end_date,
                                     area=city_code, cookies=cookie)
            for index in baidu_index.get_index():

                if info_base.count_documents(index) == 0:
                    info_base.insert_one(index)
                    print(index)
                else:
                    print('该条数据已存在')
                # data.append(index)
            # df = pd.DataFrame(data=data)
            # print("df: ", df.head())
            # df.to_excel('原始数据/%s_%s.xlsx' % (city, number), index=False)
