import datetime
import os
import random

import pandas as pd

from config import COOKIES, CITY_CODE
from get_index import BaiduIndex

if __name__ == "__main__":

    # 百度关键词
    keywords = ['招聘', '招工', '房价', '股票', '失业金', '买房', '卖房', '租房']
    start_date = '2011-01-01'
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")

    #
    for number in [22, 23]:     # TODO 每次递增
        for city, city_code in CITY_CODE.items():
            name = '%s_%s.xlsx' % (city, number)
            if name in os.listdir('原始数据'):
                print(name, '存在')
                continue

            data = []
            print('城市: ', city)
            cookie = random.choice(COOKIES)

            baidu_index = BaiduIndex(keywords=keywords, start_date=start_date,
                                     end_date=end_date,
                                     area=city_code, cookies=cookie)
            for index in baidu_index.get_index():
                data.append(index)
            df = pd.DataFrame(data=data)
            print("df: ", df.head())
            df.to_excel('原始数据/%s_%s.xlsx' % (city, number), index=False)
