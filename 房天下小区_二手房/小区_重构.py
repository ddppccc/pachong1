import json
import random
import re
import time
import uuid
import requests
import pymongo
import numpy as np
from urllib import parse
from lxml import etree
from concurrent.futures.thread import ThreadPoolExecutor
# from IP_config import delete_proxy
from config2 import get_proxy
# from city_map import make_url,city_map,citylist
from config.config import baidu_chang_gaode


def get_ua():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
        'Opera/8.0 (Windows NT 5.1; U; en)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) '
    ]
    user_agent = random.choice(user_agents)
    return user_agent


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
    retryWrites="false")['房天下']['小区_数据_202203']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['房天下']['小区_去重_202203']
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "global_cookie=f1v4y6cur4h7034ieaxs84qnk17jxobmy8b; Integrateactivity=notincludemc; newhouse_user_guid=50E5E180-78E4-4D10-DD8D-77E13BC96848; lastscanpage=0; budgetLayer=1%7Cbj%7C2019-07-30%2011%3A26%3A08; resourceDetail=1; new_search_uid=fd91130e51ddd1f2d8e5a7847545c3d8; __utmc=147393320; logGuid=2b71fa18-f559-46a3-938f-730d9fc95e2b; __utma=147393320.184954923.1564457033.1564980924.1564985308.22; __utmz=147393320.1564985308.22.9.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-verify/redirect; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; city=www; g_sourcepage=esf_xq%5Elb_pc; unique_cookie=U_o2dkb2l6lyxw2toc3w5ox86ek13jyxppisu*58; __utmb=147393320.87.10.1564985308",
    "Referer": "https://esf.fang.com/housing/",
    "upgrade-insecure-requests": "1",
    "User-Agent": get_ua()
}


def getCity_Code():
    item = {}
    response = requests.get('https://www.fang.com/SoufunFamily.htm', headers=headers, timeout=(5, 5))
    response.encoding = 'gbk'
    html = etree.HTML(response.text)
    lists = html.xpath('//div[@class="onCont"]/table//a')  # 获取城市列表 第一个鞍山
    for i in lists:
        city = i.xpath('./text()')[0]  # 鞍山
        url = i.xpath('./@href')[0]  # 获取城市地区    鞍山的url
        code = url.split('.')[0][7:]  # anshan
        # print(city,code,url)
        if city in ['波士顿', '保加利亚', '昌吉', '德国', '海外', '西雅图', '广德', '旧金山', '洛杉矶', '日本', '塞浦路斯', '西雅图', '西班牙', '希腊', '悉尼',
                    '芝加哥', '马来西亚', '澳大利亚', '美国', '纽约', '葡萄牙', '安陆', '蒙城']:
            continue
        item[city] = code
    print(item)
    return item


IpPool = [
    # "192.168.1.104:5010",
    # "118.24.52.95:5010",
    # "47.106.223.4:50002",
    'demo.spiderpy.cn',           #ip代理池
]


# def get_proxy():
#     try:
#         return requests.get(f'http://{random.choice(IpPool)}/get/').json().get('proxy')
#     except:
#         num = 3
#         while num:
#             try:
#                 return requests.get(f'http://{random.choice(IpPool)}/get/').json().get('proxy')
#             except:
#                 print('暂无ip，等待20秒')
#                 time.sleep(20)
#
#                 num -= 1
#         print('暂无ip')
def get_html(url):  # 发起请求
    proxies = {"https": get_proxy()}  #
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)  # 请求各个城市的url
        # response = requests.get(url, headers=headers, timeout=10)
        encod = response.apparent_encoding
        if encod.upper() in ['GB2312', 'WINDOWS-1254']:
            encod = 'gbk'
        if '访问验证-房天下' in response.text:
            # print('访问验证-房天下')
            return get_html(url)
        response.encoding = encod
        return response
    except Exception as e:
        # print('get_html错误',proxies, e)
        time.sleep(2)
        return get_html(url)


def get_zb(city_code, housId):
    url = 'https://ditu.fang.com/?c=channel&a=xiaoquNew&newcode=%s&city=%s&width=1200&height=455&resizePage=///house/web/map_resize.html&category=residence&esf=1' % (
        housId, city_code)         #替换%s的内容 获取各个城市坐标位置url
    res = get_html(url)
    if not res:
        return '', ''
    tree = etree.HTML(res.text)
    location = tree.xpath('/html/body/script[1]/text()')[0].replace('var mainBuilding=', '')[:-1]    #地理编码信息
    true = True
    false = False
    dicts = eval(location)               #  改动处将 json 转为字典类型
    coordx, coordy = dicts['coordx'], dicts['coordy']         #x,y坐标
    return coordx, coordy


