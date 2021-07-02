import base64
import json
import random
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import re
###
from selenium.webdriver.support.wait import WebDriverWait


from PIL import Image

from requests.adapters import HTTPAdapter

import pymongo
from urllib import parse


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
            retryWrites="false")['贝壳shen']['ZuFang']

url_data = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['贝壳shen']['ZuFang_url']


s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))#设置重试次数为3次
s.mount('https://', HTTPAdapter(max_retries=3))

headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        # 'Host': 'www.ke.com',
        "Accept-Language": "zh-CN,zh;q=0.9",
        "upgrade-insecure-requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        # 'cookie': "lianjia_uuid=bfa7ceba-65ca-4e1e-b591-2fec6f15129c; crosSdkDT2019DeviceId=-pal2xu-di1vvg-q4phzhoefy25s8p-yfip8uyx7; _ga=GA1.2.1314769215.1585729030; ke_uuid=dcb5976f4b3634b4a8bcab004ed5d775; _smt_uid=5e8452ec.5a19fece; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217134e3ece7149-0b39f3df5eee65-6701b35-1327104-17134e3ece837b%22%2C%22%24device_id%22%3A%2217134e3ece7149-0b39f3df5eee65-6701b35-1327104-17134e3ece837b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wyshenzhen%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; __xsptplus788=788.7.1592811193.1592811569.3%234%7C%7C%7C%7C%7C%23%23m3PY-nFnYwlqfjOVPI_Sk2ie3bc2rPsa%23; select_city=320200; lianjia_ssid=ca885273-46e1-48d4-a1be-a36fa1cffa99; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1594089381; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1594089399; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiOWQ4ODYyNmZhMmExM2Q0ZmUxMjk1NWE2YTRjY2JmODZkNTdmNDQ1NmNhMDA5OWRmOTM1YjJhOTU0NDFjYzMzYjg3Yjk5YjZmODc3OTRmYmRlY2VmYjFmODQyMGIyOTA5YWE3NDcxMjM0N2FhMDdhMDRjNDUzMDkyNWI1MDk2ZTAxN2RjYTIzYjMyMGZhMTM3NjkyYjYyNjMwOTE1OWZhZDFjMTI4NGMxZTk1MWY1ZTMyMmYxMmEwZTI4MTg5MDJjZjAwOGI2MDNiOWExMWNlNjhkMTkyN2VjYjcwODE2MTc5YmY4OGUxODZiYWQ1MDhjZjkyODM2YjU0YTBkYzI4M2RiNDA4ZWI0MzMyNTFjYWQyNzliNGYwMzA1ZGI0Njc4YTYxZDU5OTQzYTBlOGVhNTA3NWZkY2E3MDE2ODczYjNiOTQ2MzNmZjM3M2FhMmE2Y2JjMjFiYWUxNmU2MzA2ZVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJjY2E0ZTVlOFwifSIsInIiOiJodHRwczovL3d4LmtlLmNvbS94aWFvcXUvNDEyMDAzNDQwNDAyMDUwMC8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==",

    }
def get_proxy():
    try:
        return s.get('http://47.106.223.4:50002/get/').json().get('proxy')
    except:
        num = 3
        while num:
            try:
                return s.get('http://47.106.223.4:50002/get/').json().get('proxy')
            except:
                print('暂无ip，等待20秒')
                time.sleep(20)

                num -= 1
        print('暂无ip')

def fetch_html(url):
    '''获取页面代码'''
    number = 3
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

def get_city():
    """
    根据城市名获得行政区
    :return: {'guangming': '光明'}, CHENFJIAO  [True/False]
    """
    url = 'https://www.ke.com/city/'
    res = fetch_html(url)
    html = etree.HTML(res)
    sx = html.xpath("//ul[@class='city_list_ul']/li[@class='city_list_li city_list_li_selected']//ul/li/@data-action")#
    city = {}
    for sxz in sx[:592]:
        citys = html.xpath("//ul[@class='city_list_ul']/li[@class='city_list_li city_list_li_selected']//ul/li[@data-action='%s']/a/text()"%sxz)
        hrefs = html.xpath("//ul[@class='city_list_ul']/li[@class='city_list_li city_list_li_selected']//ul/li[@data-action='%s']/a[not(contains(@href, 'fang'))]" % sxz)  # 有.fang的没有二手房
        if hrefs != []:
            city[citys[0]] = hrefs[0].xpath('./@href')[0][2:-7]
    # print(city)
    return city
    # {'合肥': 'https://hf.ke.com/ershoufang/',...}
# def get_html(url):
#     headers = {
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Accept-Language": "zh-CN,zh;q=0.9",
#         "Cache-Control": "max-age=0",
#         "Connection": "keep-alive",
#         # "Host": "www.ke.com",
#         "Referer": "https://sz.ke.com/",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
#     # prox = get_proxy()
#     # proxies = {'http': 'http://%s' % prox, 'https': 'https://%s' % prox}
#     # res = requests.get(url, headers=headers, proxies=proxies)
#     res = requests.get(url, headers=headers)
#     res.encoding = 'utf-8'
#     # print(res.text)
#     tree = etree.HTML(res.text)
#     return tree


