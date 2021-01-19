import datetime
import os
import random

import queue
import math
import time
import json
import pandas as pd
import requests

from config import PROVINCE_CODE, CITY_CODE, COOKIES

headers = {
    'Host': 'index.baidu.com',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
}


class BaiduIndex:
    """
        百度搜索指数
        :keywords; list
        :start_date; string '2018-10-02'
        :end_date; string '2018-10-02'
        :area; int, search by cls.province_code/cls.city_code
    """

    province_code = PROVINCE_CODE
    city_code = CITY_CODE
    _all_kind = ['all', 'pc', 'wise']
    _params_queue = queue.Queue()

    def __init__(self, keywords: list, start_date: str, end_date: str, area=0, cookies=None):
        self.cookies = cookies
        self.keywords = keywords
        self._area = area
        self._init_queue(start_date, end_date, keywords)

    def get_index(self):
        """
        获取百度指数
        返回的数据格式为:
        {
            'keyword': '武林外传',
            'type': 'wise',
            'date': '2019-04-30',
            'index': '202'
        }
        """
        while 1:
            try:
                params_data = self._params_queue.get(timeout=1)
                encrypt_datas, uniqid = self._get_encrypt_datas(
                    start_date=params_data['start_date'],
                    end_date=params_data['end_date'],
                    keywords=params_data['keywords']
                )
                # print(encrypt_datas, uniqid)
                print(f"start_date: {params_data['start_date'].date()}, end_date: {params_data['end_date'].date()},"
                      f" {[i[0]['name'] for i in params_data['keywords']]}")
                key = self._get_key(uniqid)

                for encrypt_data in encrypt_datas:
                    for kind in self._all_kind:
                        encrypt_data[kind]['data'] = self._decrypt_func(
                                key, encrypt_data[kind]['data'])
                    # print(encrypt_data)
                    for formated_data in self._format_data(encrypt_data):
                        yield formated_data
            except requests.Timeout:
                self._params_queue.put(params_data)
            except queue.Empty:
                break
            self._sleep_func()

    def _init_queue(self, start_date, end_date, keywords):
        """
            初始化参数队列
        """
        keywords_list = self._split_keywords(keywords)
        time_range_list = self._get_time_range_list(start_date, end_date)
        # print(keywords_list, time_range_list)
        for start_date, end_date in time_range_list:
            for keywords in keywords_list:
                params = {
                    'keywords': keywords,
                    'start_date': start_date,
                    'end_date': end_date
                }
                # print(params)
                self._params_queue.put(params)

    def _split_keywords(self, keywords: list) -> [list]:
        """
        一个请求最多传入5个关键词, 所以需要对关键词进行切分
        """
        keywords_list = [keywords[i*5: (i+1)*5] for i in range(math.ceil(len(keywords)/5))]
        d2 = []
        for keyword in keywords_list:
            d1 = []
            for k in keyword:
                d = []
                it = {}
                it["name"] = k
                it["wordType"] = 1
                d.append(it)
                d1.append(d)
            d2.append(d1)
        return d2

    def _get_encrypt_datas(self, start_date, end_date, keywords):
        """
        :start_date; str, 2018-10-01
        :end_date; str, 2018-10-01
        :keyword; list, ['1', '2', '3']
        """
        request_args = {
            'word': str(keywords).replace("'", '"'),
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d'),
            'area': self._area,
        }

        url = 'http://index.baidu.com/api/SearchApi/index'
        html = self._http_get(url, request_args)
        datas = json.loads(html)
        # print(datas)
        try:
            uniqid = datas['data']['uniqid']
        except Exception as  e:
            print('error! ', e, datas)
            raise
        encrypt_datas = []
        for single_data in datas['data']['userIndexes']:
            encrypt_datas.append(single_data)
        return (encrypt_datas, uniqid)

    def _get_key(self, uniqid):
        url = 'http://index.baidu.com/Interface/api/ptbk?uniqid=%s' % uniqid
        html = self._http_get(url, parmas=None)
        datas = json.loads(html)
        key = datas['data']
        return key

    def _format_data(self, data):
        """
            格式化堆在一起的数据
        """
        keyword = str(data['word'])
        time_length = len(data['all']['data'])
        start_date = data['all']['startDate']
        cur_date = datetime.datetime.strptime('2010-12-27', '%Y-%m-%d')
        for i in range(time_length):
            for kind in self._all_kind:
                index_datas = data[kind]['data']
                index_data = index_datas[i] if len(index_datas) != 1 else index_datas[0]
                formated_data = {
                    'keyword': keyword,
                    'type': kind,
                    'date': cur_date.strftime('%Y-%m-%d'),
                    'index': index_data if index_data else '0'
                }
                yield formated_data
            cur_date += datetime.timedelta(days=7)

    def _http_get(self, url, parmas):
        """
            发送get请求, 程序中所有的get都是调这个方法
            如果想使用多cookies抓取, 和请求重试功能
            在这自己添加
        """
        while True:
            try:
                headers['Cookie'] = self.cookies
                response = requests.get(url, headers=headers, timeout=5, params=parmas)
                break
            except Exception as e:
                print('出错', e)
                continue

        if response.status_code != 200:
            raise requests.Timeout
        return response.text

    def _get_time_range_list(self, startdate, enddate):
        """
            切分时间段
        """
        date_range_list = []
        # print(startdate, enddate)

        startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        date_range_list.append((startdate, enddate))
        # while 1:
        #     tempdate = startdate + datetime.timedelta(days=300)
        #     if tempdate > enddate:
        #         date_range_list.append((startdate, enddate))
        #         break
        #     date_range_list.append((startdate, tempdate))
        #     startdate = tempdate + datetime.timedelta(days=1)
        return date_range_list

    def _decrypt_func(self, key, data):
        """
            数据解密方法
        """
        a = key
        i = data
        n = {}
        s = []
        for o in range(len(a)//2):
            n[a[o]] = a[len(a)//2 + o]
        for r in range(len(data)):
            s.append(n[i[r]])
        return ''.join(s).split(',')

    def _sleep_func(self):
        """
            sleep方法, 单账号抓取过快, 一段时间内请求会失败
        """
        sleep_time = random.choice(range(10, 40)) * 0.1
        time.sleep(sleep_time)


if __name__ == "__main__":
    city_list = ['石家庄', '太原', '呼和浩特', '沈阳', '长春', '哈尔滨', '南京', '沈阳',
                 '杭州', '合肥', '福州', '南昌', '济南', '郑州', '武汉', '长沙', '广州', '南宁',
                 '海口', '成都', '贵阳', '昆明', '拉萨', '西安', '兰州', '西宁', '银川', '乌鲁木齐',
                 '深圳', '北京', '天津', '上海', '重庆', '全国']

    keywords = ["古驰", "gucci", "古奇", "古琦", "迪奥", "dior", "CHANEL", "香奈儿", "香奈尔", "爱马仕", "Hermes",
         "路易威登", "LV", "Louis vuitton", "普拉达", "Prada", "蔻驰", "coach", "圣罗兰", "YSL", "Yves Saint laurent",
         "阿玛尼", "Amani", "Giorgio Armani", "劳力士", "rolex", "博柏利", "巴宝莉", "Burberry", "蒂凡尼", "蒂芙尼",
         "Tiffany", "芬迪", "fendi",
"杜嘉班纳",
"D&G",
"DG",
"巴黎世家",
"Balenciaga",
"巴利",
"BALLY",
"CK",
"Calvin Klein",
"CELINE",
"葆蝶家",
"BV",
"bottega veneta",
"miumiu",
"缪缪",
"华伦天奴",
"valentino",
"杰尼亚",
"zegna",
"Ermenegildo Zegna",
"范思哲",
"versace",
"卡地亚",
"卡帝亚",
"Cartier",
"宝格丽",
"bvlgari",
"菲拉格慕",
"Ferragamo",
"Salvatore Ferragamo"]
    keyword_type = '奢侈品'

    start_date = '2011-01-01'
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")

    for number in [1]:     # TODO 每次递增
        for city, city_code in CITY_CODE.items():
            name = '%s_%s_%s.xlsx' % (city, number, keyword_type)
            if city not in city_list: continue
            if name in os.listdir('国文临时'):
                print(name, '存在')
                continue

            data = []
            print('城市: ', city)
            cookie = random.choice(COOKIES)

            baidu_index = BaiduIndex(keywords=keywords, start_date=start_date,
                                     end_date=end_date,
                                     area=city_code, cookies=cookie)
            data_index = baidu_index.get_index()
            for index in data_index:
                data.append(index)
            df = pd.DataFrame(data=data)
            df.to_excel('国文临时/%s_%s_%s.xlsx' % (city, number, keyword_type), index=False)


    d = []
    for city in city_list:
        # if city!='郑/州': continue
        path_name_1 = os.path.join('国文临时', '{}_{}_{}.xlsx'.format(city, 1, keyword_type))
        print(city)
        df1 = pd.read_excel(path_name_1)

        df1 = df1.query('type == "all"')
        df1['keyword'] = df1['keyword'].map(lambda x: x.replace("[{'name': '", '').replace("', 'wordType': 1}]", ""))
        df1 = df1.pivot_table(values='index', columns='keyword', index='date', fill_value=0).reset_index()

        # for i in df1.columns:
        #     print(i)

        # print('columns:', len(df1.columns.unique()))
        # for i in keywords:
        #     print(i)
        #     if i not in df1.columns:
        #         print(i)
        #         keywords.remove(i)

        # print(len(keywords))
        df1['城市'] = city
        df1 = df1[['date', '城市'] + df1.columns.tolist()]
        d.append(df1)

    df = pd.concat(d)
    print(df.shape)
    df.to_excel(f'1/全国_{keyword_type}_百度指数.xlsx', index=False)
