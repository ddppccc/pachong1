import re
import time
import requests
import pymongo
import random

from lxml import etree
from config import get_proxy,get_ua,delete_proxy,statis_output
from capter_verify.captcha_run import AJK_Slide_Captcha
from zujin_descde import decode_zujin,get_font
from urllib import parse



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
            retryWrites="false")['安居客小区shen']['info']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['安居客小区shen']['has_spider']


# city_map = {
#     '郑州':'https://zhengzhou.anjuke.com/community/p1/',
#     '长春':'https://cc.anjuke.com/community/p1/',
#     '漳州':'https://zhangzhou.anjuke.com/community/p1/',
#     '乌鲁木齐':'https://wulumuqi.anjuke.com/community/p1/',
#     '沈阳':'https://sy.anjuke.com/community/p1/',
#     '哈尔滨':'https://heb.anjuke.com/community/p1/',
#     '大连':'https://dalian.anjuke.com/community/p1/',
#     '杭州':'https://hangzhou.anjuke.com/community/p1/',
# }



headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    'Connection': 'close',
    "referer": "https://www.anjuke.com/sy-city.html",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}
def getCity_Url():
    response = requests.get('https://www.anjuke.com/sy-city.html', headers=headers, timeout=(5, 5))
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)
    lists=html.xpath('/html/body/div[3]/div/div[2]/ul/li/div/a')
    city_url={}
    for data in lists:
        city=data.xpath('./text()')[0]
        url=data.xpath('./@href')[0]
        city_url[city]=url
    return city_url

def get_html(url):
    ip_number = 100
    while ip_number > 0:
        proxy = get_proxy()
        # if not proxy:
        #     print("没有ip, 等待2分钟")
        #     time.sleep(120)

        number = 3
        while number > 0:
            headers['user-agent'] = get_ua()
            try:
                response = requests.get(url, headers=headers,
                                        proxies={"https": "https://{}".format(proxy)}, timeout=(2, 5))
                # response = requests.get(url, headers=headers, timeout=(2, 5))
                response.encoding = 'utf-8'
                html = etree.HTML(response.text)
            except requests.exceptions.ProxyError:
                number = -1
                continue
            except requests.exceptions.ConnectionError:
                number = -1
                continue
            except Exception as  e:
                print("出错, 正在进行第%s尝试, ip: %s, %s" % (number, proxy, type(e)))
                number -= 1
                continue

            # 检查是否出现 58滑动验证
            if html.xpath("//div[@class='pop']/p[@class='title']"):
                print("出现滑动验证, 更改ip")
                number = -1
                continue

            # 安居客滑动验证, js破解
            if html.xpath('//*[@id="captchaForm"]'):
                # print("出现滑动验证, 更改ip")
                # number = -1
                # continue

                try:
                    proixy = "https://" + proxy
                    message = AJK_Slide_Captcha(proixy).run()
                    if message != '校验成功':
                        break
                except Exception as e:
                    print("错误原因: ", e)
                    continue

            # ip被封
            if "访问过于频繁" in "".join(html.xpath("//h2[@class='item']/text()")):
                print(proxy, "ip被封")
                number = -1
                continue

            if response.status_code in [403]:
                print(403, "休息一分钟")
                time.sleep(60)
                continue
            return html, response, proxy

        # 出错3次, 删除代理池中代理
        delete_proxy(proxy)
        ip_number -= 1
        continue
    print("全部出处")
    return '', '', ''
# def get_html(url):
#     proxies = {"https": get_proxy()}
#     try:
#         response = requests.get(url, headers=headers,timeout=10)
#         encod = response.apparent_encoding
#         if encod.upper() in ['GB2312', 'WINDOWS-1254']:
#             encod = 'gbk'
#         response.encoding = encod
#         html = etree.HTML(response.text)
#         return html,response,''
#     except Exception as e:
#         print('get_html错误',proxies, e)
#         time.sleep(2)
#         return get_html(url)


