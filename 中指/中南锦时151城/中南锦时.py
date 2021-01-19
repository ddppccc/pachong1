import os
import time
import datetime
import random
import requests
import pandas as pd

from typing import List
from dateutil.relativedelta import relativedelta

from config import cookie
from city_dis_code import GetCityCode

City = str
headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "cookie": cookie,
    "origin": "https://creis.fang.com",
    "referer": "https://creis.fang.com/land/Statistics/Index",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}


def create_assist_date(date_start=None, date_end=None):
    # 创建日期辅助表
    if date_start is None:
        date_start = '2011-01-01'
    if date_end is None:
        date_end = datetime.datetime.now().strftime('%Y-%m')

    # 转为日期格式
    datestart = datetime.datetime.strptime(date_start, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(date_end, '%Y-%m-%d')

    date_list = []
    date_list.append(datestart.strftime('%Y-%m-%d'))
    while datestart < dateend - relativedelta(months=1) + relativedelta(days=1):
        datestart += relativedelta(months=1)
        date_list.append(datestart.strftime('%Y-%m-%d'))
    return date_list


class ZhongNan:
    def __init__(self):
        pass

    def time_sleep(self):
        time.sleep(random.randint(5, 10) + random.random())

    def merge_save_data(self, list_date: List):
        """
        整理并保存最终数据
        :param list_date: 时间列表
        """
        col = ["时间", "三亚", "三明", "上海", "上饶", "东莞", "东营", "中山", "临沂", "丹东", "丽水", "乌鲁木齐", "九江", "佛山", "保定", "六安", "兰州",
               "包头",
               "北京", "北海", "南京", "南充", "南宁", "南平", "南昌", "南通", "南阳", "厦门", "合肥", "吉安", "吉林", "呼和浩特", "哈尔滨", "唐山", "嘉兴",
               "大同",
               "大理", "大连", "天津", "太原", "威海", "孝感", "宁德", "宁波", "安庆", "宜宾", "宜昌", "宜春", "宣城", "宿州", "宿迁", "岳阳", "常州",
               "常德",
               "平顶山", "广州", "廊坊", "张家口", "徐州", "德州", "忻州", "惠州", "成都", "扬州", "抚州", "新乡", "新余", "无锡", "昆明", "晋城", "杭州",
               "枣庄",
               "柳州", "株洲", "桂林", "武汉", "汕头", "江门", "池州", "沈阳", "沧州", "泉州", "泰安", "泰州", "泸州", "洛阳", "济南", "济宁", "海口",
               "淮北",
               "淮南", "淮安", "深圳", "清远", "温州", "湖州", "湘潭", "湛江", "滁州", "漳州", "潍坊", "烟台", "焦作", "牡丹江", "珠海", "盐城", "眉山",
               "石家庄",
               "福州", "秦皇岛", "绍兴", "绵阳", "肇庆", "舟山", "芜湖", "苏州", "莆田", "菏泽", "萍乡", "蚌埠", "衡水", "衢州", "襄阳", "西宁", "西安",
               "贵阳",
               "赣州", "运城", "连云港", "遵义", "邯郸", "郑州", "重庆", "金华", "铜陵", "银川", "锦州", "镇江", "长春", "长沙", "阜阳", "阳江", "阳泉",
               "青岛",
               "鞍山", "韶关", "马鞍山", "鹰潭", "黄冈", "黄山", "黄石", "齐齐哈尔", "龙岩"]
        df = pd.DataFrame(list_date, columns=['时间'])
        df_all = pd.DataFrame()
        for i in os.listdir("data"):
            print(i)
            city = i.split('.')[0]
            df1 = pd.read_excel(os.path.join('data', i))
            df2 = df1[['时间', '规划建筑面积(㎡)']]
            df3 = pd.merge(df2, df, on='时间', how='outer')[['时间', '规划建筑面积(㎡)']]
            df3.rename(columns={'规划建筑面积(㎡)': city}, inplace=True)
            df3.fillna(0, inplace=True)
            if df_all.shape[0] == 0:
                df_all = df3
            else:
                df_all = pd.merge(df_all, df3, on='时间', how='outer')
        df_all.to_excel('other/2020-数据合并.xlsx', index=False)  # 保存所有的数据, 不需要修改
        # df_all['三亚'] = ''   # TODO 三亚若有数据, 这取消本条语句
        df_all = df_all[col]

        dddd = pd.read_excel('other/中南锦时_202012.xlsx')
        dddd1 = dddd[~dddd['时间'].isin(list_date)]  # 去掉最近数据, 用刚抓的数据替换
        dddd1 = dddd1[col]
        dddd2 = pd.concat([df_all, dddd1])
        print(dddd2.head())
        dddd2.to_excel(f'中南锦时_{list_date[-1]}出.xlsx', index=False)

    def save_city(self, city: City, d_list: List):
        print(d_list)
        df = pd.DataFrame(data=d_list)
        df1 = df.rename(columns={'sRowCol': '时间', 'sExpendCol': '城市', 'iLandCount': '土地宗数(块)',
                                 'fBuildAreaAll': '建设用地面积(㎡)', 'fPlanningAreaAll': '规划建筑面积(㎡)',
                                 'sFloorAvgPrice': '成交楼面均价(元/㎡)', 'sParcelAvgPrice': '成交土地均价(元/㎡)',
                                 'sOverPrice': '平均溢价率(%)', 'ClosingPrice': '土地出让金(万元)'})
        if df1.shape[0]:
            df2 = df1.append([['时间', '城市', '土地宗数(块)', '建设用地面积(㎡)', '规划建筑面积(㎡)', '成交楼面均价(元/㎡)', '成交土地均价(元/㎡)', '平均溢价率(%)',
                             '土地出让金(万元)']])
            df2.columns = df2.loc[0]
            df2 = df2.drop(0)
        else:
            df2 = df1.copy()
        df2.to_excel('data/{}.xlsx'.format(city), index=False)

    def parse(self, start_date, end_date,  city: City, d_list: List):
        time_list = [
            # ('2011-01-01', '2013-12-31'), ('2014-01-01', '2016-12-31'), ('2017-01-01', '2019-12-31'),
            (start_date, end_date)
        ]
        for t in time_list:

            startTime, endTime = t
            print(city, startTime, endTime)
            city_code = GetCityCode(city)
            ParamMeta = {"iDataType": "1", "iDateType": 2, "sBeginTime": startTime, "sEndTime": endTime,
                         "sPermissionID": "A8305D0A-5C62-4F49-AC52-CDEE0ADF05EC", "sGroupID": "%s" % city_code,
                         "bIsCountyLevelCity": "1", "sGroupIDType": 4,
                         "sParcelConforming": "675715cc-a466-46f1-9818-832994bd1435,675715cc-a466-46f1-9818-832994bd1436",
                         "sAreaIndex": "ALL", "sRowType": "sTime", "sColumnType": "huizong", "sExpendType": "sCity",
                         "sOrderType": "sRowCol", "sOrder": "desc", "sOrderColumn": "", "type": "2",
                         "huaboxieyi": "all",
                         "sCompanyID": "", "iMarketType": "1", "iPushDateType": 1}
            data = {
                "jsonParameters": '%s' % ParamMeta
            }
            url = 'https://creis.fang.com/land/Statistics/GetLand_StatisticsCenterData'
            while True:
                self.time_sleep()
                try:
                    res = requests.post(url, headers=headers, data=data).json()

                    if res['Table4']:
                        d_list += res['Table4']
                    else:
                        print('res, ', res['Table4'], '\n', res)
                    break
                except Exception as e:
                    print(f'E: {e} ')
                    continue

            print()

    def run(self, list_date, start_date, end_date):
        for city in ["三亚", "三明", "上海", "上饶", "东莞", "东营", "中山", "临沂", "丹东", "丽水", "乌鲁木齐",
                     "九江", "佛山", "保定", "六安", "兰州", "包头", "北京", "北海", "南京", "南充", "南宁", "南平",
                     "南昌", "南通", "南阳", "厦门", "合肥", "吉安", "吉林", "呼和浩特", "哈尔滨", "唐山", "嘉兴",
                     "大同", "大理", "大连", "天津", "太原", "威海", "孝感", "宁德", "宁波", "安庆", "宜宾", "宜昌",
                     "宜春", "宣城", "宿州", "宿迁", "岳阳", "常州", "常德", "平顶山", "广州", "廊坊", "张家口", "徐州",
                     "德州", "忻州", "惠州", "成都", "扬州", "抚州", "新乡", "新余", "无锡", "昆明", "晋城", "杭州",
                     "枣庄", "柳州", "株洲", "桂林", "武汉", "汕头", "江门", "池州", "沈阳", "沧州", "泉州", "泰安",
                     "泰州", "泸州", "洛阳", "济南", "济宁", "海口", "淮北", "淮南", "淮安", "深圳", "清远", "温州",
                     "湖州", "湘潭", "湛江", "滁州", "漳州", "潍坊", "烟台", "焦作", "牡丹江", "珠海", "盐城", "眉山",
                     "石家庄", "福州", "秦皇岛", "绍兴", "绵阳", "肇庆", "舟山", "芜湖", "苏州", "莆田", "菏泽", "萍乡",
                     "蚌埠", "衡水", "衢州", "襄阳", "西宁", "西安", "贵阳", "赣州", "运城", "连云港", "遵义", "邯郸",
                     "郑州", "重庆", "金华", "铜陵", "银川", "锦州", "镇江", "长春", "长沙", "阜阳", "阳江", "阳泉",
                     "青岛", "鞍山", "韶关", "马鞍山", "鹰潭", "黄冈", "黄山", "黄石", "齐齐哈尔", "龙岩"]:

            print("城市", city)
            if city in [i.split('.')[0] for i in os.listdir('data')]:
                continue
            d_list = []
            self.parse(start_date, end_date, city, d_list)

            self.save_city(city, d_list)

        self.merge_save_data(list_date=list_date)


if __name__ == '__main__':
    # TODO 2011-2020 数据已经抓过,
    # TODO 一般月初出, 所以截止日期就填上个月的。 开始和结束时间间隔至多36月

    Start_Date, End_Date = '2020-01-01', '2020-12-31'

    list_date = [str(i).split(' ')[0][:-3] for i in create_assist_date(Start_Date, End_Date)]
    print(list_date)

    ZhongNan().run(list_date, Start_Date, End_Date)
