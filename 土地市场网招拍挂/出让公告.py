import os
import random
import re
import time
import datetime
from concurrent.futures import ThreadPoolExecutor
from 验证码 import get_proxy, TuDi
import requests
import pandas as pd
from dateutil.relativedelta import relativedelta
from urllib.parse import quote
# from scrapy import Selector
from config import delete_proxy
from lxml import etree

formDataMap = {
    'VIEWSTATE': '/wEPDwUJNjkzNzgyNTU4D2QWAmYPZBYIZg9kFgICAQ9kFgJmDxYCHgdWaXNpYmxlaGQCAQ9kFgICAQ8WAh4Fc3R5bGUFIEJBQ0tHUk9VTkQtQ09MT1I6I2YzZjVmNztDT0xPUjo7ZAICD2QWAgIBD2QWAmYPZBYCZg9kFgJmD2QWBGYPZBYCZg9kFgJmD2QWAmYPZBYCZg9kFgJmDxYEHwEFIENPTE9SOiNEM0QzRDM7QkFDS0dST1VORC1DT0xPUjo7HwBoFgJmD2QWAgIBD2QWAmYPDxYCHgRUZXh0ZWRkAgEPZBYCZg9kFgJmD2QWAmYPZBYEZg9kFgJmDxYEHwEFhwFDT0xPUjojRDNEM0QzO0JBQ0tHUk9VTkQtQ09MT1I6O0JBQ0tHUk9VTkQtSU1BR0U6dXJsKGh0dHA6Ly93d3cubGFuZGNoaW5hLmNvbS9Vc2VyL2RlZmF1bHQvVXBsb2FkL3N5c0ZyYW1lSW1nL3hfdGRzY3dfc3lfamhnZ18wMDAuZ2lmKTseBmhlaWdodAUBMxYCZg9kFgICAQ9kFgJmDw8WAh8CZWRkAgIPZBYCZg9kFgJmD2QWAmYPZBYCZg9kFgJmD2QWAmYPZBYEZg9kFgJmDxYEHwEFIENPTE9SOiNEM0QzRDM7QkFDS0dST1VORC1DT0xPUjo7HwBoFgJmD2QWAgIBD2QWAmYPDxYCHwJlZGQCAg9kFgJmD2QWBGYPZBYCZg9kFgJmD2QWAmYPZBYCZg9kFgJmD2QWAmYPFgQfAQUgQ09MT1I6I0QzRDNEMztCQUNLR1JPVU5ELUNPTE9SOjsfAGgWAmYPZBYCAgEPZBYCZg8PFgIfAmVkZAICD2QWBGYPZBYCZg9kFgJmD2QWAmYPZBYCAgEPZBYCZg8WBB8BBYwBQ09MT1I6I0QzRDNEMztCQUNLR1JPVU5ELUNPTE9SOjtCQUNLR1JPVU5ELUlNQUdFOnVybChodHRwOi8vd3d3LmxhbmRjaGluYS5jb20vVXNlci9kZWZhdWx0L1VwbG9hZC9zeXNGcmFtZUltZy94X3Rkc2N3X3p5X2NyZ2cyMDExTkhfMDEuZ2lmKTsfAwUCNDYWAmYPZBYCAgEPZBYCZg8PFgIfAmVkZAIBD2QWAmYPZBYCZg9kFgJmD2QWAgIBD2QWAmYPFgQfAQUgQ09MT1I6I0QzRDNEMztCQUNLR1JPVU5ELUNPTE9SOjsfAGgWAmYPZBYCAgEPZBYCZg8PFgIfAmVkZAIDD2QWAgIDDxYEHglpbm5lcmh0bWwFiQw8UD48QlI+PC9QPjxUQUJMRT48VEJPRFk+PFRSIGNsYXNzPWZpcnN0Um93PjxURCBzdHlsZT0iQk9SREVSLUJPVFRPTTogMXB4IHNvbGlkOyBCT1JERVItTEVGVDogMXB4IHNvbGlkOyBCT1JERVItVE9QOiAxcHggc29saWQ7IEJPUkRFUi1SSUdIVDogMXB4IHNvbGlkOyBib3JkZXI6MHB4IHNvbGlkIiB2QWxpZ249dG9wIHdpZHRoPTM3MD48UCBzdHlsZT0iVEVYVC1BTElHTjogY2VudGVyIj48QSBocmVmPSJodHRwczovL3d3dy5sYW5kY2hpbmEuY29tLyIgdGFyZ2V0PV9zZWxmPjxJTUcgdGl0bGU9dGRzY3dfbG9nZTEucG5nIGFsdD10ZHNjd19sb2dlMS5wbmcgc3JjPSJodHRwOi8vMjE4LjI0Ni4yMi4xNjYvbmV3bWFuYWdlL3VlZGl0b3IvdXRmOC1uZXQvbmV0L3VwbG9hZC9pbWFnZS8yMDIwMDYxMC82MzcyNzQwNjM0Mjg3NzExMDgxMTExMzEyLnBuZyI+PC9BPjwvUD48L1REPjxURCBzdHlsZT0iQk9SREVSLUJPVFRPTTogMXB4IHNvbGlkOyBCT1JERVItTEVGVDogMXB4IHNvbGlkOyBXT1JELUJSRUFLOiBicmVhay1hbGw7IEJPUkRFUi1UT1A6IDFweCBzb2xpZDsgQk9SREVSLVJJR0hUOiAxcHggc29saWQ7Ym9yZGVyOjBweCBzb2xpZCIgdkFsaWduPXRvcCB3aWR0aD02MjA+PFNQQU4gc3R5bGU9IkZPTlQtRkFNSUxZOiDlrovkvZMsIFNpbVN1bjsgQ09MT1I6IHJnYigyNTUsMjU1LDI1NSk7IEZPTlQtU0laRTogMTJweCI+5Li75Yqe77ya6Ieq54S26LWE5rqQ6YOo5LiN5Yqo5Lqn55m76K6w5Lit5b+D77yI6Ieq54S26LWE5rqQ6YOo5rOV5b6L5LqL5Yqh5Lit5b+D77yJPC9TUEFOPiA8UD48U1BBTiBzdHlsZT0iRk9OVC1GQU1JTFk6IOWui+S9kywgU2ltU3VuOyBDT0xPUjogcmdiKDI1NSwyNTUsMjU1KTsgRk9OVC1TSVpFOiAxMnB4Ij7mjIflr7zljZXkvY3vvJroh6rnhLbotYTmupDpg6joh6rnhLbotYTmupDlvIDlj5HliKnnlKjlj7gmbmJzcDsgJm5ic3A75oqA5pyv5pSv5oyB77ya5rWZ5rGf6Ie75ZaE56eR5oqA6IKh5Lu95pyJ6ZmQ5YWs5Y+4PC9TUEFOPiA8UD48U1BBTiBzdHlsZT0iRk9OVC1GQU1JTFk6IOWui+S9kywgU2ltU3VuOyBDT0xPUjogcmdiKDI1NSwyNTUsMjU1KTsgRk9OVC1TSVpFOiAxMnB4Ij7kuqxJQ1DlpIcxMjAzOTQxNOWPty00Jm5ic3A7ICZuYnNwO+S6rOWFrOe9keWuieWkhzExMDEwMjAwMDY2NigyKSZuYnNwOyAmbmJzcDvpgq7nrrHvvJpsYW5kY2hpbmEyMThAMTYzLmNvbSZuYnNwOyZuYnNwOzxzY3JpcHQgdHlwZT0idGV4dC9qYXZhc2NyaXB0Ij52YXIgX2JkaG1Qcm90b2NvbCA9ICgoImh0dHBzOiIgPT0gZG9jdW1lbnQubG9jYXRpb24ucHJvdG9jb2wpID8gIiBodHRwczovLyIgOiAiIGh0dHBzOi8vIik7ZG9jdW1lbnQud3JpdGUodW5lc2NhcGUoIiUzQ3NjcmlwdCBzcmM9JyIgKyBfYmRobVByb3RvY29sICsgImhtLmJhaWR1LmNvbS9oLmpzJTNGODM4NTM4NTljNzI0N2M1YjAzYjUyNzg5NDYyMmQzZmEnIHR5cGU9J3RleHQvamF2YXNjcmlwdCclM0UlM0Mvc2NyaXB0JTNFIikpOzwvc2NyaXB0PjwvU1BBTj4gPC9QPjwvVFI+PC9UQk9EWT48L1RBQkxFPjxQPiZuYnNwOzwvUD4fAQVkQkFDS0dST1VORC1JTUFHRTp1cmwoaHR0cDovL3d3dy5sYW5kY2hpbmEuY29tL1VzZXIvZGVmYXVsdC9VcGxvYWQvc3lzRnJhbWVJbWcveF90ZHNjdzIwMTNfeXdfMS5qcGcpO2Rkllk56OHtkasjpVJutwQ+oiEwAzq9DBYuOLwoA8WGSRA=',
    'EVENTVALIDATION': '/wEdAAK5d2xVTTSTPhQ3ZD/+TZ2SCeA4P5qp+tM6YGffBqgTjfWMJzQmy1b1KW8Cfb1dE3LbDQXjk5/IBk+EmcoV1t8p',
    # 文中有

}


