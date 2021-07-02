import csv
import pandas as pd

import os
import time
import re
import requests
import hashlib
from 验证码 import get_proxy, TuDi, run1
from fontTools.ttLib import TTFont
from scrapy import Selector
from config import base_font
from concurrent.futures import ThreadPoolExecutor

from queue import Queue
from threading import Thread, Lock
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
            retryWrites="false")['土地市场网招拍挂']['出让公告_数据_202107']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['土地市场网招拍挂']['出让公告_去重_202107']


# 获取详情页面
def get_parse_url(url):
    while True:
        try:
            response = run1(url)
            if 'verifyimg' in response.text:
                continue
            if '没有相关说明信息' in response.text:
                return '没有相关说明信息'
            return response
        except Exception as e:
            print('详情页: ', e, url)
            time.sleep(3)
            # response.encoding = 'utf-8'
            # return response
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
        woff = requests.get(woff_url, headers=header, timeout=(3, 10))
        with open(fileName, 'wb') as fp:
            fp.write(woff.content)
    try:
        font = TTFont(fileName)
    except:
        font = ''
    return font


def parse_info(data):
    url=data['标题url']
    if has_spider.count_documents({'标题url': url}) == 1:
        print('该地址已抓取')
        return
    global Font
    # global response
    while 1:
        try:
            response = get_parse_url(url)
            if response == '没有相关说明信息':
                return
            font_url = re.findall("url\('\.\./\.\./\.\./(.*)'\) format\('woff'\),", response.text)[0]
            Font = get_font_woff(font_url)
            break
        except:
            # print('字体url:', font_url)
            continue
    if re.search('没有相关说明信息.', response.text):
        print('该url没有信息')
        # print(response.text)
        return
    if re.search('未找到', response.text):
        print('该url没有信息')
            # print(response.text)
        return
        # time.sleep(100)
    # print(response.text)
    response = Selector(text=response.text)
    # title_ex = response.xpath('//*[@id="tdContent"]/table/tr[1]/td[1]').extract_first()
    # title_descde = decode_font(Font, title_ex)
    # title = Selector(text=title_descde).xpath('//td/text()').get()
    # print(title)
    #
    # 0
    table = response.xpath('//*[@id="tdContent"]').extract_first()
    table_decode = decode_font(Font, table)
    table_lxml = Selector(text=table_decode)

    # 法2
    # response = decode_font(tFont=Font, string_code=response.text)
    # response = Selector(text=response)
    # table_lxml = response.xpath('//*[@id="tdContent"]')
    #
    title = response.xpath('//*[@id="tdContent"]/table/tr[1]/td[1]/text()').get()
    title = decode_font(Font,title)
    for div in table_lxml.xpath("//div[@style=' font-size:12px;']"):
        try:
            t = re.findall("\((.*)\)", title)
        except:
            continue
        item = {}
        item['行政区'] = data['region']
        item['标题'] = data['title']
        item['省份'] = data['省市']
        item['城市'] = data['城市']
        item['日期'] = data['时间']
        item['公告编号'] = "".join(t) if len(t) < 2 else t[1]
        # print("item['公告编号']: ",item['公告编号'])
        item['宗地编号'] = str((
                                   div.xpath(
                                       ".//td[contains(text(), '宗地编号：')]/following-sibling::td[1]/text()").get() or '').strip())
        item['宗地总面积'] = (div.xpath(
            ".//td[contains(text(), '宗地总面积：')]/following-sibling::td[1]/text()").get() or div.xpath(
            ".//td[contains(text(), '宗地面积：')]/following-sibling::td[1]/text()").get() or '').strip()
        item['宗地坐落'] = (
                div.xpath(".//td[contains(text(), '宗地坐落：')]/following-sibling::td[1]/text()").get() or '').strip()
        item['出让年限'] = (
                div.xpath(".//td[contains(text(), '出让年限：')]/following-sibling::td[1]/text()").get() or '').strip()
        item['容积率'] = (
                div.xpath(".//td[contains(text(), '容积率：')]/following-sibling::td[1]/text()").get() or '').strip()
        item['建筑密度(%)'] = (div.xpath(
            ".//td[contains(text(), '建筑密度(%)：')]/following-sibling::td[1]/text()").get() or '').strip()
        item['绿化率(%)'] = (div.xpath(
            ".//td[contains(text(), '绿化率(%)：')]/following-sibling::td[1]/text()").get() or '').strip()
        item['建筑限高(米)'] = (div.xpath(
            ".//td[contains(text(), '建筑限高(米)：')]/following-sibling::td[1]/text()").get() or '').strip()
        item['主要用途'] = (div.xpath(
            ".//td[@colspan='6' and contains(text(), '途：')]/../following-sibling::tr[1]/td/text()").get() or div.xpath(
            ".//td[contains(text(), '途：')]/following-sibling::td/text()").get() or '').strip()
        item['面积'] = (div.xpath(
            ".//td[@colspan='3' and contains(text(), '面积')]/../following-sibling::tr[1]/td[2]/text()").get() or '').strip()
        item['起始价'] = (
                div.xpath(".//td[contains(text(), '起始价：')]/following-sibling::td[1]/text()").get() or '').strip()
        item['加价幅度'] = (
                div.xpath(".//td[contains(text(), '加价幅度：')]/following-sibling::td[1]/text()").get() or '').strip()
        item['挂牌开始时间'] = (div.xpath(
            ".//td[contains(text(), '挂牌开始时间：')]/following-sibling::td[1]/text()").get() or '').strip()
        item['挂牌截止时间'] = (div.xpath(
            ".//td[contains(text(), '挂牌截止时间：')]/following-sibling::td[1]/text()").get() or '').strip()
        item['投资强度'] = (
                div.xpath(".//td[contains(text(), '投资强度：')]/following-sibling::td[1]/text()").get() or '').strip()
        item['保证金'] = (
                div.xpath(".//td[contains(text(), '保证金：')]/following-sibling::td[1]/text()").get() or '').strip()
        item['估价报告备案号'] = (div.xpath(
            ".//tr[9]/td[6]/text()").get() or '').strip()
        item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # item['url']=url
        print(item)
        info_base.insert_one(item)
    has_spider.insert_one({'标题url': url})

        # # yield item
        # # 保存数据
        # savePath = os.path.join('土地数据', '出让公告_详情.csv')
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
        # # queue.task_done()

