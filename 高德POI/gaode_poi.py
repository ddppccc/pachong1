from bson import ObjectId
import random
import config
import requests
import os
import time
import pandas as pd
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))#设置重试次数为3次
s.mount('https://', HTTPAdapter(max_retries=3))

lst=[0,1,2,3,4,5,6,7,8,9]
for i in range(10):
    a=random.choice(lst)
    lst.remove(a)
    print(a,lst)



ulbr = config.pos.find({}, {"ulbr": 1, "_id": 0})
count2 = ulbr.count()
ls = []
for i in range(count2):
    ls.append(i)
ind = random.choice(ls)
ls.remove(ind)
print(count2)
print(ind)

print('==========')

def get_proxy():
    try:
        return s.get('http://47.106.223.4:50002/get/').json().get('proxy')
    except:
        num = 3
        while num:
            try:
                return s.get('http://47.106.223.4:50002/get/').json().get('proxy')
            except:
                print('暂无ip，等待20秒')
                time.sleep(20)

                num -= 1
        print('暂无ip')



def get_pos(id_list=[]):
    try:
        if id_list:
            current_pos = config.pos.find_one({"status": 0, "_id": {"$nin": id_list}})
        else:
            current_pos = config.pos.find_one({"status": 0})
        if current_pos:
            u_pos = config.use_pos.find_one(current_pos)
            if u_pos:
                _id = ObjectId(u_pos['_id'])
                id_list.append(_id)
                return get_pos(id_list)
            else:
                config.use_pos.insert_one(current_pos)
                return current_pos
        else:
            return None
    except Exception as e:
        print(e)
        return None

print(get_pos(id_list=[]))


def get_data(use_pos,code):
    # config.use_pos.insert_one({'pow_use':use_pos})
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        # 'Host': 'cq.ke.com',
        "Accept-Language": "zh-CN,zh;q=0.9",
        "upgrade-insecure-requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        'cookie': "lianjia_uuid=bfa7ceba-65ca-4e1e-b591-2fec6f15129c; crosSdkDT2019DeviceId=-pal2xu-di1vvg-q4phzhoefy25s8p-yfip8uyx7; _ga=GA1.2.1314769215.1585729030; ke_uuid=dcb5976f4b3634b4a8bcab004ed5d775; _smt_uid=5e8452ec.5a19fece; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217134e3ece7149-0b39f3df5eee65-6701b35-1327104-17134e3ece837b%22%2C%22%24device_id%22%3A%2217134e3ece7149-0b39f3df5eee65-6701b35-1327104-17134e3ece837b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wyshenzhen%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; __xsptplus788=788.7.1592811193.1592811569.3%234%7C%7C%7C%7C%7C%23%23m3PY-nFnYwlqfjOVPI_Sk2ie3bc2rPsa%23; select_city=320200; lianjia_ssid=ca885273-46e1-48d4-a1be-a36fa1cffa99; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1594089381; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1594089399; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiOWQ4ODYyNmZhMmExM2Q0ZmUxMjk1NWE2YTRjY2JmODZkNTdmNDQ1NmNhMDA5OWRmOTM1YjJhOTU0NDFjYzMzYjg3Yjk5YjZmODc3OTRmYmRlY2VmYjFmODQyMGIyOTA5YWE3NDcxMjM0N2FhMDdhMDRjNDUzMDkyNWI1MDk2ZTAxN2RjYTIzYjMyMGZhMTM3NjkyYjYyNjMwOTE1OWZhZDFjMTI4NGMxZTk1MWY1ZTMyMmYxMmEwZTI4MTg5MDJjZjAwOGI2MDNiOWExMWNlNjhkMTkyN2VjYjcwODE2MTc5YmY4OGUxODZiYWQ1MDhjZjkyODM2YjU0YTBkYzI4M2RiNDA4ZWI0MzMyNTFjYWQyNzliNGYwMzA1ZGI0Njc4YTYxZDU5OTQzYTBlOGVhNTA3NWZkY2E3MDE2ODczYjNiOTQ2MzNmZjM3M2FhMmE2Y2JjMjFiYWUxNmU2MzA2ZVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJjY2E0ZTVlOFwifSIsInIiOiJodHRwczovL3d4LmtlLmNvbS94aWFvcXUvNDEyMDAzNDQwNDAyMDUwMC8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==",

    }
    proxy = {'https:':'https://' + get_proxy(),
         'http:':'http://' + get_proxy()}
    key = '4fabbb7c9a939ee3942c67715f9a8f33'
    for i in range(100):
        url = 'https://restapi.amap.com/v3/place/polygon?types=' + str(code) + '&offset=20&page='+ str(i) +'&extensions=all&polygon='\
              + str(use_pos) + '&key=' + key
        res = s.get(url, headers=headers,proxies=proxy, timeout=7)
        res.encoding = 'utf-8'
        html = res.json()
        #bs = BeautifulSoup(html, parser='xml')
        if int(html['count']) == 0:
            print(i, '页已无数据，跳出', url)
            break
        item = html['pois']
        config.poi.insert_one(item)
        print(item)
        # 存数据


