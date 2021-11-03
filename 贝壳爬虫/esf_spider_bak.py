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
    retryWrites="false")['贝壳']['二手房_数据_202111']

url_data = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['贝壳']['二手房_url_202111']

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))  # 设置重试次数为3次
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
    while True:
        try:
            # return requests.get('http://1.116.204.248:5000/proxy').text
            return requests.get('http://47.106.223.4:50002/get/').json().get('proxy')
        except:
            print('暂无ip，等待20秒')
            time.sleep(20)


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
    sx = html.xpath(
        "//ul[@class='city_list_ul']/li[@class='city_list_li city_list_li_selected']//ul/li/@data-action")  #
    city = {}
    for sxz in sx:
        if '国内城市' in sxz:
            citys = html.xpath(
                "//ul[@class='city_list_ul']/li[@class='city_list_li city_list_li_selected']//ul/li[@data-action='%s']/a/text()" % sxz)
            hrefs = html.xpath(
                "//ul[@class='city_list_ul']/li[@class='city_list_li city_list_li_selected']//ul/li[@data-action='%s']/a[not(contains(@href, 'fang'))]" % sxz)  # 有.fang的没有二手房
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


def get_qx(url0, proxieslist):
    """
    根据城市名获得行政区
    :param city_name:
    :return: {'guangming': '光明'}, CHENFJIAO  [True/False]
    """
    # url0 = 'https://{}.ke.com/ershoufang/'.format(city_code_map[city_name])

    tree0, proxieslist = get_html(url0, proxieslist)
    urls = {}
    href = tree0.xpath('//div[@data-role="ershoufang"]/div/a')
    for ss in href:
        it1 = {}
        qx = ''.join(ss.xpath("./text()"))
        ur = ''.join(ss.xpath('./@href'))
        url1 = ''.join(re.findall('(.+)/ershoufang', url0)) + ur
        tree1, proxieslist = get_html(url1, proxieslist)
        strnum = ''.join(tree1.xpath('//div[@class="resultDes clear"]/h2/span/text()'))
        try:
            length0 = int(strnum)
        except:
            length0 = 0
        numpg0 = int(length0 / 30) + 2
        if length0 > 3000:
            urlList = []
            href1 = tree1.xpath('//div[@class="list-more"]/dl[1]/dd/a/@href')
            for i in href1:
                it2 = {}
                url2 = ''.join(re.findall('(.+)/ershoufang', url0)) + i
                tree2, proxieslist = get_html(url2, proxieslist)
                try:
                    length1 = int(''.join(tree2.xpath('//div[@class="resultDes clear"]/h2/span/text()')))
                except:
                    length1 = 0
                if length1 > 3000:
                    href2 = tree1.xpath('//div[@class="list-more"]/dl[2]/dd/a/@href')
                    for j in href2:
                        it3 = {}
                        url3 = ''.join(re.findall('(.+)/ershoufang', url0)) + j
                        tree3, proxieslist = get_html(url3, proxieslist)
                        try:
                            length2 = int(''.join(tree3.xpath('//div[@class="resultDes clear"]/h2/span/text()')))
                        except:
                            length2 = 0
                        if length2 == length0:
                            continue
                        elif length2 == length1:
                            continue

                        if length2 > 3000:
                            url4ls = tree3.xpath('//div[@data-role="ershoufang"]/div[2]/a/@href')
                            for ur4 in url4ls:
                                it4 = {}
                                url4 = ''.join(re.findall('(.+)/ershoufang', url0)) + ur4
                                tree4, proxieslist = get_html(url4, proxieslist)
                                try:
                                    length3 = int(
                                        ''.join(tree4.xpath('//div[@class="resultDes clear"]/h2/span/text()')))
                                except:
                                    length3 = 0
                                if length3 == length0:
                                    continue
                                elif length3 == length1:
                                    continue
                                elif length3 == length2:
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
                elif length1 == length0:
                    continue
                else:
                    numpg1 = int(length1 / 30) + 2
                    it2[url2] = numpg1
                    urlList.append(it2)
                    urls[qx] = urlList
        else:
            it1[url1] = numpg0
            urls[qx] = [it1]
    return urls


