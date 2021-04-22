<<<<<<< HEAD
from bson import ObjectId
import random
import config
=======
import re
import random
import time
>>>>>>> origin/master
import requests
import os
import time
import pandas as pd
from requests.adapters import HTTPAdapter
<<<<<<< HEAD
from bs4 import BeautifulSoup
=======
from bson.objectid import ObjectId
>>>>>>> origin/master

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))#设置重试次数为3次
s.mount('https://', HTTPAdapter(max_retries=3))
import requests
import config

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "global_cookie=f1v4y6cur4h7034ieaxs84qnk17jxobmy8b; Integrateactivity=notincludemc; newhouse_user_guid=50E5E180-78E4-4D10-DD8D-77E13BC96848; lastscanpage=0; budgetLayer=1%7Cbj%7C2019-07-30%2011%3A26%3A08; resourceDetail=1; new_search_uid=fd91130e51ddd1f2d8e5a7847545c3d8; __utmc=147393320; __utma=147393320.184954923.1564457033.1564642303.1564646708.12; __utmz=147393320.1564646708.12.5.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-verify/redirect; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; logGuid=cb4c3441-3467-4c19-ba09-1dd86b143529; g_sourcepage=ehlist; city=anshan; unique_cookie=U_11rfckz759men2uard7dzzy1i1ejys2c6di*36; __utmb=147393320.15.10.1564646708",
    "Referer": "https://esf.fang.com/newsecond/esfcities.aspx",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
}

# code='050301'
# pos='116.460988,40.006919|116.48231,40.007381;116.47516,39.99713|116.472596,39.985227|116.45669,39.984989|116.460988,40.006919'
# url='https://restapi.amap.com/v3/place/polygon?&types='+code+'&offset=20&page=1&extensions=all&output=json&polygon='+ pos + '&key=' + key
# print(url)

per_page_num = 20

max_len = per_page_num * 100


def get_html(code,pos,key,page = 1):
    try:
        url = 'https://restapi.amap.com/v3/place/polygon?&types=' + code + '&offset='+str(per_page_num)+'&page=' + str(page) + '&extensions=all&output=json&polygon=' + pos + '&key=' + key
        # print(url)
        response = requests.get(url, headers=headers, timeout=2)
        encod = response.apparent_encoding
        if encod.upper() in ['GB2312', 'WINDOWS-1254']:
            encod = 'gbk'
        response.encoding = encod
        data = response.json()
        if data.get("status", "") in [1,'1']:
            return data
        else:
            print("高德返回状态不成功,估计是这个key量使用完了...=>"+key)
            print("下面应该会开始切换key")
            return {}
    except Exception as e:
        print('高德接口访问失败了', e)
        print('先休息两分钟,让高德缓一下...')
        time.sleep(2*60)
        return {}
def get_pos(id_list=[]):
    try:
        if id_list:
            current_pos = config.pos.find_one({"status": 0, "_id": {"$nin": id_list}})
        else:
            current_pos = config.pos.find_one({"status": 0})
        if current_pos:
            u_pos = config.use_pos.find_one(current_pos)           #去重
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
def get_pos_big(current_pos):

    j = re.findall('(\d+\.\d+)?', current_pos['ulbr'])
    # pos=j[0]+','+j[3]+'|'+j[6]+','+j[9]
    l1 = format(eval(j[0]), '.6f')
    l2 = format(eval(j[3]), '.6f')
    l3 = format(eval(j[6]), '.6f')
    l4 = format(eval(j[9]), '.6f')
    pos = l1 + ',' + l2 + '|' + l3 + ',' + l4
    # print('i',i)
    # print(pos)
    return pos