def get_time_range_list(startdate, enddate):
    """
        切分时间段
    """
    date_range_list = []
    startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
    while 1:
        tempdate = startdate + relativedelta(days=1)
        if tempdate > enddate:
            date_range_list.append((startdate, enddate))
            break
        date_range_list.append((startdate, tempdate - relativedelta(days=1)))
        startdate = tempdate
    print('list',date_range_list)
    return date_range_list


def get_city_province(df, region, title):
    if region in ['驻马店市', '新乡市', '中山市', '廊坊市']:
        region = '{}本级'.format(region)
    d = df.loc[df['name'] == region]
    if d.shape[0] == 0: print(region, d)
    city, province = '', ''
    if d.shape[0] == 0:
        city_ = "".join(re.findall('(.*)市', title))
        city = city_ if len(city_) == 0 else str(city_) + '市'
        region_ = "".join(re.findall('市(.*)区', title))
        region = region_ if len(region_) == 0 else str(region_) + '区'
        try:
            province = df.loc[df['name'] == region].iloc[0]['province']
        except:
            province = ''
    elif d.shape[0] == 1:
        city = d.iloc[0]['city']
        province = d.iloc[0]['province']
    else:
        for i in range(d.shape[0]):
            if d.iloc[i]['city'].replace('市', '') in title:
                city = d.iloc[i]['city']
                province = d.iloc[i]['province']
    return city, province, region


