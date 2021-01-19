# encoding=utf-8
import csv
import json
import os
import time
import re
import random
from concurrent.futures import ThreadPoolExecutor

import requests
import pandas as pd
import hashlib
import fontTools
from queue import Queue
from threading import Thread, Lock
from fontTools.ttLib import TTFont
from scrapy import Selector
from config import base_font
from 验证码 import get_proxy,TuDi,run1
# from config import get_cookie, get_proxy, delete_proxy, stringToHex
import os, base64
import xlrd
import datetime


# base64  转图片
def base64_img(base):
    name = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
    imgdata = base64.b64decode(base.replace("data:image/bmp;base64,", ""))
    file = open('img/{}.jpg'.format(name), 'wb')
    file.write(imgdata)
    file.close()

    r = requests.post('http://192.168.88.51:7788', data=open('img/{}.jpg'.format(name), 'rb'))
    result = json.loads(r.text)['code']
    print(result)
    return result


def get_city_province(df, region, title):
    # print('region：',region)
    if region in ['漳州市','衢州市','驻马店市', '新乡市', '中山市', '廊坊市']:
        region = '{}本级'.format(region)  #加字
    d = df.loc[df['name'] == region]    # 条件查询
    # print('d:',d)
    try:
        if d.shape[0] == 0: print(region, d)
    except:
        return
    city, province = '', ''
    if d.shape[0] < 2:
        city = d.iloc[0]['city']
        province = d.iloc[0]['province']
    else:
        for i in range(d.shape[0]):
            if d.iloc[i]['city'].replace('市', '') in title:
                city = d.iloc[i]['city']
                province = d.iloc[i]['province']
    return city, province, region


# 获取详情页面
def get_parse_url(url):
    while True:
        try:
            # response = requests.get(url, headers=header, timeout=(2, 7))
            response = run1(url)
            response.encoding = 'gbk'
            # print(response.text)
            return response
        except Exception as e:
            print('详情页: ', e)
            time.sleep(2)
            continue


# 获取解析后的值
def decode_font(tFont, string_code: str):
    result = []
    for code in string_code:
        uncode = code.encode("unicode_escape")
        unicode_code = 'uni' + str(uncode).replace('b\'\\\\u', '').replace('\'', '').upper()
        try:
            content = tFont['glyf'].glyphs.get(unicode_code).data
        except:
            result.append(code)
            continue
        glyph_md5 = hashlib.md5(content).hexdigest()
        for font_hex in base_font:
            if font_hex.get('hex') == glyph_md5:
                result.append(font_hex.get('value'))
    return ''.join(result)


def get_font_woff(url):
    name = re.findall('styles/fonts/(.*)\.woff\?', url)[0]
    fileName = 'font/{}.woff'.format(name)

    if name in [i.split('.')[0] for i in os.listdir(r'font')]:
        pass

    else:
        woff_url = 'http://www.landchina.com/' + url
        header = {
            "Host": "www.landchina.com",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
            "Accept": "text/css,*/*;q=0.1",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Referer": woff_url,
            "Connection": "keep-alive"
        }
        woff = requests.get(woff_url, headers=header, timeout=(2, 5))
        with open(fileName, 'wb') as fp:
            fp.write(woff.content)
    try:
        font = TTFont(fileName)
    except:
        font = ''
    return font


