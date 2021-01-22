import csv

import pandas as pd
import sqlite3
a = ''
with sqlite3.connect('__cached__/房天下_新房_没有经纬度_data_cache.sqlite3') as con:
    c = con.cursor()
    # c.execute('''CREATE TABLE test_table
    # (date text, city text, value real)''')
    # for table in c.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    #     print("Table", table[0])
    # c.execute('''INSERT INTO test_table VALUES
    # ('2017-6-25', 'bj', 100)''')
    # c.execute('''INSERT INTO test_table VALUES
    # ('2017-6-25', 'pydataroad', 150)''')
    c.execute("SELECT * FROM 'GD'")
    a = c.fetchall()
# print(type(a))
# df = pd.DataFrame(a)
# print(df.head())
# print(df.columns)
# df.to_csv('房天下_新房_编码.csv', index=False)
li = ['城市', '区县', '标题', '标题url', '地址', '描述', '价格', '标签', '评论数量', '抓取时间',
       '抓取月份', '数据来源', 'id', '销售状态', '开盘时间', '主力户型', '占地面积', '建筑面积', '容积率',
       '绿化率', '停车位', '楼栋总数', '总户数', '物业费', '楼层状况', '城市|区县|地址','province_gd','city_gd',
      'district_gd','street_gd','level_gd','formatted_address','lon_gd','lat_gd']
with open('data/房天下_新房.csv',mode='a', newline='', encoding='utf-8-sig') as fp:
    writer = csv.writer(fp)

    writer.writerow(li)
    for j in a:
        print(j)
        writer.writerow(j)


