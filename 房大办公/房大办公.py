import random
import re
import json
import pymongo
import requests
from lxml import etree
import time
from urllib import parse
from lxml import etree

from concurrent.futures import ThreadPoolExecutor

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
    retryWrites="false")['房大办公']['数据_202110']

url_data = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['房大办公']['url_202110']


def get_proxy():
    try:
        return requests.get('http://1.116.204.248:5000/proxy').text
    except:
        print('暂无ip，等待20秒')
        time.sleep(20)


null = 'null'

startUrl = 'https://sh.zoomoffices.com/list.html'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    # cookie: Hm_lvt_565636297e5018fa9b2eb0de9ddeb696=1628478181; cityPositionId=3; cityPosition=5LiK5rW3; Hm_lpvt_565636297e5018fa9b2eb0de9ddeb696=1628479064
    'referer': 'https://bj.zoomoffices.com/',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
}


def get_tree(url, headers):
    while True:
        try:
            prox = get_proxy()
            proxies = {'http': prox,
                       'https': prox}
            response = requests.get(url, headers=headers, proxies=proxies, timeout=(3, 5))
            response.encoding = response.apparent_encoding
            res = response.text
            tree = etree.HTML(res)
            if '房大办公' in tree.xpath("//title/text()")[0] or '平台' in tree.xpath("//title/text()")[0]:
                return tree
            else:
                print(tree.xpath("//title/text()")[0])
        except:
            continue


def get_city(startUrl):
    dicts = {}
    tree = get_tree(startUrl, headers)
    lis = tree.xpath('//div[@class="citybox"]//a')
    for li in lis:
        city = ''.join(li.xpath('./span/text()'))
        url = ''.join(li.xpath('./@href'))
        cityId = ''.join(li.xpath('./@data_cityid'))
        urlList = []
        l1 = []
        l2 = []
        for pg in range(1,100):
            l1.append(url[:-5] + '-' + cityId + '-1-1-0-0-0-0-0-0-0-'+str(pg)+'-0--0-0--' + '.html')
            l2.append(url[:-5] + '-' + cityId + '-2-1-0-0-0-0-0-0-0-'+str(pg)+'-0--0-0--' + '.html')
        urlList.append(l1)
        urlList.append(l2)
        dicts[city] = urlList
    return dicts


def get_data(urlList, city, lx):
    for url in urlList:
        if url_data.count({'url':url}):
            continue
        tree = get_tree(url, headers)
    # if url_data.count({'url':url}):
    #     nextUrl = ''.join(tree.xpath('//div[@class="pages"]/a')[-1].xpath('./@href'))
    #     if nextUrl == url:
    #         return
    #     get_data(nextUrl, city, lx)
    # else:
        if len(tree.xpath('//div[@class="left clear"]/ul/li')) == 0:
            print('当前url无数据:', url)
            continue
        textList = tree.xpath('//script')
        for tex in textList:
            if 'var unionApi' in ''.join(tex.xpath('./text()')):
                text = ''.join(tex.xpath('./text()'))
                string1 = ''.join(re.findall('var unionApi=(.+}]}})', text))
                null = 'null'
                dicts = eval(string1)
                datas = dicts['data']['building_info']
                for data in datas:
                    item = {}
                    item['city'] = city
                    item['类型'] = lx
                    item['id'] = data['id']
                    item['lng'] = data['lng']
                    item['lat'] = data['lat']
                    item['name'] = data['zh_name']
                    item['价格'] = data['price']
                    item['预计成交价'] = data['predict_price']
                    item['价格单位'] = data['price_unit_name'][2:].replace("\\", '')
                    item['综合评分'] = data['score']
                    item['区县'] = data['district_name']
                    item['商圈'] = data['commercial_center_name']
                    item['特点'] = data['building_tags']
                    item['标签'] = data['label_info']
                    item['轨道交通'] = data['building_route']
                    item['数据来源'] = data['contact_name']
                    item['联系电话'] = data['contact_phone']
                    item['房型范围'] = data['scale']
                    dw = ''.join(re.findall('\d+?-\d+?(.+)',data['scale']))
                    item['所有房型'] = [x+dw for x in data['building_scale']]
                    item['地址'] = data['zh_addr']
                    item['房源数'] = data['tran_num']
                    item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    info_base.insert_one(item)
                    print(item)
                url_data.insert_one({'url': url})



def run():
    # info_base.delete_many({})
    # url_data.delete_many({})
    dicts = get_city(startUrl)
    for city in dicts:
        if url_data.count({city: '已爬取共享办公'}):
            print('已爬取', city)
            continue
        elif url_data.count({city: '正在爬取共享办公'}):
            print('正在爬取共享办公', city)
            continue
        url_data.insert_one({city: '正在爬取1'})
        urlList = dicts[city]
        get_data(urlList[0], city, '共享办公')
        # get_data(urlList[1], city, '写字楼')

        url_data.insert_one({city: '已爬取共享办公'})

if __name__ == '__main__':
    # pool = ThreadPoolExecutor()
    # url_data.delete_many({})
    # info_base.delete_many({})
    # print(info_base.find_one({'city':'北京','类型':'写字楼'}))
    run()
