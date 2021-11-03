import random
import re
import time
import requests
import pymongo
import uuid
import numpy as np
import pandas as pd

from urllib import parse
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
from city_map import zfmake_url, city_map, citylist

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
    retryWrites="false")['房天下租房shen']['租房_数据_202111']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['房天下租房shen']['租房_去重_202111']
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "global_cookie=f1v4y6cur4h7034ieaxs84qnk17jxobmy8b; Integrateactivity=notincludemc; newhouse_user_guid=50E5E180-78E4-4D10-DD8D-77E13BC96848; lastscanpage=0; budgetLayer=1%7Cbj%7C2019-07-30%2011%3A26%3A08; resourceDetail=1; new_search_uid=fd91130e51ddd1f2d8e5a7847545c3d8; __utmc=147393320; __utma=147393320.184954923.1564457033.1564642303.1564646708.12; __utmz=147393320.1564646708.12.5.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-verify/redirect; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; logGuid=cb4c3441-3467-4c19-ba09-1dd86b143529; g_sourcepage=ehlist; city=anshan; unique_cookie=U_11rfckz759men2uard7dzzy1i1ejys2c6di*36; __utmb=147393320.15.10.1564646708",
    "Referer": "https://esf.fang.com/newsecond/esfcities.aspx",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
}


def getCity_Code():
    item = {}
    response = requests.get('https://www.fang.com/SoufunFamily.htm', headers=headers, timeout=(5, 5))
    response.encoding = 'gbk'
    html = etree.HTML(response.text)
    lists = html.xpath('//div[@class="onCont"]/table//a')
    for i in lists:
        city = i.xpath('./text()')[0]
        url = i.xpath('./@href')[0]
        code = url.split('.')[0][7:]
        # print(city,code,url)
        if city in ['波士顿', '保加利亚', '昌吉', '德国', '海外', '西雅图', '广德', '旧金山', '洛杉矶', '日本', '塞浦路斯', '西雅图', '西班牙', '希腊', '悉尼',
                    '芝加哥', '马来西亚', '澳大利亚', '美国', '纽约', '葡萄牙', '安陆', '蒙城']:
            continue
        item[city] = code
    print(item)
    return item


def get_proxy():
    try:
        return requests.get('http://47.106.223.4:50002/get/').json().get('proxy')
        # return '111.202.83.35:80'
    except:
        num = 3
        while num:
            try:
                return requests.get('http://47.106.223.4:50002/get/').json().get('proxy')
            except:
                print('暂无ip，等待20秒')
                time.sleep(20)

                num -= 1
        print('暂无ip')


def get_html(url, proxieslist):
    s = 0
    while True:
        try:
            if len(proxieslist) > 0:
                proxies = proxieslist
            else:
                proxy = get_proxy()
                proxies = {"https": proxy}
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            encod = response.apparent_encoding
            if encod.upper() in ['GB2312', 'WINDOWS-1254']:
                encod = 'gbk'
            response.encoding = encod
            tree = etree.HTML(response.text)
            if '房天下' in tree.xpath("//title/text()")[0] and '出租' in tree.xpath("//title/text()")[0]:
                proxieslist = proxies
                print(s, proxies, '获取成功')
                return response, proxieslist
            if '人机认证' in response.text:
                print('该IP需要人机验证: ', proxieslist)
                proxieslist = []
                continue
            if '访问验证' in ''.join(tree.xpath('//title/text()')):
                print('出现访问验证')
                proxieslist = []
                continue
            if '跳转' in tree.xpath("//title/text()")[0]:
                print(tree.xpath("//title/text()")[0], "出现跳转页面")
                proxieslist = []
                continue
            # 可以增加一个判断是否成功的代码，如果页面不是所需页面，proxieslist赋值为空
            proxieslist = proxies
            print(s, proxies, '获取成功')
            return response, proxieslist
        except Exception as e:
            s += 1
            proxieslist = []

            # print('get_html错误', e)
            continue
    return


