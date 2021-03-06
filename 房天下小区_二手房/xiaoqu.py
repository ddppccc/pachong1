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

from IP_config import delete_proxy
from city_map import make_url,city_map,citylist
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
            retryWrites="false")['房天下小区']['info']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['房天下小区']['has_spider']
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
    item={}
    response = requests.get('https://www.fang.com/SoufunFamily.htm', headers=headers, timeout=(5, 5))
    response.encoding = 'gbk'
    html = etree.HTML(response.text)
    lists=html.xpath('//div[@class="onCont"]/table//a')
    for i in lists:
        city=i.xpath('./text()')[0]
        url=i.xpath('./@href')[0]
        code=url.split('.')[0][7:]
        # print(city,code,url)
        if city in ['波士顿','保加利亚','昌吉','德国','海外','西雅图','广德','旧金山','洛杉矶','日本','塞浦路斯','西雅图','西班牙','希腊','悉尼','芝加哥','马来西亚','澳大利亚','美国','纽约','葡萄牙','安陆','蒙城']:
            continue
        item[city]=code
    print(item)
    return item


def get_proxy():
    try:
            return requests.get('http://47.106.223.4:50002/get/').json().get('proxy')
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
def get_html(url):
    proxies = {"https": get_proxy()}
    try:
        response = requests.get(url, headers=headers,proxies=proxies, timeout=10)
        encod = response.apparent_encoding
        if encod.upper() in ['GB2312', 'WINDOWS-1254']:
            encod = 'gbk'
        response.encoding = encod
        return response
    except Exception as e:
        print('get_html错误',proxies, e)
        return get_html(url)

def get_Html_IP_xq(url, headers):
    retry_count = 10
    while retry_count > 0:
        proxy = get_proxy()
        if "!" in str(proxy):
            print("没有ip, 等待60s")
            time.sleep(60)
        number = 3
        while number > 0:
            try:
                response = requests.get(url, headers=headers, timeout=(10,10), proxies={'http': 'http://%s'%proxy, 'https': 'https://%s'%proxy})
                encod = response.apparent_encoding

                if encod in ['GB2312', 'Windows-1254']  :
                    encod = 'gbk'
                response.encoding = encod
            except Exception as e:
                number -= 1
                continue

            if response.status_code == 502:
                print("服务器错误,重新请求, 等待2秒")
                time.sleep(2)
                continue

            if '跳转' in response.text:
                t4 = "".join(re.findall("var t4=\'(.*)\';", response.text)[0])
                t3 = "".join(re.findall('var t3=\'(.*)\';', response.text)[-2])
                url = t4 + '?' + t3
                continue

            if  '璁块棶楠岃瘉' in response.text or '访问验证' in response.text:
                print('需要验证, 出现搜索引擎')
                break
            return response

        # 出错3次, 删除代理池中代理
        delete_proxy(proxy)
        retry_count -= 1
    return None


def get_info_community(url, **kwargs):
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
    # res = get_Html_IP_xq(url, headersd)
    res = get_html(url)
    if not res:
        return "退出当前详情访问"
    html = etree.HTML(res.text)

    dd_list = html.xpath("//h3[@class='f16'][contains(text(), '基本信息')]/../../div[@class='pdX16']//li")
    item_info = {}
    item_dd = { dd.xpath('string(.)').split('：', 1)[0].replace(' ', ''): dd.xpath('string(.)').split('：', 1)[-1].replace(' ', '') for dd in dd_list}

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

    description = "".join(html.xpath("/html/head/meta[@name='description']/@content"))
    item_info['占地面积'] = "".join(re.findall("占地面积(\d+\.?\d+)平方米，", description))
    location = "".join(html.xpath("/html/head/meta[@name='location']/@content"))

    try:
        long, lat = re.findall("coord=(\d+\.?\d+),(\d+\.?\d+)", location)[0]
    except:
        long, lat = '', ''
    kwargs['item_dict']['latitude'], kwargs['item_dict']['longitude'] = baidu_chang_gaode(lat, long)
    kwargs['item_dict'].update(item_info)
    kwargs['item'].append(kwargs['item_dict'])
    return kwargs['item']


def get_dist(city, GetType):
    '''
    生成行政区字典
    :param city:  城市
    :param GetType:  类型(小区)
    :return:
    '''
    dist = make_url(city, 'https://{}.esf.fang.com/housing/{}/', GetType)
    return dist


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

    has_spider_urlList = []
    for has_spider_url in has_spider.find():
        has_spider_urlList.append(has_spider_url['标题'])
    if url in has_spider_urlList:
        # print('该页数据已爬取，下一页')
        return

    headers["User-Agent"] = get_ua()
    # res = get_Html_IP_xq(url, headers)
    print('每个页面url',url)
    res = get_html(url)
    if res:
        tree = etree.HTML(res.text)
    else:
        return

    try:
        house_box = tree.xpath('//div[@class="houseList"]/div[@dataflag="bgcomare"]')
    except:
        return
    if house_box:
        print("城市：%s %s, 状态：有数据，共%s页，当前第%d页,  %s" % (city, dist, pageNumber, currPage, url))

    for house in house_box:
        item_dict = {}
        item_dict["小区"] = house.xpath('./dl/dd/p[1]/a[1]/text()')[0]
        city_code = baseUrl.split('.')[0].split('//')[1]
        code = json.loads(house.xpath("./@data-bgcomare")[0]).get('newcode')

        item_dict['小区url'] = "https://m.fang.com/xiaoqu/{city_code}/{community_code}.html".format(
            city_code=city_code, community_code=code)
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
        except: item_dict['建筑年份'] = None
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
        get_info_community(community_url, Referer=item_dict['小区url'], item=item, item_dict=item_dict)
        print(item_dict)
        if info_base.count_documents({'小区url':item_dict['小区url']}) == 1:
            continue
        info_base.insert_one(item_dict)
    has_spider.insert_one({'标题': url})


