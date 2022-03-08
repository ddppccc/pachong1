import re
import random
import requests
import time
from requests.adapters import HTTPAdapter
from bson.objectid import ObjectId
s = requests.Session()
from 高德乱码处理 import if_contain_symbol,update_data
s.mount('http://', HTTPAdapter(max_retries=3))#设置重试次数为3次
s.mount('https://', HTTPAdapter(max_retries=3))
import requests
import config
import Logger
import json

logger = Logger.LoggerFactory.getLogger("gaode_poi")

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "global_cookie=f1v4y6cur4h7034ieaxs84qnk17jxobmy8b; Integrateactivity=notincludemc; newhouse_user_guid=50E5E180-78E4-4D10-DD8D-77E13BC96848; lastscanpage=0; budgetLayer=1%7Cbj%7C2019-07-30%2011%3A26%3A08; resourceDetail=1; new_search_uid=fd91130e51ddd1f2d8e5a7847545c3d8; __utmc=147393320; __utma=147393320.184954923.1564457033.1564642303.1564646708.12; __utmz=147393320.1564646708.12.5.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-verify/redirect; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; logGuid=cb4c3441-3467-4c19-ba09-1dd86b143529; g_sourcepage=ehlist; city=anshan; unique_cookie=U_11rfckz759men2uard7dzzy1i1ejys2c6di*36; __utmb=147393320.15.10.1564646708",
    "Referer": "https://esf.fang.com/newsecond/esfcities.aspx",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
}

# 最大长度设置
max_len = 2500
# 每页长度设置  不超过25
per_page_num = 25


# 获取数据
def get_html(code, pos, page=1, retry=0):
    try:
        key = random.choice(config.gaode_key)
        url = config.api_url+'&types=' + code + '&offset='+str(per_page_num)+'&page=' + str(page) + '&polygon=' + pos + '&key=' + key
        response = requests.get(url, headers=headers, timeout=2)
        encod = response.apparent_encoding
        if encod.upper() in ['GB2312', 'WINDOWS-1254']:
            encod = 'gbk'
        response.encoding = encod
        data = json.loads(response.text)
        if data.get("status", '') in [1, '1']:
            return data
        else:
            print("高德返回状态失败", data)
            if retry < 3:
                print('重新再试...', retry)
                return get_html(code, pos, page, retry+1)
            else:
                print('重试失败,放弃...', retry)
                return {}
    except Exception as e:
        print('高德接口访问失败了', e)
        if retry < 3:
            print('异常,重新再试...', retry)
            return get_html(code, pos, page, retry+1)
        else:
            print('异常,重试失败,放弃...', retry)
            return {}


# 已抓取网格去重
def get_pos(id_list=[]):
    try:
        if id_list:
            current_pos = config.pos.find_one({"status": 1, "_id": {"$nin": id_list}})
        else:
            current_pos = config.pos.find_one({"status": 1})
        if current_pos:
            u_pos = config.use_pos.find_one(current_pos)
            if u_pos:
                _id = ObjectId(u_pos['_id'])
                id_list.append(_id)
                return get_pos(id_list)
            else:
                try:
                    config.use_pos.insert_one(current_pos)
                    return current_pos
                except Exception as e:
                    print(e)
                    return get_pos(id_list)
        else:
            return None
    except Exception as e:
        print(e)
        return None


# 数据保存
def sava_data(data):
    num = 0
    for i in data['pois']:
        is_exists = config.poi.find_one({"_id": i["id"]})
        if not is_exists:
            # i.update({"_id": i["id"]})
            if if_contain_symbol(i):
                i = update_data(i)
            print(i)
            if i:
                config.poi.insert_one(i)
        num += 1
    return num
    #return len(data.get('pois', []))

# 处理总页数
def handle_page(count):
    return count//per_page_num if count % per_page_num == 0 else (count//per_page_num) + 1