def parse(df_map):
    while True:
        if queue.empty() == True:
            break
        df = queue.get()
        # res = get_parse_url("".join(df['标题url'].tolist()))
        res = get_parse_url(df['标题url'].tolist()[0])
        if not res:
            queue.task_done()
            continue

        res.encoding = 'gbk'

        # 获取字体加密文件
        try:
            font_url = re.findall("url\('\.\./\.\./\.\./(.*)'\) format\('woff'\),", res.text)[0]
        except:
            queue.task_done()
            res.encoding = 'utf-8'
            # print(res.text)
            print('#############')
            continue
        Font = get_font_woff(font_url)
        if not Font:
            queue.task_done()
            continue

        # response = Selector(text=res.text)
        # table = response.xpath('//*[@id="tdContent"]').extract_first()
        # table_decode = decode_font(Font, table)
        # table_lxml = Selector(text=table_decode)

        # 法二
        response = decode_font(Font, res.text)
        print(response)
        if '没有相关说明信息' in response:
            item = {}
            item['行政区'] = "".join(df['行政区'].tolist())
            try:
                city, province, region = get_city_province(df_map, item['行政区'], item['标题'])
            except Exception as e:
                print('出错:', e)
                continue
            item['省份'] = province
            item['城市'] = city
            item['行政区'] = region

            item['公告编号'] = title
            item['成交日期'] = "".join(df['公示日期'].tolist())
            item['标题url'] = "".join(df['标题url'].tolist())
            item['备注'] = '没有相关信息说明'
            print(item)
        response = Selector(text=response)
        table_lxml = response.xpath('//*[@id="tdContent"]')
        # print(table_lxml.xpath("//table[@width='100%']"))

        title_ = response.xpath('//*[@id="tdContent"]/table/tr[1]/td[1]/text()').extract_first()

        title = title_.strip()

        # print(res.text)
        print("title: ", title)
        print('解析title，未进table')


        for table in table_lxml.xpath(".//table[@width='95%']"):
            print('进入table解析')
            item = {}
            item['行政区'] = "".join(df['行政区'].tolist())
            # print(type(item['行政区']))
            item['标题'] = response.xpath("//span[@id='lblTitle']/text()").get()
            try:
                city, province, region = get_city_province(df_map, item['行政区'], item['标题'])
            except Exception as e:
                print('出错:',e)
                continue
            item['省份'] = province
            item['城市'] = city
            item['行政区'] = region

            item['公告编号'] = title
            item['成交日期'] = "".join(df['公示日期'].tolist())
            item['标题url'] = "".join(df['标题url'].tolist())

            item['地块编号'] = (table.xpath(
                ".//td[contains(text(), '编号')]/following-sibling::td[1]/text()").get() or '').strip() or \
                           (table.xpath(
                               ".//td[contains(text(), '地块编号')]/following-sibling::td[1]/text()").get() or '').strip()
            try:
                item['土地面积'] = table.xpath(
                    ".//td[contains(text(), '土地面积(公顷)')]/following-sibling::td[1]/text()").get().strip()
            except:
                item['土地面积'] = ''
            item['地块位置'] = (
                    table.xpath(
                        ".//td[contains(text(), '置')]/following-sibling::td[1]/text()").get() or '').strip().replace(
                '\n', '').replace('\r', '').replace(' ', '')
            item['出让年限'] = (
                    table.xpath(
                        ".//td[contains(text(), '出让年限')]/following-sibling::td[1]/text()").get() or '').strip().replace(
                '\n', '').replace('\r', '').replace(' ', '')
            item['成交价(万元)'] = (
                    table.xpath(
                        ".//td[contains(text(), '成交价(万元)')]/following-sibling::td[1]/text()").get() or '').strip().replace(
                '\n', '').replace('\r', '').replace(' ', '')
            item['土地用途'] = (table.xpath(
                ".//td[contains(text(), '土地用途')]/following-sibling::td[1]/text()").get() or '').strip().replace('\n',
                                                                                                                '').replace(
                '\r', '').replace(' ', '')
            item['受让单位'] = (table.xpath(
                ".//td[contains(text(), '受让')]/following-sibling::td[1]/text()").get() or '').strip().replace('\n',
                                                                                                              '').replace(
                '\r', '').replace(' ', '')
            item['土地使用权限'] = (table.xpath(
                ".//td[contains(text(), '土地使用条件：')]/following-sibling::td[1]/text()").get() or '').strip().replace('\n',
                                                                                                                   '').replace(
                '\r', '').replace(' ', '')
            item['备注'] = (table.xpath(
                ".//td[contains(text(), '备')]/following-sibling::td[1]/text()").get() or '').strip().replace('\n',
                                                                                                             '').replace(
                '\r', '').replace(' ', '')
            print('item:',item)

            # 保存数据
            savePath = os.path.join('土地数据', '地块公示_详情.csv')
            # 判断是否存在当前文件夹
            if not os.path.exists(savePath):  # 不存在
                with open(savePath, 'a', newline='', encoding='gbk') as csvfile:
                    writer = csv.writer(csvfile)
                    lock = Lock()
                    lock.acquire()
                    writer.writerow(list(item.keys()))
                    writer.writerow(list(item.values()))
                    lock.release()
            else:
                with open(savePath, 'a', newline='', encoding='gbk') as csvfile:
                    writer = csv.writer(csvfile)
                    lock = Lock()
                    lock.acquire()
                    writer.writerow(list(item.values()))
                    lock.release()
        print()
        queue.task_done()


def run(threadNumber, df_map):
    f = open(r'土地数据/地块公示.csv', encoding='gbk', mode='r')
    df = pd.read_csv(f, error_bad_lines=False)
    f.close()
    df.rename(columns={'详情url': '标题url'}, inplace=True)
    print("df.shape: ", df.shape)
    df = df.drop_duplicates(subset='标题url')
    print("去重后: ", df.shape)
    try:
        f = open(r'土地数据/地块公示_详情.csv', encoding='gbk', mode='r', errors='ignore')
        df1 = pd.read_csv(f, error_bad_lines=False)
        df2 = df1.drop(index=df1[df1['标题url'].isnull()].index)
        df2 = df2.drop(index=df2[df2['地块编号'].isnull()].index)
        # df1.drop()
        print('df1: ', df1.shape)
        f.close()
        df = df[~df['标题url'].isin(df2['标题url'].tolist())]
    except Exception as e:
        print(e)
        pass
    print("去除已经解析后: ", df.shape)
    print(df.columns)
    dead_time_list = ['2012/2/28']
    number = df.shape[0]
    for i in [df.iloc[i: i + 1] for i in range(number)]:
        if i['公示日期'].all() in dead_time_list: continue
        queue.put(i)

    for i in range(threadNumber):
        t = Thread(target=parse, args=(df_map,))
        t.daemon = True
        t.start()
    time.sleep(3)
    queue.join()


if __name__ == '__main__':
    # url = 'https://www.landchina.com/DesktopModule/BizframeExtendMdl/workList/bulWorkView.aspx?wmguid=20aae8dc-4a0c-4af5-aedf-cc153eb6efdf&recorderguid=JYXT_ZJGG_13473&sitePath='
    # parse(url)
    df_map = pd.read_excel('城市_区县_映射表.xlsx')
    queue = Queue()
    # threadPool = ThreadPoolExecutor(max_workers=4)
    # future = threadPool.submit(run, 1,df_map)
    # threadPool.shutdown(wait=True)
    run(1, df_map)


    # url = 'https://www.landchina.com/DesktopModule/BizframeExtendMdl/workList/bulWorkView.aspx?wmguid=4a611fc4-42b1-4231-ac26-8d25b002dc2b&recorderguid=b2de66b4-ccf1-4808-bab0-64db9f3095fa&sitePath='
    # print(get_parse_url(url).text)