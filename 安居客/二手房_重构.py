import time
import os
import threading
import requests
import pymongo
import re
import random
from concurrent.futures import ThreadPoolExecutor
from lxml import etree
from config import get_proxy,get_ua,city_url
# from capter_verify.captcha_run import AJK_Slide_Captcha
# from fake_useragent import UserAgent
from urllib import parse
# from 乱码检测 import if_contain_symbol
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
            retryWrites="false")['安居客']['二手房_数据_202207']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['安居客']['二手房_去重_202207']


# city_url = {
#     '广州':'https://guangzhou.anjuke.com/sale/t17/',
#     '深圳':'https://shenzhen.anjuke.com/sale/t13/',
#     '北京':'https://beijing.anjuke.com/sale/t7/',
#     '成都':'https://chengdu.anjuke.com/sale/t22/',
#     '上海':'https://shanghai.anjuke.com/sale/t1/',
#             }


def clear():
    while True:
        time.sleep(600)
        os.system('cls')
def getCity_Url():
    # response = requests.get('https://www.anjuke.com/sy-city.html', headers=headers, timeout=(5, 5))
    # response.encoding = 'utf-8'
    # html = etree.HTML(response.text)
    url='https://www.anjuke.com/sy-city.html'
    html, response = get_html(url)
    lists=html.xpath('/html/body/div[3]/div/div[2]/ul/li/div/a')
    city_url={}
    for data in lists:
        city=data.xpath('./text()')[0]
        url=data.xpath('./@href')[0]
        city_url[city]=url
    return city_url

def get_html(url):
    # return sessionpage(url)
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        'Connection': 'close',
        'Host': 'www.anjuke.com',
        "referer": "https://www.anjuke.com/sy-city.html",
        "upgrade-insecure-requests": "1",
        # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        # "user-agent":UserAgent().chrome
        "user-agent": get_ua()
    }

    try:
        headers['Host']=re.findall("://(.*?\.anjuke\.com)",url)[0]
        headers['referer']=re.findall("://(.*?\.anjuke\.com)",url)[0]
    except:
        pass
    # url=url.replace('https','http')
    for i in range(2000):
        proxy=get_proxy()
        proxies = {
            "https":proxy,
            "http":proxy,
                   }
        try:
            response = requests.get(url, headers=headers,proxies=proxies, timeout=10)
            # response = requests.get(url, headers=headers, timeout=10)
            encod = response.apparent_encoding
            if response.status_code != 200:continue
            if encod.upper() in ['GB2312', 'WINDOWS-1254']:
                encod = 'gbk'
            response.encoding = encod
            if '访问验证-安居客' in response.text:
                time.sleep(2)
                continue
            html = etree.HTML(response.text)
            return html,response
        except Exception as e:
            # print('get_html错误',proxies, e)
            time.sleep(2)
    return
def sessionpage(url):
    h1 = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }
    h2 = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://www.anjuke.com/",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-site",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }
    h2['Host'] = re.findall("://(.*?\.anjuke\.com)", url)[0]
    h2['referer'] = re.findall("://(.*?\.anjuke\.com)", url)[0]
    for _ in range(1000):
        try:
            proxy = get_proxy()
            proxies = {
                "https": proxy,
                "http": proxy,
            }
            url1 = re.findall("(https://.*?\.anjuke\.com)",url)[0]
            url2 = url
            s = requests.session()
            s.get(url1, headers=h1, proxies=proxies)
            response=s.get(url2, headers=h2, proxies=proxies)
            if '访问验证-安居客' in response.text:
                # time.sleep(2)
                continue
            html = etree.HTML(response.text)
            return html, response
        except Exception as e:
            print(e)
            continue

