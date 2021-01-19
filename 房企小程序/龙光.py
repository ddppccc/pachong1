import csv
import random
import time
import urllib.parse
import pymongo
import requests
from jsonpath import jsonpath
from bson import ObjectId


url = 'https://lgbao.logan.com.cn/olshow/v1/web/product/estate/query/region/list'

headers = {
    'Host': 'lgbao.logan.com.cn',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
    'appId': '1',
    'content-type': 'application/json',
    'tenantId': '1',
    'token': '95c7c866-c7ee-4236-bfd6-c331bdd4573f',
    'userId': '1258666118505336896',
    'Referer': 'https://servicewechat.com/wx23128b96125e7ced/41/page-frame.html',
    'Accept-Encoding': 'gzip, deflate, br',
}

resp = requests.post(url=url,headers=headers,data={"region":1})
print(resp.text)