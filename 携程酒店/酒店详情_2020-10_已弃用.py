import time
import datetime
import os
import re
import requests
import pandas as pd

from queue import Queue
from threading import Thread

from scrapy import Selector


class HotelInfo():
    queue = Queue()
    cookie = '' \
             'aQQ_ajkguid=6305AFCC-CBC0-7E81-B772-0F3E8CAF04D0; id58=e87rkF62fA0P+69+G5dJAg==; 58tj_uuid=93de6c54-5f88-45a3-8243-34ae4a65663d; als=0; _ga=GA1.2.412851100.1589340123; aQQ_brokerguid=5CBF0591-9D1B-4195-94B3-52DEC65CF2D0; isp=true; wmda_uuid=d4601febfb8e422f420417ddde35517d; wmda_visited_projects=%3B6289197098934; sessid=3F2BFCBB-1877-7D9D-7B88-65CF0606151D; lps=http%3A%2F%2Fuser.anjuke.com%2Fajax%2FcheckMenu%2F%3Fr%3D0.07922823048794725%26callback%3DjQuery111309304314165137022_1591757640578%26_%3D1591757640579%7Chttps%3A%2F%2Fhy.fang.anjuke.com%2Floupan%2Fxiangce-446795.html%3Ffrom%3Dloupan_tab; twe=2; Hm_lvt_c5899c8768ebee272710c9c5f365a6d8=1589767849,1590485498,1591324449,1591757645; lp_lt_ut=4971900fb59ca0493a0bc0529772a073; Hm_lpvt_c5899c8768ebee272710c9c5f365a6d8=1591757926; _gid=GA1.2.1652451907.1591757942; wmda_session_id_6289197098934=1591769655588-85e70f80-1a52-9e47; new_uv=28; init_refer=; new_session=0; __xsptplusUT_8=1; ajk_member_verify=f%2Fj9LbXdPpabOrY6ZkUPOFe%2FGyTml%2BX%2BIbvg4cYzGWY%3D; ajk_member_verify2=MTUzNjAwMzE3fFUxNTUwOTI0MTkxMjQ3N3wx; ctid=293; __xsptplus8=8.30.1591769657.1591770080.14%232%7Cwww.baidu.com%7C%7C%7C%7C%23%23Cs05xR7uEtn86LXjWUMBBGhP1zhtU0HR%23; ajkAuthTicket=TT=af15525d3c71c205bf40b116d42c2a30&TS=1591770081864&PBODY=PCeCEJ-tBd3LC2zFL17he9pp89krf7eQ4UDEF73YjT4A-DQoTm5SFvfX6vOrhKSrjsvf68qPiKoLGLLNQsIcqiVKwa-yzEeiNIfJwVshdAnxC47VJdOVbmyfjUrGKKaH9tZpmdHtA198fRxsDujbKeN3QivweiIxidetJAPjxp8&VER=2; xzfzqtoken=BwK%2BVKixWSkOnSMlfUKfhjId0F4Deo6E3EGkq%2F2l%2Fbvs%2BfEg2PaSUFeBWfmt%2BUxjin35brBb%2F%2FeSODvMgkQULA%3D%3D'

    def __init__(self, path, city, save_file):
        self.path = path
        self.city = city
        self.save_file = save_file

    def change_str(self, str1):
        str2 = str1.replace('：', '').replace('\n', '').replace('\r', '').replace(' ', '')
        str3 = str2.replace(' ', '').replace('\t', '').replace('暂无数据', '')
        return str3

    def get_city_hotel(self, data):
        while True:
            if self.queue.empty():
                break
            url = self.queue.get()
            response = self.get_html(url)
            if not response:
                self.queue.task_done()
                continue
            # response = Selector(text=res.text)

            startTime = ''.join(re.findall('(\d+)年开业\&nbsp;', response.text))
            descTime = ''.join(re.findall('(\d+)年装修', response.text))
            homeNumber = ''.join(re.findall('(\d+)间房\&nbsp;\&nbsp;', response.text))

            item = {}
            item['城市'] = self.city
            item['酒店url'] = url
            item['开业时间'] = startTime
            item['装修时间'] = descTime
            item['房间数量'] = homeNumber
            data.append(item)
            print(item)

            self.queue.task_done()

    def run(self):
        data = []
        df = pd.read_excel(self.path)
        print(df.shape)
        url_list = df['url'].tolist()
        for url in url_list:
            self.queue.put(url)

        for i in range(15):
            time.sleep(0.2)
            t = Thread(target=self.get_city_hotel, args=(data,))
            t.daemon = True
            t.start()
        self.queue.join()

        df1 = pd.DataFrame(data)
        print('开始保存数据: ', df1.shape)
        save_path = '{}/{}.xlsx'.format(self.save_file, self.city)
        df1.to_excel(save_path, index=False)
        print('数据保存成功。')
        print('>' * 50, '\n')

    def get_html(self, url):
        headers = {
            'origin': 'https://hotels.ctrip.com',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        }
        while True:
            try:
                res = requests.get(url, headers=headers, timeout=(2, 5))
                if '404Apf_NotFoundController' in res.text:
                    return ''
                # response = Selector(text=res.text)

                # varify_code = response.xpath('//title/text()').get()
                # if '访问验证' in varify_code:
                #     print(varify_code)
                #
                #     time.sleep(5)
                #     continue
                break
            except Exception as e:
                print(url, e)
                continue
        return res


if __name__ == '__main__':
    save_file = '酒店详情信息'
    exists_city = [i.split('.')[0] for i in os.listdir(save_file)]
    for i in os.listdir('酒店数据'):
        print('\n', i)
        path = '酒店数据/' + i
        city = i.split('_')[1]
        if city in exists_city:
            print('已经存在: ', city)
            continue

        HotelInfo(path, city, save_file).run()

    # TODO
    # year = 2020
    # month = '08'
    #
    # path1 = '酒店合并详情数据/{year}-{month}携程酒店'.format(year=year, month=month)
    #
    # os.path.exists(path1) or os.makedirs(path1)
    #
    # d = []
    # for i in os.listdir(r'酒店数据'):
    #     print(i)
    #     city = i.split('_')[1]
    #     if city in [i.split('_')[1] for i in os.listdir(path1)]:
    #         continue
    #     path = r'酒店数据/' + i
    #     df = pd.read_excel(path)
    #     df = df.drop_duplicates()
    #
    #     df1 = pd.read_excel(r'酒店详情信息/{}.xlsx'.format(city))
    #     df1 = df1.drop_duplicates()
    #
    #     df2 = pd.merge(df, df1, left_on='url', right_on='酒店url')
    #     df2 = df2[['城市', 'id', 'name', 'shortName', 'img', '地址', '评论数', '评论推荐率', 'isSingleRec', 'lat', 'lon',
    #                '客户点评(5.0满分)', '酒店星级（星级和数据已存在钻石级)', 'stardesc', 'url',
    #                '起步价', '开业时间', '房间数量', '装修时间']]
    #
    #     df2.to_excel(
    #         '{path1}/{year}-{month}_{city}_{number}条数据.xlsx'.format(path1=path1, year=year, month=month, city=city,
    #                                                                 number=df2.shape[0]), index=False)
    #     d.append(df2)
    # #
    # df3 = pd.concat(d)
    # print(df3.shape)
    # #
    # df3.to_csv('酒店合并详情数据/2020-{month}_全国_酒店详细数据.csv'.format(month=month), index=False, encoding='utf-8')