def get_html(QuerySubmitConditionData, page=1):
    url = 'https://www.landchina.com/default.aspx?tabid=261'

    formData = {
        '__VIEWSTATE': formDataMap['VIEWSTATE'],  # 文中有
        '__EVENTVALIDATION': formDataMap['EVENTVALIDATION'],  # 文中有
        'hidComName': 'default',  # 无需改变
        # 'TAB_QueryConditionItem': '598bdde3-078b-4c9b-b460-2e0b2d944e86',  # 选择了发布时间
        'TAB_QueryConditionItem': '87f11024-55ab-4faf-a0af-46371e33ae66',  # 选择了公告类型
        'TAB_QuerySortItemList': 'c04b6ee6-3975-43ab-a733-28dcc4707112:False',  # 选择了网上创建时间
        'TAB_QuerySubmitConditionData': QuerySubmitConditionData,
        'TAB_QuerySubmitOrderData': 'c04b6ee6-3975-43ab-a733-28dcc4707112:False',
        'TAB_RowButtonActionControl': '',
        'TAB_QuerySubmitPagerData': page,  # 页面
        'TAB_QuerySubmitSortData': ''
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9",
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Referer': 'https://www.landchina.com/default.aspx?tabid=261',
        'Host': 'www.landchina.com',
        'Origin': 'https://www.landchina.com'
    }
    # number = 5
    # while number > 0:
    while 1:
        # number -= 1
        try:
            # ip 生成cookie
            while True:
                try:
                    print('准备代理和cookie')
                    proxy = get_proxy()

                    cookie = TuDi(proxy).run_get_ip_cookie(proxy)
                    print(f'proxy={proxy}')
                    print(f'cookie={cookie}')
                    proxies = {
                        'http': 'http://{}'.format(proxy),
                        'https': 'https://{}'.format(proxy),
                    }
                    break
                except:
                    print('准备出错。。。重试中')
                    continue
            headers['cookie'] = cookie
            try:
                res = requests.post(url=url, data=formData, headers=headers, proxies=proxies,timeout=(2,7))
            except:
                delete_proxy(proxy)
                continue
            res.encoding = 'gbk'
            # print(res.text)
            return res
        except Exception as e:
            print(url, e, '出错')
            continue


