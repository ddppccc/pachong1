import datetime
import os
import time

import requests
import pandas as pd
from config import city_map_list, Year, Month


cookie = "_RGUID=c1461406-eb54-4f73-9943-79aa0e6d7614; _RDG=28ae06a1d31f912556093f991d178ab833; _RSG=pz4LhR0565CKONREeQU3b9; _ga=GA1.2.1005284998.1591869359; MKT_CKID=1576636848313.u5oo4.4y1z; _abtest_userid=c30f87c7-e48b-4db0-8179-f94dab411936; AHeadUserInfo=VipGrade=0&VipGradeName=%C6%D5%CD%A8%BB%E1%D4%B1&UserName=&NoReadMessageCount=0; IsPersonalizedLogin=F; UUID=D0849EC573624A8E8E95D3F7016AD3D1; nfes_isSupportWebP=1; GUID=09031071210792750836; __utma=13090024.1005284998.1591869359.1597304246.1597304246.1; __utmz=13090024.1597304246.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); FlightIntl=Search=[%22BJS|%E5%8C%97%E4%BA%AC(BJS)|1|BJS|480%22%2C%22US|%E7%BE%8E%E5%9B%BD|country%22%2C%222020-08-19%22%2C%222020-08-23%22]; login_uid=E6990F62CCB2B96BF88D24990AE6B674; login_type=6; ibulanguage=CN; ibulocale=zh_cn; cookiePricesDisplayed=CNY; HotelCityID=30split%E6%B7%B1%E5%9C%B3splitShenzhensplit2020-11-4split2020-11-05split0; MKT_Pagesource=PC; _gid=GA1.2.483068620.1606124105; MKT_CKID_LMT=1606124107405; intl_ht1=h4=1_429531,1_608516,1_8065838,1_2231618,1_436915,30_66684700; _RF1=183.17.229.64; _bfa=1.1591869355582.1fns3c.1.1606183603261.1606185847170.87.531.10650016816; _bfs=1.5; _uetsid=2957de902d6f11ebaab8cfb61624f491; _uetvid=0a1124101e4e11eba79965fbd99da94b; _bfi=p1%3D102002%26p2%3D102002%26v1%3D531%26v2%3D530; _jzqco=%7C%7C%7C%7C1606124107888%7C1.262374949.1591869358657.1606186133202.1606186174159.1606186133202.1606186174159.undefined.0.0.347.347; __zpspc=9.90.1606185851.1606186174.5%232%7Cwww.baidu.com%7C%7C%7C%25E6%2590%25BA%25E7%25A8%258B%7C%23; appFloatCnt=32"


