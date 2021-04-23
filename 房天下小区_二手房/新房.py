import random
import uuid
import datetime
import os
import json
import re
import time
import pymongo
import requests
import pandas as pd
from lxml import etree
from urllib import parse
from city_map import city_map

# from sqlalchemy import create_engine
from concurrent.futures.thread import ThreadPoolExecutor

from IP_config import get_Html_IP
# from save_data import write_to_table, Update_NewHouse_Df
# from 新房详情 import get_detail_url

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
            retryWrites="false")['房天下新房']['info']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['房天下新房']['has_spider']
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
}

def getCity_Code():
    item={}
    response = requests.get('https://www.fang.com/SoufunFamily.htm', headers=headers, timeout=(5, 5))
    response.encoding = 'gbk'
    html = etree.HTML(response.text)
    lists=html.xpath('//div[@class="onCont"]/table//a')
    for i in lists:
        city=i.xpath('./text()')[0]
        url=i.xpath('./@href')[0]
        code=url.split('.')[0][7:]
        # print(city,code,url)
        if city in ['波士顿','保加利亚','昌吉','德国','海外','西雅图','广德','旧金山','洛杉矶','日本','塞浦路斯','西雅图','西班牙','希腊','悉尼','芝加哥','马来西亚','澳大利亚','美国','纽约','葡萄牙','蒙城']:
            continue
        item[city]=code
    return item


def get_proxy():
    try:
            return requests.get('http://47.106.223.4:50002/get/').json().get('proxy')
            # return '111.202.83.35:80'
    except:
        num = 3
        while num:
            try:
                return requests.get('http://47.106.223.4:50002/get/').json().get('proxy')
            except:
                print('暂无ip，等待20秒')
                time.sleep(20)

                num -= 1
        print('暂无ip')

def delete_proxy(proxy):
    html = requests.get('http://47.106.223.4:50002/delete/?proxy={}'.format(proxy))
    return html.text



def get_html(url):
    proxies = {"https": get_proxy()}
    try:
        response = requests.get(url, headers=headers,proxies=proxies, timeout=10)
        encod = response.apparent_encoding
        if encod.upper() in ['GB2312', 'WINDOWS-1254']:
            encod = 'gbk'
        response.encoding = encod
        return response
    except Exception as e:
        print('get_html错误',proxies, url,e)
        # time.sleep(10)
        return get_html(url)
def get_community_area(url, title):
    while True:
        # proxies = {"https": get_proxy()}
        try:
            # response = requests.get(url, headers=headers,proxies=proxies, timeout=10)
            response = get_html(url)
            encod = response.apparent_encoding
            if encod.upper() in ['GB2312', 'WINDOWS-1254']:
                encod = 'gbk'
            response.encoding = encod
            tree = etree.HTML(response.text)
            break
        except Exception as e:
            print('新房详情中...', e, url)
            time.sleep(2)
            continue
    item, data = [], {}

    # 销售信息
    sales_message = tree.xpath("//div[@class='main-item']/h3[contains(text(), '销售信息')]/../ul/li")
    for sales in sales_message:
        txt = re.sub('\s', '', sales.xpath('string(.)')).split('：')
        item.append(dict(zip(txt[0::2], txt[1::2])))

    # 小区规划
    Community_planning = tree.xpath('//ul[@class="clearfix list"]//li')
    for plan in Community_planning:
        txt = re.sub('\s', '', plan.xpath('string(.)')).split('：')
        item.append(dict(zip(txt[0::2], txt[1::2])))
    [data.update(i) for i in item]
    return data
def badip(proxies):
    with open('1.txt','a',encoding='utf8') as f:
        f.write(proxies)