def get_street_page(city, street_url, GetType, **kwargs):
    """
    获取每个街道下面的页面
    """
    headers['Referer'] = kwargs['Referer']
    res = get_Html_IP_xq(url=street_url, headers=headers)
    if res:
        tree = etree.HTML(res.text)
    else:
        return
    page_number = tree.xpath("//span[@class='txt']/text()")
    # 判断 有没有数据
    if len(page_number) < 1:
        print("没有数据")
        return

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

    # try:
    #     print("data数据量", len(data))
    #     useTime = saveData(data, city, GetType)  # 保存数据
    #     save_grab_dist(city, kwargs['street'], street_url, GetType)  # 保存行政区
    #     print("数据保存成功, 用时: ", useTime)
    # 
    # except Exception as e:
    #     print('城市: %s, 区域: %s, 数据保存失败, %s' % (city, kwargs['street'], e))
    # finally:
    #     del data



def get_page(city, dist_dict, GetType):
    """
    获取每个区下的页面
    """
    for dist_url, dist in dist_dict.items():
        # if dist in get_exists_dist(city, GetType):
        #     print(city, dist, '----->  已经存在')
        #     continue

        base_url = re.findall("https.*com", dist_url)[0]
        print("base_url: ", base_url, "dist_url: ", dist_url)

        # has_spider_urlList = []
        # for has_spider_url in has_spider.find():
        #     has_spider_urlList.append(has_spider_url['标题'])
        # if dist_url in has_spider_urlList:
        #     print('该页数据已爬取，下一页')
        #     break

        # res = get_Html_IP_xq(url=dist_url, headers=headers)
        res = get_html(dist_url)
        if res:
            tree = etree.HTML(res.text)
            # print('res','tree',res,tree)
        else:
            print('抓取失败')
            break
        page_number = tree.xpath("//span[@class='txt']/text()")
        print('page',page_number)

        # 判断 有没有数据
        if len(page_number) < 1:
            # save_grab_dist(city, dist, dist_url, GetType)
            print("没有数据")
            continue

        if '1000' in page_number[0]:
        # if True:
            print(page_number)
            print('当前页数大于1000页, 分页抓取')
            # 获取街道信息
            street_xpath = '//*[@id="shangQuancontain"]/a[not(contains(text(), "不限"))]'
            street_dict = dict(zip(tree.xpath(street_xpath + '/text()'), tree.xpath(street_xpath + '/@href')))
            for street, str_url in street_dict.items():
                street_url = base_url + str_url
                print('街道',street, street_url)

                # if street in get_exists_dist(city, GetType):
                #     print(city, street, '----->  已经存在')
                #     continue

                get_street_page(city, street_url, GetType, street=street,
                                Referer=dist_url, dist=dist, base_url=base_url)

        else:
            page_number = int(page_number[0][1:-1])
            print(city, dist, '页码数: ', page_number)

            # 请求每一页的url
            data, pools = [], []
            for i in range(1, page_number + 1):
                url = re.sub("0_0_\d+_0_0_0", "0_0_{}_0_0_0".format(i), dist_url)
                done = pool.submit(get_data, url, base_url, city, dist, page_number, i, data)
                pools.append(done)
            [obj.result() for obj in pools]

            # try:
            #     print("data数据量", len(data))
            #     useTime = saveData(data, city, GetType)  # 保存数据
            #     save_grab_dist(city, dist, dist_url, GetType)  # 保存行政区
            #     print("数据保存成功, 用时: ", useTime)
            # 
            # except Exception as e:
            #     print('城市: %s, 区域: %s, 数据保存失败, %s' % (city, dist, e))
            # finally:
            #     print()
            #     del data


if __name__ == '__main__':
    # cities = [i.split("_")[1] for i in os.listdir("data1/小区")]
    # cities = [i.split("_")[1] for i in os.listdir("log/小区")]

    # TODO 小区启动程序
    # TODO 直接 month为要抓取的月份
    # TODO 每月启动前,清空 log/lose_dist, log/小区  中的文件
    year = 2021
    month = 4
    # city_map=getCity_Code()
    pool = ThreadPoolExecutor(30)
    name = []

    while True:
        data = random.sample(city_map.items(), 1)
        city, city_code = data[0][0], data[0][1]


    # for city, city_code in city_map.items():


        if city == '海南省': continue

        print(city, city_code)
        if city == '绍兴':
            city_code = 'shaoxing'

        # 罗定, 望城  无用效的城市
        if city not in citylist: continue
        if city in ["罗定", "望城", '安宁', '霸州', '博罗', '长岛', '昌都', '长寿','万州', '文安', '吴江', '新建'
                    '定州', '丰都', '奉化', '涪陵', '合川', '惠东', '江都', '江津', '金坛', '莱芜', '临安', '黔江',
                    '綦江', '三河', '上虞', '顺德', '香港','东兴']:
            continue

        # GetType="小区",   抓取的是小区数据
        dist = get_dist(city, GetType="小区")
        if not dist:
            name.append(city)
        # print('没有小区的城市: ', name)

        get_page(city, dist, GetType="小区")

    pool.shutdown()

