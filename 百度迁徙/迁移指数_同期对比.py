# encoding=utf-8

import pandas as pd
import requests
import re
import json

from config import create_assist_date, c_map, dataType


# 迁入到市
def qy_city(cityCode, dtType):
    headers = {
        'Host': 'huiyan.baidu.com',
        'Referer': 'https://qianxi.baidu.com/?city=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    url = 'https://huiyan.baidu.com/migration/historycurve.jsonp'
    params = {
        "dt": dtType,
        "id": cityCode,
        "type": "move_in",
        "callback": "jsonp_1581843307547_4728266"
    }

    while True:
        try:
            res = requests.get(url, params=params, headers=headers, timeout=(2,4))
            s = re.findall('4728266\((.*)\)', res.text)[0]
            return json.loads(s)['data']['list']
        except Exception as e:
            print("运行出错: ",cityCode, dtType, e)
            continue


# 迁出到市
def qc_city(cityCode, dtType):
    headers = {
        'Host': 'huiyan.baidu.com',
        'Referer': 'https://qianxi.baidu.com/?city=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    url = 'https://huiyan.baidu.com/migration/historycurve.jsonp'
    params = {
       "dt": dtType,
        "id": cityCode,
        "type": "move_out",
        "callback": "jsonp_1581843307547_4728266"
    }

    while True:
        try:
            res = requests.get(url, params=params, headers=headers, timeout=(2,4))
            s = re.findall('4728266\((.*)\)', res.text)[0]

            return json.loads(s)['data']['list']
        except Exception as e:

            print("运行出错: ",cityCode, dtType, e)
            continue


def run(start_date, end_date):
    qianru_city = []
    qianchu_city = []
    for level, cityList in dataType.items():
        for city in cityList:

                dtType = level.replace('Level','')
                cityCode = c_map[city]
                print(dtType,  city, cityCode)

                qr_move_in_city = qy_city(cityCode, dtType)  # 迁入 城市
                for date_qr, value in qr_move_in_city.items():
                    item = {}
                    item['城市'] = city
                    item['时间'] = '{}-{}-{}'.format(str(date_qr)[0:4],
                                                   str(date_qr)[4:6], str(date_qr)[6:])
                    item['级别'] = dtType
                    item["指数"] = value
                    qianru_city.append(item)


                qc_move_out_city = qc_city(cityCode, dtType)  # 迁出 城市
                for date_qc, value in qc_move_out_city.items():
                    item = {}
                    item['城市'] = city
                    item['时间'] = '{}-{}-{}'.format(str(date_qc)[0:4],
                                                   str(date_qc)[4:6], str(date_qc)[6:])
                    item['级别'] = dtType
                    item["指数"] = value
                    qianchu_city.append(item)

    qianru_city_df = pd.DataFrame(data=qianru_city)
    qianchu_city_df = pd.DataFrame(data=qianchu_city)

    name = 'data/{}_{}_百度人口迁移指数_同期对比.xlsx'.format(start_date.replace('-', ''), end_date.replace('-', ''))
    writer = pd.ExcelWriter(name)
    qianru_city_df.to_excel(writer, sheet_name='迁入来源地', index=False)
    qianchu_city_df.to_excel(writer, sheet_name='迁出目的地', index=False)
    writer.save()
    writer.close()


if __name__ == '__main__':
    # TODO 时间
    start_date = '2020-11-01'
    end_date = '2021-01-04'
    print(start_date, end_date)
    dateList = create_assist_date(start_date, end_date)
    run(start_date, end_date)