# 处理5x5
def handle_process5X5(pos):
    sum = 0
    try:
        page1 = 1
        # 循环大类
        curr_pos = handle_pos(pos['ulbr'])
        for i in config.poicode.keys():
            data = get_html(i, curr_pos, page1)
            if data.get("status", '') in [1, '1']:
                if int(data['count']) > max_len:
                    # 循环中类
                    page2 = 1
                    for j in config.poicode[i]:
                        data = get_html(j, curr_pos, page2)
                        if data.get("status", '') in [1, '1']:
                            if int(data['count']) > max_len:
                                # 循环小类
                                page3 = 1
                                for k in config.poicode[i][j]:
                                    data = get_html(k, curr_pos, page3)
                                    if data.get("status", '') in [1, '1']:
                                        if int(data['count']) > max_len:
                                            num = handle_process2X2(pos, i)
                                            sum +=num
                                        else:
                                            num = sava_data(data)
                                            sum += num
                                            if int(data['count']) > per_page_num:
                                                for p3 in range(2, handle_page(int(data['count'])) + 1):
                                                    data = get_html(k, curr_pos, p3)
                                                    num = sava_data(data)
                                                    sum += num
                                    else:
                                        logger.info("查询POI小类返回错误:\n  POI类型代码:" + k)
                                        logger.info("  5X5网格:" + pos['ulbr'])
                            else:
                                num = sava_data(data)
                                sum += num
                                if int(data['count']) > per_page_num:
                                    for p2 in range(2, handle_page(int(data['count'])) + 1):
                                        data = get_html(j, curr_pos, p2)
                                        num =sava_data(data)
                                        sum += num
                        else:
                            logger.info("查询POI中类返回错误:\n  POI类型代码:" + j)
                            logger.info("  5X5网格:" + pos['ulbr'])
                else:
                    num = sava_data(data)
                    sum += num
                    if int(data['count']) > per_page_num:
                        for p1 in range(2, handle_page(int(data['count']))+1):
                            data = get_html(i, curr_pos, p1)
                            num =sava_data(data)
                            sum += num
            else:
                logger.info("查询POI大类返回错误:\n  POI类型代码:"+i)
                logger.info("  5X5网格:" + pos['ulbr'])
    except Exception as e:
        print('异常了...', e)
    return sum


# 处理2X2
def handle_process2X2(curr_pos, poicode):
    sum = 0
    try:
        pos_list = []
        pos_list.append(curr_pos['ulbr_0'])
        pos_list.append(curr_pos['ulbr_1'])
        pos_list.append(curr_pos['ulbr_2'])
        pos_list.append(curr_pos['ulbr_3'])
        page1 = 1
        for pl in pos_list:
            pos = handle_pos(pl)
            data = get_html(poicode, pos, page1)
            if data.get("status", '') in [1, '1']:
                for j in config.poicode[poicode]:
                    page2 = 1
                    data = get_html(j, pos, page2)
                    if data.get("status", '') in [1, '1']:
                        if int(data['count']) > max_len:
                            page3 = 1
                            for k in config.poicode[poicode][j]:
                                data = get_html(k, curr_pos, page3)
                                if data.get("status", '') in [1, '1']:
                                    num = sava_data(data)
                                    sum += num
                                    if int(data['count']) > per_page_num:
                                        for p3 in range(2, handle_page(int(data['count'])) + 1):
                                            data = get_html(k, pos, p3)
                                            num = sava_data(data)
                                            sum += num
                                    else:
                                        logger.info("查询POI返回错误:\n  POI类型代码:" + k)
                                        logger.info("  2X2网格:" + pl)
                        else:
                            num = sava_data(data)
                            sum += num
                            if int(data['count']) > per_page_num:
                                for p2 in range(2, handle_page(int(data['count'])) + 1):
                                    data = get_html(j, pl, p2)
                                    num = sava_data(data)
                                    sum += num
                    else:
                        logger.info("查询POI返回错误:\n  POI类型代码:" + j)
                        logger.info("  2X2网格:" + pl)
            else:
                num = sava_data(data)
                sum += num
                if int(data['count']) > per_page_num:
                    for p1 in range(2, handle_page(int(data['count'])) + 1):
                        data = get_html(poicode, pl, p1)
                        num = sava_data(data)
                        sum += num
    except Exception as e:
        print('异常了...', e)
    return sum


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
    # 跑前运行一遍
    # config.pos.update_many({}, {"$set": {"status": 1}})
    # print(config.pos.count_documents({"status": 1}))


    flag = True
    while flag:
        start_time = time.time()
        current_pos = get_pos(id_list=[])
        print('当前网格', current_pos)
        if current_pos:
            _sum = handle_process5X5(current_pos)
            config.pos.update_one({"_id": current_pos["_id"]}, {"$set": {"status": 0}})
            config.use_pos.delete_one(current_pos)
            print('该地址获取条数', _sum)
        else:
            flag = False
        print("耗时:", time.time()-start_time)
    # start_time = time.time()
    # current_pos = {'_id': ObjectId('6076bdebb5b5690a5413f446'), 'gridid': '548', 'city': '湛江市', 'ulbr': '110.22625878505572, 21.628665060447005, 110.27117454926169, 21.58690568737001', 'ulbr_0': '110.22625878505572, 21.628665060447005, 110.2487166671587, 21.607785373908506', 'ulbr_1': '110.22625878505572, 21.607785373908506, 110.2487166671587, 21.58690568737001', 'ulbr_2': '110.2487166671587, 21.628665060447005, 110.27117454926169, 21.607785373908506', 'ulbr_3': '110.2487166671587, 21.607785373908506, 110.27117454926169, 21.58690568737001', 'status': 1.0}
    # if current_pos:
    #     _sum = handle_process5X5(current_pos)
    #     print('该地址获取条数', _sum)
    # print("耗时:", time.time()-start_time)
    print("已经没有需要抓取的网格了...")
    print("应该已经抓取完成或者即将抓取完成...")