def get_qx(url0):
    """
    根据城市名获得行政区
    :param city_name:
    :return: {'guangming': '光明'}, CHENFJIAO  [True/False]
    """
    # url0 = 'https://{}.ke.com/ershoufang/'.format(city_code_map[city_name])


    tree0 = get_html(url0)
    urls = {}
    href = tree0.xpath('//ul[@data-target="area"]/li[@class="filter__item--level2  "]/a')
    for ss in href:
        qx = ''.join(ss.xpath("./text()"))
        ur = ''.join(ss.xpath('./@href'))

        url1 = ''.join(re.findall('(.+)/zufang', url0)) + ur
        tree1 = get_html(url1)
        urlList = []
        href1 = tree1.xpath('//ul[@class="filter__ul"]/li[@class="filter__item--level4 "]/a/@href')



        for ur2 in href1:
            it2 = {}
            url2 = ''.join(re.findall('(.+)/zufang', url0)) + ur2
            tree2 = get_html(url2)
            try:
                length1 = int(''.join(tree2.xpath('//p[@class="content__title"]/span[@class="content__title--hl"]/text()')))
            except:
                length1 = 0
            if length1 > 3000:
                href2 = tree2.xpath('//ul[@class="filter__ul"][2]/li[@class="filter__item--level5 check "]/a/@href')
                for ur3 in href2:
                    it3 = {}
                    url3 = ''.join(re.findall('(.+)/zufang', url0)) + ur3
                    tree3 = get_html(url3)
                    try:
                        length2 = int(''.join(tree3.xpath('//p[@class="content__title"]/span[@class="content__title--hl"]/text()')))
                    except:
                        length2 = 0
                    if length2 == length1:
                        continue

                    if length2 > 3000:
                        url4ls = tree3.xpath('//ul[@class="filter__ul "]/li[@class="filter__item--level5 check "]/a/@href')
                        for ur4 in url4ls:
                            it4 = {}
                            url4 = ''.join(re.findall('(.+)/zufang', url0)) + ur4
                            tree4 = get_html(url4)
                            try:
                                length3 = int(''.join(tree4.xpath('//p[@class="content__title"]/span[@class="content__title--hl"]/text()')))
                            except:
                                length3 = 0
                            if length3 == length1:
                                continue
                            elif length3 == length2:
                                continue
                            if length3 > 3000:
                                href4 = tree4.xpath('//ul[@data-target="area"]/li[@class="filter__item--level3  "]/a/@href')
                                for ur5 in href4:
                                    url5 = ''.join(re.findall('(.+)/zufang', url0)) + ur5
                                    tree5 = get_html(url5)
                                    try:
                                        length5 = int(''.join(tree5.xpath('//p[@class="content__title"]/span[@class="content__title--hl"]/text()')))
                                    except:
                                        length5 = 0
                                    if length5 == length1:
                                        continue
                                    elif length5 == length2:
                                        continue
                                    elif length5 == length3:
                                        continue

                            numpg3 = int(length3 / 30) + 2
                            it4[url4] = numpg3
                            urlList.append(it4)
                            urls[qx] = urlList

                    else:
                        numpg2 = int(length2 / 30) + 2
                        it3[url3] = numpg2
                        urlList.append(it3)
                        urls[qx] = urlList
            else:
                numpg1 = int(length1 / 30) + 2
                it2[url2] = numpg1
                urlList.append(it2)
                urls[qx] = urlList

    return urls




