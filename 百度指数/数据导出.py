# encoding=utf8
import json
import re

import pymongo
import pandas as pd
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
            retryWrites="false")['百度指数']['百度搜索指数_数据_202201']
def getwords(self):
    return json.loads(self.replace("'",'"'))[0]['name']
def getmonth(self):
    try:
        return re.findall('(\d+-\d+)-\d+',self)[0]
    except:
        print(self)
        return self

df=pd.DataFrame([i for i in info_base.find()])
df = df[['keyword', 'type', 'date', 'index', '抓取时间', '城市']]
df['keys']= df['keyword'].apply(getwords)
df['month']= df['date'].apply(getmonth)
print(df)
df.to_csv('百度指数_new.csv',mode='a+', index=False,header=False)