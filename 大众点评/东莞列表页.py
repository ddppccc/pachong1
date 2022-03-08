# encoding=utf8
from urllib import parse
import pymongo
from fontTools.ttLib import TTFont
from concurrent.futures import ThreadPoolExecutor
from 获取位置 import getpos,getmpos
from 获取评分 import getscore
from fake_useragent import UserAgent
from scrapy import Selector
import hashlib
import random
import time
import re
import os
import datetime
from lxml import etree
from mobile详情 import getmdetail
import requests
from fake_useragent import UserAgent
from config import typedict,MONGODB_CONFIG,fheaders,headers,citylist,get_proxy,gethtml,cookie_header


pagebase = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['大众点评']['美食_列表页链接_202106']
newpage = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['大众点评']['东莞_列表页链接_202107']

# print(pagebase.find_one({'cityname': '东莞'}))
# for i in pagebase.find({'cityname': '东莞'}):
#     newpage.insert_one(i)
# print('ok')


from config import typedict
a=list(typedict.keys())[list(typedict.values()).index("ch30")]
print(a)