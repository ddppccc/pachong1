# coding=utf-8
import pymongo
from urllib import parse
import requests
from lxml import etree
import time
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
            retryWrites="false")['民航']['民航_列表页链接2_202109']


headers={
    'Host': 'www.caac.gov.cn',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://www.caac.gov.cn/XXGK/XXGK/TJSJ/index_1215.html',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': '__FT10000021=2021-9-29-15-11-7; __NRU10000021=1632899467473; __RT10000021=2021-9-29-15-11-7; Hm_lvt_4014848c4e18723269ffe0193734e573=1632899468; Hm_lpvt_4014848c4e18723269ffe0193734e573=1632899852; caac=16892911; wzws_cid=52c42c91b349bcc85d2785471aa22ca8fcb46f2af0b072123bcf8e5432b14ec2a9da07159298fb4bfae1fa0328a49fb44b573f320e50f454d1071fe2e22c05ffa6229321c98020539e02c5262d54a6c5'

}


urls=[
    # 'http://www.caac.gov.cn/XXGK/XXGK/TJSJ/index_1215.html',
    # 'http://www.caac.gov.cn/XXGK/XXGK/TJSJ/index_1215_1.html',
    # 'http://www.caac.gov.cn/XXGK/XXGK/TJSJ/index_1215_2.html',
    # 'http://www.caac.gov.cn/XXGK/XXGK/TJSJ/index_1215_3.html',
    'http://www.caac.gov.cn/XXGK/XXGK/TJSJ/index_1215_5.html'
]


for url in urls:
    res=requests.get(url,headers=headers)
    res.encoding='utf8'
    html=etree.HTML(res.text)
    box=html.xpath('//div[@class="a_left"]/div/ul/li/a')
    for i in box:
        data={}
        data['标题']=i.xpath('./text()')[0]
        data['url']=i.xpath('./@href')[0]
        print(data)
        info_base.insert_one(data)
    time.sleep(30)