# encoding=utf-8
import requests
import time
import datetime
from dateutil.relativedelta import relativedelta
import pymongo
from urllib import parse
MONGODB_CONFIG = {
   "host": "8.135.119.198",
   "port": "27017",
   "user": "hladmin",
   "password": parse.quote("Hlxkd3,dk3*3@"),
   "db": "dianping",
   "collections": "dianping_collections",
}
info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['土地市场网招拍挂']['地块公示_列表_202111']
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
headers={

    'Host': 'api.landchina.com',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'Origin': 'https://www.landchina.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.landchina.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': "'zh-CN,zh;q=0.9'",


}
def getdata(start,end,page=1):
    for i in range(5):
        url='https://api.landchina.com/tCjgs/deal/list'
        postdata={"pageNum":page,
                  "pageSize":10,
                  "createStartDate":f"{start} 00:00:00",
                  "createEndDate":f"{end} 23:59:59"}
        time.sleep(1)
        res=requests.post(url,headers=headers,json=postdata)
        res.encoding='utf8'
        if res.json()['code'] == 500:
            time.sleep(5)
            continue
        print(res.json()['data']['list'])
        info_base.insert_many(res.json()['data']['list'])
        print('当前页',page)
        print('总页数',res.json()['data']['pages'])
        if page<res.json()['data']['pages']:
            page += 1
            return getdata(start, end, page)


        break



'''

__jdu=16208714644421613284524; shshshfpa=d4f0280a-3bc6-af72-3c11-78a09dbedcf4-1623812862; shshshfpb=nXYFMt6Iue1QOdPiyu4WxHA%3D%3D; pinId=8VnQf79zUzrcG1_btZMTYLV9-x-f3wj7; __jdv=76161171|direct|-|none|-|1635324582554; areaId=4; ipLoc-djd=4-51026-0-0; user-key=3707296a-f4c7-4ff6-93e8-c3dde774a8a1; TrackID=1xZk9mkU3P8fa0AGyhX_6Naw6TqHusaubI4kPcc7WZ0qns9_1nMtKGbxHpUKpUmSw8M5kZlC-_7gHuTwt85ZCIwX25pUwAzGM-pl31G14W9k; pin=jd_7a84abcdd5262; unick=jd_187236dlj; ceshi3.com=201; _tp=0JDgHNTWmdShAsXJFHMfrVOaAOd6iKtuIQOAns%2F0IZU%3D; _pst=jd_7a84abcdd5262; __jda=76161171.16208714644421613284524.1620871464.1630908673.1635324583.5; __jdc=76161171; thor=94667556541C996FE9679C6F7E56B49E00AA0E13459DEEBBAEE0675516BCBCC3470F38AECF0E0ECE4A67225187A69BDA3E835C21C2E8E19D86DE4F60AEDBC9A1F04F4DDF63CB21E5C941C8221625CF9134BC1E6BC6CAE0BCE699E129C07EBDE8599B5B612EF72252C38EFB7F65EE9EA685FF7E7CB68AD11609A88226F313AAC1CB680BB5EA07C6A3332C3D9BD124356170F0BCB7069166DCA9B5AE20A8161A4C; shshshfp=6fb49002a719c2ff56f5098dcb20191a; shshshsID=d4f9972cb7ab3afc919dcdac032e42fd_4_1635326429885; 3AB9D23F7A4B3C9B=V3OY2YILYNGDELURAYL23A3WC6DKNXKS65OJTY7XBGQGCSJ4MQTJ5XEXDH2J4WOHWIIY75FHFY2NY4R7K3ZA54IV6A; mobilev=html5; mba_muid=16208714644421613284524; __jdb=76161171.10.16208714644421613284524|5.1635324583; mba_sid=16353264424606759889337564129.2; __jd_ref_cls=Mnpm_ComponentApplied
'''


if __name__ == '__main__':
    start='2021-10-27'               #0924-1027共130199页数据 已完成1-967
    end='2021-11-15'
    getdata(start,end)
    # list=get_time_range_list(start, end)
    # print(list)