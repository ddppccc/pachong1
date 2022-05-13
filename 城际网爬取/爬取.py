import random
import pandas as pd
import re
import time
import requests
import pymongo
import uuid
import json
from urllib import parse
from lxml import etree
import time
from concurrent.futures import ThreadPoolExecutor
# from config2 import get_proxy
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
            retryWrites="false")['城际网']['教育数据_04']

has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['城际网']['杭州教育数据_05-2']

import redis

hash_table = redis.Redis(host="192.168.1.230", port=6379, db=7)




# 高德坐标获取（v3）
def get_zb(keys):
    try:
        data = hash_table.hget(name='xiaoqu', key=keys)
        location = str(data, encoding='utf8').split(',')
        return location[0], location[1]
    except:
        for timeout in range(5):
            try:
                # api请求函数
                #     print(keywords)
                gaode_key = [
                    "ac2d0d6951b7662e1b98aabb51b4aeb6",
                    "705d303822d6685c2b05915464483a9c",
                    # "9411ece7ba7c9ff934a093219215b47d",
                    "de3514f87e2d145179e4adbd0cb01b1d",
                    "f7e4985b165ebcb8d9976d0af95de9ff",
                    "24a40306a06d751baee2b89469e6bdc7"
                ]
                url = 'https://restapi.amap.com/v3/place/text?keywords=' + keys + '&offset=20&page=1&key=' + random.choice(gaode_key)
                zb = requests.get(url).json()['pois']
                text = zb[0]['location']
                hash_table.hset(name='xiaoqu', key=keys, value=str(text))
                return text.split(',')[0], text.split(',')[1]
            except Exception as e:
                print('高德接口访问失败了', '再次尝试')
        print('尝试失败,高德上无法获取该地址坐标')
        return 0.0, 0.0

def get_IP(bj):
    if bj:
        while True:
            try:
                return requests.get('http://1.116.204.248:5000/proxy').text
            except:
                print('暂无ip，等待5秒')
                time.sleep(5)
    else:
        while True:
            try:
                return requests.get('http://47.106.223.4:50002/get/').json().get('proxy')  #字典取值 ‘字典中proxy健中的值’
            except:
                print('暂无ip，等待5秒')
                time.sleep(5)


def create_request(i,page):
    # s=['beijing','shanghai','guangzhou','shenzhen','tianjin','chongqing','wuhan','hangzhou','nanjing','chengdu','shenyang','suzhou','xian','zhengzhou','qingdao','xiamen']

    base_url1 = f'http://www.go007.com/ditu/{i}_hangzhou/p{str(page)}/'
    #http://www.go007.com/ditu/xiaoxue_nanjing/
    # http://www.go007.com/ditu/xiaoxue_hangzhou/
    url=base_url1

    headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'www.go007.com',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
        }

    for i in range(5):
        try:
            proxy = get_IP(True)  # 此处加入ip代理
            proxies = {"https": proxy,'http': proxy}
            response = requests.get(url=url, headers=headers, proxies=proxies,timeout=3)
            if response.status_code == 200:
                # print(response.text)
                data_ = response.text
                # print(data_)
                if '最后一页' in data_:                              #    判断是否为最后一页   in 表示没有
                    return data_, 1     #obj =1                      # 返回request请求数据
                else:
                    return data_, 0         #此处为超过存在范围
        except:
            pass
    return 'data_', 0