class Esf_FTX:
    def __init__(self, year, month, pool):
        self.year = year
        self.month = month
        self.pool = pool

    def get_everyone_city_region(self, df, city):
        """生成每一个城市已经获取的region"""
        exists_city_df = df[df['城市'] == city]
        if not exists_city_df.shape[0]:
            exists_region = []
        else:
            exists_region = exists_city_df['区县'].tolist()
        return exists_region

    def get_dist(self, city, GetType):
        """
        生成行政区字典
        """
        number = 9
        while number > 0:
            try:
                dist = zfmake_url(city, 'https://{}.zu.fang.com{}', GetType)
                return dist

            except:
                number -= 1
                continue

    def get_data(self, baseUrl, city, dist, proxieslist):
        print('当前url:',baseUrl)
        """
        解析每一个页面
        """
        gen_url = ''.join(re.findall('(.+com)', baseUrl))
        if has_spider.count({'url':baseUrl}):
            print('该页数据已爬取，下一页')
            return

        # response = get_Html_IP(gen_url, headers=headers)





        tree, proxieslist = self.get_tree(baseUrl, proxieslist)
        if tree == '':
            return
        house_box = tree.xpath('//dd[@class="info rel"]')

        for house in house_box:
            item_dict = {}
            item_dict['城市'] = city
            item_dict['区县'] = dist
            item_dict['id'] = uuid.uuid1(node=random.randint(999, 999999))
            item_dict['标题url'] = gen_url + ''.join(house.xpath('./p[@class="title"]/a/@href'))
            item_dict['标题'] = ''.join(house.xpath('./p[@class="title"]/a/text()'))





            contents = '|'.join(house.xpath('./p[@class="font15 mt12 bold"]/text()')).replace(' ','').replace('\n','').replace('\r','')
            item_dict['类型'] = ''.join(re.findall('([合租整租])', contents))
            if item_dict['类型'] == '合租':
                item_dict['户型'] = ''
            elif item_dict['类型'] == '整租':
                item_dict['户型'] = ''.join(re.findall('\|(\d室\d{0,1}厅{0,1}\d{0,1}卫{0,1})\|', contents))
            mj = ''.join(re.findall('\|(\d+.?\d+)㎡\|', contents))
            try:
                item_dict['面积'] = np.double(mj)
            except:
                item_dict['面积'] = np.NaN
            item_dict['朝向'] = ''.join(re.findall('\|朝(.+)', contents))
            item_dict['地址'] = ''.join(house.xpath('./p[@class="gray6 mt12"]//text()'))
            item_dict['小区'] = ''.join(house.xpath('./p[@class="gray6 mt12"]/a[2]/span/text()'))
            item_dict['小区url'] = gen_url + ''.join(house.xpath('./p[@class="gray6 mt12"]/a[2]/@href'))
            item_dict['楼层'] = ''
            zj = ''.join(house.xpath('./div[@class="moreInfo"]/p/span/text()'))
            try:
                item_dict['租金'] = np.double(zj)
            except:
                item_dict['租金'] = np.NaN
            item_dict['特点'] = '|'.join(house.xpath('./p[@class="mt12"]/span/text()'))
            item_dict['数据来源'] = '房天下'
            item_dict['抓取年份'] = Year
            item_dict['抓取月份'] = Month
            item_dict['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            print(item_dict)

            info_base.insert_one(item_dict)
        has_spider.insert_one({'url': baseUrl})
        return proxieslist

    def get_tree(self,dist_url, proxieslist):
        s = 0
        while True:
            try:
                if len(proxieslist) > 0:
                    proxies = proxieslist
                else:
                    proxy = get_proxy()
                    proxies = {"https": proxy}
                response = requests.get(dist_url, headers=headers, proxies=proxies, timeout=10)
                encod = response.apparent_encoding
                if encod.upper() in ['GB2312', 'WINDOWS-1254']:
                    encod = 'gbk'
                response.encoding = encod
                if '人机认证' in response.text:
                    print('该IP需要人机验证: ', proxieslist)
                    proxieslist = []
                    continue
                tree = etree.HTML(response.text)
                if '访问验证' in ''.join(tree.xpath('//title/text()')):
                    print('出现访问验证')
                    proxieslist = []
                    continue
                if '跳转' in tree.xpath("//title/text()")[0]:
                    print(tree.xpath("//title/text()")[0], "出现跳转页面")
                    proxieslist = []
                    continue
                # 可以增加一个判断是否成功的代码，如果页面不是所需页面，proxieslist赋值为空
                if '租房信息' in ''.join(tree.xpath('//title/text()')):
                    proxieslist = proxies
                    print(s, proxies, '获取成功')
                    return tree, proxieslist
            except Exception as e:
                s += 1
                proxieslist = []

                # print('get_html错误', e)
                continue
        return

    # def get_tree(self, dist_url, proxieslist):
    #     number_tz = 0
    #     while True:
    #         res, proxieslist = get_html(dist_url, proxieslist)
    #         if res:
    #             tree = etree.HTML(res.text)
    #         else:
    #             continue
    #         if '访问验证' in ''.join(tree.xpath('//title/text()')):
    #             print('出现访问验证')
    #             proxieslist = []
    #             continue
    #         # 没有请求到正确的页面
    #         number_tz += 1
    #         if '跳转' in tree.xpath("//title/text()")[0]:
    #             print(tree.xpath("//title/text()")[0], "出现跳转页面")
    #             proxieslist = []
    #             if number_tz > 3:
    #                 break
    #             continue
    #         return tree, proxieslist
    #     return '', proxieslist

    def get_page(self, city, dist_dict, proxieslist):
        """
        获取每个区下的页面
        """
        for dist_url, dist in dist_dict.items():
            starturl = ''.join(re.findall('(.+com)',dist_url))
            ite = {}
            if dist == '不限':
                continue
            # number_tz = 0
            # while True:
            #     res = get_html(dist_url)
            #     if res:
            #         tree = etree.HTML(res.text)
            #     else:
            #         break
            #     # 没有请求到正确的页面
            #     number_tz += 1
            #     if '跳转' in tree.xpath("//title/text()")[0]:
            #         print(tree.xpath("//title/text()")[0], "%s :出现跳转页面" % dist)
            #         if number_tz > 3:
            #             break
            #         continue

            tree, proxieslist = self.get_tree(dist_url, proxieslist)
            if tree == '':
                continue

            # page_number = tree.xpath("//div[@class='page_al']/p[last()]/text()") or \
            #               tree.xpath("//div[@class='page_al']/span[contains(text(), '共')]/text()")
            numbertext = ''.join(tree.xpath('//div[@class="fanye"]/span/text()'))
            try:
                number = int(''.join(re.findall('(\d+)',numbertext)))
            except:
                continue
            # 数据量过多时：
            if number == 100:
                dist_url1_list = tree.xpath('//dl[@id="rentid_D04_02"]/dd/a/@href')[1:]
                for url1 in dist_url1_list:
                    dist_url1 = starturl + url1
                    tree1, proxieslist = self.get_tree(dist_url1, proxieslist)
                    if tree1 == '':
                        continue
                    numbertext1 = ''.join(tree1.xpath('//div[@class="fanye"]/span/text()'))
                    try:
                        number1 = int(''.join(re.findall('(\d+)', numbertext1)))
                    except:
                        continue
                    if number1 == 100:
                        dist_url2_list = tree1.xpath('//dl[@id="rentid_D04_03"]/dd/a/@href')[1:]
                        for url2 in dist_url2_list:
                            dist_url2 = starturl + url2
                            tree2, proxieslist = self.get_tree(dist_url2, proxieslist)
                            if tree2 == '':
                                continue
                            numbertext2 = ''.join(tree2.xpath('//div[@class="fanye"]/span/text()'))
                            try:
                                number2 = int(''.join(re.findall('(\d+)', numbertext2)))
                            except:
                                continue
                            if number2 == 100:
                                dist_url3_list = tree2.xpath('//div[@id="rentid_D04_08"]/a/@href')[1:]
                                for url3 in dist_url3_list:
                                    dist_url3 = starturl + url3
                                    tree3, proxieslist = self.get_tree(dist_url3, proxieslist)
                                    if tree3 == '':
                                        continue
                                    numbertext3 = ''.join(tree3.xpath('//div[@class="fanye"]/span/text()'))
                                    try:
                                        number3 = int(''.join(re.findall('(\d+)', numbertext3)))
                                    except:
                                        continue
                                    if '没有找到相符的房源' in ''.join(tree3.xpath('//p[@class="not_find_note"]/span/text()')):
                                        continue
                                    else:
                                        ite[dist_url3] = number3

                            elif '没有找到相符的房源' in ''.join(tree2.xpath('//p[@class="not_find_note"]/span/text()')):
                                continue
                            else:
                                ite[dist_url2] = number2

                    elif '没有找到相符的房源' in ''.join(tree1.xpath('//p[@class="not_find_note"]/span/text()')):
                        continue
                    else:
                        ite[dist_url1] = number1

            elif '没有找到相符的房源' in ''.join(tree.xpath('//p[@class="not_find_note"]/span/text()')):
                continue
            else:
                ite[dist_url] = number

            # {dist: [{dist_url: number},...]}

            print(ite)
            for page_url in ite:
                page_number = ite[page_url]
                l = []
                for i in range(1, page_number + 1):
                    url = page_url[:-1] + f'-i3{i}/'

                    done = self.pool.submit(self.get_data, url, city, dist, proxieslist)
                    l.append(done)
                proxieslist = [obj.result() for obj in l][-1]
        return proxieslist
            # break

    def run(self, city_map):

        print(len(city_map))
        proxieslist = []
        for city, city_code in city_map.items():

            # for city, city_code in city_map.items():
            if has_spider.count({city: '已爬取3'}):
                print('已爬取：', city)
                continue
            elif has_spider.count({city: '正在爬取'}):
                print('正在爬取：', city)
                continue
            has_spider.insert_one({city:'正在爬取'})

            exists_region = []

            # if city in citylist: continue
            # if city in ["罗定", "阿坝州", "农安", "怒江", "盘锦", '香港', '海南省']: continue
            if city in ['安达', '安宁', '安丘', '安溪', '宝应', '巴彦', '霸州', '三河', '三沙', '商河', '尚志', '韶山',
                        '宾县', '宾阳', '博罗', '长岛', '长丰', '长乐', '昌乐', '昌黎', '常宁', '长清', '长寿', '昌邑', '巢湖',
                        '崇州', '淳安', '当涂', '当阳', '大邑', '大足', '德化', '德惠', '登封', '邓州', '垫江', '定兴', '定州',
                        '东方', '东港', '东海', '东台', '都江堰', '法库', '繁昌', '肥城', '肥东', '肥西', '凤城', '丰都', '奉化',
                        '奉节', '丰县', '福安', '涪陵', '阜宁', '富阳', '高淳', '高陵', '巩义', '公主岭', '广饶', '固镇', '海安',
                        '海城', '海拉尔', '海林', '汉南', '合川', '桦甸', '怀仁', '怀远', '惠安', '惠东', '霍邱', '户县', '建德',
                        '江都', '江津', '姜堰', '简阳', '胶南', '胶州', '即墨', '靖安', '靖江', '京山', '金湖', '金坛', '金堂',
                        '进贤', '晋州', '济阳', '蓟州', '冀州', '开县', '开阳', '康平', '库尔勒', '奎屯', '莱芜', '莱西', '莱阳',
                        '莱州', '兰考', '蓝田', '老河口', '耒阳', '乐亭', '梁平', '连江', '辽中', '醴陵', '临安', '临海', '临清',
                        '临朐', '临猗', '浏阳', '溧阳', '龙海', '栾川', '滦南', '滦县', '庐江', '洛宁', '罗源', '孟津', '闽清',
                        '南安', '宁海', '蓬莱', '平度', '平山', '平潭', '平阴', '普兰店', '普宁', '迁安', '黔江', '迁西', '綦江',
                        '青龙', '清徐', '清镇', '青州', '邛崃', '栖霞', '泉港', '泉山', '荣昌', '如东', '瑞安', '瑞金', '汝阳']:  # 没有区县数据, 不要
                continue

            start = time.time()
            dist = self.get_dist(city, GetType="租房")
            # print(dist)
            proxieslist = self.get_page(city, dist, proxieslist)
            print("抓取%s 总用时: %s" % (city, time.time() - start))
            has_spider.insert_one({city: '已爬取3'})



if __name__ == '__main__':

    # url11 = 'https://zu.fang.com/house-a01/c210000-d20-g21/'


    # TODO 二手房启动程序
    # TODO 请删除 log>lose_dist 中的缓存记录
    # TODO 修改 Month为当前要抓取的月份
    Year = 2021
    Month = 7
    # city_map=getCity_Code()
    Pool = ThreadPoolExecutor(20)
    Esf_FTX(year=Year, month=Month, pool=Pool).run(city_map)
    Pool.shutdown()
