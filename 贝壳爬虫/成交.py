import datetime
import uuid
import random
import re
import math
import time
import requests
import pandas as pd
from lxml import etree
from requests.adapters import HTTPAdapter

from beike_map import get_regionscj, get_esf_code_map
from city_spider import cities
import multiprocessing
from urllib import parse
import pymongo

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))#设置重试次数为3次
s.mount('https://', HTTPAdapter(max_retries=3))

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
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


def check_data(x):
    x = str(x)
    if 'n' in x or 'N' in x:
        return ''
    elif x.count('-') == 2:
        try:
            x = datetime.datetime.strptime(x, "%Y-%m-%d").date()
        except:
            x = ''
    elif x.count('-') == 1:
        try:
            x = datetime.datetime.strptime(x, "%Y-%m").date()
        except:
            x = ''
    else:
        x = ''
    return x




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
            retryWrites="false")['贝壳shen']['ChengJiao']

url_data = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['贝壳shen']['cily_url']
# 建立连接
# info_base = pymongo.MongoClient('mongodb://localhost:27017/')['贝壳']['ChengJiao']



#
# def get_deal_time_1():
#     ''' 获取数据库中的交易时间'''
#     import psycopg2
#     con = psycopg2.connect(host='127.0.0.1', port='5432', password='1q2w3e4r',user='postgres', database='ChengJiao')
#     df = pd.read_sql_query('SELECT 区县, max(交易时间) as 交易时间 FROM public.chengjiao group by 区县;', con=con)
#     return df


def get_deal_time_2(df, region):
    try:
        dealTime = df[df['区县'] == region]['交易时间'].to_list()[0]
    except:
        dealTime = ''
    return dealTime


# 保存数据
# def write_to_table(df, schema, table_name, if_exists='append'):
#     import io
#     import pandas as pd
#     from sqlalchemy import create_engine
#     db_engine = create_engine('postgresql://postgres:1q2w3e4r@127.0.0.1/ChengJiao')  # 初始化引擎
#     # db_engine = create_engine('postgresql://postgres:123456@127.0.0.1/House')# 初始化引擎
#     #     db_engine = create_engine('postgresql://***:***@***:***/***')# 初始化引擎
#     string_data_io = io.StringIO()
#     df.to_csv(string_data_io, sep='|', index=False)
#     pd_sql_engine = pd.io.sql.pandasSQL_builder(db_engine)
#     table = pd.io.sql.SQLTable(table_name, pd_sql_engine, frame=df,
#                                index=False, if_exists=if_exists, schema=schema)  # 模式名
#     table.create()
#     string_data_io.seek(0)
#     string_data_io.readline()  # remove header
#     with db_engine.connect() as connection:
#         with connection.connection.cursor() as cursor:
#             copy_cmd = '''COPY "%s"."%s"("城市", "区县", "标题", "标题url", "朝向", "装修", "交易时间", "总价", "单价", "楼层", "建筑类型", "招拍挂", "其他信息", "id", "建筑年份") FROM STDIN HEADER DELIMITER '|' CSV''' % (
#             schema, table_name)
#             # print(copy_cmd)  # COPY "Esf_coord"."coord" FROM STDIN HEADER DELIMITER '|' CSV
#             cursor.copy_expert(copy_cmd, string_data_io)
#         connection.connection.commit()


# 获取更小一级的行政分类区
def get_next_register(url):
    html = s.get(url, headers=headers)
    html.encoding = html.apparent_encoding
    tree = etree.HTML(html.text)
    regions_xpath = "//div[@data-role='ershoufang']/div[2]/a"
    regis = dict(zip(tree.xpath(regions_xpath + '/text()'), tree.xpath(regions_xpath + '/@href')))
    regions = {key: re.sub("\/chengjiao.*", value, url) for key, value in regis.items()}  #组装更小一级的行政分类区url
    print("regions: ", regions)
    next_data = {}
    next_dist = {}
    for dist, distUrl in regions.items():
        html = s.get(distUrl, headers=headers)
        html.encoding = html.apparent_encoding
        html = etree.HTML(html.text)
        chengjiao_number = html.xpath("//div[@class='total fl']/span/text()")[0].strip()
        print("行政区分区: %s, 链接: %s, 数量: %s" % (dist, distUrl, chengjiao_number))
        next_data[distUrl] = chengjiao_number
        next_dist[distUrl] = dist
    return next_data, next_dist

