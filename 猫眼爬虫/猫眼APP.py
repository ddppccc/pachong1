# encoding=utf-8
import datetime
import os
import time
import pandas as pd
import requests

from datetime import timedelta
from concurrent.futures.thread import ThreadPoolExecutor
from map import city_codes, get_proxy, delete_proxy


class MaoYan:

    def get_data_range(self, start):
        date = (datetime.datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")
        date_list = pd.date_range(start, date, closed='right')
        date_list = [str(date).split(" ")[0] for date in date_list]
        return date_list

    # 设置代理
    def get_html_useIp(self, date, cityId):
        num = 10
        while num > 0:
            proxy = get_proxy()
            # print("proxy: ", proxy)
            if "!" in str(proxy):
                print("没有ip, 等待60s")
                time.sleep(60)
                continue
            proxies = {
                'http': 'http://{}'.format(proxy),
                'https': 'https://{}'.format(proxy)
            }
            retry_count = 2
            while retry_count > 0:
                time.sleep(0.5)
                try:
                    url = 'http://pf.maoyan.com/cinema-chain-operator/filter'
                    params = {
                        "typeId": "0",
                        "date": date,
                        "cityTier": "0",
                        "cityId": cityId
                    }
                    headers = {
                        "Host": "pf.maoyan.com",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                        "Accept-Encoding": "gzip, deflate",
                        "Connection": "keep-alive",
                        "Upgrade-Insecure-Requests": "1",
                        "Cache-Control": "max-age=0",
                    }
                    res = requests.get(url, params=params, headers=headers, proxies=proxies, timeout=(2, 5))
                    if res.status_code != 200:    # 403 更换 ip
                        print(res.status_code)
                        break
                except:
                    retry_count -= 1
                    continue
                return res

            # 出错3次, 删除代理池中代理
            delete_proxy(proxy)
            num -= 1
            print("删除ip: ", (proxy, date, cityId))
            continue
        return ''

    def get_city_data(self, city):
        try:
            path = 'data/{}.csv'.format(city)
            f = open(path, 'r', encoding='utf-8')
            df = pd.read_csv(f)
            f.close()
            endDate = df['时间'].sort_values().max()
            return endDate
        except:
            print('当前城市不存在')
            return '2012-01-01'

    def get_json_data(self, city, date, cityId, data):
        response = self.get_html_useIp(date, cityId)
        if not response or 'data' not in response.text:
            print('没有数据')
            return

        res = response.json()
        item = {}
        item['城市'] = city
        item['时间'] = date
        item['票房'] = res['data']['all']['boxInfo']
        item['人次'] = res['data']['all']['viewInfo']
        item['均场人次'] = res['data']['all']['avgShowView']
        item['平均票价'] = res['data']['all']['avgViewBox']
        data.append(item)
        print(item)

    def run(self, pool):
        for cityId, city in city_codes.items():
            start_date = self.get_city_data(city)
            print(start_date)

            data = []
            p = []
            try:
                dataList = self.get_data_range(start_date)
            except:
                continue
            for date in dataList:
                # get_json_data(city, date, cityId, data)
                d = pool.submit(self.get_json_data, city, date, cityId, data)
                p.append(d)
            [i.result() for i in p]

            if not data: continue
            df1 = pd.DataFrame(data)
            print(city, df1.shape, '\n')
            df1 = df1[['人次', '均场人次', '城市', '平均票价', '时间', '票房']]
            save_filepath = 'data/{}.csv'.format(city)
            if not os.path.exists(save_filepath):
                df1.to_csv(save_filepath, mode='a', encoding="utf-8", index=False, header=True)
            else:
                df1.to_csv(save_filepath, mode='a', encoding="utf-8", index=False, header=False)


if __name__ == '__main__':
    pool = ThreadPoolExecutor(20)
    MaoYan().run(pool)
    pool.shutdown()


