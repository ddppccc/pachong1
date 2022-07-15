import re
import time
import os
import threading
import requests
import pymongo
import random
from concurrent.futures import ThreadPoolExecutor
from lxml import etree
from config import get_proxy,get_ua,delete_proxy,statis_output
from capter_verify.captcha_run import AJK_Slide_Captcha
from zujin_descde import decode_zujin,get_font
from urllib import parse
# from 乱码检测 import if_contain_symbol
from bjregion import bjregion_zu,bjlilteregion

MONGODB_CONFIG = {
    "host": "192.168.1.28",
    "port": "27017",
    "user": "admin",
    "password": '123123',
}

info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
                retryWrites="false")['安居客']['租房_数据_202207']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['安居客']['租房_去重_202207']




# city_url = {
#     '广州':'https://gz.zu.anjuke.com/fangyuan/lx4/',
#     '深圳':'https://sz.zu.anjuke.com/fangyuan/lx4/',
#     '北京':'https://bj.zu.anjuke.com/fangyuan/lx4/',
#     '成都':'https://cd.zu.anjuke.com/fangyuan/lx4/',
#     '上海':'https://sh.zu.anjuke.com/fangyuan/lx4/',
#             }


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
    # response = requests.get('https://www.anjuke.com/sy-city.html', headers=headers, timeout=(5, 5))
    # response.encoding = 'utf-8'
    # html = etree.HTML(response.text)
    url = 'https://www.anjuke.com/sy-city.html'
    html, response = get_html(url)
    lists=html.xpath('/html/body/div[3]/div/div[2]/ul/li/div/a')       #722 个
    city_url={}
    for data in lists:                                                  #提取城市 和城市 url
        city=data.xpath('./text()')[0]
        url=data.xpath('./@href')[0]
        city_url[city]=url
    return city_url
def clear():
    while True:
        time.sleep(600)
        os.system('cls')
def get_html(url):
    while True:                        #for i in range(10):--------------------------------------------------FOR 改成了死循环
        proxies = {"https": get_proxy()}
        try:
            response = requests.get(url, headers=headers,proxies=proxies, timeout=10)
            if response.status_code==200:
                # response = requests.get(url, headers=headers, timeout=10)
                encod = response.apparent_encoding
                if encod.upper() in ['GB2312', 'WINDOWS-1254']:
                    encod = 'gbk'
                response.encoding = encod
                html = etree.HTML(response.text)
                return html,response
        except Exception as e:
            # print('get_html错误',proxies, e)
            time.sleep(2)

    return

def get_parseInfo(city,dist,liltename, url):        # 解析 函数
    tag=0
    # print(city,dist,liltename, url)
    while True:
        tag += 1
        html, response = get_html(url)
        # 检查是否出现 58滑动验证
        if html.xpath("//div[@class='pop']/p[@class='title']"):
            # print("出现滑动验证")
            continue
        # 安居客滑动验证
        if html.xpath('//*[@id="captchaForm"]'):
            # print("出现滑动验证, 更改ip")
            continue
        if "访问过于频繁" in "".join(html.xpath("//h2[@class='item']/text()")):
            print("访问过于频繁")
            continue
        if response.status_code in [403]:
            print(403, "休息2s")
            time.sleep(2)
            continue
        if '访问验证' in response.text:
            print("访问验证")
            time.sleep(2)
            continue
        if '没有找到相关房源' in response.text:
            if tag > 1:
                print('没有找到房源')
                return
            continue
        if has_spider.find_one({'标题qwfsdhjgh':url}):    #发现数据存在的话 ================================================
            next_page_url = html.xpath('string(//div[@class="multi-page"]/a[@class="aNxt"]/@href)')   # 下一页标签
            if next_page_url:
                print('该页数据已爬取，下一页')
                get_parseInfo(city,dist,liltename, next_page_url)     # 通过获取 下一页的 url 进行爬取
            else:
                title = html.xpath('/html/head/title/text()')
                print('最后一页', title)
                return
        else:
            house_div = html.xpath("//div[@class='zu-itemmod']")
            try:
                page = re.findall('/p(\d+)/', url)[0]
            except:
                page = '1'
            for house in house_div:
                item = {}
                item['城市'] = city
                try:
                    item['标题'] = house.xpath(".//h3/a/b/text()")[0]
                    item['标题url'] = house.xpath(".//h3/a/@href")[0]
                except:
                    item['标题'] = ''
                    item['标题url'] = ''
                info = house.xpath("string(.//p[@class='details-item tag'])").replace(" ", "")
                item['户型'] = "".join(re.findall("\d+室\d?厅", info))
                item['面积'] = "".join(re.findall("(\d+\.?\d+)平米", info))
                item['楼层'] = "".join(["".join(re.findall("(.*\))", i)) for i in info.split("|") if "层" in i])
                item['小区'] = "".join(house.xpath(".//address[@class='details-item']/a/text()"))
                item['小区url'] = "".join(house.xpath(".//address[@class='details-item']/a/@href"))
                item['地址'] = "".join(house.xpath(".//address[@class='details-item']/text()")).strip()
                item['数据来源'] = '安居客'
                item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                cate = []
                for i in house.xpath(".//p[@class='details-item bot-tag']//span/text()"):
                    if '整租' in i or '合租' in i:
                        item['类型'] = i
                        continue
                    elif [j for j in ['东', '南', '西', '北'] if j in i]:
                        item['朝向'] = i
                        continue
                    else:
                        cate.append(i)
                item['特点'] = "|".join(cate)
                item['租金'] = str("".join(house.xpath(".//div[@class='zu-side']//b/text()")))


                print(item)
                # if if_contain_symbol(item['小区']): continue
                info_base.insert_one(item)
            print('城市：%s %s %s,当前第%s页,获取数据量%d' % (city, dist, liltename, page, len(house_div)), url)
            has_spider.insert_one({'标题qwfsdhjgh':url})
            #=========================================================================================
            next_page_url = html.xpath('string(.//div[@class="multi-page"]/a[@class="aNxt"]/@href)')
            if next_page_url:
                get_parseInfo(city,dist,liltename,next_page_url)
            else:
                if not has_spider.find_one({'liltename': url}):
                    has_spider.insert_one({'liltename': url})
                return
        break
