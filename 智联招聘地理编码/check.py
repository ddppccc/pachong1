import json

import requests
import base64
import os
import pandas as pd
import csv
from datetime import datetime

os.chdir("D:\Project\智联招聘地理编码")


# 读取文件
def read_file_path(yuan_path, bian_path):
    df = pd.read_excel(yuan_path,  usecols=['city','number','positionURL'])
    # df = pd.read_csv(yuan_path,  usecols=['city','number','positionURL'])
    # 去除没有链接的row
    df = df[df['positionURL'].notnull()]
    df.drop_duplicates('number','first', inplace=True)
    index = df[df['positionURL']=='http://jobs.zhaopin.com/CC862610360J00380255002.htm'].index
    print('删除 为空的index: ', index)
    df.drop(index=index, inplace=True)

    try:
        f = open(bian_path, 'rb')
        df_bian = pd.read_csv(f, usecols=["招聘人数","地址","number"])
        f.close()
    except Exception as e:
        # df_bian = pd.DataFrame()
        print("当前文件不存在: ", e)
        return df

    # 去除已经抓取过得number
    df_bian = df_bian[df_bian['招聘人数'].notnull()]
    df = df[~ df["number"].isin(df_bian['number'])]
    df["index"] = range(df.shape[0])
    df = df.set_index("index")
    return df


# 保存文件
def save_data(save_path, city):

    file_prefix = os.path.join(save_path, '{}_{}_'.format(datetime.now().strftime('%y-%m-%d'), city))
    save_filepath = ''.join([file_prefix, '{}.csv'.format("地理编码")])


    os.path.exists(save_path) or os.mkdir(save_path)
    today = datetime.now()
    file_name = "{}-{}-{}_{}_编码.csv".format(today.year, today.month, today.day, city)
    save_path = os.path.join(save_path, file_name)


    with open(save_path, 'a', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['招聘人数', '岗位描述', 'longitude', 'latitude', '地址', '城市', 'number', 'url'])



if __name__ == '__main__':

    # bian_path = "D:/Project/智联招聘地理编码/data/19-07-24_佛山.csv"
    # f = open(bian_path, 'rb')
    # df_bian = pd.read_csv(f, usecols=["招聘人数", "地址", "number"])
    # f.close()
    # print(df_bian.head())

    url = "http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=0c2bbe2a64db4931a27168a3f4ed2b6d&orderno=YZ2019867158hM09b7&returnType=2&count=2"
    html = requests.get(url).json()
    print(html)
    if html["ERRORCODE"] in ["10036","10038","10055"]:
        print("提取过快,请至少5秒提取一次")
    if html["ERRORCODE"] == "10032":
        print("今日提取已达上限")
    for i in html["RESULT"]:
        ip = i['ip'] + ":" + i['port']
        print(ip)
