# encoding=utf-8
import csv
import json
import time
import re
import os
import base64
import requests
import pandas as pd
import hashlib
from queue import Queue
from threading import Thread, Lock
from fontTools.ttLib import TTFont
from scrapy import Selector
from config import base_font
from 验证码 import TuDi
import pymongo
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
            retryWrites="false")['土地市场网招拍挂']['地块公示_数据_202107']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['土地市场网招拍挂']['地块公示_去重_202107']


# base64  转图片
def base64_img(base):
    name = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
    imgdata = base64.b64decode(base.replace("data:image/bmp;base64,", ""))
    file = open('img/{}.jpg'.format(name), 'wb')
    file.write(imgdata)
    file.close()

    r = requests.post('http://127.0.0.1:7788', data=open('img/{}.jpg'.format(name), 'rb'))
    result = json.loads(r.text)['code']
    print(result)
    return result


def get_city_province(df, region, title):
    if region in ['驻马店市', '新乡市', '中山市', '廊坊市']:
        region = '{}本级'.format(region)
    d = df.loc[df['name']==region]
    if d.shape[0] == 0: print(region, d)
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
    # return get_html(url)
    proxy, cookie = TuDi().run()
    # print(proxy,cookie)
    try:
        header = {
            "Host": "www.landchina.com",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
            "Accept": "text/css,*/*;q=0.1",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            'Cookie': cookie,
            "Referer": url,
            "Connection": "keep-alive"
        }

        response = requests.get(url, headers=header, timeout=(10, 10), proxies=proxy)
        if '验证码' in response.text or 'verifyimg' in response.text:
            response.encoding = 'gbk'
        return response
    except Exception as e:
        print('获取详情页错误')
        return get_parse_url(url)


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


def format_str(str1):
    return str1.strip().replace('\n', '').replace('\r', '').replace(' ', '').replace('\ufffd', '')


def get_font_woff(url):
    name = re.findall('styles/fonts/(.*)\.woff\?', url)[0]
    fileName = 'font/{}.woff'.format(name)

    if name in [i.split('.')[0] for i in os.listdir(r'font')]:
        pass

    else:
        while True:
            proxy, cookie = TuDi().run()
            try:
                woff_url = 'http://www.landchina.com/' + url
                header = {
                    "Host": "www.landchina.com",
                    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
                    "Accept": "text/css,*/*;q=0.1",
                    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                    "Accept-Encoding": "gzip, deflate",
                    'Cookie': cookie,
                    "Referer": woff_url,
                    "Connection": "keep-alive"
                }
                woff = requests.get(woff_url, headers=header, timeout=(2, 5), proxies=proxy)
                if '详细错误' in woff.text or '验证码不能为空' in woff.text or '网站访问认证页面' in woff.text:
                    print('字体下载error....')
                    continue

                with open(fileName, 'wb') as fp:
                    fp.write(woff.content)
                break

            except Exception as e:
                print('字体下载error: ', e)
                continue
    try:
        font = TTFont(fileName)
    except:
        return None
    return font

def getInfo():
    list = f.readline()
    l = list.split(',')
    info_url = l[-1].strip()
    date = l[2]
    region=l[0]
    return info_url,region,date