class XieChengHotel:
    def __init__(self):
        pass

    def get_html(self, city, cityId, pageNo=1):
        headers = {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-type": "application/json;charset=UTF-8",
            "cookie": cookie,
            "origin": "https://hotels.ctrip.com",
            "p": "65655477155",
            "referer": "https://hotels.ctrip.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",

        }
        today = datetime.datetime.now().date()  # 今天，如 "2020-06-11"
        last_time = today + datetime.timedelta(hours=24)
        tomorrow = last_time.strftime("%Y-%m-%d")  # 明天，如 '2020-06-12'

        params = {
            "meta": {
                "fgt": "",
                "hotelId": "",
                "priceToleranceData": "",
                "priceToleranceDataValidationCode": "",
                "mpRoom": [],
                "hotelUniqueKey": "",
                "shoppingid": "",
                "minPrice": "",
                "minCurr": ""
            },
            "seqid": "",
            "deduplication": [5753968,31496795,15215620,2152907,40876153,5376578,6027806,26408651,1958595,5300582,6386791,
                              21336129,36190324,14095153,1006044,67847421,13481115,4836517,9639502,5444585,21630177,
                              41853137,50394431,17591275,2863931,18444358,2302188,6069044,739022,21918257],
            "filterCondition": {
                "star": [],
                "rate": "",
                "rateCount": [],
                "priceRange": {
                    "lowPrice": 0,
                    "highPrice": -1
                },
                "priceType": "",
                "breakfast": [],
                "payType": [],
                "bedType": [],
                "bookPolicy": [],
                "bookable": [],
                "discount": [],
                "zone": [],
                "landmark": [],
                "metro": [],
                "airportTrainstation": [],
                "location": [],
                "cityId": [],
                "amenty": [],
                "promotion": [],
                "category": [],
                "feature": [],
                "brand": [],
                "popularFilters": [],
                "hotArea": [],
                "ctripService": []
            },
            "searchCondition": {
                "sortType": "1",
                "adult": 1,
                "child": 0,
                "age": "",
                "pageNo": pageNo,      # TODO
                "optionType": "City",
                "optionId": f"{cityId}",  # TODO
                "lat": 0,
                "destination": "",
                "keyword": "",
                "cityName": city,  # TODO
                "lng": 0,
                "cityId": cityId,  # TODO
                "checkIn": f"{str(today)}",  # TODO
                "checkOut": f"{str(tomorrow)}",  # TODO
                "roomNum": 1,
                "mapType": "gd",
                "travelPurpose": 0,
                "countryId": 1,
                "url": f"https://hotels.ctrip.com/hotels/list?city={cityId}&checkin={str(today).replace('-', '/')}&checkout={str(tomorrow).replace('-', '/')}&optionId={cityId}&optionType=City&directSearch=0&display={city}&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1&",
                "pageSize": 25,
                "timeOffset": 28800,
                "radius": 0,
                "directSearch": 0,
                "signInHotelId": 0,
                "signInType": 0
            },
            "queryTag": "NORMAL",
            "genk": True,
            "genKeyParam": {
                "a": 0,
                "b": str(today),  # TODO
                "c": str(tomorrow),  # TODO
                "d": "zh-cn",
                "e": 2
            },
            "webpSupport": False,
            "platform": "online",
            "pageID": "102002",
            "head": {
                "Version": "",
                "userRegion": "CN",
                "Locale": "zh-CN",
                "LocaleController": "zh-CN",
                "TimeZone": "8",
                "Currency": "CNY",
                "PageId": "102002",
                "webpSupport": True,
                "userIP": "",
                "P": "65655477155",
                "ticket": "",
                "clientID": "1591869355582.1fns3c",
                "group": "ctrip",
                "Frontend": {
                    "vid": "1591869355582.1fns3c",
                    "sessionID": 87,
                    "pvid": 531
                },
                "Union": {
                    "AllianceID": "",
                    "SID": "",
                    "Ouid": ""
                },
                "HotelExtension": {
                    "group": "CTRIP",
                    "hasAidInUrl": False,
                    "Qid": "226747472106",
                    "WebpSupport": True,
                    "hotelUuidKey": "7H4Y4fiB8efsE4SEGYLoYltEHYpQeOdE5hjpGWSYzgjBGWQlYZDjgY7NvMBrbDv7QwDY1Axd0w8mYnUjgY9oIkzYLGyPoj6teG3ezhYmfjLoyhYQ4vOqvQAYm3wfpjl4ekdi83JdYoYkcv7dedUY9bi31YNYDYMfI1TWBYnbYBZip7iM8iaSj1YlOwgTELfYMGwznETcJ7XYQfwnY0nRtLwksWHZwMHRscvDzy4qjXGYdAWXZvo6WdFiTYfkRndw1AI66xNPjP5j14eOAjM7iggxkmicgYScEqAyf1WgoJzYz0RfQJ9tvqZR5qjzFwL1v13iszJocJMnJ0ajPpYGY4qjogwpFvotjFYPGRBqJnkiMnwoXeN4jcfwL1EaYDnRaSJTDiXdwQPeznjnDYsUEZY6lRb5w4kWF3wb4RXbvoNyLmENLjh3isAWhnw6Q"
                }
            }
        }
        url = 'https://m.ctrip.com/restapi/soa2/16709/json/HotelSearch?testab=40664a87d2ca70ad99f77ec804090703200d0e80ffe5510854d3bdfdd5d8d2e3'
        while True:
            try:
                res = requests.post(url, headers=headers, json=params, timeout=(2, 7))
                resJson = res.json()
                return resJson
            except Exception as e:
                print('出错', e)
                time.sleep(1)
                continue

    def parse(self, city_map, page, data_all, error_flag=0):
        city_pinyin, city, cityId = city_map['data'].split('|')
        html = self.get_html(city, cityId, pageNo=page)
        try:
            hotelList = html.get('Response').get('hotelList').get('list')
        except Exception as e:
            print('错误原因: ',e)
            error_flag += 1
            page += 1
            if error_flag <= 3:
                self.parse(city_map, page=page, data_all=data_all, error_flag=error_flag)
            return

        print(f"城市: {city}, 当前页数: {page}, 酒店数量: {html.get('Response').get('resultTitle')}, 当前页数酒店数量: {len(hotelList)}")
        for hotel in hotelList:
            item = dict()
            item['城市'] = city
            item['商圈'] = hotel.get('position').get('area')
            item['id'] = hotel.get('base').get('hotelId')
            item['酒店名称'] = hotel.get('base').get('hotelName')
            item['酒店星级'] = hotel.get('base').get('star')
            item['起步价'] = hotel.get('money').get('price', '')
            item['地址'] = hotel.get('position').get('address')
            item['lon'] = hotel.get('position').get('lng')
            item['lat'] = hotel.get('position').get('lat')
            item['评论数量'] = hotel.get('comment').get('content')
            try:
                item['特点'] = ' '.join(hotel.get('base').get('tags'))
            except:
                item['特点'] = ''
            item['综合评分'] = hotel.get('score').get('number')
            try:
                item['评分详情'] = {i['content']: i['number'] for i in hotel.get('score').get('subScore')}
            except:
                item['评分详情'] = ''
            # print(item)
            data_all.append(item)

        if len(hotelList) >= 25:
            page += 1
            self.parse(city_map, page=page, data_all=data_all)


    def run(self):

        for city_map in city_map_list:
            print(city_map)
            # if city_map['display'] != '武汉': continue
            if city_map['display'] in [i.split('_')[1] for i in os.listdir('酒店数据')]:
                print('已经存在', '\n')
                continue
            data_all = []
            self.parse(city_map, page=1, data_all=data_all)

            df = pd.DataFrame(data_all)
            df = df[['城市', '商圈', 'id', '酒店名称', '酒店星级', '起步价', '地址', 'lon', 'lat', '特点', '评论数量', '综合评分', '评分详情']]
            save_dir = '酒店数据'
            os.path.exists(save_dir) or os.makedirs(save_dir)
            file_name = "{}_{}_{}条携程酒店数据.xlsx".format(currentDate, city_map['display'], len(data_all))
            try:
                df.to_excel(os.path.join(save_dir, file_name), index=False)
                print(f"城市: {city_map['display']}, 数据量: {len(data_all)}, 保存成功\n")
            except:
                continue


if __name__ == '__main__':


    # TODO 修改 config 中的时间
    currentDate = f'{Year}-{Month}'
    XieChengHotel().run()