def get_parseInfo(city,dist,liltename,url):
    tag=0
    while True:
        tag += 1
        if city in tiaozhuancity:
            html, response = sessionpage(url)
        else:
            html, response = get_html(url)
        # 检查是否出现 58滑动验证
        if html.xpath("//div[@class='pop']/p[@class='title']"):
            # print("3出现滑动验证")
            continue
        # 安居客滑动验证
        if html.xpath('//*[@id="captchaForm"]'):
            # print("3出现滑动验证, 更改ip")
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
                return
            continue
        if has_spider.find_one({'标题':url}):
            next_page_url = html.xpath('string(//a[@class="next next-active"]/@href)')
            if next_page_url:
                print('该页数据已爬取，下一页',url)
                get_parseInfo(city,dist,liltename, next_page_url)
            else:
                title=html.xpath('/html/head/title/text()')
                print('最后一页',title)
                if not has_spider.find_one({'liltename': url}):
                    has_spider.insert_one({'liltename': url})

                return
        else:

            li_list = html.xpath('//*[@id="__layout"]//div[@class="property"]')
            try:
                page=re.findall('/p(\d+)',url)[0]
            except:
                page='1'
            for li in li_list:
                item = {}
                item['城市'] = city
                item['区县'] = li.xpath('string(.//p[@class="property-content-info-comm-address"]/span[1]/text())').replace('\n', '').strip()
                item['标题'] = li.xpath('string(.//div[@class="property-content-detail"]/div[@class="property-content-title"]/h3)').replace('\n','').strip()
                item['标题url'] = li.xpath('string(./a/@href)').replace('\n','').strip()
                item['小区'] = li.xpath('string(.//p[@class="property-content-info-comm-name"])').replace('\n','').strip()
                item['户型'] = li.xpath('string(.//div[@class="property-content-info"]/p[1])').replace('\n','').strip()
                item['面积'] = li.xpath('string(.//div[@class="property-content-info"]/p[2])').replace('\n','').strip()
                item['朝向'] = li.xpath('string(.//div[@class="property-content-info"]/p[3])').replace('\n','').strip()
                item['楼层'] = li.xpath('string(.//div[@class="property-content-info"]/p[4])').replace('\n','').strip()
                item['建筑年份'] = li.xpath('string(.//div[@class="property-content-info"]/p[5])').replace('\n','').strip()
                item['地址'] = li.xpath('string(.//p[@class="property-content-info-comm-address"])').replace('\n','').replace('\xa0','').replace(' ','').strip()
                item['标签'] = li.xpath('string(.//div[@class="property-content-info"]/span[@class="property-content-info-tag"])').replace('\n','').replace('\xa0','').replace(' ','').strip()
                item['总价'] = li.xpath('string(.//div[@class="property-price"]/p[1])')
                item['单价'] = li.xpath('string(.//div[@class="property-price"]/p[2])')
                item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                # if if_contain_symbol(item['小区']):continue
                # print(item)
                # print('')
                info_base.insert_one(item)
            print('城市：%s %s %s,当前第%s页,获取数据量%d' % (city,dist,liltename,page, len(li_list)),url)
            has_spider.insert_one({'标题': url})

            next_page_url = html.xpath('string(//div[@class="pagination"]/a[@class="next next-active"]/@href)')
            if next_page_url:
                # print('下一页')
                get_parseInfo(city,dist,liltename, next_page_url)
            else:
                if not has_spider.find_one({'liltename': url}):
                    has_spider.insert_one({'liltename': url})
                return
        break

def getdist(city,url):
    gtnumber=0
    # if city=='阿拉善盟': return {
    #     '阿拉善左旗':'https://alashanmeng.anjuke.com/sale/alashanzuoqi/',
    #     '额济纳旗':'https://alashanmeng.anjuke.com/sale/ejinaqi/',
    #     '阿拉善右旗':'https://alashanmeng.anjuke.com/sale/alashanyouqi/',
    #     '阿拉善盟周边':'https://alashanmeng.anjuke.com/sale/alashanmengzhoubian/',
    # }
    # if city=='昌乐': return {
    #     '昌乐城区':'https://changle.anjuke.com/sale/changlecq/',
    #     '昌乐周边':'https://changle.anjuke.com/sale/changleqt/',
    # }
    dist = {}
    while True:
        if city in tiaozhuancity:
            html, response = sessionpage(url+'?from=navigation')
        else:
            html, response = get_html(url+'?from=navigation')
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
        dist={}
        tables=html.xpath('//div[@class="filter-wrap filter-region"]/section[@class="filter-content"]/ul/li')[1:]
        for i in tables:
            distname=i.xpath('./a/text()')[0]
            disturl=i.xpath('./a/@href')[0]
            # print(disturl.split('/')[-2])
            if re.findall('(/ls1)',disturl):
                disturl=disturl.replace('/ls1','')
            disturl=url+re.findall('sale/(.*?)/',disturl)[0]
            dist[distname]=disturl
        break
    return dist