def get_html(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        # "Host": "www.ke.com",
        # "Referer": "https://sz.ke.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
    prox = get_proxy()
    proxies = {'http': 'http://%s' % prox, 'https': 'https://%s' % prox}
    res = s.get(url, headers=headers, proxies=proxies, timeout=(5, 10))
    # res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    # print(res.text)
    tree = etree.HTML(res.text)
    return tree
# 获取每一页的信息, 保存
def get_data(url, city):
    num = 1
    while num > 0:
        try:
            # proxy = get_proxy()
            # proixy = "https://" + proxy
            # # has_spider_urllist = []
            # # for i in url_data.find():
            # #     has_spider_urllist.append(i['url'])

            #
            # html = s.get(url, proxies=proixy, headers=headers)
            # html.encoding = html.apparent_encoding
            tree = get_html(url)
            num -= 1
        except Exception as e:
            print(url, "出错195", e)

            continue
        houses = tree.xpath("//ul[@class='listContent']/li/div[@class='info']")
        time.sleep(2)

        if houses:
            data, flag = [], 0
            for house in houses:
                items = {}
                items["id"] = uuid.uuid1(node=random.randint(1000000, 99999999))
                items['城市'] = city
                qx_str = tree.xpath('//div[@class="total fl"]/span/following-sibling::text()')[0]
                items['区县'] = "".join(re.findall("套+(\w+)成交", qx_str)).strip()
                items['标题'] = house.xpath(".//div[@class='title']/a/text()")[0]  # 标题
                items['标题url'] = house.xpath(".//div[@class='title']/a/@href")[0]  # 标题连接
                if url_data.find_one({'url': items['标题url']}):
                    print('以爬取，下一页')
                    continue
                houseInfo = "".join(house.xpath(".//div[@class='houseInfo']/text()")).strip()
                items["朝向"] = houseInfo.split("|")[0]
                items["装修"] = houseInfo.split("|")[1]
                items['交易时间'] = "".join(house.xpath(".//div[@class='dealDate']/text()")).strip().replace(".", "-")
                items['总价'] = "".join(house.xpath("string(.//div[@class='totalPrice'])")).replace("\t", "").replace(
                    "\n", "").replace(" ", "")
                items['总价'] = "".join(re.findall("\d+", items['总价']))
                items['单价'] = "".join(house.xpath("string(.//div[@class='unitPrice'])")).replace("\t", "").replace("\n",
                                                                                                                   "").replace(
                    " ", "")
                items['单价'] = "".join(re.findall("(\d+)元", items['单价']))

                # items['楼层'] =house.xpath(".//div[@class='positionInfo']/span/following-sibling::text()")
                positionIcon = "".join(house.xpath(".//div[@class='positionInfo']/span/following-sibling::text()")).strip(' ').strip('\n').strip(' ')
                items['楼层'] = positionIcon.split(' ')[0]#"".join(re.findall("(.*)\)", positionIcon)).strip()


                houseType = positionIcon #"".join(re.findall("\)(.*)", positionIcon)).strip()
                items['建筑类型'] = "".join(re.findall("建(.*)", houseType)) or houseType
                items['建筑年份'] = "".join(re.findall("(\d+)年建", houseType))

                items['其他信息'] = "/".join(house.xpath(".//span[@class='dealHouseTxt']//span/text()")).strip()
                items['招拍挂'] = "/".join(house.xpath(".//span[@class='dealCycleTxt']//span/text()")).strip()
                items['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                print(items)

                info_base.insert_one(items)
                url_data.insert_one({'url': items['标题url']})


                # 判断是否有数据，没有就直接存入mongo
                # if info_base.count_documents({'标题url': items['标题url']})==0:
                #     print('存入')
                #     info_base.insert_one(items)
                # else:
                #     print('数据已存在')
                # print(items)


                data.append(items)
            df = pd.DataFrame(data=data)
            if df.shape[0] != 0:
                print(df.shape)
                df['交易时间'] = df['交易时间'].map(check_data)
                df = df[["城市", "区县", "标题", "标题url", "朝向", "装修", "交易时间", "总价", "单价", "楼层", "建筑类型",
                         "招拍挂", "其他信息", "id", "建筑年份"]]
                # write_to_table(df, 'public', "chengjiao")
            if flag == 1:
                return 1
        break
    return 0









# 构造每个页面的url
def get_page_data(page, url, city, dis=None):
    number = math.ceil(int(page) / 30)
    # g_list = []
    for i in range(1, number + 1):
        urls = url + "pg%s/" % i
        print(urls)
        get_data(urls, city)

        # if get_data(urls, city, district, dealTime) == 1:
        #     return

        # 第一次爬取使用协程,抓取全部数据, 以后爬取只需按部就班,
        # 后边判断时间, 作为停止条件
        # # 这里修改为 协程爬取   控制协程的数量,
    #     g = gevent.spawn(get_data, urls, city, district)
    #     g_list.append(g)
    #     print("城市: %s, 区县: %s  %s, 总页数: %s, 当前页数: %s" % (city, district,dis, number, i))
    # gevent.joinall(g_list)


# 获取每一个行政区,
def get_html_page(url, city, district):
    try:
        html = s.get(url, headers=headers)
        html.encoding = html.apparent_encoding
        tree = etree.HTML(html.text)
        chengjiao_number = tree.xpath("//div[@class='total fl']/span/text()")[0].strip()
    except Exception as e:
        return "请求失败"

    # 判断 当前区下的成交的房数量


    if int(chengjiao_number) == 0:
        print(district, '没有数据')
        return
    # elif int(chengjiao_number) > 3000:    # 第一次跑判断为获取全部数据
    # elif int(chengjiao_number) > 3000000:  # 忽略次分支              在 beike_map.py 中修改过，所以 chengjiao_number 永远小于 2000
    #     next_data, next_dist = get_next_register(url)
    #     for disturl, number in next_data.items():
    #         print("街道: ", next_dist[disturl], disturl, number, )
    #         get_page_data(number, disturl, city, district)
    #     return
    else:
        print('当前行政区: %s, %s, 数量: %s' % (city, district, chengjiao_number))
        get_page_data(chengjiao_number, url, city, district)


def run():
    #df = get_deal_time_1()

    # 生成最新的二手房映射表
    city_map = get_esf_code_map()
    print("city_map: ", city_map)
# shen

    for city_name in city_map:  # 城市名   多个程序一起跑时更改 city_name
        try:
            if info_base.find_one({"城市": city_name[0]}):
                print("这个城市正在抓或者已经抓过了: %s" % city_name)
                continue

            register, CHENGJIAO = get_regionscj(city_name, city_map)
            print("当前城市: %s, \n抓取到的分区: %s, \n" % (city_name, register))
            if not CHENGJIAO:  # 没有成交字段
                print("%s: 没有成交字段," % city_name)
                continue

            # star = time.time()  # 计时,单个城市的爬取速率
            # p_list = []
            for district, disturls in register.items():
                for disturl in disturls:
                    get_html_page(disturl, city_name, district)

            #     dealTime = get_deal_time_2(df, district) # 获取最近成交时间
            #
            #     p = multiprocessing.Process(target=get_html_page, args=(disturl, city_name, district, dealTime))
            #     p.start()
            #     p_list.append(p)
            # for p in p_list:
            #     p.join()

            print(city_name)
        except Exception as  e:
            print('aaaaaaaaaaaa',e)


if __name__ == '__main__':
    run()

