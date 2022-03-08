import requests
from lxml import etree
import pymongo
from urllib import parse
from lxml import etree
import redis
import random
from config2 import get_proxy
import threading
import queue

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
    retryWrites="false")['房天下']['小区_数据_202202']
hash_table = redis.Redis(host="192.168.1.230", port=6379, db=7)
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    # "cookie": "global_cookie=c6aoaf4j7v7qlpk8n9w9glfw350kn8dhasc; global_wapandm_cookie=21yy14cclipulx9pmag96412a2ekn9trr3j; lastscanpage=0; city=nc; csrfToken=wPS-ZjYTKrv-2_moKlqLinTA; __utma=147393320.67191117.1617855649.1642491378.1645583051.118; __utmc=147393320; __utmz=147393320.1645583051.118.71.utmcsr=nc.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; unique_cookie=U_t0v9ikomca7hqraskkxkrfo5u1wkzyxno99*8; g_sourcepage=esf_xq%5Esy_wap; mencity=lnta; unique_wapandm_cookie=U_g2qlgbem2je8ghy1km0ztnpmc2rkzyxhf6t*6",
    "pragma": "no-cache",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"98\", \"Google Chrome\";v=\"98\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Mobile Safari/537.36"
}


def get_zb(city, name, d):
    d = dict(d)
    gaode_key = [
        "ac2d0d6951b7662e1b98aabb51b4aeb6",
        "705d303822d6685c2b05915464483a9c",
        # "9411ece7ba7c9ff934a093219215b47d",
        "de3514f87e2d145179e4adbd0cb01b1d",
        "f7e4985b165ebcb8d9976d0af95de9ff"
    ]
    keyword = name
    try:
        try:
            text = str(hash_table.hget(name='xiaoqu', key=keyword), encoding="utf-8").split(',')
        except Exception as e:
            url = 'https://restapi.amap.com/v3/place/text?citylimit=true&city=' + city + \
                  '&keywords=' + keyword + '&offset=20&page=1&key=' + \
                  random.choice(gaode_key)
            zb = requests.get(url).json()['pois']
            text = zb[0]['location'].split(',')
            # print(keyword)
            try:
                hash_table.hset(name='xiaoqu', key=keyword, value=zb[0]['location'])
            except:
                pass
        d['longitude'] = text[0]
        d['latitude'] = text[1]
        # print(d)
        return d
    except Exception as e:
        print('未获取到坐标')
        d['longitude'] = 0
        d['latitude'] = 0
        return d


def getitem(item):
    url = item['小区url']
    for _ in range(6):
        try:
            proxies = {"https": get_proxy()}
            res = requests.get(url, headers=headers, proxies=proxies)
            if '获取小区失败' in res.text:
                item['产权描述']='获取小区失败'
                info_base.update_one({'_id': item['_id']}, {"$set": item})
                return 
            res.encoding = 'utf8'
            html = etree.HTML(res.text)
            i = html.xpath('//section[@class="xqItems flextable-space xqGenerInfo"]/div[2]')[0]
            # item={}
            # item['建筑年代']=i.xpath('./ul[1]/li[1]/p/text()')[0]
            item['物业类型'] = i.xpath('./ul[1]/li[2]/p/text()')[0]
            item['房屋总数'] = i.xpath('./ul[1]/li[3]/p/text()')[0]
            item['楼栋总数'] = i.xpath('./ul[1]/li[4]/p/text()')[0]
            item['绿化率'] = i.xpath('./ul[1]/li[5]/p/text()')[0]
            item['容积率'] = i.xpath('./ul[1]/li[6]/p/text()')[0]
            item['产权描述'] = i.xpath('./ul[2]/li[1]/p/text()')[0]
            item['建筑类型'] = i.xpath('./ul[2]/li[2]/p/text()')[0]
            item['物业费'] = i.xpath('./ul[2]/li[3]/p/text()')[0]
            # item['物业公司']=i.xpath('./ul[2]/li[5]/p/text()')[0]
            item['停车位'] = i.xpath('./ul[2]/li[6]/p/text()')[0]
            # item['开发商']=i.xpath('./ul[2]/li[7]/p/text()')[0]
        except Exception as e:
            
            continue
        item = get_zb(item['城市'], item['小区'], item)
        print(item)
        info_base.update_one({'_id': item['_id']}, {"$set": item})
        return
    info_base.update_one({'_id': item['_id']}, {"$set": item})

# a=info_base.find_one({'小区url': 'https://m.fang.com/xiaoqu/lnta/1633132991.html'})
# # print(a)
# getitem(a)

def run():
    while 1:
        data = q.get()
        getitem(data)


if __name__ == '__main__':
    # for data in info_base.find({'产权描述': None}):
    #     getitem(data)

    q = queue.Queue(60)
    for t in range(30):
        t = threading.Thread(target=run)
        t.setDaemon(True)
        t.start()
    for d in info_base.find({'产权描述': None}, no_cursor_timeout = True):
        q.put(d)
    time.sleep(100000)
