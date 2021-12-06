import requests
from lxml import etree
import re
import time
import random
from config import gainiandict,bankuaidict
import pymongo
from urllib import parse
# from web import getcookie
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
            retryWrites="false")['同花顺']['概念行业板块_数据_202108']
has_info = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['同花顺']['概念行业板块_去重_202108']

def headers():
    with open('cookie.txt', 'r') as f:
        Cookie = f.read()
    headers = {

        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': f'log=; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1={str(int(time.time()))}; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1={str(int(time.time()))}; v=AzTSqnZb6XfHjX276uy2VyvhBfmlDVGPmjXsQM6VwWtCatov9h0oh-pBvJAd',
        # 'Cookie': Cookie,
        'Host': 'q.10jqka.com.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    }
    return headers

keys= {'概念板块':gainiandict,
       '同花顺行业':bankuaidict}
def get_proxy():
    try:
            return requests.get('http://1.116.204.248:6000/proxy2').text
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

for k,v in gainiandict.items():
    code=re.findall('code/(\d+)/',v)[0]
    pages=1
    page=1
    tag=0
    while tag<pages:
        tag += 1
        while True:
            # 概念264648    同花顺行业199112
            # url=f'http://q.10jqka.com.cn/gn/detail/field/264648/order/desc/page/{str(page)}/ajax/1/code/{code}'
            url=f'http://q.10jqka.com.cn/gn/detail/code/308594/'
            # url=f'http://q.10jqka.com.cn/gn/detail/field/199112/order/desc/page/{str(page)}/ajax/1/code/{code}'
            # proxies = {"http": get_proxy()}
            res=requests.get(url,headers=headers())
            rescook=res.cookies.get_dict()
            time.sleep(random.choice([5,10,15]))
            if res.status_code != 200:
                # getcookie(url)
                time.sleep(10)
                print(res.status_code)
                continue
            res.encoding='gbk'
            html=etree.HTML(res.text)
            if '暂无成份股数据' in res.text:break
            if page == 1:
                pages=html.xpath('//*[@id="m-page"]/span/text()')[0]
                pages=re.findall('\d+/(\d+)',pages)[0]
                pages=int(pages)
            if page < pages:
                page += 1

            box=html.xpath('/html/body/table/tbody/tr')
            for i in box:
                item = {}
                item['代码']=i.xpath('./td[2]/a/text()')[0]
                item['板块']='概念板块'
                item['概念/行业']=k
                item['名称']=i.xpath('./td[3]/a/text()')[0]
                item['现价']=i.xpath('./td[4]/text()')[0]
                item['涨跌幅']=i.xpath('./td[5]/text()')[0]
                item['涨跌']=i.xpath('./td[6]/text()')[0]
                item['涨速']=i.xpath('./td[7]/text()')[0]
                item['换手率']=i.xpath('./td[8]/text()')[0]
                item['量比']=i.xpath('./td[9]/text()')[0]
                item['振幅']=i.xpath('./td[10]/text()')[0]
                item['成交额']=i.xpath('./td[11]/text()')[0]
                item['流通股']=i.xpath('./td[12]/text()')[0]
                item['流通市值']=i.xpath('./td[13]/text()')[0]
                item['市盈率']=i.xpath('./td[14]/text()')[0]
                # if info_base.find_one(item):
                #     print('数据已存在')
                #     continue
                print(item)
                print(item)
                # try:
                #     info_base.insert_one(item)
                # except:
                #     print('存储出错')
            break
























# urls=['http://q.10jqka.com.cn/gn/','http://q.10jqka.com.cn/thshy/']
# res=requests.get(urls[0],headers=headers)
# res.encoding='gbk'
# html=etree.HTML(res.text)
# box=html.xpath('/html/body/div[2]/div[1]/div/div/div/a')
# dict={}
# for i in box:
#     title=i.xpath('./text()')[0]
#     url=i.xpath('./@href')[0]
#     dict[title]=url
# for k,v in dict.items():
#     print(f'"{k}":"{v}",')