def get_zu_url(index_url):
    html, response = get_html(index_url)
    try:
        new_url = html.xpath('//div[@id="glbNavigation"]/div/ul[@class="L_tabsnew"]/li[4]/a/@href')   #   每个城市租房 url
        return new_url[0]
    except:
        return ""

def getdist(city,url):
    if city == '北京':
        return bjregion_zu
    gtnumber=0
    while True:
        html,response=get_html(url)
        # 检查是否出现 58滑动验证     ##   每个城市租房页面   url
        if html.xpath("//div[@class='pop']/p[@class='title']"):
            # print("出现滑动验证")
            continue
        # 安居客滑动验证
        if html.xpath('//*[@id="captchaForm"]'):
            # print("出现滑动验证, 更改ip")
            continue
        if "访问过于频繁" in "".join(html.xpath("//h2[@class='item']/text()")):
            print("访问过于频繁")
            continue
        if response.status_code in [403]:
            print(403, "休息2s")
            time.sleep(2)
            continue
        if '访问验证' in response.text:
            print("访问验证")
            time.sleep(2)
            continue
        dist={}
        if city == '北京':
            tables=html.xpath('//*[@id="__layout"]/div/section/section[2]/section/div[1]/section/ul/li/a')[1:]
        else:
            tables=html.xpath('/html/body/div[5]/div[2]/div[1]/span[2]/div/a')[1:] or \
                   html.xpath('/html/body/div[5]/div[2]/div[1]/span[2]/a')[1:] or html.xpath('//*[@id="district-item"]/a')[1:]
        # x=response.text
        for i in tables:
            try:
                distname=i.xpath('./text()')[0]
                disturl=i.xpath('./@href')[0]       # 获取一个城市 的所有的  区域url
                # print(distname,disturl)
            except:
                continue
            dist[distname]=disturl        #  城市名字对应url 连接
        break
    print(city,'爬到的区域:',dist)
    return dist

