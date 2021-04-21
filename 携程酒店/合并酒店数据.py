import os
import pandas as pd
import pymongo

from config import Year, Month
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
            retryWrites="false")['携程酒店']['数据']

url_data = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['携程酒店']['已合并id']
year = Year
month = Month

# 合并后保存位置
path1 = '酒店合并详情数据/{year}-{month}携程酒店'.format(year=year, month=month)
os.path.exists(path1) or os.makedirs(path1)

for i in os.listdir(r'酒店数据'):
    print(i)
    city = i.split('_')[1]
    if city in [i.split('_')[1] for i in os.listdir(path1)]:
        continue
    path = r'酒店数据/' + i
    df = pd.read_excel(path)
    df = df.drop_duplicates()

    df1 = pd.read_csv(r'酒店详情信息/{}.csv'.format(city))
    df1 = df1.drop_duplicates()

    df2 = pd.merge(df, df1, left_on='id', right_on='id')

    col = ['城市','商圈','id','酒店名称','酒店星级','起步价','地址','lon','lat','特点','评论数量','综合评分','评分详情',
           '开业时间','户型详情','房间数量','酒店简介','附近','抓取时间']

    df2 = df2[col]
    for length in range(len(df2)):
        item = dict(df2.iloc[length])
        item['id'] = int(item['id'])

        if url_data.find_one({'已合并id': item['id']}):
            print('当前id已合并')
            continue

        try:
            item['酒店星级'] = int(item['酒店星级'])
        except:
            print('酒店星级')
        try:
            item['开业时间'] = int(item['开业时间'])
        except:
            print('开业时间')
        try:
            item['房间数量'] = int(item['房间数量'])
        except:
            print('房间数量')
        print(length,item)
        # 保存数据
        info_base.insert_one(item)
        url_data.insert_one({'已合并id': item['id']})

    # 合并一个文件完成，删除 path, r'酒店详情信息/{}.csv'.format(city)
    os.remove(path)
    os.remove(r'酒店详情信息/{}.csv'.format(city))


# df3 = pd.concat(d)
# print(df3)
#df3.to_csv('酒店合并详情数据/2020-{month}_全国_酒店详细数据.csv'.format(month=month), index=False, encoding='utf-8')

