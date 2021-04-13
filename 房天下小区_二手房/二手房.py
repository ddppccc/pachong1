# -*- coding: utf-8 -*-
"""
@Time    : 2020/11/30
@version : python 3.7
@Description：二手房
"""

import random
import re
import time
import requests
import pymongo
import uuid
import numpy as np
import pandas as pd

from urllib import parse
from lxml import etree
from sqlalchemy import create_engine
from concurrent.futures import ThreadPoolExecutor

from IP_config import get_Html_IP
from city_map import make_url, city_map
from save_data import saveData, save_grab_dist, get_exists_dist

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
            retryWrites="false")['房天下二手房']['info']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['房天下二手房']['has_spider']
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "global_cookie=f1v4y6cur4h7034ieaxs84qnk17jxobmy8b; Integrateactivity=notincludemc; newhouse_user_guid=50E5E180-78E4-4D10-DD8D-77E13BC96848; lastscanpage=0; budgetLayer=1%7Cbj%7C2019-07-30%2011%3A26%3A08; resourceDetail=1; new_search_uid=fd91130e51ddd1f2d8e5a7847545c3d8; __utmc=147393320; __utma=147393320.184954923.1564457033.1564642303.1564646708.12; __utmz=147393320.1564646708.12.5.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-verify/redirect; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; logGuid=cb4c3441-3467-4c19-ba09-1dd86b143529; g_sourcepage=ehlist; city=anshan; unique_cookie=U_11rfckz759men2uard7dzzy1i1ejys2c6di*36; __utmb=147393320.15.10.1564646708",
    "Referer": "https://esf.fang.com/newsecond/esfcities.aspx",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
}

def get_html(url):
    try:
        response = requests.get(url, headers=headers, timeout=2)
        encod = response.apparent_encoding
        if encod.upper() in ['GB2312', 'WINDOWS-1254']:
            encod = 'gbk'
        response.encoding = encod
        return response
    except Exception as e:
        pass


