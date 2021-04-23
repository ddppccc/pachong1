# coding:utf-8
import re
import math
from urllib import parse
import time
import pymongo
import requests
import pandas as pd

from sqlalchemy import create_engine
from config import Update_NewHouse, make_date, newHouse_map


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
            retryWrites="false")['贝壳']['XinFang']

url_data = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['贝壳']['xf_url']


class NewHouse:
    def __init__(self, year, month):
        self.year = year
        self.month = month

    def baidu_chang_gaode(self, lat, lng):
        '''百度坐标转高德'''
        if not lat or not lng:
            return "", ""
        lng, lat = float(lng), float(lat)
        x_pi = 3.14159265358979324 * 3000.0 / 180.0

        x = lng - 0.0065
        y = lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
        lng = z * math.cos(theta)
        lat = z * math.sin(theta)
        return lat, lng

    # def get_exists_city(self, month):
    #     """获取当月已经获取的城市"""
    #     sql = f"""SELECT distinct "城市" FROM public."NewHouse_2020" where 抓取月份={month} and 数据来源='贝壳';"""
    #     exists_city = pd.read_sql_query(sql=sql, con=engine)
    #     # engine.close()
    #     exists_city_list = exists_city['城市'].tolist()
    #     return exists_city_list

    def get_html(self, url):
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        params = {"_t": "1"}
        print(url)
        while True:
            try:
                res = requests.get(url, headers=headers, params=params).json()
                return res
            except Exception as e:
                print('error!!! ', url, params, e)
                continue


    def get_page_info(self, city, url, data, **kwargs):
        if url_data.find_one({'url':url}):
            print('已爬取')
            return 0
        ''' 获取详情页信息 '''
        res = self.get_html(url)
        houseList = res['data']['list']
        print(f"当前城市: {city}")
        if not houseList: return
        for house in houseList:
            houseDict = dict()
            houseDict['城市'] = city
            houseDict['区县'] = house['district_name']
            houseDict['标题'] = house['title']
            houseDict['建面'] = house['resblock_frame_area_range']
            range_area = house['resblock_frame_area_range'].replace('㎡', '').split('-')
            if len(range_area) == 2:
                houseDict['最小建面'], houseDict['最大建面'] = range_area
            elif len(range_area) == 1:
                houseDict['最小建面'], houseDict['最大建面'] = range_area[0], range_area[0]
            else:
                houseDict['最小建面'], houseDict['最大建面'] = '', ''

            houseDict['latitude'], houseDict['longitude'] = self.baidu_chang_gaode(house['latitude'], house['longitude'])
            houseDict['标题url'] = re.sub("(/loupan/.*)", house['url'], url)
            houseDict['地址'] = house['address']
            houseDict['分类'] = house['house_type']
            date = house['open_date'].replace('-99', '-01') if '99' in house['open_date'] else house['open_date']
            houseDict['开盘时间'] = '' if date == '2001-01-01' else date
            houseDict['标签'] = '%s' % house['tags']
            houseDict['户型'] = house['frame_rooms_desc']
            houseDict['总价'] = house['total_price_start']
            houseDict['均价'] = house['average_price']
            houseDict['装修'] = house['decoration']
            houseDict['房屋描述'] = '%s' % house['converged_rooms']
            houseDict['楼盘亮点'] = house['project_desc']
            houseDict['销售情况'] = house['sale_status']

            houseDict['抓取年份'] = self.year
            houseDict['抓取月份'] = self.month
            houseDict['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print(houseDict)
            data.append(houseDict)
            info_base.insert_one(houseDict)
        url_data.insert_one({'url':url})


    # 获取所有城市映射表
    def get_city_info(self, city, url):
        print(url)
        res = self.get_html(url=url)
        data = []
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',res)
        # totalNumber = res['data']['total']
        # if totalNumber == '0': return
        # totalPage = int(totalNumber) // 10 + 1
        for i in range(1, 100):  # 获取每一页的详细信息
            page_url = url + 'pg%s/' % i
            self.get_page_info(city, page_url, data=data, page=i)

        # df = pd.DataFrame(data)
        # df = Update_NewHouse().update(df)
        # df.to_sql(name='NewHouse_2020', con=engine, schema='public', if_exists='append', index=False)
        # print(f'{city}, 保存成功')


    def run(self, newHouse_map):
        # exists_city_list = self.get_exists_city(self.month)
        for city, city_url in newHouse_map.items():
            if city in ['大治'] : print('贝壳已舍去'); continue
            # if city in exists_city_list: print('已存在,跳过 '); continue
            print(city, city_url)
            local_list = city_url.split('/')[-1].split('-')
            base = city_url.replace(city_url.split('/')[-1],'')
            for local_area in local_list:
                city_url = base + local_area
                print(city_url)
                self.get_city_info(city, city_url)
            # print()


if __name__ == '__main__':
    # TODO 请注意不同年份下 储存的表的名称不相同, 请修改
    # TODO 修改每月抓取时间(可自定义), 位置 config >> make_date

    Year, Month, Day = make_date()
    #engine = create_engine('postgresql://postgres:1q2w3e4r@127.0.0.1/NewHouse').connect()  # 连接本地的新房数据库
    NewHouse(year=Year, month=Month).run(newHouse_map)
    #engine.close()