def getdata_1(data_):
    # 获取网页情况

    tree=etree.HTML(data_)
    res=tree.xpath('//ul[@class="slist"]/li')                #//ul[@class="slist"]/li
    # print(res)           li[1]/dl/dd/ol/li[2]

    for da in res:
        item = {}
        item['mingcheng'] = da.xpath('.//h3/a/text()')[0]         #/ul[@class="slist"]/li//h3/a/@href
        item['xiangqingye'] = da.xpath('.//h3/a/@href')[0]

        lis = da.xpath('./dl/dd/ol/li')                   #//ul[@class="slist"]/li/dl/dd/ol/li  下面的文本
        for li in lis:

            text = ''.join(li.xpath('./text()'))                #第一个li标签下的文本是否含有 学校类型   将文本以 空格进行连接
            if '学校类型' in text:
                item['学校类型'] = li.xpath('./span/text()')

            else:
                # 对一个对象使用split（）方法，会将其分割整合成为一个列表，那么自然就可以采用下标来查找相应的值
                lists = text.split('：')                                  #文本以 ： 进行分割 成为列表  通常用于将字符串切片并转换为列表。
                if lists[0] == '联系电话' or lists[0] == '电话':            #  判断是否为电话号码  因为为乱码，所以需要这一步骤
                    lists[1] = lists[1].replace("%", "\\").encode('utf-8').decode('unicode_escape')

                item[lists[0]] = lists[1]
        # print(item)
        item['x'], item['y'] = get_zb(item['mingcheng'])   #---------高德地理坐标---------------------------------
        if 'youeryuan' not in item['xiangqingye'] or 'xiaoxue' not in item['xiangqingye']:
            item = getdata_(item)
        print(item)
        info_base.insert_one(item)


def getdata_(item):
    base_url ='http://www.go007.com'
    url = base_url+item['xiangqingye'][:24]+'_lianxiwm.html'
    # print(url)
    # 'http://www.go007.com/ditu/gaozhong/1430457_lianxiwm.html'    #联系我们取得联系电话
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
    }


    proxy = get_IP(True)  # 此处加入ip代理
    proxies = {"https": proxy,'http': proxy}

    response = requests.get(url=url, headers=headers,proxies=proxies)  # (3)
    if response.status_code == 200:
        # print(response.text)
        data_ = response.text
        # print(data_)
        print(response.text)
        data_2 = response.text
        tree = etree.HTML(data_2)
        try:
            item['通讯地址']  = tree.xpath('//dd[@class="lxfs"]/dl[1]//dd')
            cc = tree.xpath('//dd[@class="lxfs"]/dl[2]//dd')
        except:
            item['通讯地址']=None
        try:
            item['电话'] = cc.replace("%", "\\").encode('utf-8').decode('unicode_escape')
        except:
            item['电话'] =None
    # print(item)
        return item

    else:
        return item


if __name__ == '__main__':
    # lists = list(info_base.find())
    # df = pd.DataFrame(lists)
    # df.to_csv('南京教育数据_04.csv', index=False)
    # info_base.delete_many({})
    # has_spider.delete_many({})
    # 南京教育   大学   高中  初中   小学
    # http://www.go007.com/ditu/daxue_nanjing/
    # http://www.go007.com/ditu/gaozhong_nanjing/
    # http://www.go007.com/ditu/chuzhong_nanjing/
    # http://www.go007.com/ditu/xiaoxue_nanjing/
    # http://www.go007.com/ditu/youeryuan_nanjing/
    # http://www.go007.com/ditu/youeryuan_nanjing/p2/
    # http://www.go007.com/ditu/youeryuan_nanjing/p3/

    # http://www.go007.com /ditu/daxue_hangzhou/
    # 幼儿园    xpath  //ul[@class="slist"]/li
    l=['youeryuan','xiaoxue','chuzhong','gaozhong','daxue']
    # print(len(l))
    for i in l:  # 注意左闭右开
        page = 1

        while True:
            if has_spider.find_one({i + str(page):'已爬取'}):
                print('该页数据已爬取，开始下一页或者下个界面')
                page+=1
                continue
            data_, bj = create_request(i, page)
            if bj == 0:
                break       #跳出while循环   进行for 的遍历
           #获取数据解析
            getdata_1(data_)

            has_spider.insert_one({i + str(page): '已爬取'})


            page += 1
            time.sleep(1)
            #     print(page)