def get_data(city,qx,houses,url):
    if 'rt200600000001' in url:
        lenxing = '整租'
    else:
        lenxing = '合租'


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

    print('运行', url)
    if url_data.find_one({'url': url}):
        print('当前url已爬取')
        return
    for house in houses:
        items = {}
        items['城市'] = city
        items['区县'] = qx
        items['标题url'] = ''.join(re.findall('(.+)/zufang',url)) + "".join(house.xpath('./a[@class="content__list--item--aside"]/@href'))
        # if url_data.find_one({'url': items['标题url']}):
        #     print('当前url已爬取')
        #     continue
        items['标题'] = "".join(house.xpath('./a[@class="content__list--item--aside"]/@title'))
        houseInfo = "|".join(house.xpath('./div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/i/following-sibling::text()')).replace(" ", "").replace("\n", "")

        # 户型
        items['户型'] = "".join(re.findall('\d室\d{0,1}厅{0,1}\d{0,1}卫{0,1}',houseInfo))
        if len(items['户型']) == 0:
            items['户型'] = np.NaN

        # 面积
        area = "".join(re.findall('(\d+\.?\d+)㎡',houseInfo))
        try:
            items['面积'] = np.double(area)
        except:
            items['面积'] = np.double(None)

        # 楼层
        items['楼层'] = "".join(house.xpath('./div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/span[@class="hide"]/text()')).replace(" ", "").replace("\n", "")



        # 朝向
        items['朝向'] = "".join(re.findall('\|([东南西北]{1,2})\|',houseInfo))

        # 标签
        items['特点'] = "|".join(house.xpath('./div[@class="content__list--item--main"]/p[@class="content__list--item--bottom oneline"]/i/text()'))

        zj = ''.join(house.xpath('./div[@class="content__list--item--main"]/span[@class="content__list--item-price"]//text()'))
        try:
            items['租金'] = np.double(''.join(re.findall('(\d+\.?\d+)',zj)))
        except:
            items['租金'] = np.double(None)
        items['类型'] = lenxing

        items['数据来源'] = ''.join(house.xpath('./div[@class="content__list--item--main"]/p[@class="content__list--item--brand oneline"]/span[@class="brand"]/text()')).replace(' ','').replace('\n','')
        items['维护'] = ''.join(house.xpath('./div[@class="content__list--item--main"]/p[@class="content__list--item--brand oneline"]/span[@class="content__list--item--time oneline"]/text()')).replace(' ','')
        items['地址'] = ''.join(house.xpath('./div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/a/text()'))
        items['小区url'] = ''.join(house.xpath('./div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/a[3]/@href'))
        items['小区'] = ''.join(house.xpath('./div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/a[3]/text()'))
        items['抓取年份'] = 2021
        items['抓取月份'] = 5
        items['抓取时间'] = '2021-05-27'
        # items['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print(items)
        info_base.insert_one(items)
        # url_data.insert_one({'url':items['标题url']})
    url_data.insert_one({'url': url})



def get_html(url):
    for i in range(10):
        proxies = {"https": get_proxy()}
        try:
            response = requests.get(url, headers=headers,proxies=proxies, timeout=10)
            encod = response.apparent_encoding
            if encod.upper() in ['GB2312', 'WINDOWS-1254']:
                encod = 'gbk'
            response.encoding = encod
            html = etree.HTML(response.text)
            print('获取成功')
            return html
        except Exception as e:
            print('get_html错误',proxies, e)
            time.sleep(2)

    return


def delete_proxy(proxy):
    html = requests.get('http://47.106.223.4:50002/delete/?proxy={}'.format(proxy))
    return html.text





def run():
    l = []
    citycod = get_city()
    for city in citycod:

        if url_data.find_one({city: '正在爬取'}):
            print("这个城市正在抓或者已经抓过了: %s" % city)
            continue
        elif url_data.find_one({city: '已爬取'}):
            print("这个城市正在抓或者已经抓过了: %s" % city)
            continue
        url_data.insert_one({city: '正在爬取'})


        cityurl = citycod[city]
        qx = get_qx('http://'+cityurl+'.ke.com/zufang/')
        for region_name, base_urlss in qx.items():  # {区县：[{url:数据条数},...] , ......}
            for base_urls in base_urlss:  # base_urlss：  [{url:数据条数},...]
                base_url = list(base_urls.keys())[0]  # url
                print(base_url)
                for i in range(1, base_urls[base_url]):  # 遍历有数据的页
                    url = ''.join(re.findall('(.+zufang/.+/)', base_url)) + "pg" + str(i) + ''.join(
                        re.findall('zufang/.+/(.+)', base_url))
                    response = get_html(url)

                    houses = response.xpath('//div[@class="content__list--item"]')
                    if houses:
                        # print('运行', url)
                        # if url_data.find_one({'url': url}):
                        #     print('当前url已爬取')
                        #     continue
                        # get_data(city, region_name, houses, url)

                        done = pool.submit(get_data, city, region_name, houses, url)
                        l.append(done)


                        # url_data.insert_one({'url': url})
                    else:
                        break
                [obj.result() for obj in l]
        url_data.insert_one({city:'已爬取'})

            #             yield scrapy.Request(url=url,
            #                                  callback=self.parse,
            #                                  meta={
            #                                      'item': {'base_url': base_url,
            #                                               'region_name': region_name,
            #                                               'city': city_name}
            #                                  })
            #
            #
            #
            #
            # for pg in range(1,100):
            #     url = href+'pg'+str(pg)+'/'
            #     res = fetch_html(url)
            #     response = etree.HTML(res)
            #
            #     houses = response.xpath("//ul[@log-mod='list']//li[@class='clear']")
            #     if houses:
            #         print('运行',url)
            #         get_data(city,ke,houses)
            #     else:
            #         break



if __name__ == '__main__':
    pool = ThreadPoolExecutor(5)
    # get_city()
    # url = 'https://hf.ke.com/ershoufang/'
    # get_qx('合肥',url)
    # url = 'https://hf.ke.com/ershoufang/konggangjingjishifanqu/'+'pg3/'
    # get_data(url)
    run()