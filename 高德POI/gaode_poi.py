import config
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
import pymongo
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

key=config.gaode_key[0]
def get_html(code,pos,key,page = 1):
    try:

        url = 'https://restapi.amap.com/v3/place/polygon?&types=' + code + '&offset=20&page=' + str(page) + '&extensions=all&output=json&polygon=' + pos + '&key=' + key
        # print(url)
        response = requests.get(url, headers=headers, timeout=2)
        encod = response.apparent_encoding
        if encod.upper() in ['GB2312', 'WINDOWS-1254']:
            encod = 'gbk'
        response.encoding = encod
        data = response.json()
        return data
    except Exception as e:
        print('获取页面失败',e)
# def get_pos_big():
#     # search=config.pos                       #数据表格
#     # has=config.use_pos                  #已抓取
#     for i in config.pos.find():
#         j=re.findall('\d+',i['ulbr'])
#         k=j[0]+'.'+j[1]+','+j[2]+'.'+j[3]+'|'+ j[4]+'.'+j[5]+','+j[6]+'.'+j[7]
#         break
#     return k
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
def get_pos_small():
    # search=config.pos                       #数据表格
    # has=config.use_pos                  #已抓取
    for i in config.pos.find():
        small_pos_list=[]
        j=re.findall('(\d+\.\d+)?',i['ulbr_0'])
        l1 = format(eval(j[0]), '.6f')
        l2 = format(eval(j[3]), '.6f')
        l3 = format(eval(j[6]), '.6f')
        l4 = format(eval(j[9]), '.6f')
        pos = l1 + ',' + l2 + '|' + l3 + ',' + l4
        small_pos_list.append(pos)
        j = re.findall('(\d+\.\d+)?', i['ulbr_0'])
        l1 = format(eval(j[0]), '.6f')
        l2 = format(eval(j[3]), '.6f')
        l3 = format(eval(j[6]), '.6f')
        l4 = format(eval(j[9]), '.6f')
        pos = l1 + ',' + l2 + '|' + l3 + ',' + l4
        small_pos_list.append(pos)
        j = re.findall('(\d+\.\d+)?', i['ulbr_0'])
        l1 = format(eval(j[0]), '.6f')
        l2 = format(eval(j[3]), '.6f')
        l3 = format(eval(j[6]), '.6f')
        l4 = format(eval(j[9]), '.6f')
        pos = l1 + ',' + l2 + '|' + l3 + ',' + l4
        small_pos_list.append(pos)
        j = re.findall('(\d+\.\d+)?', i['ulbr_0'])
        l1 = format(eval(j[0]), '.6f')
        l2 = format(eval(j[3]), '.6f')
        l3 = format(eval(j[6]), '.6f')
        l4 = format(eval(j[9]), '.6f')
        pos = l1 + ',' + l2 + '|' + l3 + ',' + l4
        small_pos_list.append(pos)
        break
    return small_pos_list
def sava_data(data,current_pos):                    #数据处理

    for i in data['pois']:
        print(i)
        config.poi.insert_one(i)

    pass
def get_code(pos,code_list):
    try:
        for i in config.poicode.keys():
            # print('getcode',i,pos,key)
            data=get_html(i,pos,key)
            # print('count',data['count'],'code',i)
            if int(data['count']) > 2000:
                for j in config.poicode[i]:
                    data = get_html(j, pos, key)
                    # print('count',data['count'],'code',j)
                    if int(data['count']) > 2000:
                        for k in config.poicode[i][j]:
                            # print(k)
                            data = get_html(k, pos, key)
                            # print('count', data['count'],'code',k)
                            if int(data['count']) > 2000:
                                return code_list
                            else:
                                code_list.append(k)
                    else:
                        code_list.append(j)
            else:
                code_list.append(i)
        return code_list
    except Exception as e:
        print('获取code失败',e)
        return code_list
if __name__ == '__main__':
    while True:
        code_list=[]
        current_pos=get_pos()
        # current_pos = config.pos.find_one({"status": 0})
        #判断是否在use_pos表中
        # count = config.use_pos.count_documents({"ulbr": current_pos['ulbr']})
        # count = config.use_pos.count_documents({"ulbr": 'DDDD'})
        # if count != 0:
        #     print("该数据已抓取")
        #     continue
        # else:
        #     print('该数据没有抓取')
        j = re.findall('(\d+\.\d+)?', current_pos['ulbr'])
        # print(j)
        # pos = j[0] + '.' + j[1] + ',' + j[2] + '.' + j[3] + '|' + j[4] + '.' + j[5] + ',' + j[6] + '.' + j[7]
        # pos=j[0]+','+j[3]+'|'+j[6]+','+j[9]
        l1=format(eval(j[0]), '.6f')
        l2=format(eval(j[3]), '.6f')
        l3=format(eval(j[6]), '.6f')
        l4=format(eval(j[9]), '.6f')
        pos=l1+','+l2+'|'+l3+','+l4
        print(pos)
        code_list = get_code(pos,code_list)
        print(code_list)
        if len(code_list) == 0:
            continue
        for code in code_list:
            data = get_html(code, pos, key)
            sava_data(data, current_pos)
            # print(data)
            count_num=int(data['count'])
            page = 2
            while count_num-20 > 0:
                data=get_html(code, pos, key,page=page)
                sava_data(data, current_pos)
                count_num=count_num-20
                page=page+1
        try:
            config.pos.update_one(current_pos,{"$set":{"status":1}})
            print('状态更新成功')
            # config.use_pos.insert_one(current_pos)
            # print('数据记录成功')
        except Exception as e:
            print(e)

# current_pos=get_pos()
# print(current_pos)
# print(type(current_pos))
# l=config.pos.find_one(current_pos)
# print(l)
# x = config.use_pos.delete_many({})
# print(x.deleted_count, "个文档已删除")
# print(config.use_pos.count_documents({}))
# print(config.poi.count_documents({}))