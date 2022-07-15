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
    daaa = df[indexName].rolling(5).mean()
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
    region_df['date'] = pd.to_datetime(region_df[date], format='%Y-%m-%d')# 改时间格式
    region_df = region_df.sort_values('date')
    region_df['time'] = [x.strftime("%Y-%m-01") for x in region_df['date']].copy()

    df = region_df.pivot_table(index=['城市', 'time'],
                               values=indexName, aggfunc=np.sum).reset_index()  # 日数据 统计成月度
    df = df[~df['time'].isin(['2022-01-01'])]      #----------------------not in
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
        # data['城市'] = '全国'   #  ----------------------------------等于全国的·时候
        data['time']=i[1]
        data['index']=str(i[2])
        if data['index'] =='None':
            data['index'] =0
        # print(data)
        if data['time']  in needlist:continue         #-----------
        # if data['城市'] == '全国': continue
        ldata.append(data)
    return ldata





# def delt():
#     sql = '''select * from "public"."city_hlindex_fj" WHERE city_name = '全国' '''
#     conn = psycopg2.connect(database="zhongzi", user="postgres",
#                             password="123123", host="192.168.1.230", port="5432")
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     lists = cursor.fetchall()
#     df = pd.DataFrame(lists)
# delt()




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
    # needlist=[
    #     '2011-01-01',
    #     '2011-02-01',
    #     '2011-03-01',
    #     '2011-04-01',
    #     '2011-05-01',
    #     '2011-06-01',
    #     '2011-07-01',
    #     '2011-08-01',
    #     '2011-09-01',
    #     '2011-10-01',
    #     '2011-11-01',
    #     '2011-12-01',
    #     '2012-01-01',
    #     '2012-02-01',
    #     '2012-03-01',
    #     '2012-04-01',
    #     '2012-05-01',
    #     '2012-06-01',
    #     '2012-07-01',
    #     '2012-08-01',
    #     '2012-09-01',
    #     '2012-10-01',
    #     '2012-11-01',
    #     '2012-12-01',
    #     '2013-01-01',
    #     '2013-02-01',
    #     '2013-03-01',
    #     '2013-04-01',
    #     '2013-05-01',
    #     '2013-06-01',
    #     '2013-07-01',
    #     '2013-08-01',
    #     '2013-09-01',
    #     '2013-10-01',
    #     '2013-11-01',
    #     '2013-12-01',
    #     '2014-01-01',
    #     '2014-02-01',
    #     '2014-03-01',
    #     '2014-04-01',
    #     '2014-05-01',
    #     '2014-06-01',
    #     '2014-07-01',
    #     '2014-08-01',
    #     '2014-09-01',
    #     '2014-10-01',
    #     '2014-11-01',
    #     '2014-12-01',
    #
    #     '2015-01-01',
    #     '2015-02-01',
    #     '2015-03-01',
    #     '2015-04-01',
    #     '2015-05-01',
    #     '2015-06-01',
    #     '2015-07-01',
    #     '2015-08-01',
    #     '2015-09-01',
    #     '2015-10-01',
    #     '2015-11-01',
    #     '2015-12-01',
    #
    #     '2016-01-01',
    #     '2016-02-01',
    #     '2016-03-01',
    #     '2016-04-01',
    #     '2016-05-01',
    #     '2016-06-01',
    #     '2016-07-01',
    #     '2016-08-01',
    #     '2016-09-01',
    #     '2016-10-01',
    #     '2016-11-01',
    #     '2016-12-01',
    #
    #     '2017-01-01',
    #     '2017-02-01',
    #     '2017-03-01',
    #     '2017-04-01',
    #     '2017-05-01',
    #     '2017-06-01',
    #     '2017-07-01',
    #     '2017-08-01',
    #     '2017-09-01',
    #     '2017-10-01',
    #     '2017-11-01',
    #     '2017-12-01',
    #
    #     '2018-01-01',
    #     '2018-02-01',
    #     '2018-03-01',
    #     '2018-04-01',
    #     '2018-05-01',
    #     '2018-06-01',
    #     '2018-07-01',
    #     '2018-08-01',
    #     '2018-09-01',
    #     '2018-10-01',
    #     '2018-11-01',
    #     '2018-12-01',
    #
    #     '2019-01-01',
    #     '2019-02-01',
    #     '2019-03-01',
    #     '2019-04-01',
    #     '2019-05-01',
    #     '2019-06-01',
    #     '2019-07-01',
    #     '2019-08-01',
    #     '2019-09-01',
    #     '2019-10-01',
    #     '2019-11-01',
    #     '2019-12-01',
    #
    #     '2020-01-01',
    #     '2020-02-01',
    #     '2020-03-01',
    #     '2020-04-01',
    #     '2020-05-01',
    #     '2020-06-01',
    #     '2020-07-01',
    #     '2020-08-01',
    #     '2020-09-01',
    #     '2020-10-01',
    #     '2020-11-01',
    #     '2020-12-01',
    #
    #     '2021-01-01',
    #     '2021-02-01',
    #     '2021-03-01',    #     '2021-04-01',
    #     '2021-05-01',
    #     '2021-06-01',
    #     '2021-07-01',
    #     '2021-08-01',
    #     '2021-09-01',
    #     '2021-10-01',
    #     '2021-11-01',
    #     '2021-12-01',
    #     '2022-01-01',
    #     '2022-02-01',
    #     '2022-03-01',
    #     '2021-01-01',
    #     '2021-02-01',
    #     '2021-03-01',
    #     '2021-04-01',
    #     '2021-05-01',
    #     '2021-06-01',
    #     '2021-07-01',
    #     '2021-08-01',
    #     '2021-09-01',
    #     '2021-10-01',
    #     '2021-11-01',
    #     '2021-12-01',
    #     '2022-01-01',
    #     '2022-02-01',
    #     '2022-03-01',
    # ]
    needlist = [
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
            '2022-01-01',
            '2022-02-01',
            '2022-03-01',
                '2022-04-01',
                ] #
    flag=False
    df=pd.read_csv('05百度指数_new.csv')              #-----------------------------'百度指数_new.csv
    for keys_df in df.groupby('keys'):
        # if keys_df[0] not in ['买房', '卖房']:
        #     continue  #-----------------默认为 in 跑城市
        # if keys_df[0] != '卖房':continue
        print('当前', keys_df[0])
        tablename=tabledict[keys_df[0]].get('table')
        head=tabledict[keys_df[0]].get('head')
        df_=pd.DataFrame(getlastdata())

        # keys_df[1]['城市'] = '全国'         #----------------------------------等于全国的·时候
        df=day2month(keys_df[1])

        #
        #
        # print('df:\n',df)
        # print('df_:\n',df_)

        df = pd.concat([df, df_], axis=0, ignore_index=True)


        # df = boll(df, head)#--------------------------------------------------------------------------------------------
        # df = df[df['city_name'] == '全国']
        # #
        # #
        # # 入库
        # savedata(df, tablename)#----------------------------------------------------
        # # 入csv
        # df.to_csv(f'e:/入库/{tablename}.csv', index=False)
        # print(df)


        for city_df in df.groupby('城市'):    #===============================城市分类的时候
            # if city_df[0] != '深圳':continue
            # if city_df[0] == '石河子':
            #     flag=True
            #     continue
            # if not flag:continue
            df=boll(city_df[1],head)
            # 入库
            # savedata(df,tablename)
        #     print('1')
            df.to_csv(f'e:/入库/{tablename}.csv', index=False)