def parse_page(page, **kwargs):
    # 添加
    # city_list = ['成都市', '贵阳市', '西安市', '重庆市', '桂林市', '南宁市', '昆明市']
    print('当前页面: ', page, '\t', kwargs['QuerySubmitConditionData'])
    res = get_html(kwargs['QuerySubmitConditionData'], page=page)
    if not res:
        print('没有res')
        return
    # response = Selector(text=res.text)
    response = etree.HTML(res.text)
    d_list = []

    for tr in response.xpath('//*[@id="TAB_contentTable"]//tr[@id]'):
        item = {}
        item['行政区'] = tr.xpath('./td[2]/text() | ./td[2]/span/@title').get()
        item['供应标题'] = tr.xpath('./td[3]/a/span/@title | ./td[3]/a/text()').get()
        city, province, region = get_city_province(kwargs['df_map'], item['行政区'], item['供应标题'])
        item['省份'] = province
        item['城市'] = city
        # 添加快速筛选城市    之前的数据在土地数据被封中和data中，重来后需要放回原来的位置
        # if item['城市'] not in city_list:
        #     continue
        item['行政区'] = region

        item['公告类型'] = tr.xpath('./td[4]/text()').get()
        item['发布时间'] = tr.xpath('./td[5]/text()').get()
        item['标题url'] = 'https://www.landchina.com' + tr.xpath('./td[3]/a/@href').get()
        if item['公告类型'] not in ['招标', '拍卖', '挂牌']:
            continue
        row = ''
        for i in item:
            row = row + str(item[i]) + ','
        d_list.append(row)
        # data_item = parse_info(item['标题url'])
        print(item)
    f = open('土地数据/出让公告.csv', 'a')

    for d in d_list:
        try:
            f.write(d + '\n')
        except:
            continue
    f.close()
        # for i in data_item:
        #     t1 = item.copy()
        #     t1.update(i)
        #     print("t1: ", t1)
        #     kwargs['data'].append(t1)


