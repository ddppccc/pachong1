import datetime
import json
import os
import random
import re
import time
import uuid
from urllib import parse

import requests
from lxml import etree
import numpy as np
import pymongo
import scrapy

from beike_map import get_regions, get_esf_code_map
from city_spider import crawl_city_process
from city_spider import cities
from config import make_date

year, month, day = make_date()

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
            retryWrites="false")['贝壳']['ESF']

url_data = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['贝壳']['esf_url']



class Spider(scrapy.Spider):
    name = "BeiKe_esf"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        # 'Host': 'cq.ke.com',
        "Accept-Language": "zh-CN,zh;q=0.9",
        "upgrade-insecure-requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        'cookie': "lianjia_uuid=bfa7ceba-65ca-4e1e-b591-2fec6f15129c; crosSdkDT2019DeviceId=-pal2xu-di1vvg-q4phzhoefy25s8p-yfip8uyx7; _ga=GA1.2.1314769215.1585729030; ke_uuid=dcb5976f4b3634b4a8bcab004ed5d775; _smt_uid=5e8452ec.5a19fece; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217134e3ece7149-0b39f3df5eee65-6701b35-1327104-17134e3ece837b%22%2C%22%24device_id%22%3A%2217134e3ece7149-0b39f3df5eee65-6701b35-1327104-17134e3ece837b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wyshenzhen%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; __xsptplus788=788.7.1592811193.1592811569.3%234%7C%7C%7C%7C%7C%23%23m3PY-nFnYwlqfjOVPI_Sk2ie3bc2rPsa%23; select_city=320200; lianjia_ssid=ca885273-46e1-48d4-a1be-a36fa1cffa99; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1594089381; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1594089399; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiOWQ4ODYyNmZhMmExM2Q0ZmUxMjk1NWE2YTRjY2JmODZkNTdmNDQ1NmNhMDA5OWRmOTM1YjJhOTU0NDFjYzMzYjg3Yjk5YjZmODc3OTRmYmRlY2VmYjFmODQyMGIyOTA5YWE3NDcxMjM0N2FhMDdhMDRjNDUzMDkyNWI1MDk2ZTAxN2RjYTIzYjMyMGZhMTM3NjkyYjYyNjMwOTE1OWZhZDFjMTI4NGMxZTk1MWY1ZTMyMmYxMmEwZTI4MTg5MDJjZjAwOGI2MDNiOWExMWNlNjhkMTkyN2VjYjcwODE2MTc5YmY4OGUxODZiYWQ1MDhjZjkyODM2YjU0YTBkYzI4M2RiNDA4ZWI0MzMyNTFjYWQyNzliNGYwMzA1ZGI0Njc4YTYxZDU5OTQzYTBlOGVhNTA3NWZkY2E3MDE2ODczYjNiOTQ2MzNmZjM3M2FhMmE2Y2JjMjFiYWUxNmU2MzA2ZVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJjY2E0ZTVlOFwifSIsInIiOiJodHRwczovL3d4LmtlLmNvbS94aWFvcXUvNDEyMDAzNDQwNDAyMDUwMC8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==",

    }

    def start_requests(self):

        self.city_name = self.settings.get("city_name", '全国')
        city_names = list(filter(lambda x: self.city_name in x, cities))
        # print("city_names", city_names)
        # if info_base.find_one({"城市": city_names}):
        #     print("这个城市正在抓或者已经抓过了: %s" % self.city_name)
        #     return
        if not city_names:
            print("没有找到城市: %s" % self.city_name)
            return

        # 有数据  生成区县字典
        regions, cj = get_regions(self.city_name, cities)
        city_name = self.city_name
        for region_name, base_url in regions.items():
            for i in range(1,101):
                url = base_url+"pg"+str(i)+"/"
                yield scrapy.Request(url=url,
                                     callback=self.parse,
                                     meta={
                                         'item': {'base_url': base_url,
                                                  'region_name': region_name,
                                                  'city': city_name}
                                     })


    def fetch_html(self, url ):

        '''获取页面代码'''
        number = 3
        while number > 0:
            try:
                res = requests.get(url, headers=self.headers, timeout=7)
                res.encoding = 'utf-8'
                if '人机认证' in res.text:
                    print('需要人机验证: ', res.url)
                    time.sleep(70)
                    continue
                if res.status_code == 404:
                    print('返回状态码404, ', url)
                    return ' '

                return res.text
            except Exception as e:
                number -= 1
                print('fetch_html: ', e, url)
                continue
        return ''

    # 获取district详情信息
    def parse(self, response):

        # with open("city_href.json", 'r', encoding='utf-8') as fp:
        #     cities = json.loads(fp.read())
        # for ke in cities.keys():
        #     print()
        #     url = 'https://' + cities[ke] + '/ershoufang/'
        #     res = self.fetch_html(url)
        #     html = etree.HTML(res)
        #     sx = html.xpath("//div[@data-role='ershoufang']/div/a/@title")
        #     for sxz in sx:
        #         city = ke
        #         district = html.xpath("//div[@data-role='ershoufang']/div/a[@title='%s']/text()" % sxz)[0]
        #         dist_url = html.xpath("//div[@data-role='ershoufang']/div/a[@title='%s']/@href" % sxz)[0][12:]





        item = response.meta['item']
        city = item['city']
        district = item['region_name']
        dist_url = item['base_url']
        print(item)
        print('dist_url',dist_url)
        # 换成自己的
        # res = self.fetch_html(dist_url)
        # response = etree.HTML(res)
        # self.parse(response)










        if '人机认证' in response.text:
            print('需要人机验证: ', response.url)
            time.sleep(60*10)   # 等待自己消失

        houses = response.xpath("//ul[@log-mod='list']//li[@class='clear']")
        print(response.url)
        if houses:
            for house in houses:
                items = {}
                items['id'] = uuid.uuid1(node=random.randint(100, 9999999))
                items['城市'] = city
                items['区县'] = district
                items['标题url'] = house.xpath(".//div[@class='title']/a/@href").get()
                if url_data.find_one({'url': items['标题url']}):
                    print('当前url已爬取')
                    continue
                items['小区'] = house.xpath(".//div[@class='positionInfo']/a/text()").get()
                houseInfo = "".join(house.xpath("./div/div[2]/div[2]/text()").extract()).replace(" ", "").replace("\n", "")

                # 户型
                items['户型'] = "".join(re.findall('\d室\d{0,1}厅{0,1}', ''.join([type_info for type_info in houseInfo.split('|') if '室' in type_info])))
                if len(items['户型']) == 0:
                    items['户型'] = np.NaN

                # 面积
                area = "".join(re.findall('(\d+\.?\d+)平米', "".join([type_info for type_info in houseInfo.split('|') if '米' in type_info])))
                try:
                    items['面积'] = float(area)
                except:
                    items['面积'] = np.NaN

                # 楼层
                items['楼层'] = "".join(re.findall("(.*\))", "".join([type_info for type_info in houseInfo.split('|') if '层' in type_info])))
                if len(items['楼层']) == 0:
                    items['楼层'] = np.NaN

                # 建筑年份
                houseYear = "".join(re.findall('(\d+)年', ''.join( [type_info for type_info in houseInfo.split('|') if '建' in type_info])))
                try:
                    items['建筑年份'] = int(houseYear)
                except:
                    items['建筑年份'] = np.NaN

                # 朝向
                items['朝向'] = "".join(
                    ''.join([type_info for type_info in houseInfo.split('|') if '东' in type_info or '西' in type_info \
                             or '南' in type_info or '北' in type_info]))
                if len(items['朝向']) == 0:
                    items['朝向'] = np.NaN

                flower = "".join(house.xpath("./div/div[2]/div[3]/text()").extract()).replace(" ", "").replace("\n", "")
                items['关注人数'] = ''.join(re.findall('(\d+)人', flower))
                if len(items['关注人数']) == 0:
                    items['关注人数'] = np.NaN

                # 标签
                items['标签'] = "|".join(house.xpath("./div/div[2]/div[4]/span/text()").extract())
                if len(items['标签']) == 0:
                    items['标签'] = np.NaN

                # 总价
                try:
                    totalPrice = house.xpath(".//div[@class='totalPrice']/span/text()").get().strip()
                    items['总价'] = float(totalPrice)
                except:
                    try:
                        totalPrice = house.xpath(".//div[@class='totalPrice totalPrice2']/span/text()").get().strip()
                        items['总价'] = float(totalPrice)
                    except:
                        items['总价'] = np.NaN
                # totalPrice = "".join(re.findall('(\d+\.?\d+)万', str(totalPrice)))
                # try:
                #     items['总价'] = float(totalPrice)
                # except:
                #     items['总价'] = np.NaN

                # 单价
                try:
                    unitPrace = house.xpath(".//div[@class='unitPrice']/span/text()").get().strip()
                    unitPrace = "".join(re.findall('(\d+\.?\d+)元', unitPrace))
                    try:
                        items['单价'] = float(unitPrace)
                    except:
                        items['单价'] = np.NaN
                except:
                    items['单价'] = np.NaN

                items['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                items['数据来源'] = '贝壳'

                items['地址'] = items['城市']+items['区县']+items['小区']
                items['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                info_base.insert_one(items)
                url_data.insert_one({'url': items['标题url']})
                print(items)
                yield items


            # next_page = json.loads(response.xpath("//div[@class='page-box house-lst-page-box']/@page-data").get())
            # next_page1 = response.xpath("//div[@class='pagination_group_a']/a")
            # totalPage = next_page['totalPage']
            # curPage = next_page['curPage']
            # print('当前页',curPage)
            # for i in range(curPage, totalPage + 1):
            #     curPage = i + 1
            #     if curPage > totalPage:
            #         print(f'{district}\t总页数：{totalPage}, 已经爬完')
            #         return
            #     else:
            #         print(f'当前城市：{city},\t当前区：{district},\t总页数：{totalPage}, 当前页：{curPage}')
            #         next_page_url = dist_url + 'pg' + str(curPage) + '/'
            #         print(next_page_url)
            #         yield scrapy.Request(url=next_page_url, callback=self.parse,dont_filter=True)
                    #return scrapy.Request(url=sum, callback=self.parse, meta={'item': items})
                # break
        #













if __name__ == '__main__':
    # TODO 每个月跑程序之前 清理下上个月缓存的数据 位置: data/esf
    # TODO 修改每月抓取时间(可自定义), 位置 config >> make_date

    # 生成最新的esf映射表
    get_esf_code_map()

    # params = {
    #     'save_dir': "data/esf",  # 保存位置
    #     'save_name': 'beke_esf'  # 保存数据名,
    #    }

    for city_name in cities:  #
        print("城市: ", city_name)
        p = crawl_city_process(city_name, Spider)
        if p:
            p.start()
            p.join()