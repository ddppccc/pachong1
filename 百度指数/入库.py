# encoding=utf8
import json
import re
import psycopg2
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

def boll(df,head, date='date', indexName='index'):
    df=df.sort_values('time')
    df[indexName] = df[indexName].interpolate(limit_area='inside')
    df['布林中轨'] = df[indexName].rolling(19).mean()
    df['std'] = df[indexName].rolling(19).std()
    df['布林上轨'] = df['布林中轨'] + df['std'] * 2
    df['布林下轨'] = df['布林中轨'] - df['std'] * 2
    df = df.rename(columns={indexName: head, '布林中轨': 'blzg', '布林上轨': 'blsg', '布林下轨': 'blxg','城市':'city_name'})
    df=df[['city_name', 'time', head, 'blzg', 'blsg', 'blxg']]
    df = df[df['time'].isin(needlist)]
    print(df)
    return df

def savedata(df,tablename):
    engine = create_engine('postgresql+psycopg2://postgres:123123@192.168.1.230:5432/zhongzi')
    con = engine.connect()
    pd.set_option('expand_frame_repr', False)
    df.to_sql(name=tablename, con=con, if_exists='append',index=False)
    con.close()

def day2month(region_df,date='date',indexName='index'):
    region_df = region_df[~region_df['type'].isin(['pc','wise'])]
    region_df['date'] = pd.to_datetime(region_df[date], format='%Y-%m-%d')
    region_df = region_df.sort_values('date')
    region_df['time'] = [x.strftime("%Y-%m-01") for x in region_df['date']].copy()

    df = region_df.pivot_table(index=['城市', 'time'], values=indexName,
                               aggfunc=np.sum).reset_index()  # 日数据 统计成月度
    df = df[~df['time'].isin(['2022-01-01'])]
    return df

def getlastdata():
    sql_str = f'''SELECT city_name,time,mf FROM "public"."city_hlindex_buyf"  WHERE "time" >= '2018-01-01';'''
    conn = psycopg2.connect(database="zhongzi", user="postgres",
                                password="123123", host="192.168.1.230", port="5432")
    cursor = conn.cursor()
    cursor.execute(sql_str)
    head=['id','city_x','city_y','月薪_k','招聘人数','x','y','type','industry_all','size','industry','workingexp','month','year']
    data_list = cursor.fetchall()
    # print(data_list)
    ldata=[]
    for i in data_list:
        data={}
        data['城市']=i[0]
        data['time']=i[1]
        data['index']=str(i[2])
        if data['index'] =='None':
            data['index'] =0
        # print(data)
        if data['time'] in needlist:continue
        ldata.append(data)
    return ldata
tabledict={
    '买房':{
        'table':'city_hlindex_buyf',
        'head':'mf',
    },
    '房价':{
        'table':'city_hlindex_fj',
        'head':'fj',
    },
    '股票':{
        'table':'city_hlindex_gp',
        'head':'gp',
    },
    '卖房':{
        'table':'city_hlindex_mf',
        'head':'mf',
    },
    '失业金':{
        'table':'city_hlindex_syj',
        'head':'syj',
    },
    '租房':{
        'table':'city_hlindex_zf',
        'head':'zf',
    },
    '招工':{
        'table':'city_hlindex_zg',
        'head':'zg',
    },
    '招聘':{
        'table':'city_hlindex_zp',
        'head':'zp',
    },
}
if __name__ == '__main__':
    needlist=[
        '2021-01-01',
        '2021-02-01',
        '2021-03-01',
        '2021-04-01',
        '2021-05-01',
        '2021-06-01',
        '2021-07-01',
        '2021-08-01',
        '2021-09-01',
        '2021-10-01',
        '2021-11-01',
        '2021-12-01',
    ]
    flag=False
    df=pd.read_csv('百度指数_new.csv')
    for keys_df in df.groupby('keys'):
        if keys_df[0] in ['买房','卖房']:continue
        # if keys_df[0] != '卖房':continue
        tablename=tabledict[keys_df[0]].get('table')
        head=tabledict[keys_df[0]].get('head')
        df_=pd.DataFrame(getlastdata())
        df=day2month(keys_df[1])
        df = pd.concat([df,df_ ], axis=0, ignore_index=True)
        for city_df in df.groupby('城市'):
            # if city_df[0] != '深圳':continue
            # if city_df[0] == '石河子':
            #     flag=True
            #     continue
            # if not flag:continue
            df=boll(city_df[1],head)
            savedata(df,tablename)

