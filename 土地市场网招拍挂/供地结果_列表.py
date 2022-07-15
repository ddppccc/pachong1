import requests
import datetime
import time
from gethash import gethash
import pymongo
import os
from urllib import parse

MONGODB_CONFIG = {
    "host": "192.168.1.28",
    "port": "27017",
    "user": "admin",
    "password": '123123',
}
info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['土地市场网招拍挂']['供地结果_列表_202204']  # 抓取的月份


def get_proxy():
    while True:
        try:
            ip = requests.get('http://47.111.226.234:8000/getip2/').text
            if '403' in ip:
                continue
            return ip
            # return requests.get('http://1.116.204.248:5000/proxy').text
        except:
            # num = 3
            # while num:
            #     try:
            #         return requests.get('http://1.116.204.248:5000/proxy').text
            #     except:
            #         print('暂无ip，等待20秒')
            #         time.sleep(20)
            #         num -= 1
            print('暂无ip')


headers = {
    "Host": "api.landchina.com",
    "Connection": "keep-alive",
    # "Content-Length": "57",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    # "Hash": "9546b4181e34cbbb49ad05e2a7ec024954f7da1c52c026a6873b46da33f1edd5",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    "sec-ch-ua-platform": "\"Windows\"",
    "Origin": "https://www.landchina.com",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://www.landchina.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9"
}
regiondict = {
    "北京市": "11",
    "天津市": "12",
    "河北省": "13",
    "山西省": "14",
    "内蒙古": "15",
    "辽宁省": "21",
    "吉林省": "22",
    "黑龙江省": "23",
    "上海市": "31",
    "江苏省": "32",
    "浙江省": "33",
    "安徽省": "34",
    "福建省": "35",
    "江西省": "36",
    "山东省": "37",
    "河南省": "41",
    "湖北省": "42",
    "湖南省": "43",
    "广东省": "44",
    "广西壮族": "45",
    "海南省": "46",
    "重庆市": "50",
    "四川省": "51",
    "贵州省": "52",
    "云南省": "53",
    "西藏": "54",
    "陕西省": "61",
    "甘肃省": "62",
    "青海省": "63",
    "宁夏回族": "64",
    "新疆维吾尔": "65",
    "新疆兵团": "66",
}
def get_eData(keys):
    command = os.popen("node sy " + keys)
    result = command.read().replace('\n', '')
    command.close()  # 关闭Node.js
    return result
keys = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36' + str(
    datetime.datetime.now().day) + 'list'
headers['Hash'] = get_eData(keys)
# headers['Hash'] = gethash(keys)


def get_time_range_list(startdate, enddate):
    """
        切分时间段
    """
    date_range_list = []
    startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
    while 1:
        tempdate = startdate + datetime.timedelta(days=1)
        if tempdate > enddate:
            date_range_list.append((str(startdate.date()), str(enddate.date())))
            break
        date_range_list.append((str(startdate.date()), str((tempdate - datetime.timedelta(days=1)).date())))
        startdate = tempdate
    return date_range_list


def getdata(date, regionname, regioncode, page=1):
    url = 'https://api.landchina.com/tGdxm/result/list'
    # postdata = {"pageNum": page, "pageSize": 10, "startDate": "", "endDate": ""}
    postdata = {"pageNum": page,
                "pageSize": 10,
                "xzqDm": regioncode,
                "startDate": f"{date[0]} 00:00:00",
                "endDate": f"{date[0]} 23:59:59"}

    for i in range(10):
        proxy = get_proxy()
        proxies = {
            "https": proxy,
            "http": proxy,
        }
        try:
            time.sleep(1)
            res = requests.post(url, json=postdata, proxies=proxies, headers=headers)
            # res = requests.post(url, json=postdata, proxies=proxies, headers=headers)
            # print(res.json())
            with open('log.txt', encoding='utf8') as f:
                t = f.read()
            try:
                bj = date[0] + regionname + str(regioncode) + 'page' + str(page)
            except:
                pass
            print(bj)
            if bj not in t:

                if res.json()['data']['pageNum'] != page:
                    continue
                if regionname not in res.text: continue
                print('当前页', page)
                print('总页数', res.json()['data']['pages'])

                for data in res.json()['data']['list']:
                    try:
                        print(data)
                    except:
                        pass
                    # if info_base.find({'tdZl': data['tdZl'], 'xzqFullName': data['xzqFullName'],
                    #                    'tdYt': data['tdYt']}):  # ------------------------
                    #     print('当前数据已存在', data)  # 停住了才修改的 ，会使速度变慢
                    #     continue
                    info_base.insert_one(data)
                print('数据量', len(res.json()['data']['list']))
                with open('log.txt', 'a', encoding='utf8') as f:
                    f.write(date[0] + regionname + str(regioncode) + 'page' + str(page) + '\n')
            if page < res.json()['data']['pages']:
                page += 1
                return getdata(date, regionname, regioncode, page)
            break                      #在循环结构中使用break语句，如果执行了break语句，那么就退出循环，接着执行循环结构下面的第一条语句
        except Exception as e:
            pass


if __name__ == '__main__':
    start = '2021-10-26'
    end = '2022-04-30'

    # print(len(regiondict))
    daterange = get_time_range_list(start, end)
    print(daterange)

    for k, v in regiondict.items():
        if k != '广东省': continue
        for date in daterange:
            with open('log.txt', encoding='utf8') as f:
                t = f.readline()
            if k + date[0] in t:
                continue
            getdata(date, k, v)
            # with open('log.txt', 'a', encoding='utf8') as f:
            #     f.write(k + date[0] + '\n')
    # for i in range(1,601):
    #     getdata(i)
    #     print(i,'已完成')
    #     time.sleep(1)
