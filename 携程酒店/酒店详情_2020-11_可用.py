import json
import time
import datetime
import os
import re
import requests
import pandas as pd
import numpy as np

from queue import Queue
from threading import Thread
from config import get_cityId


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

# 建立连接
# mymong = pymongo.MongoClient(host='localhost',port=27017)['中国房价网']['已爬取url']
url_data = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['携程酒店']['已爬取文件']


class HotelInfo(object):
    queue = Queue()
    cookie = '' \
             'aQQ_ajkguid=6305AFCC-CBC0-7E81-B772-0F3E8CAF04D0; id58=e87rkF62fA0P+69+G5dJAg==; 58tj_uuid=93de6c54-5f88-45a3-8243-34ae4a65663d; als=0; _ga=GA1.2.412851100.1589340123; aQQ_brokerguid=5CBF0591-9D1B-4195-94B3-52DEC65CF2D0; isp=true; wmda_uuid=d4601febfb8e422f420417ddde35517d; wmda_visited_projects=%3B6289197098934; sessid=3F2BFCBB-1877-7D9D-7B88-65CF0606151D; lps=http%3A%2F%2Fuser.anjuke.com%2Fajax%2FcheckMenu%2F%3Fr%3D0.07922823048794725%26callback%3DjQuery111309304314165137022_1591757640578%26_%3D1591757640579%7Chttps%3A%2F%2Fhy.fang.anjuke.com%2Floupan%2Fxiangce-446795.html%3Ffrom%3Dloupan_tab; twe=2; Hm_lvt_c5899c8768ebee272710c9c5f365a6d8=1589767849,1590485498,1591324449,1591757645; lp_lt_ut=4971900fb59ca0493a0bc0529772a073; Hm_lpvt_c5899c8768ebee272710c9c5f365a6d8=1591757926; _gid=GA1.2.1652451907.1591757942; wmda_session_id_6289197098934=1591769655588-85e70f80-1a52-9e47; new_uv=28; init_refer=; new_session=0; __xsptplusUT_8=1; ajk_member_verify=f%2Fj9LbXdPpabOrY6ZkUPOFe%2FGyTml%2BX%2BIbvg4cYzGWY%3D; ajk_member_verify2=MTUzNjAwMzE3fFUxNTUwOTI0MTkxMjQ3N3wx; ctid=293; __xsptplus8=8.30.1591769657.1591770080.14%232%7Cwww.baidu.com%7C%7C%7C%7C%23%23Cs05xR7uEtn86LXjWUMBBGhP1zhtU0HR%23; ajkAuthTicket=TT=af15525d3c71c205bf40b116d42c2a30&TS=1591770081864&PBODY=PCeCEJ-tBd3LC2zFL17he9pp89krf7eQ4UDEF73YjT4A-DQoTm5SFvfX6vOrhKSrjsvf68qPiKoLGLLNQsIcqiVKwa-yzEeiNIfJwVshdAnxC47VJdOVbmyfjUrGKKaH9tZpmdHtA198fRxsDujbKeN3QivweiIxidetJAPjxp8&VER=2; xzfzqtoken=BwK%2BVKixWSkOnSMlfUKfhjId0F4Deo6E3EGkq%2F2l%2Fbvs%2BfEg2PaSUFeBWfmt%2BUxjin35brBb%2F%2FeSODvMgkQULA%3D%3D'

    def __init__(self, path, city, city_id, save_file):
        self.path = path
        self.city = city
        self.city_id = city_id
        self.save_file = save_file

    def get_proxy(self):
        return requests.get("http://47.106.223.4:50002/get/").json().get('proxy')

    def delete_proxy(self, proxy):
        html = requests.get("http://47.106.223.4:50002/delete/?proxy={}".format(proxy))
        return html.text

    def cleaning_data(self):
        df = pd.read_excel(self.path)
        df = df.drop_duplicates(subset='id')

        exists_path = os.path.join(self.save_file, f'{self.city}.csv')
        if os.path.exists(exists_path):
            df1 = pd.read_csv(exists_path)
            df = df[~df['id'].isin(df1['id'])]
        print(f'去掉已存在的数据后: {df.shape}')
        return df

    def make_date(self):
        d = datetime.datetime.now().date()
        d1 = d + datetime.timedelta(hours=24)
        today = d1.strftime("%Y-%m-%d")  # 今天，如 "2020-06-11"
        last_time = d1 + datetime.timedelta(hours=24)
        tomorrow = last_time.strftime("%Y-%m-%d")  # 明天，如 '2020-06-12'
        return today, tomorrow

    def change_str(self, str1):
        str2 = str1.replace('：', '').replace('\n', '').replace('\r', '').replace(' ', '')
        str3 = str2.replace(' ', '').replace('\t', '').replace('暂无数据', '')
        return str3

    def get_html(self, hotelId):
        headers = {
            'origin': 'https://hotels.ctrip.com',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        }
        url = 'https://hotels.ctrip.com/hotels/detail/'

        today, tomorrow = self.make_date()
        params = {
            "hotelId": hotelId,
            "checkIn": str(today),
            "checkOut": str(tomorrow),
            "cityId": self.city_id,
            "minprice": "",
            "mincurr": "",
            "adult": "1",
            "children": "0",
            "ages": "",
            "crn": "1",
            "curr": "",
            "fgt": "",
            "stand": "",
            "stdcode": "",
            "hpaopts": "",
            "mproom": "",
            "ouid": "",
            "shoppingid": "",
            "roomkey": "",
            "highprice": "-1",
            "lowprice": "0",
            "showtotalamt": "",
        }
        ip_number = 5
        while ip_number > 0:
            proxy = self.get_proxy()
            proxies = {'http': 'http://%s' % proxy, 'https': 'https://%s' % proxy}
            if not proxy:
                print("没有ip, 等待30分钟")
                time.sleep(30)
                continue

            number = 3
            while number > 0:
                try:

                    res = requests.get(url, params=params, headers=headers, timeout=(2, 5), proxies=proxies)
                    # if url_data.find_one({'已爬取的url': res.url}):
                    #     print('当前url已爬取')
                    #     continue
                    # print(res.url)
                    # url_data.insert_one({'已爬取的url': res.url})
                    #print(res.url)###################################################################################################################################
                    if '404Apf_NotFoundController' in res.text:
                        return ''
                    return res

                except Exception as e:
                    # print(url, e)
                    number -= 1
                    continue

            self.delete_proxy(proxy)
            ip_number -= 1
            continue
        return ''

    def get_home_info(self, hotelId):
        url = 'https://m.ctrip.com/restapi/soa2/16709/json/rateplan?testab=dfb1cddf4c131c511e73c1259ed0e35e437772a59cd76cf2cb8848b7a7218a41'
        headers = {
            'origin': 'https://hotels.ctrip.com',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        }
        today, tomorrow = self.make_date()
        params = {
            "checkIn": str(today),
            "checkOut": str(tomorrow),
            "priceType": "",
            "adult": 1,
            "popularFacilityType": "",
            "mpRoom": "",
            "fgt": "",
            "hotelUniqueKey": "",
            "child": 0, "roomNum": 1,
            "masterHotelId": hotelId,
            "age": "",
            "cityId": self.city_id,
            "roomkey": "",
            "minCurr": "",
            "minPrice": "",
            "hotel": hotelId,
            "ctripTrace": {
                "listRoomId": 406584048, "listShadowId": 0, "listPrice_cx": "458", "exchange": "1.0", "currency": "RMB",
                "maskDifAvgCnyPrice": "0"
            },
            "filterCondition": {},
            "genk": True,
            "genKeyParam": {
                "a": hotelId,
                "b": str(today),
                "c": str(tomorrow)
                , "d": "zh-cn",
                "e": 2
            },
            "head": {
                "Locale": "zh-CN", "Currency": "CNY", "Device": "PC", "UserIP": "183.17.229.64", "Group": "",
                "ReferenceID": "", "UserRegion": "CN", "AID": None, "SID": None, "Ticket": "", "UID": "",
                "IsQuickBooking": "",
                "ClientID": "1591869355582.1fns3c", "OUID": None, "TimeZone": "8", "P": "65655477155",
                "PageID": "102003",
                "Version": "",
                "HotelExtension": {
                    "WebpSupport": True, "group": "CTRIP", "Qid": "367584861701", "hasAidInUrl": False,
                    "hotelUuidKey": "aH0Y1ZR4me0aIpzWfYAtYF5EdYa1e7hEBOjo6WZYZfvXHj5QWq7jUYN0RGzJ6NvsbjZY8QiS4iUfi7cRXYSMY8XwNkyGlj1AYXDeAZyp4jzOygYPSv1fxdDYZowaojQqeo4iOFYkYPYL5v7hepZYSbisMY4YNYDAIa7W3Y7ZYAmifAiSpiAHjbY59w6SE7TYNcw6TEnhJ9BYFcwdYZ7RsAwQMWH9wPmYMTWapjo4wTUEM4y4PJqojLpvNYMaRd4wSbIbbxNLj1BjSceUgjaMiBBxshignYdDEBsyZbWl6JoYcgR08JGavfpRz3jZ7wf5vnHiP8JZMJM5J81jOHY8Y9AjQ8w58vscjkY4tR8cJSFi3awPpegDjf4wsLESYOgRHLJPDiMlw1Oe5Njh4YnhEsYf3R7lwPdWANwkZYP1W5hjmZwPUE8QwMsjUXJZS",
                    "hotelUuid": "16LXVtZGQXBPC7lS"},
                "Frontend": {"vid": "1591869355582.1fns3c", "sessionID": 91, "pvid": 545}}, "ServerData": ""
        }

        ip_number = 5
        while ip_number > 0:

            proxy = self.get_proxy()
            proxies = {'http': 'http://%s' % proxy, 'https': 'https://%s' % proxy}
            if not proxy:
                print("没有ip, 等待30s")
                time.sleep(30)
                continue

            number = 3
            while number > 0:
                try:
                    res = requests.post(url, headers=headers, json=params, timeout=(2, 7), proxies=proxies)
                    resJson = res.json()
                    return resJson
                except Exception as e:
                    # print('出错', e)
                    time.sleep(1)
                    number -= 1
                    continue

            self.delete_proxy(proxy)
            ip_number -= 1
            continue
        return ''

    def get_city_hotel(self, data):
        while True:
            if self.queue.empty():
                break
            hotelId = self.queue.get()
            response = self.get_html(hotelId)

            house_resJson = self.get_home_info(hotelId=hotelId)

            if not response or not house_resJson:
                self.queue.task_done()
                continue

            res = re.search(r'''window\.IBU_HOTEL=(.*);
    __webpack_public_path__''', r'%s' % response.text, flags=re.S).group(1)
            resJson = json.loads(res)
            if not resJson:
                self.queue.task_done()
                continue

            item = {}
            item['id'] = hotelId
            try:
                placeList = resJson.get('initData').get('position').get('placeList').get('list')
                if not placeList:
                    item['附近'] = {}
                else:
                    item['附近'] = {i['type']: i['hover'] for i in placeList}
            except:
                item['附近'] = {}

            try:
                base_label = resJson.get('initData').get('staticHotelInfo').get('hotelInfo').get('basic').get('label')
            except:
                print("base_label: 'NoneType' object has no attribute 'get'" )
                self.queue.task_done()
                continue
            if not base_label or base_label is None:
                item['开业时间'] = ''
                item['客房数'] = ''
            try:
                for label in base_label:
                    if '开业' in label:
                        item['开业时间'] = label.split('：')[1]
                    if '客房' in label:
                        item['房间数量'] = label.split('：')[1]
            except:
                print("for label in base_label:  TypeError: 'NoneType' object is not iterable")
                item['开业时间'] = ''
                item['客房数'] = ''
            item['酒店简介'] = resJson.get('initData').get('staticHotelInfo').get('hotelInfo').get('basic').get(
                'description')

            # 获取户型信息
            baseRooms = house_resJson.get('Response').get('baseRooms')
            it_d = dict()
            for rooms in baseRooms:
                it = dict()
                roomName = rooms.get('baseRoom').get('roomName')
                try:
                    it['面积'] = rooms.get('baseRoom').get('roomSize').get('text')
                except:
                    it['面积'] = ''
                it['楼层'] = rooms.get('baseRoom').get('roomFloor')
                it['户型类型'] = ''.join(
                    list(set([','.join(i.get('bed').get('contentList')) for i in rooms.get('saleRoom')])))
                try:
                    it['户型均价'] = np.mean(
                        [round(float(i.get('money').get('price') or 0), 2) for i in rooms.get('saleRoom')])
                except Exception as e:
                    #print(e)
                    it['户型均价'] = ''
                it_d[roomName] = it
            item['户型详情'] = it_d
            print(item)##########################################################################################
            data.append(item)

            self.queue.task_done()

    def run(self):
        data = []
        df = self.cleaning_data()
        if not df.shape[0]:
            return
        id_list = df['id'].tolist()
        for hotelId in id_list:
            self.queue.put(hotelId)

        for i in range(15):
            time.sleep(0.2)
            t = Thread(target=self.get_city_hotel, args=(data,))
            t.daemon = True
            t.start()
        self.queue.join()

        df1 = pd.DataFrame(data)
        print('开始保存数据: ', df1.shape)
        save_path = '{}/{}.csv'.format(self.save_file, self.city)
        if os.path.exists(save_path):
            df1.to_csv(save_path, mode='a', index=False, header=False)
        else:
            df1.to_csv(save_path, mode='a', index=False, header=True)
        print('数据保存成功。')
        print('>' * 50, '\n')


if __name__ == '__main__':

    save_file = '酒店详情信息'
    for i in os.listdir('酒店数据'):
        if url_data.find_one({'已爬取的文件名': i}):
            print('当前文件所有字段已爬取并保存完毕')
            continue
        print('开始：', i)
        path = '酒店数据/' + i
        city = i.split('_')[1]
        city_id = get_cityId(city)
        HotelInfo(path, city, city_id, save_file).run()
        url_data.insert_one({'已爬取的文件名': i})