def get_detail_url(url, title, dataDict, data):
    while True:
        Infodata = dict()
        proxies = {"https": get_proxy()}
        try:
            # response = requests.get(url, headers=headers,proxies=proxies, timeout=10)
            response = get_html(url)
            encod = response.apparent_encoding
            if encod.upper() in ['GB2312', 'WINDOWS-1254']:
                encod = 'gbk'
            response.encoding = encod
            tree = etree.HTML(response.text)
            break
        except Exception as e:
            badip(proxies)
            print("get_detail_url error: ",proxies,e)
            continue

    # 楼盘详情url
    try:
        durl = tree.xpath('//*[@id="orginalNaviBox"]/a[contains(text(), "楼盘详情") or contains(text(), "详细信息")]/@href')[0]
        detail_url = "https:" + durl if 'http' not in durl else durl
        # print('durl',detail_url)
        if 'ld.newhouse' in durl:
            print('出现: ld.newhouse', durl)
        else:
            # print('执行get_community_area')
            Infodata = get_community_area(detail_url, title)
    except Exception as e:
        print('get_detail_url函数中, 详情错误',e)
        # print('get_detail_url函数中, 详情错误')
        Infodata = dict()
    dataDict['销售状态'] = Infodata.get('销售状态', '')
    dataDict['开盘时间'] = Infodata.get('开盘时间', '')
    dataDict['主力户型'] = Infodata.get('主力户型', '')
    dataDict['占地面积'] = Infodata.get('占地面积', '')
    dataDict['建筑面积'] = Infodata.get('建筑面积', '')
    dataDict['容积率'] = Infodata.get('容积率', '')
    dataDict['绿化率'] = Infodata.get('绿化率', '')
    dataDict['停车位'] = Infodata.get('停车位', '')
    dataDict['楼栋总数'] = Infodata.get('楼栋总数', '')
    dataDict['总户数'] = Infodata.get('总户数', '')
    dataDict['物业费'] = Infodata.get('物业费', '')
    dataDict['楼层状况'] = Infodata.get('楼层状况', '')

    data.append(dataDict)