def getInfo():
    data={}
    try:
        list = f.readline()
        l = list.split(',')
        data['region']=l[0]
        data['title']=l[1]
        data['省市']=l[2]
        data['城市']=l[3]
        data['类型']=l[4]
        data['时间']=l[5]
        data['标题url']=l[6]
        # print(data)
    except:
        return  None
    return data
if __name__ == '__main__':
    f = open(r'土地数据/出让公告.csv', encoding='gbk', mode='r')
    while True:
        data = getInfo()
        if not data:
            continue
        parse_info(data)
    f.close()
    # df = pd.read_csv(f, error_bad_lines=False,index_col='标题url')
    # # 这里是筛选日期
    #
    # df['公示日期'] = df['公示日期'].map(lambda x: '' if '20' not in x or '公示' in x else x)
    # df['公示日期'] = pd.to_datetime(df['公示日期'])
    # df = df.query("公示日期 > '2020-08-01'")
    # df['公示日期'] = df['公示日期'].map(lambda x: str(x).split(' ')[0])
    # f.close()
    # print(df.head(5))
    # threadPool = ThreadPoolExecutor(max_workers=8)
    # p = []
    # try:
    #     f = open(r'土地数据/出让公告_详情.csv',encoding='gbk',mode='r')
    #     df2 = pd.read_csv(f,error_bad_lines=False)
    #     f.close()
    #     has_spider_list = df2['标题url'].tolist()
    # except:
    #     has_spider_list = []

    # for url in df.index:
    #     if url in has_spider_list:
    #         continue
    #     try:
    #         item = {}
    #         item['标题url'] = url
    #         item['行政区'] = df.loc[[url]]['行政区'][0]
    #         item['供应标题'] = df.loc[[url]]['供应标题'][0]
    #         item['省份'] = df.loc[[url]]['省份'][0]
    #         item['城市'] = df.loc[[url]]['城市'][0]
    #         item['公告类型'] = df.loc[[url]]['公告类型'][0]
    #         item['发布时间'] = df.loc[[url]]['公示日期'][0]

        #     # print(url)
        #     parse_info(url,item)
        #     # future = threadPool.submit(parse_info, item['标题url'],item)
        #     # p.append(future)
        # except:
        #     continue
    #
    # [i.result() for i in p]
    #
    # threadPool.shutdown()

