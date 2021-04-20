# encoding=utf-8
import pandas as pd
import requests
import re
import json

from config import create_assist_date, c_map, dataType
import pymongo
from urllib import parse
from multiprocessing import Process,Pool
MONGODB_CONFIG = {
   "host": "8.135.119.198",
   "port": "27017",
   "user": "hladmin",
   "password": parse.quote("Hlxkd3,dk3*3@"),
   "db": "dianping",
   "collections": "dianping_collections",
}
qianruCity_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['百度迁徙_迁徙数据']['qianruCity']
qianruCity_has = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['百度迁徙_迁徙数据']['qianruCity_has']

qianchuCity_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['百度迁徙_迁徙数据']['qianchuCity']
qianchuCity_has = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['百度迁徙_迁徙数据']['qianchuCity_has']

qianruProvince_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['百度迁徙_迁徙数据']['qianruProvince']
qianruProvince_has = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['百度迁徙_迁徙数据']['qianruProvince_has']

qianchuProvince_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['百度迁徙_迁徙数据']['qianchuProvince']
qianchuProvince_has = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['百度迁徙_迁徙数据']['qianchuProvince_has']


# 迁入到市
def qy_city(cityCode, date, dtType):
    headers = {
        'Host': 'huiyan.baidu.com',
        'Referer': 'https://qianxi.baidu.com/?city=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }

    # url = 'https://huiyan.baidu.com/migration/cityrank.jsonp'
    url = 'https://huiyan.baidu.com/migration/cityrank.jsonp?dt='+dtType+'&id='+cityCode+'&type=move_in&date='+date+'&callback=jsonp_1581843307547_4728266'
    if qianruCity_has.count_documents({'标题url':url}) == 1:
        print('该数据已抓取')
        return None
    params = {
       "dt": dtType,
        "id": cityCode,
        "type": "move_in",
        "date": date,
        "callback": "jsonp_1581843307547_4728266"
    }


    while True:
        try:
            print(url)
            res = requests.get(url, headers=headers, timeout=(2,4))
            # print('res',res.json())
            s = re.findall(r'4728266\((.*)\)', res.text)[0]
            # print(json.loads(s)['data']['list'])
            qianruCity_has.insert_one({'标题url':url})
            return json.loads(s)['data']['list']
        except Exception as e:
            print("qy_city运行出错: ",cityCode, date, dtType, e)
            continue

# 迁入到省
def qy_province(cityCode, date, dtType):
    headers = {
        'Host': 'huiyan.baidu.com',
        'Referer': 'https://qianxi.baidu.com/?city=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    # url = 'https://huiyan.baidu.com/migration/provincerank.jsonp'
    url = 'https://huiyan.baidu.com/migration/provincerank.jsonp?dt=' + dtType + '&id=' + cityCode + '&type=move_in&date=' + date + '&callback=jsonp_1581843307547_4728266'
    if qianruProvince_has.count_documents({'标题url':url}) == 1:
        print('该数据已抓取')
        return None
    params = {
        "dt": dtType,
        "id": cityCode,
        "type": "move_in",
        "date": date,
        "callback": "jsonp_1581843307547_4728266"
    }

    while True:
        try:
            res = requests.get(url,  headers=headers, timeout=(2,4))
            s = re.findall('4728266\((.*)\)', res.text)[0]
            # print(json.loads(s)['data']['list'])
            qianruProvince_has.insert_one({'标题url':url})
            return json.loads(s)['data']['list']
        except Exception as e:
            print("qy_province运行出错: ",cityCode, date, dtType, e)
            continue

# 迁出到市
def qc_city(cityCode, date, dtType):
    headers = {
        'Host': 'huiyan.baidu.com',
        'Referer': 'https://qianxi.baidu.com/?city=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    # url = 'https://huiyan.baidu.com/migration/cityrank.jsonp'
    url = 'https://huiyan.baidu.com/migration/cityrank.jsonp?dt=' + dtType + '&id=' + cityCode + '&type=move_out&date=' + date + '&callback=jsonp_1581843307547_4728266'
    if qianchuCity_has.count_documents({'标题url':url}) == 1:
        print('该数据已抓取')
        return None
    params = {
       "dt": dtType,
        "id": cityCode,
        "type": "move_out",
        "date": date,
        "callback": "jsonp_1581843307547_4728266"
    }

    while True:
        try:
            res = requests.get(url,  headers=headers, timeout=(2,4))
            s = re.findall('4728266\((.*)\)', res.text)[0]
            # print(json.loads(s)['data']['list'])
            qianchuCity_has.insert_one({'标题url':url})
            return json.loads(s)['data']['list']
        except Exception as e:

            print("qc_city运行出错: ",cityCode, date, dtType, e)
            continue

# 迁出到省
def qc_province(cityCode, date, dtType):
    headers = {
        'Host': 'huiyan.baidu.com',
        'Referer': 'https://qianxi.baidu.com/?city=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    # url = 'https://huiyan.baidu.com/migration/provincerank.jsonp'
    url = 'https://huiyan.baidu.com/migration/provincerank.jsonp?dt=' + dtType + '&id=' + cityCode + '&type=move_out&date=' + date + '&callback=jsonp_1581843307547_4728266'
    if qianchuProvince_has.count_documents({'标题url':url}) == 1:
        print('该数据已抓取')
        return None
    params = {
        "dt": dtType,
        "id": cityCode,
        "type": "move_out",
        "date": date,
        "callback": "jsonp_1581843307547_4728266"
    }

    while True:
        try:
            res = requests.get(url, params=params, headers=headers, timeout=(2,4))
            s = re.findall('4728266\((.*)\)', res.text)[0]
            # print(json.loads(s)['data']['list'])
            qianchuProvince_has.insert_one({'标题url':url})
            return json.loads(s)['data']['list']
        except Exception as e:
            print("qc_province运行出错: ",cityCode, date, dtType, e)
            continue


def run(dateList, start_date, end_date):
    qianru_city = []
    qianru_province = []
    qianchu_city = []
    qianchu_province = []
    for level, cityList in dataType.items():
        for city in cityList:
            print(city)
            # if city not in ['全国']: continue
            for date in dateList:
                try:
                    date_rep = date.replace('-', '')
                except:
                    date_rep = date
                dtType = level.replace('Level','')
                cityCode = c_map[city]
                print(dtType,  city, cityCode, date, date_rep)
                # print('code date type',cityCode,date_rep,dtType)
                # print('type',type(cityCode),type(date_rep),type(dtType))

                qr_move_in_city = qy_city(cityCode, date_rep, dtType)  # 迁入 城市
                # qr_move_in_city = qy_city('340100','20210219','city')  # /迁入 城市
                if qr_move_in_city:
                    for qr in qr_move_in_city:
                        qr['城市'] = city
                        qr['时间'] = date
                        qr['级别'] = dtType
                        qr["比例(%)"] = qr.pop("value")
                        qr["迁入来源地"] = qr.pop("city_name")
                        # print(f'{qr=}')
                        # qianru_city.append(qr)
                        # print(qianruCity_base.count_documents(qr))
                        qianruCity_base.insert_one(qr)
                        print(qr)
                        # print(qianruCity_base.count_documents(qr))



                qr_move_in_province = qy_province(cityCode, date_rep, dtType)  # 迁入 省份
                if qr_move_in_province:
                    for qr in qr_move_in_province:
                        qr['城市'] = city
                        qr['时间'] = date
                        qr['级别'] = dtType
                        qr["比例(%)"] = qr.pop("value")
                        qr["迁入来源地"] = qr.pop("province_name")
                        # print(f'{qr=}')
                        # qianru_province.append(qr)
                        # print(qianruProvince_base.count_documents(qr))
                        qianruProvince_base.insert_one(qr)
                        print(qr)
                        # print(qianruProvince_base.count_documents(qr))



                qc_move_out_city = qc_city(cityCode, date_rep, dtType)  # 迁出 城市
                if qc_move_out_city:
                    for qc in qc_move_out_city:
                        qc['城市'] = city
                        qc['时间'] = date
                        qc['级别'] = dtType
                        qc["比例(%)"] = qc.pop("value")
                        qc["迁出目的地"] = qc.pop("city_name")
                        # print(f'{qc=}')

                        # qianchu_city.append(qc)
                        # print(qianchuCity_base.count_documents(qc))
                        qianchuCity_base.insert_one(qc)
                        print(qc)
                        # print(qianchuCity_base.count_documents(qc))


                qc_move_out_province = qc_province(cityCode, date_rep, dtType)  # 迁出 省份
                if qc_move_out_province:
                    for qc in qc_move_out_province:
                        qc['城市'] = city
                        qc['时间'] = date
                        qc['级别'] = dtType
                        qc["比例(%)"] = qc.pop("value")
                        qc["迁出目 的地"] = qc.pop("province_name")
                        # print(f'{q=}')

                        # qianchu_province.append(q)
                        # print(qianchuProvince_base.count_documents(qc))
                        qianchuProvince_base.insert_one(qc)
                        print(qr)
                        # print(qianchuProvince_base.count_documents(qc))


    # qianru_city_df = pd.DataFrame(data=qianru_city)
    # qianru_province_df = pd.DataFrame(data=qianru_province)
    # qianchu_city_df = pd.DataFrame(data=qianchu_city)
    # qianchu_province_df = pd.DataFrame(data=qianchu_province)
    #
    # name = 'data/{}_{}_百度人口迁移指数.xlsx'.format(start_date.replace('-',''), end_date.replace('-',''))
    # writer = pd.ExcelWriter(name)
    # qianru_city_df.to_excel(writer, sheet_name='迁入来源地_城市', index=False)
    # qianru_province_df.to_excel(writer, sheet_name='迁入来源地_省份', index=False)
    # qianchu_city_df.to_excel(writer, sheet_name='迁出目的第_城市', index=False)
    # qianchu_province_df.to_excel(writer, sheet_name='迁出目的地_省份', index=False)
    # writer.save()
    # writer.close()


if __name__ == '__main__':
    # TODO 时间
    start_date = '2021-01-01'
    end_date = '2021-04-19'
    print(start_date, end_date)
    dateList = create_assist_date(start_date, end_date)
    run(dateList, start_date, end_date)