def run(startdate, enddate, df_map):
    # city_list = ['成都市', '贵阳市', '西安市', '重庆市', '桂林市', '南宁市', '昆明市']

    for i in get_time_range_list(startdate, enddate):
        if '{}-{}-{}'.format(i[0].year, i[0].month, i[0].day) in ['2015-9-5']:
            continue
        print('{}-{}-{}~{}-{}-{}'.format(i[0].year, i[0].month, i[0].day, i[1].year, i[1].month, i[1].day))
        data_list = []
        QuerySubmitConditionData = '598bdde3-078b-4c9b-b460-2e0b2d944e86:{}-{}-{}~{}-{}-{}'.format(
            i[0].year, i[0].month, i[0].day, i[1].year, i[1].month, i[1].day)

        # 判断是否存在
        if QuerySubmitConditionData + '\n' in open(r'土地log/出让公告.txt', mode='r', encoding='utf-8').readlines():
            print("已经存在", QuerySubmitConditionData, '\n')
            continue
        time.sleep(random.randint(10, 15) * 0.1 * 3)
        res = get_html(QuerySubmitConditionData)
        if not res: continue
        # response = Selector(text=res.text)
        response = etree.HTML(res.text)

        try:
            totalPage = "".join(
                re.findall('共(\d+)页', response.xpath("//td[@class='pager' and @align='right']/text()").get()))
        except:
            totalPage = 1
        print('总页数: ', totalPage, QuerySubmitConditionData)
        print('当前页面: ', 1, QuerySubmitConditionData)
        d_list = []
        for tr in response.xpath('//*[@id="TAB_contentTable"]//tr[@id]'):
            item = {}
            item['行政区'] = tr.xpath('./td[2]/text() | ./td[2]/span/@title').get()
            item['供应标题'] = tr.xpath('./td[3]/a/span/@title | ./td[3]/a/text()').get()
            city, province, region = get_city_province(df_map, item['行政区'], item['供应标题'])

            # -----------------------
            # if city not in city_list:
            #     continue
            # ------------------------
            item['省份'] = province

            item['城市'] = city

            item['行政区'] = region
            item['公告类型'] = tr.xpath('./td[4]/text()').get()
            item['发布时间'] = tr.xpath('./td[5]/text()').get()
            # item['网上创建时间'] = tr.xpath('./td[6]/text()').get()
            item['标题url'] = 'https://www.landchina.com' + tr.xpath('./td[3]/a/@href').get()
            print(item)
            if item['公告类型'] not in ['招标', '拍卖', '挂牌', '公开公告']:
                continue
            row = ''
            for i in item:
                row = row + str(item[i]) + ','
            d_list.append(row)
            # data_item = parse_info(item['标题url'])
            print(item)
        f = open('土地数据/出让公告.csv', 'a')

        for d in d_list:
            try:
                f.write(d + '\n')
            except:
                continue
        f.close()
            # --------------------------------------
            # data_item = parse_info(item['标题url'])
            # if data_item is None:
            #     continue
            # for i in data_item:
            #     t1 = item.copy()
            #     t1.update(i)
            #     print("t1: ", t1)
            #     data_list.append(t1)
            #---------------------------------------

        # 判断页数
        if int(totalPage) > 1:
            # 解析每一页
            for page in range(2, int(totalPage) + 1):
                # if page !=2: continue
                parse_page(page=page, QuerySubmitConditionData=QuerySubmitConditionData, data=data_list, df_map=df_map)

        # # 保存数据
        # df = pd.DataFrame(data=data_list)
        # try:
        #     df = df[['省份', '城市', '行政区', '供应标题', '公告编号', '公告类型', '发布时间', '标题url', '宗地编号', '宗地总面积', '宗地坐落', '出让年限', '容积率',
        #              '建筑密度(%)', '绿化率(%)', '建筑限高(米)', '主要用途', '面积', '起始价', '加价幅度', '投资强度', '保证金']]
        # except:
        #     continue
        # if os.path.exists('土地数据/出让公告.csv'):
        #     try:
        #         print(1)
        #         df.to_csv(r'土地数据/出让公告.csv', mode='a', header=False, index=False, encoding="gbk", sep=',')
        #     except:
        #         continue
        # else:
        #     print(2)
        #     df.to_csv(r'土地数据/出让公告.csv', mode='a', header=True, index=False, encoding="gbk", sep=',')

        # 保存时间记录
        with open('土地log/出让公告.txt', mode='a', encoding='gbk') as fp:
            fp.writelines([QuerySubmitConditionData, '\n'])
        print()


if __name__ == '__main__':
    # startdate, enddate = '2011-1-1', '2020-11-1'
    startdate, enddate = '2021-01-01', '2021-04-19'
    df_map = pd.read_excel('城市_区县_映射表.xlsx')
    threadPool = ThreadPoolExecutor(max_workers=12)
    future = threadPool.submit(run ,startdate,enddate,df_map)
    threadPool.shutdown(wait=True)
    # run(startdate, enddate, df_map)