def get_pos_small(current_pos):
    small_pos_list =[]
    j = re.findall('(\d+\.\d+)?', current_pos['ulbr_0'])
    l1 = format(eval(j[0]), '.6f')
    l2 = format(eval(j[3]), '.6f')
    l3 = format(eval(j[6]), '.6f')
    l4 = format(eval(j[9]), '.6f')
    pos = l1 + ',' + l2 + '|' + l3 + ',' + l4
    small_pos_list.append(pos)
    j = re.findall('(\d+\.\d+)?', current_pos['ulbr_1'])
    l1 = format(eval(j[0]), '.6f')
    l2 = format(eval(j[3]), '.6f')
    l3 = format(eval(j[6]), '.6f')
    l4 = format(eval(j[9]), '.6f')
    pos = l1 + ',' + l2 + '|' + l3 + ',' + l4
    small_pos_list.append(pos)
    j = re.findall('(\d+\.\d+)?', current_pos['ulbr_2'])
    l1 = format(eval(j[0]), '.6f')
    l2 = format(eval(j[3]), '.6f')
    l3 = format(eval(j[6]), '.6f')
    l4 = format(eval(j[9]), '.6f')
    pos = l1 + ',' + l2 + '|' + l3 + ',' + l4
    small_pos_list.append(pos)
    j = re.findall('(\d+\.\d+)?', current_pos['ulbr_3'])
    l1 = format(eval(j[0]), '.6f')
    l2 = format(eval(j[3]), '.6f')
    l3 = format(eval(j[6]), '.6f')
    l4 = format(eval(j[9]), '.6f')
    pos = l1 + ',' + l2 + '|' + l3 + ',' + l4
    small_pos_list.append(pos)
    return small_pos_list
def sava_data(data,current_pos):                    #数据处理
    num=0
    for i in data['pois']:
        is_exists = config.poi.find_one({"_id": i["id"]})
        if not is_exists:
            i.update({"_id": i["id"]})
            print(i)
            config.poi.insert_one(i)
        num=num+1
    return num

def get_code(big_pos,small_pos_list,code_dic, key):
    code_dic[big_pos] = []
    for small_pos in small_pos_list:
        code_dic[small_pos] = []
        # print('smallpos',small_pos)
    for big_class_code in config.poicode.keys():
        data = get_html(big_class_code, big_pos, key)
        if int(data['count']) > max_len:
            for small_pos in small_pos_list:
                data = get_html(big_class_code, small_pos, key)
                if int(data['count']) > 1:
                    get_mid_code(big_class_code,code_dic,big_pos,small_pos)
                else:
                    code_dic[small_pos].append(big_class_code)
        else:
            code_dic[big_pos].append(big_class_code)
    return code_dic

def get_mid_code(big_class_code,code_dic,big_pos,small_pos,key):      #获取中类
    for mid_class_code in config.poicode[big_class_code].keys():
        data = get_html(mid_class_code, big_pos, key)
        if int(data['count']) > 1:
            data = get_html(mid_class_code, small_pos, key)
            if int(data['count']) > max_len:
                get_small_code(big_class_code,mid_class_code, code_dic, big_pos, small_pos)
            else:
                code_dic[small_pos].append(mid_class_code)
        else:
            code_dic[big_pos].append(mid_class_code)
    return code_dic

def get_small_code(big_class_code,mid_class_code,code_dic,big_pos,small_pos,key):        #获取小类
    for small_class_code in config.poicode[big_class_code][mid_class_code]:
        data = get_html(small_class_code, big_pos, key)
        if int(data['count']) > max_len:
            code_dic[small_pos].append(small_class_code)
        else:
            code_dic[big_pos].append(small_class_code)
    return code_dic


def run():
    while True:
        key = random.choice(config.gaode_key)
        print("这次是这个key=>"+key)
        current_pos = get_pos()
        try:
            big_pos = get_pos_big(current_pos)
            small_pos_list = get_pos_small(current_pos)
        except Exception as e:
            print("获取网格坐标出错了...重新来过！", e)
            continue
        try:
            code_dic = {}
            code_dic=get_code(big_pos,small_pos_list,code_dic,key)
            print('dict', code_dic)
            sum = 0
            for pos,codes in code_dic.items():
                for code in codes:
                    data = get_html(code, pos, key)
                    if not data:
                        print("没获取到数据,尝试切换key-1")
                        key = random.choice(config.gaode_key)
                        continue
                    num=sava_data(data, current_pos)
                    sum=sum+num
                    count_num = int(data['count'])
                    page = 2
                    while count_num - per_page_num > 0:
                        data = get_html(code, pos, key, page=page)
                        if not data:
                            print("没获取到数据,尝试切换key-2")
                            key = random.choice(config.gaode_key)
                            continue
                        num=sava_data(data, current_pos)
                        sum = sum + num
                        count_num = count_num - per_page_num
                        page = page + 1
            config.pos.update_one(current_pos, {"$set": {"status": 1}})
            print('该地址获取条数', sum)
        except Exception as e:
            print("不知道什么异常了,反正就是没获取到数据，休息两分钟...", e)
            time.sleep(2*60)
            continue


if __name__ == '__main__':
    run()



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