# 解析页面
def get_data(url, city,page_number,page, data):
    has_spider_urlList = []
    for has_spider_url in has_spider.find():
        has_spider_urlList.append(has_spider_url['标题'])
    if url in has_spider_urlList:
        print('该页数据已爬取，下一页')
        return 0
        # html, response, _ = get_html(url)
        # next_page_url = html.xpath('string(//a[@class="next next-active"]/@href)')
        # if next_page_url:
        #     print('该页数据已爬取，下一页')
        #     get_data(url, city, data)
        # else:
        #     print('最后一页')
        #     return

    # res = get_Html_IP(url, headers)
    res = get_html(url)
    tree = etree.HTML(res.text)
    house_list = tree.xpath("//div[@id='newhouse_loupai_list']/ul/li[@id]")

    # l = []
    for house in house_list:
        dataDict = {}
        try:
            dataDict['标题'] = house.xpath(".//div[@class='nlcd_name']/a/text()")[0].replace("\t", '').replace("\n",'').replace(" ", "").strip()
            if 'È' in dataDict['标题'] or 'ó' in dataDict['标题'] or 'ô' in dataDict['标题']:
                print('标题有问题')
                continue
        except:
            print('没有标题', url)
            continue
        dataDict['标题url'] = "https:" + house.xpath(".//div[@class='nlcd_name']/a/@href")[0]
        addr = house.xpath(".//div[@class='address']/a")[0].xpath('string(.)')
        addr = addr.replace("\n", "").replace("\t", "").replace(" ", "")
        dataDict['区县'] = "".join(re.findall("\[(.*)\]", addr))
        dataDict['地址'] = ''.join(house.xpath(".//div[@class='address']/a/@title")).lstrip(dataDict['区县'])
        dataDict['描述'] = ('|'.join(house.xpath(".//div[@class='house_type clearfix']//a/text()")) or '') \
                         + "".join(house.xpath(".//div[@class='house_type clearfix']/text()"))
        dataDict['描述'] = dataDict['描述'].replace('\t','').replace('\n','').replace('－', '').strip()
        dataDict['价格'] = ("".join(house.xpath(".//div[@class='nhouse_price']/span/text()")) or '') \
                         + ("".join(house.xpath(".//div[@class='nhouse_price']/label[1]/text()")) or '') \
                         + ("".join(house.xpath(".//div[@class='nhouse_price']/label[2]/text()")) or '') \
                         + ("".join(house.xpath(".//div[@class='nhouse_price']/i/text()")) or '') \
                         + ("".join(house.xpath(".//div[@class='nhouse_price']/em/text()")) or '')
        dataDict['价格'] = dataDict['价格'].replace('�','㎡')
        tag = " ".join(house.xpath(".//div[@class='fangyuan']/span/text()")) \
              + " " + " ".join(house.xpath(".//div[@class='fangyuan']/a/text()")) \
              + " " + " ".join(house.xpath(".//div[@class='fangyuan']/a/em/text()"))
        dataDict['标签'] = tag.replace("\n", "").replace("\t", "")
        dataDict['评论数量'] = "".join(re.findall("\d+", "".join(house.xpath(".//span[@class='value_num']/text()"))))
        dataDict['城市'] = city
        dataDict['抓取年份'] = year
        dataDict['抓取月份'] = month
        dataDict['数据来源'] = "房天下"
        dataDict["id"] = uuid.uuid1(node=random.randint(100, 99999999))
        dataDict['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # get_detail_url(dataDict['标题url'], dataDict['标题'], dataDict, data)
        # 获取详情页内容
        # l.append(pool.submit(get_detail_url, dataDict['标题url'], dataDict['标题'], dataDict, data))
        get_detail_url(dataDict['标题url'], dataDict['标题'], dataDict, data)

        print(dataDict)
        info_base.insert_one(dataDict)
    has_spider.insert_one({'标题': url})

    # [i.result() for i in l]


def get_html_page(url, city):
    # res = get_Html_IP(url, headers)
    proxies = {"https": get_proxy()}
    try:
        # res = requests.get(url, headers=headers,proxies=proxies, timeout=(10, 10))
        res = get_html(url)
        res.encoding = 'utf-8'
        if not res:
            print('米有res')
            return
        tree = etree.HTML(res.text)

        pageNumber = "".join(tree.xpath("//div[@class='otherpage']/span/text()"))
        try:
            page = re.findall("\/(\d+)", pageNumber)[0]
        except:
            print("page: ", pageNumber)
            return
        print("pageNumber: ", pageNumber, page, url)

        if page == 0:
            print('城市: 没有数据', )

        # data = []
        # for i in range(1, int(page) + 1):
        #     page_url = url + "b9{}/".format(i)
        #     print('城市: {}, 页数: {}, 当前页: {}'.format(city, page, i))
        #     get_data(page_url, city, data)

        l, data = [], []
        for i in range(1, int(page) + 1):
            page_url = url + "b9{}/".format(i)
            done = pool.submit(get_data, page_url,city,int(page),i,data)
            l.append(done)
        [obj.result() for obj in l]
    except Exception as e:
        print('获取页面失败',e)
    # if not data:
    #     print('没有数据')
    #     return
    # df = pd.DataFrame(data)
    # df = Update_NewHouse_Df().update(df)
    # # TODO 保存到本地的 新房库
    # write_to_table(df, DB='NewHouse', schema="public", table_name="NewHouse_2021", spiderType='newhouse')
    # print(f'{city}, {df.shape}, 保存成功')



def run():
    # with open('city_map.json', 'r', encoding="utf-8") as fp:
    #     city_code = json.load(fp)

    # exists_city = check_sql()
    for city, pinyin in city_map.items():

        # if city  in exists_city: print(f'{city}, 已存在\n'); continue
        if city in [
            '阿拉尔', '阿里', '宝应', '汉川', '凤城', '京山', '五指山', '文昌', '桦甸', '晋州', '康平', '辽中',
            '琼海', '瑞安', '三沙', '山南', '图木舒克', '新丰', '新民', '临清','韶山', '香港', '海南省'
        ]:
            print(city, '不抓取')
            continue

        url = "https://newhouse.fang.com/house/s/" if city == '北京' else "https://{}.newhouse.fang.com/house/s/".format(pinyin)

        print( '\n','城市: ', city, url)
        get_html_page(url, city)


if __name__ == '__main__':
    # TODO 新房启动程序
    # TODO 直接 month为要抓取的月份
    year = 2021
    month = 4
    day = 28
    # city_map=getCity_Code()
    pool = ThreadPoolExecutor(30)
    run()
    pool.shutdown()

