import random
import re
import time
import requests
import pymongo
import uuid
import json
from urllib import parse
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
from config2 import get_proxy
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
            retryWrites="false")['房天下']['二手房_数据_202204']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['房天下']['二手房_去重_202204']
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    # "Cookie": "global_cookie=f1v4y6cur4h7034ieaxs84qnk17jxobmy8b; Integrateactivity=notincludemc; newhouse_user_guid=50E5E180-78E4-4D10-DD8D-77E13BC96848; lastscanpage=0; budgetLayer=1%7Cbj%7C2019-07-30%2011%3A26%3A08; resourceDetail=1; new_search_uid=fd91130e51ddd1f2d8e5a7847545c3d8; __utmc=147393320; __utma=147393320.184954923.1564457033.1564642303.1564646708.12; __utmz=147393320.1564646708.12.5.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-verify/redirect; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; logGuid=cb4c3441-3467-4c19-ba09-1dd86b143529; g_sourcepage=ehlist; city=anshan; unique_cookie=U_11rfckz759men2uard7dzzy1i1ejys2c6di*36; __utmb=147393320.15.10.1564646708",
    # "Referer": "https://esf.fang.com/newsecond/esfcities.aspx",
    # "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
}
IpPool=[
        "192.168.1.104:5010",
        # "192.168.1.130:5010",
        "118.24.52.95:5010",
        # "47.106.223.4:50002"
        ]

# def get_proxy():
#     try:
#         return proxyMeta
#         # return requests.get(f'http://{random.choice(IpPool)}/get/').json().get('proxy')
#         # return super_proxy_url
#         # return requests.get('http://192.168.1.131:5010/get/').json().get('proxy')
#     except:
#         num = 3
#         while num:
#             try:
#                 return requests.get(f'http://{random.choice(IpPool)}/get/').json().get('proxy')
#                 # return super_proxy_url
#                 # return requests.get('http://192.168.1.131:5010/get/').json().get('proxy')
#             except:
#                 print('暂无ip，等待20秒')
#                 time.sleep(20)
# 
#                 num -= 1
#         print('暂无ip')
def get_html(url):
    proxies = {"https": get_proxy()}
    try:
        response = requests.get(url, headers=headers,proxies=proxies,timeout=10)
        encod = response.apparent_encoding
        if encod.upper() in ['GB2312', 'WINDOWS-1254']:
            encod = 'gbk'
        response.encoding = encod
        if '访问验证-房天下' in response.text:
            # print('访问验证-房天下')
            return get_html(url)
        return response
    except Exception as e:
        # print('get_html错误',e)
        time.sleep(2)
        return  get_html(url)

def get_regions(city_name, GetType):
    for i in range(10):
        """
        根据城市名获得行政区
        :type  二手房抓取
        :param city_name:
        :return: {'guangming': '光明'}
        """
        # 二手房
        if GetType == '二手房':
            url = 'https://{}.esf.fang.com/'.format(city_map[city_name])
            if city_name == '北京':
                url = 'https://esf.fang.com/'
            print('\n将在 %s 爬取行政区' % url)
            res = get_html(url)
            html=etree.HTML(res.text)

            regions_xpath = "//span[contains(text(), '区域')]//following-sibling::ul//a"
            regions = dict(zip(html.xpath(regions_xpath + '/@href'), html.xpath(regions_xpath + '/text()')))
            regions = {key.rsplit('/', 2)[-2]: value for key, value in regions.items() if
                       '周边' not in value and '全部' not in value}
            if not regions:
                continue
            return regions

        else:  # 小区
            url = 'https://{}.esf.fang.com/housing/'.format(city_map[city_name])
            if city_name == '北京':
                url = 'https://esf.fang.com/housing/'
            if city_name == '绍兴':
                url = 'https://shaoxing.esf.fang.com/housing/'
            print('\n将在 %s 爬取行政区' % url)

            res = get_html(url)
            html=etree.HTML(res.text)

            regions_xpath = "//*[@id='houselist_B03_02']/div[@class='qxName']/a"
            regions = dict(zip(html.xpath(regions_xpath + '/@href'), html.xpath(regions_xpath + '/text()')))
            regions = {key.rsplit('/', 2)[-2]: value for key, value in regions.items() if
                       '不限' not in value and '全部' not in value and '周边' not in value}
            if not regions:
                continue
            return regions
    return {}

