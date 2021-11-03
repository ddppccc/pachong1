import re
import time
import requests
import pymongo
# import random

from lxml import etree
from config import get_proxy, get_ua, delete_proxy, statis_output
from urllib import parse
from concurrent.futures import ThreadPoolExecutor

MONGODB_CONFIG = {
    "host": "8.135.119.198",
    "port": "27017",
    "user": "hladmin",
    "password": parse.quote("Hlxkd3,dk3*3@"),
    "db": "dianping",
    "collections": "dianping_collections",
}

# 建立连接
info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['安居客小区shen']['数据_202111']
# info_base = pymongo.MongoClient('127.0.0.1',27017)['sy']['安居客小区']
# has_spider = pymongo.MongoClient('127.0.0.1',27017)['sy']['安居客小区url']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['安居客小区shen']['url_202111']

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-user": "?1",
    'Connection': 'close',
    # "Host": "www.anjuke.com",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}


def getCity_Url():
    response = requests.get('https://www.anjuke.com/sy-city.html', headers=headers, timeout=(5, 5))
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)
    lists = html.xpath('/html/body/div[3]/div/div[2]/ul/li/div/a')
    city_url = {}
    for data in lists:
        city = data.xpath('./text()')[0]
        url = data.xpath('./@href')[0]
        city_url[city] = url
    return city_url


def get_html(url, proxieslist):
    s = 0
    while True:
        try:
            if len(proxieslist) > 0:
                proxies = proxieslist
            else:
                proxy = get_proxy()
                proxies = {"https": proxy}
            response = requests.get(url, headers=headers, proxies=proxies, timeout=(5, 10))
            encod = response.apparent_encoding
            if encod.upper() in ['GB2312', 'WINDOWS-1254']:
                encod = 'gbk'
            response.encoding = encod
            if '人机认证' in response.text:
                proxieslist = []
                continue
            html = etree.HTML(response.text)
            if '登录' in ''.join(html.xpath('//head/title/text()')):
                proxieslist = []
                continue
            if '访问验证-安居客' in ''.join(html.xpath('//head/title/text()')):
                proxieslist = []
                continue
            if "访问过于频繁" in "".join(html.xpath("//h2[@class='item']/text()")):
                proxieslist = []
                continue
            if '点击去完成' in "".join(html.xpath('//div[@class="verify-button"]//text()')):
                proxieslist = []
                continue

            if response.status_code in [403]:
                continue
            if '小区大全' in ''.join(html.xpath('//head/title/text()')):
                proxieslist = proxies
                print(s, proxieslist, '获取成功')
                return html, proxieslist
        except Exception as e:
            s += 1
            proxieslist = []

            # print('get_html错误', e)
            continue




# def get_html(url):
#     for i in range(10):
#         proxies = {"https": get_proxy()}
#         try:
#             response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
#             encod = response.apparent_encoding
#             if encod.upper() in ['GB2312', 'WINDOWS-1254']:
#                 encod = 'gbk'
#             response.encoding = encod
#             html = etree.HTML(response.text)
#             print('获取成功')
#             return html, response, proxies['https']
#         except Exception as e:
#             print('get_html错误', proxies, e)
#             time.sleep(2)
#
#     return