def get_parseInfo(city,url,area_name):
    print('当前url',url)
    # has_spider_list = has_spider.find()
    if has_spider.find_one({'url':url}):#################
        return

    # 判断是否最后一页
    count = 0
    while 1:
        count += 1
        html, response, _ = get_html(url)
        total_num = html.xpath('string(//span[@class="total-info"])')
        if total_num:
            break
        elif count == 3:
            return
        else:
            print('暂无数据，无法判断，暂停10s')
            time.sleep(10)
            continue

    house_div = html.xpath("//a[@class='li-row']")
    if len(house_div) == 0:
        return
    for house in house_div:
        item = {}
        item['city_name'] = city
        item['标题'] = house.xpath('string(./div[@class="li-info"]/div[@class="li-title"]/div[@class="nowrap-min li-community-title"])')
        item['详情url'] = house.xpath('string(@href)')
        check_map = house.xpath('string(./div[@class="li-info"]/div[@class="detail nowrap-max"]/span[3]/a/@href)')
        try:
            item['latitude'] = re.search('l1=(.*?)&',check_map).group(1)
            item['longitude'] = re.search('l2=(.*?)&',check_map).group(1)
        except:
            item['latitude'] = ''
            item['longitude'] = check_map
        try:
            item['竣工时间'] = re.search('\d+', house.xpath('string(./div[@class="li-info"]/div[@class="props nowrap"]/span[@class="year"])')).group()
        except:
            item['竣工时间'] = house.xpath('string(./div[@class="li-info"]/p[@class="props nowrap"]/span[@class="year"])')
        item['地址'] = house.xpath('string(./div[@class="li-info"]/div[@class="props nowrap"]/span["year"]/following-sibling::span/following-sibling::span)').replace(' - ', '-')
        try:
            item['二手房上架数'] = re.search('\d+',house.xpath('string(./div[@class="li-info"]/div[@class="detail nowrap-max"]/span[1])')).group()
        except:
            item['二手房上架数'] = house.xpath('string(./div[@class="li-info"]/div[@class="detail nowrap-max"]/span[1])')
        try:
            item['在租套数'] = re.search('\d+',house.xpath('string(./div[@class="li-info"]/div[@class="detail nowrap-max"]/span[2])')).group()
        except:
            item['在租套数'] = house.xpath('string(./div[@class="li-info"]/div[@class="detail nowrap-max"]/span[2])')
        item['价格'] = house.xpath('string(./div[@class="li-side"]/div[@class="community-price"]/strong)')
        perpare = house.xpath('string(./div[@class="li-side"]/span)').strip().replace('\n','')
        sign = house.xpath('string(./div[@class="li-side"]/span/@class)')
        if 'red' in sign:
            item['涨跌幅'] = '+' + perpare
        elif 'green' in sign:
            item['涨跌幅'] = '-' + perpare
        print(item)
        item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        info_base.insert_one(item)
    # 存入数据
    has_spider.insert_one({'url':url})
    time.sleep(5)

    next_page_url = html.xpath('string(//div[@class="pagination page-bar"]/a[@class="next next-active"]/@href)')
    if next_page_url:
        get_parseInfo(city,next_page_url,area_name)
    else:
        print('最后一页')
        return


if __name__ == '__main__':
    city_url=getCity_Url()
    for item,url in city_url.items():
        key = item
        print(key,url)

        if info_base.find_one({'city_name':key}):
            print('当前城市已被爬取或正在爬取：',key)
            continue

        html, response, _ = get_html(url+"/community/")
        area = html.xpath('//ul[@class="region-parents"]/li')[1:-1]
        aaaaa = response.text
        for area_else in area:
            url1 = area_else.xpath('string(./a/@href)')
            area_name = area_else.xpath('string(./a)')
            # has_spider_list = has_spider.find()
            # if url in has_spider_list:
            #     continue


            # 增加判断长度 1250
            html1, response1, _ = get_html(url1)
            text = ''.join(html1.xpath('//div[@class="sort-row"]/span/text()'))
            try:
                length = int(''.join(re.findall('(\d+)',text)))
            except:
                continue
            if length >= 1250:
                hlist = html1.xpath('//div[@class="filter-wrap"][1]//ul[@class="line"]/li/a/@href')[1:]
                for url2 in hlist:
                    html2, response2, _ = get_html(url2)
                    text2 = ''.join(html2.xpath('//div[@class="sort-row"]/span/text()'))
                    try:
                        length2 = int(''.join(re.findall('(\d+)', text2)))
                    except:
                        continue
                    if length2 >= 1250:
                        hlist2 = html2.xpath('//div[@class="filter-wrap"][2]//ul[@class="line"]/li/a/@href')[1:]
                        for url3 in hlist2:
                            html3, response3, _ = get_html(url3)
                            text3 = ''.join(html3.xpath('//div[@class="sort-row"]/span/text()'))
                            try:
                                length3 = int(''.join(re.findall('(\d+)', text3)))
                            except:
                                continue
                            if length3 >= 1250:
                                hlist3 = html3.xpath('//div[@class="filter-wrap"][2]//ul[@class="line"]/li/a/@href')[1:]
                                for url4 in hlist3:
                                    get_parseInfo(key,url4,area_name)
                            else:
                                get_parseInfo(key,url3,area_name)
                    else:
                        get_parseInfo(key,url2,area_name)
            else:
                get_parseInfo(key,url1,area_name)



            # get_parseInfo(key,url,area_name)
        # statis_output('{}_{}.csv'.format(key,time.strftime("%Y-%m", time.localtime())),
        #
        #               ['city_name', '标题', '详情url','latitude','longitude', '竣工时间', '地址', '二手房上架数', '在租套数', '价格', '涨跌幅'],
        #               info_base,key)
        # break