def get_info_community(url, **kwargs):  # url为小区详情页url
    """
    获取详情页信息
    """
    headersd = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "cookie": "global_cookie=f1v4y6cur4h7034ieaxs84qnk17jxobmy8b; Integrateactivity=notincludemc; newhouse_user_guid=50E5E180-78E4-4D10-DD8D-77E13BC96848; lastscanpage=0; new_search_uid=5dd284492bf9e36ec3167802eb661d30; vh_newhouse=1_1572405532_2117%5B%3A%7C%40%7C%3A%5D48b328b27aeb63f035147f34d59ab583; SoufunSessionID_Office=1_1575511536_1026; searchConN=1_1575531244_1408%5B%3A%7C%40%7C%3A%5D474a3f1633bc4c0e2c26e7317b0fd256; __utmc=147393320; newhouse_chat_guid=32BA44BA-3F58-32FC-3309-830CB20DA5E9; cloudtypeforb=2; _sf_group_flag=esf; sourcepage=logout_home%5Elb_jingjipc; city=suzhou; __utmz=147393320.1577155662.68.49.utmcsr=sh.esf.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/housing/30__0_39_0_0_20_0_0_0/; jiatxShopWindow=1; mencity=sh; global_wapandm_cookie=x6itqigir4ip23lah2ujdxjr817k4jcnzxp; __jsluid_s=b386beb847ab8e6bb434ec0ad473125b; __utma=147393320.617781738.1569207583.1577164675.1577168002.71; unique_cookie=U_e43nmw5n31o0djlop6gnzpf8n1zk4i1pw9y*157; Captcha=314367386A4D424C476B72384B67632F4866624B4C7144342B49354D53594F7733487A36536751624F703159596863362F7A5668667A55544C4165586958772B44484768374953656964593D; g_sourcepage=esf_xq%5Esy_wap; __utmt_t0=1; __utmt_t1=1; __utmb=147393320.45.10.1577168002; unique_wapandm_cookie=U_x6itqigir4ip23lah2ujdxjr817k4jcnzxp*13",
        "pragma": "no-cache",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Mobile Safari/537.36",
    }
    res = get_html(url)
    if not res:
        return "退出当前详情访问"
    html = etree.HTML(res.text)

    # ‘//*[@id="dsy_D01_03"]/div[1]/a’   主页二手房的xpath

    ###dd_list = html.xpath("//h3[@class='f16'][contains(text(), '基本信息')]/../../div[@class='pdX16']//li")   #请求url为详情页·的url  ?
    dd_list = html.xpath("/html/body/div[3]/div[4]/div[1]/div/div/ul/li")  # 详情页定位 基本信息 均价，地址
    item_info = {}
    # item_dd = { dd.xpath('string(.)').split('：', 1)[0].replace(' ', ''): dd.xpath('string(.)').split('：', 1)[-1].replace(' ', '') for dd in dd_list}
    item_dd = {}
    for dd in dd_list:
        # key = dd.xpath('string(.)').split('：', 1)[0].replace(' ', '')
        # value = dd.xpath('string(.)').split('：', 1)[-1].replace(' ','')
        # item_dd[key] = value
        try:
            key = dd.xpath('./span/text()')[0].replace(' ', '')     #键
            item_dd[key] = dd.xpath('./p/text()')[0]                 #键值
        except:
            continue

        # item_info['产权描述'] = dd.xpath('./span/text()')
        # item_info['物业类型'] = dd.xpath('./div/ul/li[6]/p/text()')
        # item_info['建筑类型'] = dd.xpath('./div/ul/li[8]/p/text()')
        # item_info['建筑面积'] = dd.xpath('./div/ul/li[9]/p/text()')
        #
        # item_info['房屋总数'] = dd.xpath('./div/ul/li[11]/p/text()')
        # item_info['楼栋总数'] = dd.xpath('./div/ul/li[12]/p/text')
        # item_info['绿化率'] = dd.xpath('./div/ul/li[13]/p/text()')
        # item_info['容积率'] = dd.xpath('./div/ul/li[14]/p/text()')
        # item_info['物业费'] = dd.xpath('./div/ul/li[15]/p/text()')
        # item_info['停车位'] = dd.xpath('./div[2]/div/ul/li[6]/p/text()')
        #
        # item_info['占地面积'] = dd.xpath('./div/ul/li[10]/p/text()')

    item_info['产权描述'] = item_dd.get('产权描述', None)
    item_info['物业类型'] = item_dd.get('物业类型', None)
    item_info['建筑类型'] = item_dd.get('建筑类型', None)
    item_info['建筑面积'] = item_dd.get('建筑面积', None)

    item_info['房屋总数'] = item_dd.get('房屋总数', None)
    item_info['楼栋总数'] = item_dd.get('楼栋总数', None)
    item_info['绿化率'] = item_dd.get('绿化率', None)
    item_info['容积率'] = item_dd.get('容积率', None)
    item_info['物业费'] = item_dd.get('物业费', None)
    item_info['停车位'] = item_dd.get('停车位', None)
    item_info['占地面积'] = item_dd.get('占地面积', None)
    # /html/body/div[3]/div[4]/div[1]/div[1]./div/ul/li[4]

    ### description = "".join(html.xpath("/html/head/meta[@name='description']/@content"))
    ###item_info['占地面积'] = "".join(re.findall("占地面积(\d+\.?\d+)平方米，", description))

    # location = "".join(html.xpath("/html/head/meta[@name='location']/@content"))

    long, lat = get_zb(kwargs['city_code'], kwargs['code'])
    kwargs['item_dict']['latitude'], kwargs['item_dict']['longitude'] = baidu_chang_gaode(lat, long)
    kwargs['item_dict'].update(item_info)            #进行修改处
    kwargs['item'].append(kwargs['item_dict'])       #修改处
    return kwargs['item']