def get_count(use_pos,code):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        # 'Host': 'cq.ke.com',
        "Accept-Language": "zh-CN,zh;q=0.9",
        "upgrade-insecure-requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        'cookie': "lianjia_uuid=bfa7ceba-65ca-4e1e-b591-2fec6f15129c; crosSdkDT2019DeviceId=-pal2xu-di1vvg-q4phzhoefy25s8p-yfip8uyx7; _ga=GA1.2.1314769215.1585729030; ke_uuid=dcb5976f4b3634b4a8bcab004ed5d775; _smt_uid=5e8452ec.5a19fece; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217134e3ece7149-0b39f3df5eee65-6701b35-1327104-17134e3ece837b%22%2C%22%24device_id%22%3A%2217134e3ece7149-0b39f3df5eee65-6701b35-1327104-17134e3ece837b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wyshenzhen%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; __xsptplus788=788.7.1592811193.1592811569.3%234%7C%7C%7C%7C%7C%23%23m3PY-nFnYwlqfjOVPI_Sk2ie3bc2rPsa%23; select_city=320200; lianjia_ssid=ca885273-46e1-48d4-a1be-a36fa1cffa99; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1594089381; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1594089399; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiOWQ4ODYyNmZhMmExM2Q0ZmUxMjk1NWE2YTRjY2JmODZkNTdmNDQ1NmNhMDA5OWRmOTM1YjJhOTU0NDFjYzMzYjg3Yjk5YjZmODc3OTRmYmRlY2VmYjFmODQyMGIyOTA5YWE3NDcxMjM0N2FhMDdhMDRjNDUzMDkyNWI1MDk2ZTAxN2RjYTIzYjMyMGZhMTM3NjkyYjYyNjMwOTE1OWZhZDFjMTI4NGMxZTk1MWY1ZTMyMmYxMmEwZTI4MTg5MDJjZjAwOGI2MDNiOWExMWNlNjhkMTkyN2VjYjcwODE2MTc5YmY4OGUxODZiYWQ1MDhjZjkyODM2YjU0YTBkYzI4M2RiNDA4ZWI0MzMyNTFjYWQyNzliNGYwMzA1ZGI0Njc4YTYxZDU5OTQzYTBlOGVhNTA3NWZkY2E3MDE2ODczYjNiOTQ2MzNmZjM3M2FhMmE2Y2JjMjFiYWUxNmU2MzA2ZVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJjY2E0ZTVlOFwifSIsInIiOiJodHRwczovL3d4LmtlLmNvbS94aWFvcXUvNDEyMDAzNDQwNDAyMDUwMC8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==",

    }
    # use_pos = '116.460988,40.006919|116.48231,40.007381;116.47516,39.99713|116.472596,39.985227|116.45669,39.984989|116.460988,40.006919'
    proxy = {'https:': 'https://' + get_proxy(),
             'http:': 'http://' + get_proxy()}
    key = '4fabbb7c9a939ee3942c67715f9a8f33'
    url = 'https://restapi.amap.com/v3/place/polygon?types=' + str(code) \
          + '&offset=20&extensions=all&output=xml&polygon=' \
          + use_pos + '&key=' + key
    res = s.get(url, headers=headers, proxies=proxy, timeout=7)
    html = res.text
    bs = BeautifulSoup(html, parser='xml')
    coun = bs.find('count').text
    return int(coun)

def bl(aa_0):
    a1_0 = "%.6f" % float(aa_0[0])
    a2_0 = "%.6f" % float(aa_0[1])
    a3_0 = "%.6f" % float(aa_0[2])
    a4_0 = "%.6f" % float(aa_0[3])
    use_pos_0 = str(a1_0) + ',' + str(a2_0) + ',' + str(a3_0) + ',' + str(a4_0)
    return use_pos_0

def run(use_pos,code,asd):
    coun = get_count(use_pos,code)
    if coun>2000:#改为中类
        zhong_codeList = config.poicode[code].keys()
        for zhong_code in zhong_codeList:
            coun = get_count(zhong_code, code)
            if coun > 2000:# 改为小类
                xiao_codeList = config.poicode[code][zhong_code].keys()
                for xiao_code in xiao_codeList:
                    coun = get_count(xiao_code, code)
                    if coun > 2000:#改为2*2小网格
                        ulbr0 = config.pos.find({"ulbr":asd}, {"ulbr_0": 1, "_id": 0})
                        aa_0 = str(ulbr0[0]['ulbr_0']).split(', ')
                        use_pos_0 = bl(aa_0)
                        get_data(use_pos_0,xiao_code)

                        ulbr1 = config.pos.find({"ulbr": asd}, {"ulbr_1": 1, "_id": 0})
                        aa_1 = str(ulbr1[0]['ulbr_0']).split(', ')
                        use_pos_1 = bl(aa_1)
                        get_data(use_pos_1, xiao_code)

                        ulbr2 = config.pos.find({"ulbr": asd}, {"ulbr_2": 1, "_id": 0})
                        aa_2 = str(ulbr2[0]['ulbr_0']).split(', ')
                        use_pos_2 = bl(aa_2)
                        get_data(use_pos_2, xiao_code)

                        ulbr3 = config.pos.find({"ulbr": asd}, {"ulbr_3": 1, "_id": 0})
                        aa_3 = str(ulbr3[0]['ulbr_0']).split(', ')
                        use_pos_3 = bl(aa_3)
                        get_data(use_pos_3, xiao_code)
            else:
                get_data(use_pos,zhong_code)
    else:
        get_data(use_pos, code)#继续


if __name__ == '__main__':
    ulbr = config.pos.find({}, {"ulbr": 1, "_id": 0})
    count2 = ulbr.count()
    ls = []
    for i in range(count2):
        ls.append(i)
    for i in range(count2):
        a = random.choice(lst)
        lst.remove(a)
        asd = str(ulbr[a]['ulbr'])
        aa = asd.split(', ')
        use_pos = bl(aa)
        # 判断是否爬取过了
        get_pos(id_list=[])
        code_list = config.poicode.keys()
        for code in code_list:
            run(use_pos, code,asd)