def get_parseInfo(city, url, area_name, proxieslist):
    if has_spider.count({'url': url}):
        print('当前url已爬取', url)
        return proxieslist
    print('当前url', url)
    count = 0
    while 1:
        count += 1
        html, proxieslist = get_html(url, proxieslist)
        if html == '':
            continue
        total_num = html.xpath('string(//span[@class="total-info"])')
        if total_num:
            break
        elif count == 10:
            return proxieslist
        else:
            continue

    house_div = html.xpath("//a[@class='li-row']")
    if len(house_div) == 0:
        return proxieslist
    for house in house_div:
        item = {}
        item['city_name'] = city
        item['标题'] = house.xpath(
            'string(./div[@class="li-info"]/div[@class="li-title"]/div[@class="nowrap-min li-community-title"])')
        item['详情url'] = house.xpath('string(@href)')
        check_map = house.xpath('string(./div[@class="li-info"]/div[@class="detail nowrap-max"]/span[3]/a/@href)')
        try:
            item['latitude'] = re.search('l1=(.*?)&', check_map).group(1)
            item['longitude'] = re.search('l2=(.*?)&', check_map).group(1)
        except:
            item['latitude'] = ''
            item['longitude'] = check_map
        try:
            item['竣工时间'] = re.search('\d+', house.xpath(
                'string(./div[@class="li-info"]/div[@class="props nowrap"]/span[@class="year"])')).group()
        except:
            item['竣工时间'] = house.xpath('string(./div[@class="li-info"]/p[@class="props nowrap"]/span[@class="year"])')
        item['地址'] = house.xpath(
            'string(./div[@class="li-info"]/div[@class="props nowrap"]/span["year"]/following-sibling::span/following-sibling::span)').replace(
            ' - ', '-')
        try:
            item['二手房上架数'] = re.search('\d+', house.xpath(
                'string(./div[@class="li-info"]/div[@class="detail nowrap-max"]/span[1])')).group()
        except:
            item['二手房上架数'] = house.xpath('string(./div[@class="li-info"]/div[@class="detail nowrap-max"]/span[1])')
        try:
            item['在租套数'] = re.search('\d+', house.xpath(
                'string(./div[@class="li-info"]/div[@class="detail nowrap-max"]/span[2])')).group()
        except:
            item['在租套数'] = house.xpath('string(./div[@class="li-info"]/div[@class="detail nowrap-max"]/span[2])')
        item['价格'] = house.xpath('string(./div[@class="li-side"]/div[@class="community-price"]/strong)')
        perpare = house.xpath('string(./div[@class="li-side"]/span)').strip().replace('\n', '')
        sign = house.xpath('string(./div[@class="li-side"]/span/@class)')
        if 'red' in sign:
            item['涨跌幅'] = '+' + perpare
        elif 'green' in sign:
            item['涨跌幅'] = '-' + perpare
        print(item)
        item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        info_base.insert_one(item)
    # 存入数据
    has_spider.insert_one({'url': url})
    time.sleep(5)

    next_page_url = ''.join(html.xpath('//div[@class="pagination page-bar"]/a[@class="next next-active"]/@href'))
    if next_page_url:
        proxieslist = get_parseInfo(city, next_page_url, area_name, proxieslist)
    else:
        print('最后一页')
        return proxieslist


if __name__ == '__main__':
    proxieslist = []
    pool = ThreadPoolExecutor(15)
    city_url = getCity_Url()
    for key, url in city_url.items():
        print(key, url)
        if has_spider.count({key: '正在爬取'}):
            print('正在爬取或已爬取')
            continue
        elif has_spider.count({key: '已爬取'}):
            print('正在爬取或已爬取')
            continue
        has_spider.insert_one({key: '正在爬取'})

        html, proxieslist = get_html(url + "/community", proxieslist)
        if html == '':
            continue
        area = html.xpath('//ul[@class="region-parents"]/li')[1:]
        if area == []:
            continue
        for area_else in area:
            l = []
            url1 = area_else.xpath('string(./a/@href)')
            area_name = area_else.xpath('string(./a)')

            # 增加判断长度 1250
            html1, proxieslist = get_html(url1, proxieslist)
            if html1 == '':
                continue
            text = ''.join(html1.xpath('//div[@class="sort-row"]/span/text()'))
            try:
                length = int(''.join(re.findall('(\d+)', text)))
            except:
                length = 0
            if length >= 1250:
                hlist = html1.xpath('//div[@class="filter-wrap"][1]//ul[@class="line"]/li/a/@href')[1:]
                for url2 in hlist:
                    html2, proxieslist = get_html(url2, proxieslist)
                    if html2 == '':
                        continue
                    text2 = ''.join(html2.xpath('//div[@class="sort-row"]/span/text()'))
                    try:
                        length2 = int(''.join(re.findall('(\d+)', text2)))
                    except:
                        length2 = 0
                    if length2 >= 1250:
                        hlist2 = html2.xpath('//div[@class="filter-wrap"][2]//ul[@class="line"]/li/a/@href')[1:]
                        for url3 in hlist2:
                            html3, proxieslist = get_html(url3, proxieslist)
                            if html3 == '':
                                continue
                            text3 = ''.join(html3.xpath('//div[@class="sort-row"]/span/text()'))
                            try:
                                length3 = int(''.join(re.findall('(\d+)', text3)))
                            except:
                                length3 = 0
                            if length3 >= 1250:
                                hlist3 = html3.xpath('//div[@class="filter-wrap filter-region"]//div[@class="region-childs"]/li/a/@href')[1:]
                                for url4 in hlist3:
                                    done = pool.submit(get_parseInfo, key, url4, area_name, proxieslist)
                                    l.append(done)
                            else:
                                done = pool.submit(get_parseInfo, key, url3, area_name, proxieslist)
                                l.append(done)
                    else:
                        done = pool.submit(get_parseInfo, key, url2, area_name, proxieslist)
                        l.append(done)
            else:
                done = pool.submit(get_parseInfo, key, url1, area_name, proxieslist)
                l.append(done)
            print(len(l))
            proxieslist = [obj.result() for obj in l][-1]
        has_spider.insert_one({key: '已爬取'})
    print('爬取完成')
    input()