def get_regions(city_name, GetType):
    for i in range(10):
        """
        根据城市名获得行政区
        :type  二手房抓取
        :param city_name:
        :return: {'guangming': '光明'}
        """
        # 二手房页面
        if GetType == '二手房':
            url = 'https://{}.esf.fang.com/'.format(city_map[city_name])
            if city_name == '北京':
                url = 'https://esf.fang.com/'
            print('\n将在 %s 爬取行政区' % url)
            res = get_html(url)
            html = etree.HTML(res.text)

            regions_xpath = "//span[contains(text(), '区域')]//following-sibling::ul//a"
            regions = dict(zip(html.xpath(regions_xpath + '/@href'), html.xpath(regions_xpath + '/text()')))
            regions = {key.rsplit('/', 2)[-2]: value for key, value in regions.items() if
                       '周边' not in value and '全部' not in value}
            if not regions:
                continue
            return regions


        else:  # 小区页面
            url = 'https://{}.esf.fang.com/housing/'.format(city_map[city_name])
            if city_name == '北京':
                url = 'https://esf.fang.com/housing/'
            if city_name == '绍兴':
                url = 'https://shaoxing.esf.fang.com/housing/'
            print('\n将在 %s 爬取行政区' % url)

            res = get_html(url)
            html = etree.HTML(res.text)

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

            if not regions:
                continue
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
            dist = make_url(city, 'https://{}.esf.fang.com/housing/{}/', GetType)
            return dist

        except:
            number -= 1
            continue
    print('获取区域失败')


