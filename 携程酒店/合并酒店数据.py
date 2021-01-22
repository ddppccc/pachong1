import os
import pandas as pd
from config import Year, Month


year = Year
month = Month

# 合并后保存位置
path1 = '酒店合并详情数据/{year}-{month}携程酒店'.format(year=year, month=month)
os.path.exists(path1) or os.makedirs(path1)

d = []
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
           '开业时间','户型详情','房间数量','酒店简介','附近']

    df2 = df2[col]

    df2.to_excel(
        '{path1}/{year}-{month}_{city}_{number}条数据.xlsx'.format(path1=path1, year=year, month=month, city=city,
                                                                number=df2.shape[0]), index=False)
    d.append(df2)

df3 = pd.concat(d)
print(df3.shape)

df3.to_csv('酒店合并详情数据/2020-{month}_全国_酒店详细数据.csv'.format(month=month), index=False, encoding='utf-8')

