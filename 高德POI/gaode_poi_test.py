import re
import random
import requests
import time
from requests.adapters import HTTPAdapter
from bson.objectid import ObjectId

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


max_len = 2500
per_page_num = 25


#获取数据
def get_html(code, pos, page=1):
    try:
        key = random.choices(config.gaode_key)
        url = config.api_url+'&types=' + code + '&offset='+str(per_page_num)+'&page=' + str(page) + '&polygon=' + pos + '&key=' + key
        response = requests.get(url, headers=headers, timeout=2)
        encod = response.apparent_encoding
        if encod.upper() in ['GB2312', 'WINDOWS-1254']:
            encod = 'gbk'
        response.encoding = encod
        data = response.json()
        if data.get("status", '') in [1, '1']:
            return data
        else:
            print('获取返回数据失败...')
            return {}
    except Exception as e:
        print('异常了...', e)
        return {}


# 已抓取网格去重
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


# 数据保存
def sava_data(data):
    for i in data['pois']:
        is_exists = config.poi.find_one({"_id": i["id"]})
        if not is_exists:
            i.update({"_id": i["id"]})
            print(i)
            config.poi.insert_one(i)


def handle_page(count):
    return count//25 if count % 25 == 0 else (count//25) + 1



#处理5x5
def handle_process5X5(pos):
    try:
        page = 1
        # 循环大类
        for i in config.poicode.keys():
            curr_pos = handle_pos(pos['ulbr'])
            data = get_html(i, curr_pos, page)
            if data.get("status", '') in [1, '1']:
                if int(data['count']) > max_len:
                    # 循环中类
                    page = 1
                    for j in config.poicode[i]:
                        data = get_html(j, curr_pos, page)
                        if data.get("status", '') in [1, '1']:
                            if int(data['count']) > max_len:
                                # 循环小类
                                page = 1
                                for k in config.poicode[i][j]:
                                    data = get_html(k, curr_pos, page)
                                    if data.get("status", '') in [1, '1']:
                                        if int(data['count']) > max_len:
                                            handle_process2X2(pos, i)
                                        else:
                                            sava_data(data)
                                            if handle_page(int(data['count'])) > 2:
                                                for p in range(2, handle_page(int(data['count'])) + 1):
                                                    data = get_html(k, curr_pos, p)
                                                    sava_data(data)
                                    else:
                                        print("查询POI小类返回错误:\n  POI类型代码:" + k)
                                        print("  5X5网格:" + pos['ulbr'])
                            else:
                                sava_data(data)
                                if handle_page(int(data['count'])) > 2:
                                    for p in range(2, handle_page(int(data['count'])) + 1):
                                        data = get_html(j, curr_pos, p)
                                        sava_data(data)
                        else:
                            print("查询POI中类返回错误:\n  POI类型代码:" + j)
                            print("  5X5网格:" + pos['ulbr'])
                else:
                    sava_data(data)
                    if handle_page(int(data['count'])) > 2:
                        for p in range(2, handle_page(int(data['count']))+1):
                            data = get_html(i, curr_pos, p)
                            sava_data(data)
            else:
                print("查询POI大类返回错误:\n  POI类型代码:"+i)
                print("  5X5网格:" + pos['ulbr'])
    except Exception as e:
        print('异常了...', e)


#处理2X2
def handle_process2X2(curr_pos, poicode):
    try:
        pos_list = []
        pos_list.append(curr_pos['ulbr_0'])
        pos_list.append(curr_pos['ulbr_1'])
        pos_list.append(curr_pos['ulbr_2'])
        pos_list.append(curr_pos['ulbr_3'])
        page = 1
        for pl in pos_list:
            pos = handle_pos(pl)
            for j in config.poicode[poicode]:
                data = get_html(j, pos, page)
                if data.get("status", '') in [1, '1']:
                    if int(data['count']) > max_len:
                        page = 1
                        for k in config.poicode[poicode][j]:
                            data = get_html(k, curr_pos, page)
                            if data.get("status", '') in [1, '1']:
                                sava_data(data)
                                if handle_page(int(data['count'])) > 2:
                                    for p in range(2, handle_page(int(data['count'])) + 1):
                                        data = get_html(k, pos, p)
                                        sava_data(data)
                                else:
                                    print("查询POI返回错误:\n  POI类型代码:" + k)
                                    print("  2X2网格:" + pl)
                    else:
                        sava_data(data)
                        if handle_page(int(data['count'])) > 2:
                            for p in range(2, handle_page(int(data['count'])) + 1):
                                data = get_html(j, pl, p)
                                sava_data(data)
                else:
                    print("查询POI返回错误:\n  POI类型代码:" + j)
                    print("  2X2网格:" + pl)
    except Exception as e:
        print('异常了...', e)


# 坐标转换为实际需要的参数
def handle_pos(pos=""):
    j = re.findall('(\d+\.\d+)?', pos)
    l1 = format(eval(j[0]), '.6f')
    l2 = format(eval(j[3]), '.6f')
    l3 = format(eval(j[6]), '.6f')
    l4 = format(eval(j[9]), '.6f')
    this_pos = l1 + ',' + l2 + '|' + l3 + ',' + l4
    return this_pos


if __name__ == '__main__':
    # flag = True
    # while flag:
    #     #current_pos = get_pos()
    #     current_pos = {'_id': ObjectId('6076840d1058790d7ece375c'), 'gridid': '87', 'city': '七台河市',
    #                    'ulbr': '130.25298531886688, 46.00935192833246, 130.29790108307287, 45.978147293498665',
    #                    'ulbr_0': '130.25298531886688, 46.00935192833246, 130.27544320096987, 45.99374961091556',
    #                    'ulbr_1': '130.25298531886688, 45.99374961091556, 130.27544320096987, 45.978147293498665',
    #                    'ulbr_2': '130.27544320096987, 46.00935192833246, 130.29790108307287, 45.99374961091556',
    #                    'ulbr_3': '130.27544320096987, 45.99374961091556, 130.29790108307287, 45.978147293498665',
    #                    'status': 0}
    #     if current_pos:
    #         handle_process5X5(current_pos)
    #         config.pos.update({"_id": current_pos["_id"]}, {"$set": {"status": 1}})
    #     else:
    #         flag = False
    print(int(time.time() * 1000))
    current_pos = {'_id': ObjectId('6076840d1058790d7ece375c'), 'gridid': '87', 'city': '七台河市',
                      'ulbr': '130.25298531886688, 46.00935192833246, 130.29790108307287, 45.978147293498665',
                      'ulbr_0': '130.25298531886688, 46.00935192833246, 130.27544320096987, 45.99374961091556',
                      'ulbr_1': '130.25298531886688, 45.99374961091556, 130.27544320096987, 45.978147293498665',
                      'ulbr_2': '130.27544320096987, 46.00935192833246, 130.29790108307287, 45.99374961091556',
                      'ulbr_3': '130.27544320096987, 45.99374961091556, 130.29790108307287, 45.978147293498665',
                      'status': 0}
    if current_pos:
        handle_process5X5(current_pos)
                   #         config.pos.update({"_id": current_pos["_id"]}, {"$set": {"status": 1}})
    print(int(time.time() * 1000))
    print("已经没有需要抓取的网格了...")
    print("应该已经抓取完成或者即将抓取完成...")