def get_data(url, baseUrl, city, dist, pageNumber, currPage, item):
    """
    解析每一个页面
    :param url:         每一页的url
    :param baseUrl:     根url
    :param city:        城市
    :param dist:        行政区
    :param pageNumber:  总页数
    :param currPage:    当前页数
    :return: dataList
    """
    number_tz = 0
    while True:
        if has_spider.find_one({'标题': url}):
            print('该页数据已爬取，下一页')
            return

        headers["User-Agent"] = get_ua()
        # print('每个页面url',url)
        res = get_html(url)
        if res:
            tree = etree.HTML(res.text)
        else:
            return
        number_tz += 1

        try:
            house_box = tree.xpath('//div[@class="houseList"]/div[@dataflag="bgcomare"]')
        except:
            print('获取house_box出错')
            return
        try:
            x = house_box[0]
        except Exception as e:
            print(e, url)
            if number_tz > 3:
                break
            continue
        # if house_box:
        #     print("城市：%s %s, 状态：有数据，共%s页，当前第%d页,  %s" % (city, dist, pageNumber, currPage, url))

        for house in house_box:
            item_dict = {}
            try:
                item_dict["小区"] = house.xpath('./dl/dd/p[1]/a[1]/text()')[0]
            except:
                continue
            city_code = baseUrl.split('.')[0].split('//')[1]
            code = json.loads(house.xpath("./@data-bgcomare")[0]).get('newcode')
            item_dict['小区url'] = 'https://{city_code}.esf.fang.com/loupan/{community_code}/housedetail.htm'.format(
                city_code=city_code, community_code=code)
            # item_dict['小区url'] = "https://m.fang.com/xiaoqu/{city_code}/{community_code}.html".format(
            #     city_code=city_code, community_code=code)        #城市编码，地址 小区url
            item_dict['类型'] = house.xpath('./dl/dd/p[1]/span[1]/text()')[0]
            if item_dict['类型'] not in ['住宅', '别墅']:
                continue
            try:
                item_dict['单价'] = house.xpath('./div/p[1]/span/text()')[0].strip()
                item_dict['涨跌幅'] = house.xpath('./div/p[2]/span/text()')[0].strip()
            except:
                item_dict['单价'] = None
                item_dict['涨跌幅'] = None
            # item_dict['单价'] = house.xpath('./div/p[1]/span/text()')
            # item_dict['涨跌幅'] = house.xpath('./div/p[2]/span/text()')
            item_dict['在售套数'] = house.xpath('./dl/dd/ul/li[1]/a/text()')[0].strip()
            item_dict['在租套数'] = house.xpath('./dl/dd/ul/li[2]/a/text()')[0].strip()
            try:
                item_dict['建筑年份'] = re.findall("\d+", house.xpath('./dl/dd/ul/li[3]/text()')[0])[0]
            except:
                item_dict['建筑年份'] = None
            if city == '海南省':
                item_dict['城市'] = dist
            else:
                item_dict['城市'] = city
            item_dict['区县'] = dist
            item_dict['id'] = uuid.uuid1(node=random.randint(1000, 99999))
            try:
                addr = "-".join(house.xpath("./dl/dd/p[2]//a/text()"))
            except:
                addr = ''
            try:
                addrInfo = "".join(house.xpath("./dl/dd/p[2]/text()")).strip().split(' ')[1]
            except:
                addrInfo = ''
            item_dict['地址'] = addr + '-' + addrInfo
            # item_dict['longitude'] = np.NaN
            # item_dict['latitude'] = np.NaN
            # item_dict['date'] = f'{year}-{month}-28'
            # item_dict['抓取年份'] = year
            # item_dict['抓取月份'] = month
            item_dict['数据来源'] = '房天下'
            community_url = item_dict['小区url']
            item_dict['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # print("城市-区县: {}-{}, 小区: {}, 小区url: {}".format(city, dist, item_dict['小区'], item_dict['小区url']))
            get_info_community(community_url, Referer=item_dict['小区url'], item=item, item_dict=item_dict, code=code,
                               city_code=city_code)

            info_base.insert_one(item_dict)
            info_base.update_one({'小区url': item_dict['小区url']}, {'$set':item_dict})
            # sum.append(1)
            # print(len(sum),item_dict)

        print("城市：%s %s, 状态：有数据，共%s页，当前第%d页,  %s" % (city, dist, pageNumber, currPage, url), len(house_box))
        has_spider.insert_one({'标题': url})
        break


def get_street_page(city, street_url, GetType, **kwargs):
    """
    获取每个街道下面的页面
    """
    number_tz = 0
    while True:
        headers['Referer'] = kwargs['Referer']
        res = get_html(street_url)
        if res:
            tree = etree.HTML(res.text)
        else:
            return
        page_number = tree.xpath("//span[@class='txt']/text()")
        # 判断 有没有数据
        number_tz += 1
        if '跳转' in tree.xpath("//title/text()")[0]:
            print(tree.xpath("//title/text()")[0], "%s :出现跳转页面" % dist)
            if number_tz > 3:
                break
            continue
        if '很抱歉，没有找到' in res.text:
            if number_tz > 3:
                break
            continue

        page_number = int(page_number[0][1:-1])
        print(city, kwargs['dist'], kwargs['street'], '页码数: ', page_number)

        # 请求每一页的url
        data, pools = [], []
        for i in range(1, page_number + 1):
            url = re.sub("0_0_\d+_0_0_0", "0_0_{}_0_0_0".format(i), street_url)

            # TODO 原生
            # get_data(url=url, baseUrl=kwargs['base_url'], city=city, pageNumber=page_number,
            # currPage=i, dist=kwargs['dist'], item=data)

            # 启用线程池 url, baseUrl, city, dist, pageNumber, currPage, item
            done = pool.submit(get_data, url, kwargs['base_url'], city, kwargs['dist'], page_number, i, data)
            pools.append(done)
        [obj.result() for obj in pools]
        break


def get_page(city, dist_dict, GetType):
    """
    获取每个区下的页面
    """
    # for dist_url, dist in dist_dict.items():
    while dist_dict:
        data2 = random.sample(dist_dict.items(), 1)
        dist_url, dist = data2[0][0], data2[0][1]

        if has_spider.find_one({'区域url': dist_url}):
            print('该区域已抓取')
            del dist_dict[dist_url]
            continue

        base_url = re.findall("https.*com", dist_url)[0]
        print("base_url: ", base_url, "dist_url: ", dist_url)
        number_tz = 0
        while True:

            res = get_html(dist_url)
            if res:
                tree = etree.HTML(res.text)
                # print('res','tree',res,tree)
            else:
                print('抓取失败')
                break
            page_number = tree.xpath("//span[@class='txt']/text()")
            # print('page',page_number)

            # 判断 有没有数据
            number_tz += 1
            if '跳转' in tree.xpath("//title/text()")[0]:
                print(tree.xpath("//title/text()")[0], "%s :出现跳转页面" % dist)
                if number_tz > 5:
                    break
                continue
            if '很抱歉，没有找到' in res.text:
                if number_tz > 3:
                    has_spider.insert_one({'区域url': dist_url})
                    print('页面没有内容')
                    break
                continue
            try:
                page_number = int(page_number[0][1:-1])
            except:
                if number_tz > 3:
                    print('获取页数失败')
                    break
                continue
            if page_number > 99:
                # if True:
                print(page_number)
                print('当前页数大于100页, 分页抓取')
                # 获取街道信息
                street_xpath = '//*[@id="shangQuancontain"]/a[not(contains(text(), "不限"))]'
                street_dict = dict(zip(tree.xpath(street_xpath + '/text()'), tree.xpath(street_xpath + '/@href')))
                print(street_dict)
                for street, str_url in street_dict.items():
                    street_url = base_url + str_url
                    print('街道', street, street_url)

                    get_street_page(city, street_url, GetType, street=street,
                                    Referer=dist_url, dist=dist, base_url=base_url)
                has_spider.insert_one({'区域url': dist_url})

            else:

                print(city, dist, '页码数: ', page_number)

                # 请求每一页的url
                data, pools = [], []
                for i in range(1, page_number + 1):
                    url = re.sub("0_0_\d+_0_0_0", "0_0_{}_0_0_0".format(i), dist_url)
                    done = pool.submit(get_data, url, base_url, city, dist, page_number, i, data)
                    pools.append(done)
                [obj.result() for obj in pools]
                has_spider.insert_one({'区域url': dist_url})
            break
        del dist_dict[dist_url]


if __name__ == '__main__':
    # get_info_community('https://sh.esf.fang.com/loupan/1210012000/housedetail.htm', city_code='sh', code='1210012000')
    # TODO 小区启动程序
    # TODO 直接 month为要抓取的月份
    # TODO 每月启动前,清空 log/lose_dist, log/小区  中的文件
    year = 2022
    month = 2
    with open('city_map.json', 'r', encoding='utf-8') as f:
        city_map = json.load(f)
    # city_map=getCity_Code()
    pool = ThreadPoolExecutor(30)
    name = []
    sum = []
    # print(info_base.count_documents({}))
    while city_map:
        data = random.sample(city_map.items(), 1)
        city, city_code = data[0][0], data[0][1]
        # city, city_code = '北京','bj'
        # city, city_code = '扬州','yz'
        # city, city_code = '重庆','cq'

        if city == '海南省':
            del city_map[city]
            continue

        print(city, city_code)
        if city == '绍兴':
            city_code = 'shaoxing'

        # 罗定, 望城  无用效的城市
        if city in ['波士顿', '保加利亚', '昌吉', '德国', '海外', '西雅图', '广德', '旧金山', '洛杉矶', '日本', '塞浦路斯', '西雅图',
                    '西班牙', '希腊', '悉尼', '芝加哥', '马来西亚', '澳大利亚', '美国', '纽约', '葡萄牙', '安陆', '蒙城']:
            del city_map[city]
            continue
        if city in ["罗定", "望城", '安宁', '霸州', '博罗', '长岛', '昌都', '长寿', '万州', '文安', '吴江', '新建'
                                                                                      '定州', '丰都', '奉化', '涪陵', '合川',
                    '惠东', '江都', '江津', '金坛', '莱芜', '临安', '黔江',
                    '綦江', '三河', '上虞', '顺德', '香港', '东兴']:
            del city_map[city]
            continue
        if has_spider.find_one({'抓取完成城市': city}):
            print('该城市已抓取完成')
            del city_map[city]
            continue
        # GetType="小区",   抓取的是小区数据
        dist = get_dist(city, GetType="小区")
        if not dist:
            name.append(city)
        # print('没有小区的城市: ', name)
        # print('dist',dist)
        get_page(city, dist, GetType="小区")
        has_spider.insert_one({'抓取完成城市': city})
    pool.shutdown()