def make_url(city_name, url_fmt, GetType, city_code='suoxie'):
    for i in range(10):
        # 获取城市中文名称
        # filter()
        # 函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表。
        # 该接收两个参数，第一个为函数，第二个为序列，序列的每个元素作为参数传递给函数进行判，然后将值为True的返回到新列表中
        city_name = list(filter(lambda x: city_name in x, city_map))[0]

        # 获取城市名称拼音
        code = city_map.get(city_name)

        print(code, code)
        if city_name == '绍兴' and GetType == '小区':
            code = 'shaoxing'
        if code:
            # 获取城市的行政区划分列表
            regions = {url_fmt.format(code, key): value for key, value in get_regions(city_name, GetType).items()}

            print(city_name, code, '\n提取到的分区: ', regions)
            return regions
        elif city_name == '北京':
            regions = {'https://{}esf.fang.com/{}/'.format(code, key): value for key, value in
                       get_regions(city_name, GetType).items()}
            if GetType != '二手房':
                regions = {'https://{}esf.fang.com/housing/{}/'.format(code, key): value for key, value in
                           get_regions(city_name, GetType).items()}
            if not regions:continue
            print(city_name, code, '\n提取到的分区: ', regions)

            return regions
        else:
            return {}
    return {}

def get_dist(city, GetType):
    """
    生成行政区字典
    """
    number = 9
    while number > 0:
        try:
            dist = make_url(city, 'https://{}.esf.fang.com/{}/', GetType)
            return dist

        except:
            number -= 1
            continue
    print('获取区域失败')

def getpage(dist_url, dist,city):
    base_url = re.findall("https.*com", dist_url)[0]
    print("base_url: ", base_url, "dist_url: ", dist_url)  # https://abazhou.esf.fang.com
    number_tz = 0
    new_dist_url=''
    while True:
        if new_dist_url:
            res = get_html(new_dist_url)
        else:
            res = get_html(dist_url)
        if res:
            tree = etree.HTML(res.text)
        else:
            break
        # 没有请求到正确的页面
        number_tz += 1
        if '跳转' in tree.xpath("//title/text()")[0]:
            print(tree.xpath("//title/text()")[0], "%s :出现跳转页面" % dist)
            if number_tz > 5:

                break
            new_dist_url = dist_url + '?rfss=1-cea2c81823be8420b6-b1'
            continue
        if '很抱歉，没有找到' in res.text:
            if number_tz > 3:
                has_spider.insert_one({'区域url': dist_url})
                break

            continue

        page_number = tree.xpath("//div[@class='page_al']/p[last()]/text()") or \
                      tree.xpath("//div[@class='page_al']/span[contains(text(), '共')]/text()")

        print('pagenum', page_number)

        if len(page_number) < 1:
            print(tree.xpath('//title/text()'))
            print("没有数据")
            continue

        page_number = int(page_number[0][1:-1])
        # print('-------------',page_number)
        if page_number > 99:
            getliltedist(dist_url, base_url,dist,city,tree)
        else:
            l, data = [], []
            for i in range(1, page_number + 1):
                url = dist_url + f'i3{i}/'
                done = pool.submit(get_data,base_url, url, city, dist, page_number, i, data)
                l.append(done)
            [obj.result() for obj in l]
            print("最终数据量: ", len(data))
            has_spider.insert_one({'区域url': dist_url})
        break
