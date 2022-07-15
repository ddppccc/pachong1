import datetime
import os
import random
import time

import pandas as pd

from config import COOKIES, CITY_CODE
from get_index import BaiduIndex
import pymongo
from urllib import parse
from multiprocessing import Process,Pool
MONGODB_CONFIG = {
    "host": "192.168.1.28",
    "port": "27017",
    "user": "admin",
    "password": '123123',
}
info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['百度指数']['百度搜索指数_数据_202207']

if __name__ == "__main__":
    # 4545
    year = 2022
    month = 7
    day = 4
    # 百度关键词
    keywords = ['招聘', '招工', '房价', '股票', '失业金', '买房', '卖房', '租房']    #['招聘', '招工', '房价', '股票', '失业金', '买房', '卖房', '租房']
    start_date = '2022-06-05'    #-----间隔区间-2021-01-01----------------------------------------上次时间'2022-03-04' 2022-04-01
    end_date = '2022-07-04'      #'2022-04-01'     2022-05-05


    for number in [22, 23]:     # TODO 每次递增
        for city, city_code in CITY_CODE.items():
            # city = '全国'                    #改----------------------------------------------------------------
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
                index['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                index['城市'] = city
                index['抓取年份'] = year
                index['抓取月份'] = month
                index['抓取日期'] = day
                if info_base.count_documents({'keyword':index['keyword'],'type':index['type'],'date':index['date'],'城市':city}) == 0:
                    info_base.insert_one(index)

                    print(index)
                else:
                    print('该条数据已存在')
                # data.append(index)
            # df = pd.DataFrame(data=data)
            # print("df: ", df.head())
            # df.to_excel('原始数据/%s_%s.xlsx' % (city, number), index=False)