def parse(df_map):
    while True:
        # if queue.empty() == True:
        #     break
        # df = queue.get()
        # info_url = "".join(df['标题url'].tolist())
        # print("info_url: ", info_url)
        # if 'land' not in info_url:
        #     queue.task_done()
        #     continue

        info_url,region, date = getInfo()
        if has_spider.count_documents({'标题url': info_url}) == 1:
            print('该地址已抓取')
            continue
        res = get_parse_url(info_url)
        if not res or '没有相关说明信息' in res.text:
            with open('土地log/地块公示坏url.text', 'a') as fp:
                fp.write(info_url)
                fp.write('\n')
            # queue.task_done()
            print('nodata')
            continue
        res.encoding = 'gbk'


        # print('开始获取字体加密文件')
        # 获取字体加密文件
        try:
            font_url = re.findall("url\('\.\./\.\./\.\./(.*)'\) format\('woff'\),", res.text)[0]
            # print('加密文件url',font_url)
        except:
            # queue.task_done()
            print(res.text)
            print('#############')
            continue

        # print('开始获取font')
        Font = get_font_woff(font_url)
        if not Font:
            print('没有FONT')
            # queue.task_done()
            continue
        # print('FONT',Font)

        response = Selector(text=res.text)
        table = response.xpath('//*[@id="tdContent"]').extract_first()
        table_decode = decode_font(Font, table)
        table_lxml = Selector(text=table_decode)
        # 法二
        # response = decode_font(Font, res.text)
        # response = Selector(text=response)
        # response = etree.HTML(res.text)
        # table = response.xpath('//*[@id="tdContent"]')[0]
        # table_decode = decode_font(Font, table)
        # table_lxml=etree.HTML(table_decode)

        titles = table_lxml.xpath('.//text()')
        title= titles[3].get().strip()

        tables = table_lxml.xpath(".//table[@width='100%']")
        # print(tables)
        if not tables:
            with open('土地log/地块公示坏url.text', 'a') as fp:
                fp.write(info_url)
                fp.write('\n')

        for table in tables:
            item = {}
            # item['行政区'] = "".join(df['行政区'].tolist())
            item['行政区'] = region
            item['标题'] = response.xpath("//span[@id='lblTitle']/text()").get()
            city, province, region = get_city_province(df_map, item['行政区'], item['标题'])
            item['省份'] = province
            item['城市'] = city
            item['行政区'] = region
            item['公告编号'] = title
            item['成交日期'] = date
            item['标题url'] = info_url
            item['地块编号'] = (table.xpath(".//td[contains(text(), '编号')]/following-sibling::td[1]/text()").get() or '').strip() or\
                           (table.xpath(".//td[contains(text(), '地块编号')]/following-sibling::td[1]/text()").get() or '').strip()
            try:
                item['土地面积'] = table.xpath(
                ".//td[contains(text(), '土地面积(公顷)')]/following-sibling::td[1]/text()").get().strip()
            except:
                item['土地面积'] = ''
            item['地块位置'] = format_str(
                    table.xpath(".//td[contains(text(), '置')]/following-sibling::td[1]/text()").get() or '')
            item['出让年限'] = format_str(
                    table.xpath(".//td[contains(text(), '出让年限')]/following-sibling::td[1]/text()").get() or '')
            item['成交价(万元)'] = format_str(
                    table.xpath(".//td[contains(text(), '成交价(万元)')]/following-sibling::td[1]/text()").get() or '')
            item['土地用途'] = format_str(table.xpath(
                ".//td[contains(text(), '土地用途')]/following-sibling::td[1]/text()").get() or '')

            a = table.xpath(".//tr/td[1][contains(text(), '用地')]/text()").extract()
            b = table.xpath(".//tr/td[1][contains(text(), '用地')]/following-sibling::td[1]/text()").extract()
            item['明细用途'] = dict(zip(a, b))
            # print(f"明细用途: {item['明细用途']} ")
            item['受让单位'] = format_str(table.xpath(
                ".//td[contains(text(), '受让')]/following-sibling::td[1]/text()").get() or '')
            item['土地使用权限'] = format_str(table.xpath(
                ".//td[contains(text(), '土地使用条件：')]/following-sibling::td[1]/text()").get() or '')
            item['备注'] = format_str(table.xpath( ".//td[contains(text(), '备')]/following-sibling::td[1]/text()").get() or '')
            item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print(item)
            info_base.insert_one(item)
        has_spider.insert_one({'标题url': info_url})




            # # 保存数据
            # savePath = os.path.join('土地数据', '地块公示_详情.csv')
            # # 判断是否存在当前文件夹
            # if not os.path.exists(savePath):  # 不存在
            #     with open(savePath, 'a', newline='', encoding='gbk') as csvfile:
            #         writer = csv.writer(csvfile)
            #         lock = Lock()
            #         lock.acquire()
            #         writer.writerow(list(item.keys()))
            #         writer.writerow(list(item.values()))
            #         lock.release()
            # else:
            #     with open(savePath, 'a', newline='', encoding='gbk') as csvfile:
            #         writer = csv.writer(csvfile)
            #         lock = Lock()
            #         lock.acquire()
            #         writer.writerow(list(item.values()))
            #         lock.release()
        # print()
        # queue.task_done()


# def run(threadNumber, df_map):
    # with open('土地log/地块公示坏url.text', 'r') as fp:
    #     d = fp.readlines()
    # d = [i.strip() for i in d]
    #
    # f = open(r'土地数据/地块公示.csv', encoding='gbk', mode='r')
    # df = pd.read_csv(f, error_bad_lines=False)
    # f.close()
    #
    # df.rename(columns={'详情url':'标题url'}, inplace=True)
    # df = df[~df['行政区'].isin(['511603000', '511903000', '421303000','341504000', '440309000', '440310000', '330383000', '350598000'])]
    # df = df[~df['标题url'].isin(d)]
    #
    # # 这里是筛选日期
    # # df['公示日期'] = df['公示日期'].map(lambda x: '' if '20' not in x or '公示' in x else x)
    # # df['公示日期'] = pd.to_datetime(df['公示日期'])
    # # df = df.query("公示日期 > '2020-06-01'")
    # # df['公示日期'] = df['公示日期'].map(lambda x: str(x).split(' ')[0])
    #
    # print("df.shape: ", df.shape)
    # df = df.drop_duplicates(subset='标题url')
    # print("去重后: ", df.shape)
    # try:
    #     f = open(r'土地数据/地块公示_详情.txt', encoding='gbk', mode='r', errors='ignore')
    #     df1 = pd.read_csv(f, error_bad_lines=False)
    #     df2 = df1.drop(index=df1[df1['标题url'].isnull()].index)
    #     df2 = df2.drop(index=df2[df2['地块编号'].isnull()].index)
    #     # df1.drop()
    #     print('df1: ', df1.shape)
    #     f.close()
    #     df = df[~df['标题url'].isin(df2['标题url'].tolist())]
    # except Exception as e:
    #     print(e)
    #
    # print("去除已经解析后: ", df.shape)
    #
    # number = df.shape[0]
    # for i in [df.iloc[i: i + 1] for i in range(number)]:
    #     queue.put(i)
    # parse(df_map)
    # for i in range(threadNumber):
    #     t = Thread(target=parse, args=(df_map,))
    #     t.daemon = True
    #     t.start()
    # time.sleep(3)
    # queue.join()



if __name__ == '__main__':
    # df1: (288439, 16)
    # 去除已经解析后: (284652, 4) # 283754  274289
    f = open('土地数据/地块公示.csv', encoding='gbk', mode='r')
    df_map = pd.read_excel('城市_区县_映射表.xlsx')
    # queue = Queue()
    # run(1, df_map)
    parse(df_map)
    f.close()
