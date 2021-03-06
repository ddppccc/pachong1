import json
import random
import re
import time
import uuid
from urllib import parse

import pandas as pd
import pymongo
import requests

from lxml import etree
from concurrent.futures.thread import ThreadPoolExecutor
from sqlalchemy import create_engine
from requests.adapters import HTTPAdapter
from config import write_to_table, cities

MONGODB_CONFIG = {
    "host": "8.135.119.198",
    "port": "27017",
    "user": "hladmin",
    "password": parse.quote("Hlxkd3,dk3*3@"),
    "db": "dianping",
    "collections": "dianping_collections",
}

# 建立连接
info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['贝壳']['小区_数据_202111']

url_data = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['贝壳']['小区_url_202111']

data_list = []


class Community_BeiKe:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        # 'Host': 'cq.ke.com',
        "Accept-Language": "zh-CN,zh;q=0.9",
        "upgrade-insecure-requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        # 'cookie': "lianjia_uuid=bfa7ceba-65ca-4e1e-b591-2fec6f15129c; crosSdkDT2019DeviceId=-pal2xu-di1vvg-q4phzhoefy25s8p-yfip8uyx7; _ga=GA1.2.1314769215.1585729030; ke_uuid=dcb5976f4b3634b4a8bcab004ed5d775; _smt_uid=5e8452ec.5a19fece; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217134e3ece7149-0b39f3df5eee65-6701b35-1327104-17134e3ece837b%22%2C%22%24device_id%22%3A%2217134e3ece7149-0b39f3df5eee65-6701b35-1327104-17134e3ece837b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wyshenzhen%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; __xsptplus788=788.7.1592811193.1592811569.3%234%7C%7C%7C%7C%7C%23%23m3PY-nFnYwlqfjOVPI_Sk2ie3bc2rPsa%23; select_city=320200; lianjia_ssid=ca885273-46e1-48d4-a1be-a36fa1cffa99; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1594089381; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1594089399; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiOWQ4ODYyNmZhMmExM2Q0ZmUxMjk1NWE2YTRjY2JmODZkNTdmNDQ1NmNhMDA5OWRmOTM1YjJhOTU0NDFjYzMzYjg3Yjk5YjZmODc3OTRmYmRlY2VmYjFmODQyMGIyOTA5YWE3NDcxMjM0N2FhMDdhMDRjNDUzMDkyNWI1MDk2ZTAxN2RjYTIzYjMyMGZhMTM3NjkyYjYyNjMwOTE1OWZhZDFjMTI4NGMxZTk1MWY1ZTMyMmYxMmEwZTI4MTg5MDJjZjAwOGI2MDNiOWExMWNlNjhkMTkyN2VjYjcwODE2MTc5YmY4OGUxODZiYWQ1MDhjZjkyODM2YjU0YTBkYzI4M2RiNDA4ZWI0MzMyNTFjYWQyNzliNGYwMzA1ZGI0Njc4YTYxZDU5OTQzYTBlOGVhNTA3NWZkY2E3MDE2ODczYjNiOTQ2MzNmZjM3M2FhMmE2Y2JjMjFiYWUxNmU2MzA2ZVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJjY2E0ZTVlOFwifSIsInIiOiJodHRwczovL3d4LmtlLmNvbS94aWFvcXUvNDEyMDAzNDQwNDAyMDUwMC8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==",

    }

    def __init__(self, year, month):
        self.year = year
        self.month = month

    def get_regions(self, city_code, proxieslist):
        """
        根据城市名获得行政区
        :return: {'guangming': '光明'}, CHENFJIAO  [True/False]
        """
        # url = 'https://{}.ke.com/xiaoqu/'.format(city_code)
        url = city_code
        response, proxieslist = self.get_html(url, proxieslist)
        html = etree.HTML(response)
        try:
            regions_xpath = "//div[@data-role='ershoufang']/div/a"
            regions = dict(zip(html.xpath(regions_xpath + '/text()'), html.xpath(regions_xpath + '/@href')))
            xiaoqu_url = url + '{}/'
            regions = {key: xiaoqu_url.format(value.rsplit('/', 2)[1]) for key, value in regions.items()}
            return regions, proxieslist
        except Exception as e:
            print('get_html: ', e, url)
            regions, proxieslist = self.get_regions(city_code, proxieslist)
            return regions, proxieslist

    # def fetch_html(self, url ):
    #     '''获取页面代码'''
    #     number = 3
    #     while number > 0:
    #         try:
    #             res = requests.get(url, headers=self.headers, timeout=7)
    #             res.encoding = 'utf-8'
    #             if '人机认证' in res.text:
    #                 print('需要人机验证: ', res.url)
    #                 time.sleep(70)
    #                 continue
    #             if res.status_code == 404:
    #                 print('返回状态码404, ', url)
    #                 return ' '
    #
    #             return res.text
    #         except Exception as e:
    #             number -= 1
    #             print('fetch_html: ', e, url)
    #             continue
    #     return ''

    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))  # 设置重试次数为3次
    s.mount('https://', HTTPAdapter(max_retries=3))

    def get_proxy(self):
        while True:
            try:
                # return requests.get('http://1.116.204.248:5000/proxy').text
                return requests.get('http://47.106.223.4:50002/get/').json().get('proxy')

            except:
                print('暂无ip，等待20秒')
                time.sleep(20)

    def get_html(self, url, proxieslist):
        s = 0
        while True:
            try:
                if len(proxieslist) > 0:
                    proxies = proxieslist
                else:
                    proxy = self.get_proxy()
                    proxies = {"https": proxy}
                response = requests.get(url, headers=self.headers, proxies=proxies, timeout=10)
                encod = response.apparent_encoding
                if encod.upper() in ['GB2312', 'WINDOWS-1254']:
                    encod = 'gbk'
                response.encoding = encod
                # html = etree.HTML(response.text)
                if '人机认证' in response.text:
                    print('该IP需要人机验证: ', proxieslist)
                    proxieslist = []
                    continue
                proxieslist = proxies
                print(s, proxies, '获取成功')
                return response.text, proxieslist
            except Exception as e:
                s += 1
                proxieslist = []

                # print('get_html错误', e)
                continue
        return '', proxieslist

    # def get_html(self, url):
    #     for i in range(20):
    #         proxy = self.get_proxy()
    #         try:
    #             response = requests.get(url, headers=self.headers, proxies={"https": proxy, "http": proxy},
    #                                     timeout=(3, 5))
    #             encod = response.apparent_encoding
    #             if encod.upper() in ['GB2312', 'WINDOWS-1254']:
    #                 encod = 'gbk'
    #             response.encoding = encod
    #             # html = etree.HTML(response.text)
    #             print('获取成功')
    #             return response.text
    #         except Exception as e:
    #             print('get_html错误', proxy, e)
    #             time.sleep(2)
    #     return ''
    def get_city(self, proxieslist):
        """
        根据城市名获得行政区
        :return: {'guangming': '光明'}, CHENFJIAO  [True/False]
        """
        url = 'https://www.ke.com/city/'
        res,proxieslist = self.get_html(url, proxieslist)
        html = etree.HTML(res)
        sx = html.xpath(
            "//ul[@class='city_list_ul']/li[@class='city_list_li city_list_li_selected']//ul/li/@data-action")  #
        city = {}
        for sxz in sx:
            if '国内城市' in sxz:
                citys = html.xpath(
                    "//ul[@class='city_list_ul']/li[@class='city_list_li city_list_li_selected']//ul/li[@data-action='%s']/a/text()" % sxz)
                hrefs = html.xpath(
                    "//ul[@class='city_list_ul']/li[@class='city_list_li city_list_li_selected']//ul/li[@data-action='%s']/a/@href" % sxz)  # 有.fang的没有二手房
                city[citys[0]] = 'https:' + hrefs[0] + '/xiaoqu/'
        # print(city)
        return city
    def get_street_page_url(self, url, proxieslist, **kwargs):
        ''' 获取街道下的页面详情'''
        city, region, street = kwargs['城市'], kwargs['区县'], kwargs['街道']
        street_url = kwargs['街道url']
        data_list = kwargs['data_list']

        html, proxieslist = self.get_html(url, proxieslist)
        if not html: return proxieslist
        tree = etree.HTML(html)
        try:
            number = tree.xpath("//h2[@class='total fl']/span/text()")[0].strip()
        except:
            number = '0'
        if number == '0':
            return proxieslist

        print(city, region, street, tree.xpath("string(//h2[@class='total fl'])"))
        # 下一页
        next_page = tree.xpath("//div[@class='page-box house-lst-page-box']/@page-data")[0]
        totalPage = int(json.loads(next_page)["totalPage"])

        # 请求所有页面
        for i in range(totalPage):
            curPage = i + 1
            next_page_url = street_url + 'pg' + str(curPage) + '/'
            print('当前页面url: ', next_page_url)
            proxieslist = self.get_list_page(next_page_url, proxieslist, city, region, data_list)
        return proxieslist

    def get_page_url(self, url, proxieslist, **kwargs):
        ''' 获取行政区的下的页面详情 '''
        city, region, region_url = kwargs['城市'], kwargs['区县'], kwargs['区县url']
        html, proxieslist = self.get_html(url, proxieslist)
        if not html: return proxieslist
        tree = etree.HTML(html)
        try:
            number = tree.xpath("//h2[@class='total fl']/span/text()")[0].strip()
        except:
            return proxieslist

        global data_list
        if number == '0':
            return proxieslist
        if int(number) > 3000:
            street_xpath = "//div[@data-role='ershoufang']/div[2]//a"
            street_base_url = kwargs['区县url'].split('/xiaoqu')[0]
            street_dict = dict(zip(tree.xpath(street_xpath + '/text()'), tree.xpath(street_xpath + '/@href')))

            for street, value in street_dict.items():
                street_url = street_base_url + value
                proxieslist = self.get_street_page_url(street_url, proxieslist, 城市=city, 区县=region, 街道=street,
                                                       街道url=street_url,
                                                       data_list=data_list)
            return proxieslist

        else:
            print(city, region, region_url, tree.xpath("string(//h2[@class='total fl'])"))
            next_page = tree.xpath("//div[@class='page-box house-lst-page-box']/@page-data")[0]
            totalPage = int(json.loads(next_page)["totalPage"])

            # 请求所有页面
            for i in range(totalPage):
                curPage = i + 1
                next_page_url = region_url + 'pg' + str(curPage) + '/'
                print('当前页面url: ', next_page_url)
                proxieslist = self.get_list_page(next_page_url, proxieslist, city, region, data_list)

        print("当前小区的数量: ", len(data_list))
        return proxieslist

    def get_list_page(self, url, proxieslist, city, region, data_list):
        '''获取每一页列表页数据'''
        if url_data.find_one({'url': url}):
            print('当前url已爬取', url)
            return proxieslist
        html, proxieslist = self.get_html(url, proxieslist)
        if not html: return proxieslist
        tree = etree.HTML(html)
        houses = tree.xpath("//ul[@log-mod='list']/li[@class='clear xiaoquListItem CLICKDATA']")
        p = []
        for house in houses:
            data = {}
            data['城市'] = city
            data['区县'] = region
            data['小区'] = house.xpath(".//div[@class='title']/a/@title")[0]
            data['小区url'] = house.xpath(".//div[@class='title']/a/@href")[0]
            houseInfo = house.xpath(".//div[@class='houseInfo']/a/text()")
            data['成交情况'] = "".join([i for i in houseInfo if '成交' in i])
            data['再租套数'] = "".join(["".join(re.findall("\d+", i)) for i in houseInfo if '出租' in i])

            data['地址'] = "-".join(house.xpath(".//div[@class='positionInfo']//a/text()"))
            data['建筑年份'] = "".join(
                re.findall("\d+", re.sub("\s+", "", "".join(house.xpath(".//div[@class='positionInfo']/text()")))))

            # 标签
            data['标签'] = "".join(house.xpath(".//div[@class='tagList']/span/text()"))
            data['单价'] = "".join(
                re.findall("\d+\.?\d+", house.xpath("string(.//div[@class='totalPrice']/span/text())")))
            data['单价描述'] = "".join(house.xpath(".//div[@class='priceDesc']/text()"))
            data['在售套数'] = house.xpath(".//div[@class='xiaoquListItemSellCount']/a/span/text()")[0]
            data['抓取月份'] = self.month
            data['抓取年份'] = self.year
            print(data)
            if data['小区url'] == 'https://wx.ke.com/xiaoqu/4120034740837231/':
                continue
            # proxieslist = self.get_page_information(data['小区url'], proxieslist, data, data_list)
            done = pool.submit(self.get_page_information, data['小区url'], proxieslist, data, data_list)
            p.append(done)
        url_data.insert_one({'url': url})
        [obj.result() for obj in p]

    def get_page_information(self, url, proxieslist, item, data_list):
        ''' 获取每一页列表页数据 '''
        html, proxieslist = self.get_html(url, proxieslist)
        if not html: return proxieslist
        response = etree.HTML(html)
        try:
            xiaoquInfoItem = response.xpath("//div[@class='xiaoquInfo']/div[@class='xiaoquInfoItem']")
        except Exception as e:
            print("小区详情error ", e)
            return proxieslist
        try:
            location = re.findall("resblockPosition:'(.*)',", html)[0]
            item['longitude'], item['latitude'] = location.split(",")
        except:
            item['longitude'], item['latitude'] = '', ''
        for infoItem in xiaoquInfoItem:
            if infoItem.xpath("./span[@class='xiaoquInfoLabel']/text()")[0] == '建筑类型':
                item['建筑类型'] = infoItem.xpath("./span[@class='xiaoquInfoContent']/text()")[0]
            elif infoItem.xpath("./span[@class='xiaoquInfoLabel']/text()")[0] == '物业费用':
                item['物业费用'] = infoItem.xpath("./span[@class='xiaoquInfoContent']/text()")[0].strip()
            elif infoItem.xpath("./span[@class='xiaoquInfoLabel']/text()")[0] == '物业公司':
                item['物业公司'] = infoItem.xpath("./span[@class='xiaoquInfoContent']/text()")[0].strip()
                # print('物业公司', property_company)
            elif infoItem.xpath("./span[@class='xiaoquInfoLabel']/text()")[0] == '开发商':
                item['开发商'] = infoItem.xpath("./span[@class='xiaoquInfoContent']/text()")[0].strip()
            elif infoItem.xpath("./span[@class='xiaoquInfoLabel']/text()")[0] == '楼栋总数':
                item['楼栋总数'] = infoItem.xpath("./span[@class='xiaoquInfoContent']/text()")[0].strip()
            elif infoItem.xpath("./span[@class='xiaoquInfoLabel']/text()")[0] == '房屋总数':
                item['房屋总数'] = infoItem.xpath("./span[@class='xiaoquInfoContent']/text()")[0].strip()
            item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        data_list.append(item)
        info_base.insert_one(item)

    # 启动
    def run_community(self):
        # df = self.get_exists_dist(self.month)
        proxieslist = {}
        cities = self.get_city(proxieslist)
        for city, city_code in cities.items():
            if city in ['江阴']:
                continue
            if url_data.count({city: '已爬取'}):
                print('当前城市已爬取：', city)
                continue
            elif url_data.count({city: '正在爬取'}):
                print('当前城市正在爬取：', city)
                continue
            url_data.insert_one({city: '正在爬取'})
            # if city not in ['丹东']: continue
            # exists_region = self.get_everyone_city_region(df, city)
            self.headers['Host'] = '{}.ke.com'.format(city_code)
            regions, proxieslist = self.get_regions(city_code, proxieslist)  # 生成行政区列表
            if not regions:
                continue

            for region, region_url in regions.items():
                if city + '_' + region in ['广州_南海', '广州_顺德', '佛山_番禺', '佛山_白云']:
                    continue
                print(city, region, region_url)
                # if region in exists_region or '周边' in region:
                #     print(city, region, '----->  已经存在')
                #     continue
                data_dict = {}
                data_dict['城市'] = city
                data_dict['区县'] = region
                data_dict['区县url'] = region_url
                proxieslist = self.get_page_url(region_url, proxieslist, **data_dict)
            url_data.insert_one({city: '已爬取'})


if __name__ == '__main__':
    # TODO 修改抓取时间, 年份不同, 请注意插入he查询的的表的名称
    Year = time.localtime(time.time()).tm_year
    Month = time.localtime(time.time()).tm_mon

    pool = ThreadPoolExecutor(20)
    Community_BeiKe(year=Year, month=Month).run_community()
    pool.shutdown()
