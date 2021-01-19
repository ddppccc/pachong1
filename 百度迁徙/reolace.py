import pandas as pd
import datetime

item = {
    1: '01-10~02-17',
    2: '01-10~01-24',
    3: '01-25~02-17'
}

df1 = pd.read_excel('data/2020年_20200101_20200218_百度人口迁移指数.xlsx', sheet_name='迁入来源地_城市')
df2 = pd.read_excel('data/2020年_20200101_20200218_百度人口迁移指数.xlsx', sheet_name='迁入来源地_省份')
df3 = pd.read_excel('data/2020年_20200101_20200218_百度人口迁移指数.xlsx', sheet_name='迁出目的第_城市')
df4 = pd.read_excel('data/2020年_20200101_20200218_百度人口迁移指数.xlsx', sheet_name='迁出目的地_省份')

df1['时间'] = df1['时间'].map(lambda x: item[x])
df2['时间'] = df2['时间'].map(lambda x: item[x])
df3['时间'] = df3['时间'].map(lambda x: item[x])
df4['时间'] = df4['时间'].map(lambda x: item[x])
#
qianru_city_df = df1.copy()
qianru_province_df = df2.copy()
qianchu_city_df = df3.copy()
qianchu_province_df = df4.copy()


d = datetime.datetime.now().strftime('%Y%m%d')
name = 'data/2020年_{}_{}_百度人口迁移指数_综合.xlsx'.format('20200101',d)
writer = pd.ExcelWriter(name)
qianru_city_df.to_excel(writer, sheet_name='迁入来源地_城市', index=False)
qianru_province_df.to_excel(writer, sheet_name='迁入来源地_省份', index=False)
qianchu_city_df.to_excel(writer, sheet_name='迁出目的第_城市', index=False)
qianchu_province_df.to_excel(writer, sheet_name='迁出目的地_省份', index=False)
writer.save()
writer.close()