def getliltedist(dist_url,base_url, dist,city,html):
    tables=html.xpath('//*[@id="ri010"]/div[1]/ul/li[2]/ul/li/a')
    litleurllist={}
    for i in tables:
        litleurl = base_url + i.xpath('./@href')[0]
        # litleurllist.append(litleurl)
        litlename=i.xpath('./text()')[0]
        litleurllist[litlename]=litleurl
    print('提取到的litleurl',litleurllist)
    for litlename,litleurl in litleurllist.items():
        number_tz = 0
        new_litleurl=''
        while True:
            if new_litleurl:
                res = get_html(new_litleurl)
            else:
                res = get_html(litleurl)
            if res:
                tree = etree.HTML(res.text)
            else:
                break
            # 没有请求到正确的页面
            number_tz += 1
            if '跳转' in tree.xpath("//title/text()")[0]:
                print(tree.xpath("//title/text()")[0], "%s :出现跳转页面" % dist)
                if number_tz > 5:
                    break
                new_litleurl=litleurl+'?rfss=1-b73f9920263a852442-11'
                continue
                
            if '很抱歉，没有找到' in res.text:
                if number_tz > 3:
                    break
                continue

            page_number = tree.xpath("//div[@class='page_al']/p[last()]/text()") or \
                          tree.xpath("//div[@class='page_al']/span[contains(text(), '共')]/text()")
            
            print('pagenum', page_number)

            if len(page_number) < 1:
                print(tree.xpath('//title/text()'))
                # save_grab_dist(city, dist, dist_url, GetType)
                print("没有数据")
                continue

            page_number = int(page_number[0][1:-1])

            l, data = [], []
            for i in range(1, page_number + 1):
                url = litleurl + f'i3{i}/'
                done = pool.submit(get_data,base_url, url, city, dist, page_number, i, data,litlename)
                l.append(done)
            [obj.result() for obj in l]
            print("最终数据量: ", len(data))
            break
        # break
    has_spider.insert_one({'区域url': dist_url})