def get_data(city, qx, proxieslist, url):
    if url_data.find_one({'url': url}):
        print('当前url已爬取')
        return proxieslist
    print('运行', url)
    tag = 5
    while tag > 0:
        response, proxieslist = get_html(url, proxieslist)
        houses = response.xpath("//ul[@log-mod='list']//li[@class='clear']")
        if houses:
            for house in houses:
                items = {}
                items['城市'] = city
                items['区县'] = qx
                items['标题url'] = house.xpath("./a/@href")[0]
                # if url_data.find_one({'url': items['标题url']}):
                #     print('当前url已爬取')
                #     continue
                # items['标题'] = house.xpath("./a/@title")[0]
                items['小区'] = ''.join(house.xpath("./div[@class='info clear']/div[@class='address']/div/div/a/text()"))
                houseInfo = "".join(house.xpath("./div/div[2]/div[2]/text()")).replace(" ", "").replace("\n", "")

                # 户型
                items['户型'] = "".join(re.findall('\d室\d{0,1}厅{0,1}', ''.join(
                    [type_info for type_info in houseInfo.split('|') if '室' in type_info])))
                if len(items['户型']) == 0:
                    items['户型'] = np.NaN

                # 面积
                area = "".join(re.findall('(\d+\.?\d+)平米',
                                          "".join([type_info for type_info in houseInfo.split('|') if '米' in type_info])))
                try:
                    items['面积'] = float(area)
                except:
                    items['面积'] = np.NaN

                # 楼层
                items['楼层'] = "".join(
                    re.findall("(.*\))", "".join([type_info for type_info in houseInfo.split('|') if '层' in type_info])))
                if len(items['楼层']) == 0:
                    items['楼层'] = np.NaN

                # 建筑年份
                houseYear = "".join(
                    re.findall('(\d+)年', ''.join([type_info for type_info in houseInfo.split('|') if '建' in type_info])))
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

                flower = "".join(house.xpath("./div/div[2]/div[3]/text()")).replace(" ", "").replace("\n", "")
                items['关注人数'] = ''.join(re.findall('(\d+)人', flower))
                if len(items['关注人数']) == 0:
                    items['关注人数'] = np.NaN

                # 标签
                items['标签'] = "|".join(house.xpath("./div/div[2]/div[4]/span/text()"))
                if len(items['标签']) == 0:
                    items['标签'] = np.NaN

                # 总价
                totalPrice = house.xpath(
                    "./div[@class='info clear']/div[@class='address']/div[@class='priceInfo']/div[@class='totalPrice']/span/text()")
                totalPrice = "".join(re.findall('(\d)', str(totalPrice)))
                try:
                    items['总价'] = float(totalPrice)
                except:
                    items['总价'] = np.NaN

                # 单价
                unitPrace = house.xpath(
                    "./div[@class='info clear']/div[@class='address']/div[@class='priceInfo']/div[@class='unitPrice']/span/text()")
                unitPrace = "".join(re.findall('(\d+\.?\d+)元', str(unitPrace)))
                try:
                    items['单价'] = float(unitPrace)
                except:
                    items['单价'] = np.NaN

                items['数据来源'] = '贝壳'

                items['地址'] = ''.join(house.xpath("./div[@class='info clear']/div[@class='address']/div/div/a/text()"))
                items['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                print(items)
                info_base.insert_one(items)
                # url_data.insert_one({'url':items['标题url']})
            tag = -1
        else:
            tag -= 1
            print('当前页面无数据')
            continue
    url_data.insert_one({'url': url})
    return proxieslist


def get_html(url, proxieslist):
    s = 0
    while True:
        try:
            if len(proxieslist) > 0:
                proxies = proxieslist
            else:
                proxy = get_proxy()
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
            # 可以增加一个判断是否成功的代码，如果页面不是所需页面，proxieslist赋值为空
            proxieslist = proxies
            print(s, proxies, '获取成功')
            return html, proxieslist
        except Exception as e:
            s += 1
            proxieslist = []

            # print('get_html错误', e)
            continue
    return


# def get_html(url):
#     for i in range(20):
#     # while True:
#         proxies = {"https": get_proxy()}
#         try:
#             response = requests.get(url, headers=headers,proxies=proxies, timeout=10)
#             encod = response.apparent_encoding
#             if encod.upper() in ['GB2312', 'WINDOWS-1254']:
#                 encod = 'gbk'
#             response.encoding = encod
#             html = etree.HTML(response.text)
#             print('获取成功')
#             return html
#         except Exception as e:
#             print('get_html错误',proxies, e)
#             time.sleep(2)
#
#     return


def delete_proxy(proxy):
    html = requests.get('http://192.168.1.104:5010/delete/?proxy={}'.format(proxy))
    return html.text


def run():
    l = []
    proxieslist = []
    citycod = get_city()
    for city in citycod:

        if url_data.find_one({city: '已爬取'}):
            print("这个城市已经抓过了: %s" % city)
            continue
        elif url_data.find_one({city: '正在爬取'}):
            print("这个城市正在抓: %s" % city)
            continue
        print('开始：', city)
        url_data.insert_one({city: '正在爬取'})
        cityurl = citycod[city]
        qx = get_qx('http://' + cityurl + '.ke.com/ershoufang/', proxieslist)
        for region_name, base_urlss in qx.items():  # {区县：[{url:数据条数},...] , ......}
            for base_urls in base_urlss:  # base_urlss：  [{url:数据条数},...]
                base_url = list(base_urls.keys())[0]  # url
                print(base_url)
                for i in range(1, base_urls[base_url]):  # 遍历有数据的页
                    url = ''.join(re.findall('(.+ershoufang/.+/)', base_url)) + "pg" + str(i) + ''.join(
                        re.findall('ershoufang/.+/(.+)', base_url))

                    done = pool.submit(get_data, city, region_name, proxieslist, url)
                    l.append(done)
                [obj.result() for obj in l]
        url_data.insert_one({city: '已爬取'})

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
    pool = ThreadPoolExecutor()
    # get_city()
    # url = 'https://hf.ke.com/ershoufang/'
    # get_qx('合肥',url)
    # url = 'https://hf.ke.com/ershoufang/konggangjingjishifanqu/'+'pg3/'
    # get_data(url)
    run()
