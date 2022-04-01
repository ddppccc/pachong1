import random
import uuid
import datetime
import os
import json
import re
import time
import pymongo
import requests
# import pandas as pd
from lxml import etree
from urllib import parse
# from city_map import city_map
from config2 import get_proxy
from concurrent.futures.thread import ThreadPoolExecutor

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
            retryWrites="false")['房天下']['新房_数据_202203']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['房天下']['新房_去重_202203']
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


IpPool = [
    # "192.168.1.104:5010",
    # "118.24.52.95:5010",
    # "47.106.223.4:50002",
    'demo.spiderpy.cn',
]
# def get_proxy():
#     try:
#         return requests.get(f'http://{random.choice(IpPool)}/get/').json().get('proxy')
#     except:
#         num = 3
#         while num:
#             try:
#                 return requests.get(f'http://{random.choice(IpPool)}/get/').json().get('proxy')
#             except:
#                 print('暂无ip，等待20秒')
#                 time.sleep(20)
#
#                 num -= 1
#         print('暂无ip')





def get_html(url):
    for i in range(100):
        proxie= get_proxy()
        proxies = {
            "https": proxie,
            "http": proxie,
                   }
        try:
            # time.sleep(3)
            response = requests.get(url, headers=headers,proxies=proxies, timeout=10)
            # response = requests.get(url, headers=headers, timeout=100)
            encod = response.apparent_encoding
            if encod.upper() in ['GB2312', 'WINDOWS-1254']:
                encod = 'gbk'
            response.encoding = encod
            if '访问验证-房天下' in response.text:
                # print('访问验证-房天下')
                return get_html(url)
            return response
        except Exception as e:
            # print('get_html错误',proxies, url,e)
            time.sleep(2)
    return

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

# def badip(proxies):
#     with open('1.txt','a',encoding='utf8') as f:
#         f.write(proxies)
def get_detail_url(url, title, dataDict, data):
    for i in range(3):
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
        except Exception as e:
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
            continue
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
        break
# 解析页面
def get_data(url, city,page_number,page, data):
    if has_spider.find_one({'标题':url}):
        print('该页数据已爬取，下一页')
        return

    res = get_html(url)
    tree = etree.HTML(res.text)
    house_list = tree.xpath('//div[@id="newhouse_loupan_list"]/ul/li[@id]')

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
        dataDict['标题url'] = house.xpath(".//div[@class='nlcd_name']/a/@href")[0]
        try:
            addr = house.xpath(".//div[@class='address']/a")[0].xpath('string(.)')
        except:
            continue
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
        # dataDict["id"] = uuid.uuid1(node=random.randint(100, 99999999)) 3.11
        dataDict['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # get_detail_url(dataDict['标题url'], dataDict['标题'], dataDict, data)
        # 获取详情页内容
        # l.append(pool.submit(get_detail_url, dataDict['标题url'], dataDict['标题'], dataDict, data))
        get_detail_url(dataDict['标题url'], dataDict['标题'], dataDict, data)
        while True:
            try:
                newcode = re.findall("loupan/(\d+).htm", dataDict['标题url'])[0]
                # print('newcode', newcode)
            except:
                break
            proxies = {"https": get_proxy()}
            try:
                gisurl='https://ditu.fang.com/?c=channel&a=xiaoquNew&newcode='+str(newcode)+'&city=&width=1200&height=455&resizePage=//house/web/map_resize.html&category=residence'
                gisres = get_html(gisurl)
                encod = gisres.apparent_encoding
                if encod.upper() in ['GB2312', 'WINDOWS-1254']:
                    encod = 'gbk'
                gisres.encoding = encod
                break
            except Exception as e:
                print("获取经纬度error: ",dataDict['标题url'], proxies, e)
                continue
        for i in range(5):
            try:
                dataDict['lng'] =re.findall('"mapx":"(.*?)"',gisres.text)[0]
                dataDict['lat'] =re.findall('"mapy":"(.*?)"',gisres.text)[0]
            except:
                if i != 4:continue
                dataDict['lng'] = ''
                dataDict['lat'] = ''
        # print(dataDict)
        if info_base.find_one(dataDict):continue
        info_base.insert_one(dataDict)
    if (page < page_number) and (len(house_list) < 18):
        print('数据缺失，继续抓取')
        return get_data(url, city,page_number,page, data)
    print(f"城市：{city} , 状态：有数据，共{page_number}页，当前第{page}页", url, len(house_list))
    has_spider.insert_one({'标题': url})

    # [i.result() for i in l]


def get_html_page(url, city):

    number_tz = 0
    while True:
        number_tz += 1
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
            if number_tz > 5:
                print('获取页码失败')
                break
            continue
        print("pageNumber: ", pageNumber, page, url)

        if page == 0:
            print(city,'没有数据')
            if number_tz > 5:
                break
            continue

        l, data = [], []
        for i in range(1, int(page) + 1):
            page_url = url + "b9{}/".format(i)
            done = pool.submit(get_data, page_url,city,int(page),i,data)
            l.append(done)
        [obj.result() for obj in l]
        break
    has_spider.insert_one({'抓取完成城市': city})



def run():
    with open('city_map.json', 'r', encoding='utf-8') as f:
        city_map = json.load(f)

    # for city, pinyin in city_map.items():
    while city_map:
        data = random.sample(city_map.items(), 1)
        city, pinyin = data[0][0], data[0][1]
        # city, pinyin = '重庆','cq'
        # if city  in exists_city: print(f'{city}, 已存在\n'); continue
        if city in ['波士顿','保加利亚','昌吉','德国','海外','西雅图','广德','旧金山','洛杉矶','日本','塞浦路斯','西雅图',
                    '西班牙','希腊','悉尼','芝加哥','马来西亚','澳大利亚','美国','纽约','葡萄牙','安陆','蒙城']:
            del city_map[city]
            continue
        if city in [
            '阿拉尔', '阿里', '宝应', '汉川', '凤城', '京山', '五指山', '文昌', '桦甸', '晋州', '康平', '辽中',
            '琼海', '瑞安', '三沙', '山南', '图木舒克', '新丰', '新民', '临清','韶山', '香港', '海南省'
        ]:
            print(city, '不抓取')
            del city_map[city]
            continue

        url = "https://newhouse.fang.com/house/s/" if city == '北京' else "https://{}.newhouse.fang.com/house/s/".format(pinyin)
        print( '\n','城市: ', city, url)

        # if city not in ['眉山', ]:
        #     del city_map[city]
        #     continue

        if has_spider.find_one({'抓取完成城市': city}):
            print('该城市已抓取完成')
            del city_map[city]
            continue
        get_html_page(url, city)
        del city_map[city]


if __name__ == '__main__':
    # TODO 新房启动程序
    # TODO 直接 month为要抓取的月份
    # print(info_base.count_documents({'城市':'北京'}))
    #抓取的时间
    year = 2022
    month = 3
    day = 11
    # city_map=getCity_Code()
    pool = ThreadPoolExecutor(30)

    # for i in ['眉山']:
    #     x=info_base.delete_many({'城市':i})
    #     print(x.deleted_count,'个文档已删除')

    run()
    pool.shutdown()
    # get_data('url', 'city', 'page_number', 'page', [])

    
    