def getliltedist(city,dist,dist_url):
    while True:
        if city in tiaozhuancity:
            html, response = sessionpage(dist_url)
        else:
            html, response = get_html(dist_url)
        # 检查是否出现 58滑动验证
        if html.xpath("//div[@class='pop']/p[@class='title']"):
            # print("2出现滑动验证")
            continue
        # 安居客滑动验证
        if html.xpath('//*[@id="captchaForm"]'):
            # print("2出现滑动验证, 更改ip")
            continue
        if "访问过于频繁" in "".join(html.xpath("//h2[@class='item']/text()")):
            print("访问过于频繁")
            continue
        if response.status_code in [403]:
            print(403, "休息2s")
            time.sleep(2)
            continue

        tables = html.xpath('//*[@id="__layout"]/div/section/section[2]/section/div[1]/section/ul[2]/li/a')[1:]
        if tables == []:
            tables = html.xpath('//*[@id="__layout"]/div/section/section[2]//section/div[1]/section/ul[2]/li/a')[1:]

        # for li in tables:
        #     url=li.xpath('./@href')[0].strip()
        #     liltename = li.xpath('./text()')[0].strip()
        #     print(liltename,url)
        #     get_parseInfo(city,dist,liltename, url)
        l = []
        baseurl=re.findall('(https://.*?\.anjuke\.com/sale/)',dist_url)[0]
        for li in tables:
            url = li.xpath('./@href')[0]
            newurl=baseurl+re.findall('sale/(.*?)/',url)[0]+'/?from=SearchBar'
            # print('url',url)
            # print('newurl',newurl)
            liltename=li.xpath('./text()')[0].strip()
            if has_spider.find_one({'liltename':newurl}):
                print('该地区已抓取')
                continue
            # get_parseInfo(city, dist, liltename, url)
            print('开始进行抓取',city,newurl)
            done = pool.submit(get_parseInfo,city,dist,liltename, newurl)
            l.append(done)
        [obj.result() for obj in l]

        break


badcity = ['阿坝州', '大邑', '金堂', '淳安', '富阳', '临安', '桐庐', '铜梁', '丰都', '长寿', '涪陵',
           '南川', '永川', '綦江', '黔江', '万州', '江津', '合川', '普兰店', '平阴', '济阳', '商河',
           '中牟', '巩义', '宁乡', '无极', '辛集', '元氏', '即墨', '胶南', '周至', '户县', '蓝田',
           '宁海', '肥东', '肥西', '庐江', '长丰', '长乐', '连江', '平潭', '宜良', '辽中', '新民',
           '新建', '白沙县', '儋州市', '澄迈县', '定安', '琼中', '屯昌', '文昌市', '农安', '陵水',
           '保亭', '东方市', '龙门', '永登', '榆中', '文安', '汝阳', '宾阳', '横县', '晋安', '上虞',
           '乐亭', '滦县', '丰县', '睢宁', '江都', '肇源', '当涂', '巴州', '延吉', '大冶', '景洪',
           '吉首', '英德', '兴义', '凌源', '江油市', '都匀', '乌兰浩特', '瑞丽']
tiaozhuancity = ['阿拉善盟', '昌乐']
if __name__ == '__main__':
    # print(info_base.count_documents({'城市':'潮州'}))
    # city_url = getCity_Url()
    # for k,v in city_url.items():
    #     print(f"'{k}':'{v}',")
    pool = ThreadPoolExecutor(1)
    t1 = threading.Thread(target=clear)
    t1.setDaemon(True)
    t1.start()

#调出函数进行调试----------------------------------------------------------------------------------------------------------
    # getliltedist('象山', '象山周边', 'https://xiangshanxian.anjuke.com/sale/xiangshanqita')


    # x=has_spider.delete_many({})
    # print(x.deleted_count,'个文档已删除')
    # print(info_base.count_documents({}))
    # print(has_spider.count_documents({}))
    # print(has_spider.find_one())

    # for i in ['章丘']:
    #     x=info_base.delete_many({'城市':i})
    #     print(x.deleted_count,'个文档已删除')


    while city_url:
        data = random.sample(city_url.items(), 1)
        city, url = data[0][0], data[0][1]
        # if city not in ['甘南', '铁岭', '海门', '陆丰', '海北', '邵武', '贵阳', '韩城']:   #阿拉善盟、昌乐 未抓取
        #     del city_url[city]
        #     continue

        if city in badcity:
            del city_url[city]
            continue
        if has_spider.find_one({'已爬取城市12': city}):   #--------------------------------------跳出判断条件
            print(city,'该城市已抓取')
            del city_url[city]
            continue
        dists=getdist(city,url+ "/sale/")
        print(city, '爬到的区域:', dists)
        # dists=getdist('鸡西', 'https://jixi.anjuke.com/sale/')

        # for dist,dist_url in dists.items():


        while dists:
            # 区域抓取

            data2 = random.sample(dists.items(), 1)
            dist, dist_url = data2[0][0], data2[0][1]
            if has_spider.find_one({'区域url12': dist_url}):  #--------------------------------------跳出判断条件
                print('该区域已抓取')
                del dists[dist]
                continue
            try:
                getliltedist(city,dist,dist_url)
                if not has_spider.find_one({'区域url12': dist_url}): #--------------------------------------跳出判断条件
                    has_spider.insert_one({'区域url12': dist_url})   #--------------------------------------跳出判断条件
                del dists[dist]
            except Exception as e:
                print(e)

                del dists[dist]
                continue
        if not has_spider.find_one({'已爬取城市12': city}):    #--------------------------------------跳出判断条件
            has_spider.insert_one({'已爬取城市12': city})       #--------------------------------------跳出判断条件
        del city_url[city]
    pool.shutdown()