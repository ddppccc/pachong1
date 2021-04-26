import re
import random
import time
import requests
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
        print(int(time.time()))
        current_pos = get_pos(id_list=[])
        print(int(time.time()))
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
            config.use_pos.remove(current_pos)
            print('该地址获取条数', sum)
        except Exception as e:
            print("不知道什么异常了,反正就是没获取到数据，休息两分钟...", e)
            time.sleep(2*60)
            continue


if __name__ == '__main__':
    run()




