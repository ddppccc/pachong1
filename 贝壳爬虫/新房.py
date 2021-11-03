# coding:utf-8
import re
import math
from urllib import parse
import time
import pymongo
import requests
import pandas as pd
from lxml import etree
from requests.adapters import HTTPAdapter
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
            retryWrites="false")['贝壳']['新房_数据_202111']

url_data = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['贝壳']['新房_url_202111']


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
        s = 0
        while True:
            try:
                if len(proxieslist) > 0:
                    proxies = proxieslist
                else:
                    proxy = self.get_proxy()
                    proxies = {"https": proxy}
                res = requests.get(url, headers=headers, params=params, proxies=proxies, timeout=(3, 5)).json()
                print(s, proxies, '获取成功')
                return res, proxieslist
            except Exception as e:
                # print('error!!! ', url, params, e)
                proxieslist = {}
                s += 1
                continue

    def fetch_html(self, url):
        '''获取页面代码'''
        number = 3
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            # 'Host': 'www.ke.com',
            "Accept-Language": "zh-CN,zh;q=0.9",
            "upgrade-insecure-requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            # 'cookie': "lianjia_uuid=bfa7ceba-65ca-4e1e-b591-2fec6f15129c; crosSdkDT2019DeviceId=-pal2xu-di1vvg-q4phzhoefy25s8p-yfip8uyx7; _ga=GA1.2.1314769215.1585729030; ke_uuid=dcb5976f4b3634b4a8bcab004ed5d775; _smt_uid=5e8452ec.5a19fece; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217134e3ece7149-0b39f3df5eee65-6701b35-1327104-17134e3ece837b%22%2C%22%24device_id%22%3A%2217134e3ece7149-0b39f3df5eee65-6701b35-1327104-17134e3ece837b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wyshenzhen%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; __xsptplus788=788.7.1592811193.1592811569.3%234%7C%7C%7C%7C%7C%23%23m3PY-nFnYwlqfjOVPI_Sk2ie3bc2rPsa%23; select_city=320200; lianjia_ssid=ca885273-46e1-48d4-a1be-a36fa1cffa99; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1594089381; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1594089399; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiOWQ4ODYyNmZhMmExM2Q0ZmUxMjk1NWE2YTRjY2JmODZkNTdmNDQ1NmNhMDA5OWRmOTM1YjJhOTU0NDFjYzMzYjg3Yjk5YjZmODc3OTRmYmRlY2VmYjFmODQyMGIyOTA5YWE3NDcxMjM0N2FhMDdhMDRjNDUzMDkyNWI1MDk2ZTAxN2RjYTIzYjMyMGZhMTM3NjkyYjYyNjMwOTE1OWZhZDFjMTI4NGMxZTk1MWY1ZTMyMmYxMmEwZTI4MTg5MDJjZjAwOGI2MDNiOWExMWNlNjhkMTkyN2VjYjcwODE2MTc5YmY4OGUxODZiYWQ1MDhjZjkyODM2YjU0YTBkYzI4M2RiNDA4ZWI0MzMyNTFjYWQyNzliNGYwMzA1ZGI0Njc4YTYxZDU5OTQzYTBlOGVhNTA3NWZkY2E3MDE2ODczYjNiOTQ2MzNmZjM3M2FhMmE2Y2JjMjFiYWUxNmU2MzA2ZVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJjY2E0ZTVlOFwifSIsInIiOiJodHRwczovL3d4LmtlLmNvbS94aWFvcXUvNDEyMDAzNDQwNDAyMDUwMC8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==",

        }
        while number > 0:
            try:
                res = requests.get(url, headers=headers, timeout=7)
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
    def get_city(self):
        """
        根据城市名获得行政区
        :return: {'guangming': '光明'}, CHENFJIAO  [True/False]
        """
        url = 'https://www.ke.com/city/'
        res = self.fetch_html(url)
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
                city[citys[0]] = 'https:' + hrefs[0] + '/loupan/'
        # print(city)
        return city

    def get_page_info(self, proxieslist, city, url, data, **kwargs):
        ''' 获取详情页信息 '''
        res, proxieslist = self.get_html(url, proxieslist)
        houseList = res['data']['list']
        print(f"当前城市: {city}")
        if not houseList: return proxieslist
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
            if url_data.find_one({'url': houseDict['标题url']}):
                print('已爬取')
                continue
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
            url_data.insert_one({'url': houseDict['标题url']})
        return proxieslist

    def get_tree(self, url, proxieslist):
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
        s = 0
        while True:
            try:
                if len(proxieslist) > 0:
                    proxies = proxieslist
                else:
                    proxy = self.get_proxy()
                    proxies = {"https": proxy}
                response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
                encod = response.apparent_encoding
                if encod.upper() in ['GB2312', 'WINDOWS-1254']:
                    encod = 'gbk'
                response.encoding = encod
                if '人机认证' in response.text:
                    print('该IP需要人机验证: ', proxieslist)
                    proxieslist = []
                    continue
                html = etree.HTML(response.text)
                proxieslist = proxies
                print(s, proxies, '获取成功')
                return html, proxieslist
            except Exception as e:
                s += 1
                proxieslist = []

                # print('get_html错误', e)
                continue
    # 获取所有城市映射表
    def get_city_info(self, city, url, proxieslist):
        print(url)
        tree, proxieslist = self.get_tree(url, proxieslist)

        data = []
        strnum = ''.join(tree.xpath('//div[@class="resblock-have-find"]/span[@class="value"]/text()'))
        if strnum == '':
            print('当前页面无数据')
            return
        length = int(strnum)
        print(length)
        if length > 2000:
            for ap in range(1,10):
                jgurl = url + 'ap%s/' % ap
                jgtree, proxieslist = self.get_tree(jgurl, proxieslist)
                strnumjg = ''.join(jgtree.xpath('//div[@class="resblock-have-find"]/span[@class="value"]/text()'))

                for i in range(1, int(int(strnumjg)/10)+2):  # 获取每一页的详细信息                         有问题 length 用的是
                    page_url = url + 'pg%s' % i + 'ap%s/' % ap
                    proxieslist = self.get_page_info(proxieslist, city, page_url, data=data, page=i)
        # totalNumber = res['data']['total']
        # if totalNumber == '0': return
        # totalPage = int(totalNumber) // 10 + 1
        else:
            for i in range(1, int(length/10)+2):  # 获取每一页的详细信息
                page_url = url + 'pg%s/' % i
                proxieslist = self.get_page_info(proxieslist, city, page_url, data=data, page=i)

        # df = pd.DataFrame(data)
        # df = Update_NewHouse().update(df)
        # df.to_sql(name='NewHouse_2020', con=engine, schema='public', if_exists='append', index=False)
        # print(f'{city}, 保存成功')
        return proxieslist


    def run(self):
        proxieslist = {}
        # exists_city_list = self.get_exists_city(self.month)
        newHouse_map = self.get_city()
        for city, city_url in newHouse_map.items():
            if city in ['大治'] : print('贝壳已舍去'); continue
            if url_data.count({city:'已爬取'}):
                print('已爬取')
                continue
            elif url_data.count({city:'正在爬取'}):
                print('正在爬取')
                continue
            url_data.insert_one({city: '正在爬取'})
            # if city in exists_city_list: print('已存在,跳过 '); continue
            print(city, city_url)
            local_list = city_url.split('/')[-1].split('-')
            base = city_url.replace(city_url.split('/')[-1],'')
            for local_area in local_list:
                city_url = base + local_area
                print(city_url)
                proxieslist = self.get_city_info(city, city_url, proxieslist)
            # print()
            url_data.insert_one({city: '已爬取'})


if __name__ == '__main__':
    # TODO 请注意不同年份下 储存的表的名称不相同, 请修改
    # TODO 修改每月抓取时间(可自定义), 位置 config >> make_date

    Year = time.localtime(time.time()).tm_year
    Month = time.localtime(time.time()).tm_mon
    #engine = create_engine('postgresql://postgres:1q2w3e4r@127.0.0.1/NewHouse').connect()  # 连接本地的新房数据库
    NewHouse(year=Year, month=Month).run()
    #engine.close()