def getliltedist(city,dist,dist_url):
    # if city=='北京':
    #     dist_url='https://anjuke.com'+dist_url.split('anjuke.com')[-1]
    #     l = []
    #     for liltename, url in bjlilteregion.get(dist).items():
    #
    #         if has_spider.find_one({'liltename': url}):
    #             print('该地区已抓取')
    #             continue
    #         # print(liltename,url)
    #         done = pool.submit(get_parseInfo, city, dist, liltename, url)
    #         l.append(done)
    #     [obj.result() for obj in l]
    #     return


    while True:
        htm, response= get_html(dist_url)
        html=etree.HTML(response.text)
        # 检查是否出现 58滑动验证
        if html.xpath("//div[@class='pop']/p[@class='title']"):
            # print("出现滑动验证")
            continue
        # 安居客滑动验证
        if html.xpath('//*[@id="captchaForm"]'):
            # print("出现滑动验证, 更改ip")
            continue
        if "访问过于频繁" in "".join(html.xpath("//h2[@class='item']/text()")):
            print("访问过于频繁")
            continue
        if response.status_code in [403]:
            print(403, "休息2s")
            time.sleep(2)
            continue

        if city == '北京ds':
            tables = []
            l = []
            for liltename,url in bjlilteregion.get(dist).items():

                if has_spider.find_one({'liltename': url}):
                    print('该地区已抓取')
                    continue
                # print(liltename,url)
                done = pool.submit(get_parseInfo, city, dist, liltename, url)    #dists为 区域地区 和 区域url   加入线程池
                l.append(done)
            [obj.result() for obj in l]
        else:
            tables=html.xpath('//div[@class="items"]/span[@class="elems-l"]/div/div/a')[1:] or \
               html.xpath('//div[@class="items"]/span[@class="elems-l"]/div/a')[1:] or html.xpath('//*[@id="listlist"]/div[4]/div[1]/div[2]/a')[1:]

        # for li in tables:
        #     url=li.xpath('./@href')[0]
        #     liltename = li.xpath('./text()')[0]
        #     print(liltename, url)
            # get_parseInfo(city,dist,liltename, url)


        l = []
        for li in tables:
            url = li.xpath('./@href')[0]
            liltename=li.xpath('./text()')[0].strip()
            if has_spider.find_one({'liltename':url}):
                print('该地区已抓取')
                continue
            # print(liltename,url)
            done = pool.submit(get_parseInfo,city,dist,liltename, url)
            l.append(done)
        [obj.result() for obj in l]

        break
badcity=['阿坝州','大邑','金堂','淳安','富阳','临安','桐庐','铜梁','丰都','长寿','涪陵',
         '南川','永川','綦江','黔江','万州','江津','合川','普兰店','平阴','济阳','商河',
         '中牟','巩义','宁乡','无极','辛集','元氏','即墨','胶南','周至','户县','蓝田',
         '宁海','肥东','肥西','庐江','长丰','长乐','连江','平潭','宜良','辽中','新民',
         '新建','白沙县','儋州市','澄迈县','定安','琼中','屯昌','文昌市','农安','陵水',
         '保亭','东方市','龙门','永登','榆中','文安','汝阳','宾阳','横县','晋安','上虞',
         '乐亭','滦县','丰县','睢宁','江都','肇源','当涂','巴州']
if __name__ == '__main__':
    # cityssss = [ '重庆']      #     跑了后面差的城市======================================================================

    # print(info_base.count_documents({}))
    city_url = getCity_Url()
    pool = ThreadPoolExecutor(30)
    t1 = threading.Thread(target=clear)
    t1.setDaemon(True)
    t1.start()
    # for city, url in city_url.items():
    # for i in ['湘潭']:
    #     x=info_base.delete_many({'城市':i})
    #     print(x.deleted_count,'个文档已删除')
    while city_url:
        data = random.sample(city_url.items(), 1)    #随机获取 一个元素  [('潜江', 'https://qianjiang.anjuke.com')]
        city, url = data[0][0], data[0][1]           #'潜江', 'https://qianjiang.anjuke.com'

        # if city not in cityssss:
        #     continue
        # city, url = '重庆', 'https://chongqing.anjuke.com'

        # if city not in ['湘潭']:
        #     del city_url[city]
        #     continue
        print(city)
        if city in badcity:
            del city_url[city]
            continue
        if has_spider.find_one({'已爬取城市': city}):
            print('该城市已抓取')
            del city_url[city]
            continue
        if city in ['阿里','阿勒泰','茌平']:
            del city_url[city]
            continue

        new_url = get_zu_url(url)      ##   每个城市租房页面   url
        if new_url == "https://haiwai.anjuke.com" or (not new_url):   # 判断是否存在
            del city_url[city]
            continue
        print(new_url)
        dists = getdist(city,new_url)     #dists为 区域地区 和 区域url
        # for dist, dist_url in dist.items():
        while dists:

            data2 = random.sample(dists.items(), 1)    #dists为 区域地区 和 区域url
            dist, dist_url = data2[0][0], data2[0][1]
            print(dist, dist_url)
            if has_spider.find_one({'区域url': dist_url}):
                print('该区域已抓取')
                del dists[dist]
                continue
                #=======================================================================================================
            # try:
            getliltedist(city,dist,dist_url)
            if not has_spider.find_one({'区域url': dist_url}):
                has_spider.insert_one({'区域url': dist_url})
            del dists[dist]
            # except:
            #     del dists[dist]
            #     continue
        if not has_spider.find_one({'已爬取城市': city}):
            has_spider.insert_one({'已爬取城市': city})
        del city_url[city]
    print("已完成...")
    pool.shutdown()
