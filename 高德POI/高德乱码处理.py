# encoding=utf-8
import random
import requests
import re
from urllib import parse
import pymongo
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
    retryWrites="false")['gaode']['poi_202110']
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "global_cookie=f1v4y6cur4h7034ieaxs84qnk17jxobmy8b; Integrateactivity=notincludemc; newhouse_user_guid=50E5E180-78E4-4D10-DD8D-77E13BC96848; lastscanpage=0; budgetLayer=1%7Cbj%7C2019-07-30%2011%3A26%3A08; resourceDetail=1; new_search_uid=fd91130e51ddd1f2d8e5a7847545c3d8; __utmc=147393320; __utma=147393320.184954923.1564457033.1564642303.1564646708.12; __utmz=147393320.1564646708.12.5.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-verify/redirect; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; logGuid=cb4c3441-3467-4c19-ba09-1dd86b143529; g_sourcepage=ehlist; city=anshan; unique_cookie=U_11rfckz759men2uard7dzzy1i1ejys2c6di*36; __utmb=147393320.15.10.1564646708",
    "Referer": "https://esf.fang.com/newsecond/esfcities.aspx",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
}
gaode_key = [
    # "4fabbb7c9a939ee3942c67715f9a8f33",
    "ac2d0d6951b7662e1b98aabb51b4aeb6",            #
    "705d303822d6685c2b05915464483a9c",          #
    "9411ece7ba7c9ff934a093219215b47d",        #
    "de3514f87e2d145179e4adbd0cb01b1d",         #
    "f7e4985b165ebcb8d9976d0af95de9ff"       #
]
def update_data(source,retry=0):
    try:
        key = random.choice(gaode_key)
        url = 'https://restapi.amap.com/v3/place/detail?output=json&key=' + key +'&id='+source['id']
        response = requests.get(url, headers=headers, timeout=2)
        encod = response.apparent_encoding
        if encod.upper() in ['GB2312', 'WINDOWS-1254']:
            encod = 'gbk'
        response.encoding = encod
        data = response.json()
        # print(data)
        if data.get("status", '') in [1, '1']:
            return data['pois'][0]
        else:
            print("高德返回状态失败", data)
            if retry < 3:
                print('重新再试...', retry)
                return update_data(source, retry + 1)
            else:
                print('重试失败,放弃...', retry)
                return {}
    except Exception as e:
        print('高德接口访问失败了', e)
        if retry < 3:
            print('异常,重新再试...', retry)
            return update_data(source, retry + 1)
        else:
            print('异常,重试失败,放弃...', retry)
            return {}

def update_database(oldsource,newsource):
    info_base.update_one({'_id':oldsource['_id']},{"$set":newsource})


def if_contain_symbol(source):
    if re.search(r"\W", source['cityname'].replace(' ','')):
        return True
    else:
        return False


luanmastr='''

'''
if __name__ == '__main__':

    # from bson.objectid import ObjectId
    #
    # source=info_base.find_one({'_id':ObjectId('6166287106cea8af969e9264')})   #获取一条数
    # update_data(source)
    # if if_contain_symbol(source):            #判断是否乱码
    #     newsource=update_data(source)            #获取正常编码数据
    #     update_database(source,newsource)    #数据库更新数据
    # else:
    #     print('无乱码')
    #     print(source)

    num=1
    for city in info_base.distinct('cityname'):
        if re.search(r"\W", city.replace(' ','')):
            for source in info_base.find({'cityname':city}):

                if if_contain_symbol(source):  # 判断是否乱码

                    newsource = update_data(source)  # 获取正常编码数据

                    update_database(source, newsource)  # 数据库更新数据
                    print('成功更新',num)
                    num+=1