class Esf_FTX:
    def __init__(self, year, month, pool):
        self.year = year
        self.month = month
        self.pool = pool

    # def get_exists_dists(self, month):
    #     """
    #      查看当月已经存的城市行政区
    #     """
    #     print('等待获取当前月已经抓取的城市列表......')
    #     # TODO 连接本地电脑
    #     # engine = create_engine('postgresql://postgres:123456@127.0.0.1/ESF').connect()
    #     # TODO 连接NAS
    #     engine = create_engine('postgresql://postgres:1q2w3e4r@192.168.88.254:15432/ESF').connect()
    #     # TODO, 年份不同修改 表名
    #     sql = f"""SELECT distinct "城市", "区县" FROM public."Esf_2021" where 抓取月份={month} and 数据来源='房天下';"""
    #     df = pd.read_sql_query(sql=sql, con=engine)
    #     engine.close()
    #     print(f'已经抓取城市数量: {df["城市"].unique().shape}')
    #     return df

    def get_everyone_city_region(self, df, city):
        """生成每一个城市已经获取的region"""
        exists_city_df = df[df['城市'] == city]
        if not exists_city_df.shape[0]:
            exists_region = []
        else:
            exists_region = exists_city_df['区县'].tolist()
        return exists_region

    def get_dist(self, city, GetType):
        """
        生成行政区字典
        """
        number = 9
        while number > 0:
            try:
                dist = make_url(city, 'https://{}.esf.fang.com/{}/', GetType)
                return dist

            except:
                number -= 1
                continue

    def get_data(self, baseUrl, city, dist, pageNumber, currPage, data=None):
        """
        解析每一个页面
        """
        number_tz = 0
        while True:
            gen_url = baseUrl
            has_spider_urlList = []
            for has_spider_url in has_spider.find():
                has_spider_urlList.append(has_spider_url['标题'])
            if gen_url in has_spider_urlList:
                print('该页数据已爬取，下一页')
                break


            # response = get_Html_IP(gen_url, headers=headers)
            res = get_html(gen_url)
            if res:
                tree = etree.HTML(res.text)
            else:
                break

            number_tz += 1
            if "跳转" in tree.xpath("//title/text()"):
                if number_tz > 4:
                    break
                print('没有获取到真正的页面')
                continue

            house_box = tree.xpath("//div[@class='shop_list shop_list_4']/dl[@dataflag='bg']")
            if house_box:
                print(f"城市：{city} {dist}, 状态：有数据，共{pageNumber}页，当前第{currPage}页")

            for house in house_box:
                item_dict = {}
                item_dict['id'] = uuid.uuid1(node=random.randint(999, 999999))
                item_dict['标题url'] = gen_url + house.xpath('.//dt[@class="floatl"]/a/@href')[0]
                contents = house.xpath(".//p[@class='tel_shop']/text()")

                for cont in contents:
                    conts = cont.replace(" ", "").replace('\n', '').replace('\r', '')
                    if '室' in conts:
                        item_dict['户型'] = "".join(re.findall("\d室?\d厅?", conts))
                    if "�" in conts or "㎡" in conts:
                        item_dict['面积'] = "".join(re.findall("(\d+\.?\d+)", conts))
                    if '层' in conts:
                        item_dict['楼层'] = conts.strip()
                    if '南' in conts or '北' in conts or '东' in conts or '西' in conts:
                        item_dict['朝向'] = conts.strip()
                    if '建' in conts:
                        item_dict['建筑年份'] = "".join(re.findall("(\d+)年", conts))

                if "建筑年份" not in item_dict.keys():
                    item_dict['建筑年份'] = None
                elif "户型" not in item_dict.keys():
                    item_dict['户型'] = None
                elif "面积" not in item_dict.keys():
                    item_dict['面积'] = None
                elif "楼层" not in item_dict.keys():
                    item_dict['楼层'] = None
                elif "朝向" not in item_dict.keys():
                    item_dict['朝向'] = None

                try:
                    item_dict['小区'] = house.xpath(".//p[@class='add_shop']/a/@title")[0]
                except:
                    return

                # 地址
                try:
                    item_dict['地址'] = house.xpath(".//p[@class='add_shop']/span/text()")[0]
                except:
                    item_dict['地址'] = None

                try:
                    item_dict['总价'] = house.xpath(".//dd[@class='price_right']/span[@class='red']/b/text()")[0].replace(
                        '$',
                        '')
                    unit_price = house.xpath(".//dd[@class='price_right']/span[2]/text()")[0]
                    item_dict['单价'] = "".join(re.findall("(\d+\.?\d+)元", unit_price)).replace('$', '')
                except:
                    print('error!!, 单价错误')
                    item_dict['总价'] = None
                    item_dict['单价'] = None

                # 标签
                item_dict['标签'] = "|".join(house.xpath(".//p[@class='clearfix label']//span/text()"))
                item_dict['抓取时间'] = f'{self.year}-{self.month}-28'
                item_dict['抓取年份'] = self.year
                item_dict['抓取月份'] = self.month
                item_dict['数据来源'] = '房天下'

                item_dict['城市'] = city
                item_dict['区县'] = dist
                item_dict['关注人数'] = None  # followInfo
                item_dict['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                data.append(item_dict)
                print(item_dict)
                info_base.insert_one(item_dict)
            has_spider.insert_one({'标题': gen_url})
            return data
        return

    def get_page(self, city, dist_dict, GetType, exists_region):
        """
        获取每个区下的页面
        """
        for dist_url, dist in dist_dict.items():

            # if dist in exists_region or dist in get_exists_dist(city, GetType):
            #     print(city, dist, '----->  已经存在')
            #     continue

            base_url = re.findall("https.*com", dist_url)[0]
            print("base_url: ", base_url, "dist_url: ", dist_url)  # https://abazhou.esf.fang.com
            number_tz = 0
            while True:
                res = get_html(dist_url)
                if res:
                    tree = etree.HTML(res.text)
                else:
                    break
                # 没有请求到正确的页面
                number_tz += 1
                if '跳转' in tree.xpath("//title/text()")[0]:
                    print(tree.xpath("//title/text()")[0], "%s :出现跳转页面" % dist)
                    if number_tz > 3:
                        break
                    continue

                page_number = tree.xpath("//div[@class='page_al']/p[last()]/text()") or \
                              tree.xpath("//div[@class='page_al']/span[contains(text(), '共')]/text()")

                print('pagenum',page_number)


                if len(page_number) < 1:
                    print(tree.xpath('//title/text()'))
                    # save_grab_dist(city, dist, dist_url, GetType)
                    print("没有数据")
                    break

                page_number = int(page_number[0][1:-1])

                l, data = [], []
                for i in range(1, page_number + 1):
                    url = dist_url + f'i3{i}/'

                    done = self.pool.submit(self.get_data, url, city, dist, page_number, i, data)
                    l.append(done)
                [obj.result() for obj in l]
                print("最终数据量: ", len(data))

                # try:
                #     useTime = saveData(data, city, GetType)  # 保存数据
                #     print("数据保存成功, 用时: ", useTime)
                # except Exception as e:
                #     print('城市: %s, 区域: %s, 数据保存失败, %s' % (city, dist, e))
                break

    def run(self, city_map):
        # df = self.get_exists_dists(self.month)

        print(len(city_map))
        for city, city_code in city_map.items():
            # exists_region = self.get_everyone_city_region(df, city)
            exists_region = []

            if city in ["罗定", "阿坝州", "农安", "怒江", "盘锦", '香港', '海南省']: continue
            if city in ['安达', '安宁', '安丘', '安溪', '宝应', '巴彦', '霸州', '三河', '三沙', '商河', '尚志', '韶山',
                        '宾县', '宾阳', '博罗', '长岛', '长丰', '长乐', '昌乐', '昌黎', '常宁', '长清', '长寿', '昌邑', '巢湖',
                        '崇州', '淳安', '当涂', '当阳', '大邑', '大足', '德化', '德惠', '登封', '邓州', '垫江', '定兴', '定州',
                        '东方', '东港', '东海', '东台', '都江堰', '法库', '繁昌', '肥城', '肥东', '肥西', '凤城', '丰都', '奉化',
                        '奉节', '丰县', '福安', '涪陵', '阜宁', '富阳', '高淳', '高陵', '巩义', '公主岭', '广饶', '固镇', '海安',
                        '海城', '海拉尔', '海林', '汉南', '合川', '桦甸', '怀仁', '怀远', '惠安', '惠东', '霍邱', '户县', '建德',
                        '江都', '江津', '姜堰', '简阳', '胶南', '胶州', '即墨', '靖安', '靖江', '京山', '金湖', '金坛', '金堂',
                        '进贤', '晋州', '济阳', '蓟州', '冀州', '开县', '开阳', '康平', '库尔勒', '奎屯', '莱芜', '莱西', '莱阳',
                        '莱州', '兰考', '蓝田', '老河口', '耒阳', '乐亭', '梁平', '连江', '辽中', '醴陵', '临安', '临海', '临清',
                        '临朐', '临猗', '浏阳', '溧阳', '龙海', '栾川', '滦南', '滦县', '庐江', '洛宁', '罗源', '孟津', '闽清',
                        '南安', '宁海', '蓬莱', '平度', '平山', '平潭', '平阴', '普兰店', '普宁', '迁安', '黔江', '迁西', '綦江',
                        '青龙', '清徐', '清镇', '青州', '邛崃', '栖霞', '泉港', '泉山', '荣昌', '如东', '瑞安', '瑞金', '汝阳']:  # 没有区县数据, 不要
                continue

            start = time.time()
            dist = self.get_dist(city, GetType="二手房")
            # print(dist)
            self.get_page(city, dist, GetType="二手房", exists_region=exists_region)
            print("抓取%s 总用时: %s" % (city, time.time() - start))


if __name__ == '__main__':
    # TODO 二手房启动程序
    # TODO 请删除 log>lose_dist 中的缓存记录
    # TODO 修改 Month为当前要抓取的月份
    Year = 2021
    Month = 4

    Pool = ThreadPoolExecutor(20)
    Esf_FTX(year=Year, month=Month, pool=Pool).run(city_map)
    Pool.shutdown()