def get_data( baseUrl,gen_url, city, dist, pageNumber, currPage, data=None,litlename=None):
    """
    解析每一个页面
    """
    number_tz = 0
    new_gen_url=''
    while True:
        if has_spider.find_one({'页面url': gen_url}):
            print('该页数据已爬取，下一页')
            return

        if new_gen_url:
            res = get_html(new_gen_url)
        else:
            res = get_html(gen_url)
        if res:
            tree = etree.HTML(res.text)
        else:
            break

        number_tz += 1
        if "<title>跳转...</title>" in res.text:
            if number_tz > 4:
                break
            print('出现跳转')
            new_gen_url=gen_url+'?rfss=1-1b2aafb3a63b84a055-36'
            continue

        house_box = tree.xpath('//div[@class="shop_list shop_list_4"]/dl[@dataflag]')
        try:
            x=house_box[0]
        except Exception as e:
            print(e, gen_url)
            if number_tz > 3:
                break
            gen_url = gen_url + '?rfss=1-3724cb132627851347-b1'
            continue
        for house in house_box:
            item_dict = {}
            item_dict['id'] = uuid.uuid1(node=random.randint(999, 999999))
            try:
                item_dict['标题url'] = baseUrl + house.xpath('.//dt[@class="floatl"]/a/@href')[0]
            except Exception as e:
                # print('获取url错误',e,gen_url)
                continue
            # item_dict['小区域'] = litlename
            contents = house.xpath(".//p[@class='tel_shop']/text()")

            for cont in contents:
                conts = cont.replace(" ", "").replace('\n', '').replace('\r', '')
                if '室' in conts:
                    item_dict['户型'] = "".join(re.findall("(\d室?\d厅?)", conts))
                if "�" in conts or "㎡" in conts:
                    item_dict['面积'] = "".join(re.findall("(\d+\.?\d+)", conts))
                if '层' in conts:
                    item_dict['楼层'] = conts.strip()
                if '南' in conts or '北' in conts or '东' in conts or '西' in conts:
                    item_dict['朝向'] = conts.strip()
                if '建' in conts:
                    item_dict['建筑年份'] = "".join(re.findall("(\d+)年", conts))

            # if "建筑年份" not in item_dict.keys():
            #     item_dict['建筑年份'] = None
            # elif "户型" not in item_dict.keys():
            #     item_dict['户型'] = None
            # elif "面积" not in item_dict.keys():
            #     item_dict['面积'] = None
            # elif "楼层" not in item_dict.keys():
            #     item_dict['楼层'] = None
            # elif "朝向" not in item_dict.keys():
            #     item_dict['朝向'] = None

            try:
                item_dict['小区'] = house.xpath(".//p[@class='add_shop']/a/@title")[0]
            except:
                return

            # 地址
            try:
                item_dict['地址'] = house.xpath(".//p[@class='add_shop']/span/text()")[0]
            except:
                # item_dict['地址'] = None
                pass
            try:
                item_dict['总价'] = house.xpath(".//dd[@class='price_right']/span[@class='red']/b/text()")[0].replace(
                    '$',
                    '')
                unit_price = house.xpath(".//dd[@class='price_right']/span[2]/text()")[0]
                item_dict['单价'] = "".join(re.findall("(\d+\.?\d+)元", unit_price)).replace('$', '')
            except:
                print('error!!, 单价错误')
                # item_dict['总价'] = None
                # item_dict['单价'] = None

            # 标签
            item_dict['标签'] = "|".join(house.xpath(".//p[@class='clearfix label']//span/text()"))
            item_dict['抓取年份'] = Year
            item_dict['抓取月份'] = Month
            item_dict['数据来源'] = '房天下'
            item_dict['城市'] = city
            item_dict['区县'] = dist
            # item_dict['关注人数'] = None  # followInfo
            item_dict['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            data.append(item_dict)

            # print(item_dict)
            info_base.insert_one(item_dict)
        print(f"城市：{city} {dist}, 状态：有数据，共{pageNumber}页，当前第{currPage}页", gen_url, len(house_box))
        has_spider.insert_one({'页面url': gen_url})
        return data
    return
if __name__ == '__main__':
    # TODO 二手房启动程序
    # TODO 请删除 log>lose_dist 中的缓存记录
    # TODO 修改 Month为当前要抓取的月份
    Year = 2022
    Month = 4
    pool = ThreadPoolExecutor(30)
    # print(info_base.count_documents({}))
    with open('city_map.json','r', encoding='utf-8') as f:
        city_map = json.load(f)
    print(len(city_map))
    
    # for i in ['眉山']:
    #     x=info_base.delete_many({'城市':i})
    #     print(x.deleted_count,'个文档已删除')
    
    while city_map:
    # for city,city_code in city_map.items():
        data = random.sample(city_map.items(), 1)
        city, city_code = data[0][0], data[0][1]

        if city in ["罗定", "阿坝州", "农安", "怒江", "盘锦", '香港', '海南省']:
            del city_map[city]
            continue
        if city in ['波士顿','保加利亚','昌吉','德国','海外','西雅图','广德','旧金山','洛杉矶','日本','塞浦路斯','西雅图',
                    '西班牙','希腊','悉尼','芝加哥','马来西亚','澳大利亚','美国','纽约','葡萄牙','安陆','蒙城']:
            del city_map[city]
            continue
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
            del city_map[city]
            continue

        # if city not in ['兰州','杭州','廊坊']:
        #     del city_map[city]
        #     continue

        if has_spider.find_one({'抓取完成城市': city}):
            print('该城市已抓取完成')
            del city_map[city]
            continue
        dists = get_dist(city, GetType="二手房")
        # print('dist',dists)

        # for dist_url, dist in dists.items():

        while dists:
            data2 = random.sample(dists.items(), 1)
            dist_url, dist = data2[0][0], data2[0][1]

            if has_spider.find_one({'区域url': dist_url}):
                print('该区域已抓取')
                del dists[dist_url]
                continue
            getpage(dist_url,dist,city)
            del dists[dist_url]
        has_spider.insert_one({'抓取完成城市': city})
        del city_map[city]
    pool.shutdown()