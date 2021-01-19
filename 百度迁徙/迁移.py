# encoding=utf-8
import pandas as pd
import requests
import re
import json

from config import create_assist_date, c_map, dataType


# 迁入到市
def qy_city(cityCode, date, dtType):
    headers = {
        'Host': 'huiyan.baidu.com',
        'Referer': 'https://qianxi.baidu.com/?city=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    url = 'https://huiyan.baidu.com/migration/cityrank.jsonp'
    params = {
       "dt": dtType,
        "id": cityCode,
        "type": "move_in",
        "date": date,
        "callback": "jsonp_1581843307547_4728266"
    }

    while True:
        try:
            res = requests.get(url, params=params, headers=headers, timeout=(2,4))
            s = re.findall(r'4728266\((.*)\)', res.text)[0]
            return json.loads(s)['data']['list']
        except Exception as e:
            print("运行出错: ",cityCode, date, dtType, e)
            continue

# 迁入到省
def qy_province(cityCode, date, dtType):
    headers = {
        'Host': 'huiyan.baidu.com',
        'Referer': 'https://qianxi.baidu.com/?city=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    url = 'https://huiyan.baidu.com/migration/provincerank.jsonp'
    params = {
        "dt": dtType,
        "id": cityCode,
        "type": "move_in",
        "date": date,
        "callback": "jsonp_1581843307547_4728266"
    }

    while True:
        try:
            res = requests.get(url, params=params, headers=headers, timeout=(2,4))
            s = re.findall('4728266\((.*)\)', res.text)[0]
            return json.loads(s)['data']['list']
        except Exception as e:
            print("运行出错: ",cityCode, date, dtType, e)
            continue

# 迁出到市
def qc_city(cityCode, date, dtType):
    headers = {
        'Host': 'huiyan.baidu.com',
        'Referer': 'https://qianxi.baidu.com/?city=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    url = 'https://huiyan.baidu.com/migration/cityrank.jsonp'
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

            return json.loads(s)['data']['list']
        except Exception as e:

            print("运行出错: ",cityCode, date, dtType, e)
            continue

# 迁出到省
def qc_province(cityCode, date, dtType):
    headers = {
        'Host': 'huiyan.baidu.com',
        'Referer': 'https://qianxi.baidu.com/?city=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    url = 'https://huiyan.baidu.com/migration/provincerank.jsonp'
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
            return json.loads(s)['data']['list']
        except Exception as e:
            print("运行出错: ",cityCode, date, dtType, e)
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

                qr_move_in_city = qy_city(cityCode, date_rep, dtType)  # 迁入 城市
                for qr in qr_move_in_city:
                    qr['城市'] = city
                    qr['时间'] = date
                    qr['级别'] = dtType
                    qr["比例(%)"] = qr.pop("value")
                    qr["迁入来源地"] = qr.pop("city_name")
                    # print(f'{qr=}')
                    qianru_city.append(qr)

                qr_move_in_province = qy_province(cityCode, date_rep, dtType)  # 迁入 省份
                for qr in qr_move_in_province:
                    qr['城市'] = city
                    qr['时间'] = date
                    qr['级别'] = dtType
                    qr["比例(%)"] = qr.pop("value")
                    qr["迁入来源地"] = qr.pop("province_name")
                    # print(f'{qr=}')
                    qianru_province.append(qr)

                qc_move_out_city = qc_city(cityCode, date_rep, dtType)  # 迁出 城市
                for qc in qc_move_out_city:
                    qc['城市'] = city
                    qc['时间'] = date
                    qc['级别'] = dtType
                    qc["比例(%)"] = qc.pop("value")
                    qc["迁出目的地"] = qc.pop("city_name")
                    # print(f'{qc=}')
                    qianchu_city.append(qc)

                qc_move_out_province = qc_province(cityCode, date_rep, dtType)  # 迁出 省份
                for q in qc_move_out_province:
                    q['城市'] = city
                    q['时间'] = date
                    q['级别'] = dtType
                    q["比例(%)"] = q.pop("value")
                    q["迁出目 的地"] = q.pop("province_name")
                    # print(f'{q=}')
                    qianchu_province.append(q)

    qianru_city_df = pd.DataFrame(data=qianru_city)
    qianru_province_df = pd.DataFrame(data=qianru_province)
    qianchu_city_df = pd.DataFrame(data=qianchu_city)
    qianchu_province_df = pd.DataFrame(data=qianchu_province)

    name = 'data/{}_{}_百度人口迁移指数.xlsx'.format(start_date.replace('-',''), end_date.replace('-',''))
    writer = pd.ExcelWriter(name)
    qianru_city_df.to_excel(writer, sheet_name='迁入来源地_城市', index=False)
    qianru_province_df.to_excel(writer, sheet_name='迁入来源地_省份', index=False)
    qianchu_city_df.to_excel(writer, sheet_name='迁出目的第_城市', index=False)
    qianchu_province_df.to_excel(writer, sheet_name='迁出目的地_省份', index=False)
    writer.save()
    writer.close()


if __name__ == '__main__':
    # TODO 时间
    start_date = '2020-12-10'
    end_date = '2020-12-31'
    print(start_date, end_date)
    dateList = create_assist_date(start_date, end_date)
    run(dateList, start_date, end_date)
