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
            retryWrites="false")['???????????????']['info']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['???????????????']['has_spider']
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
        if city in ['?????????','????????????','??????','??????','??????','?????????','??????','?????????','?????????','??????','????????????','?????????','?????????','??????','??????','?????????','????????????','????????????','??????','??????','?????????','??????','??????']:
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
                print('??????ip?????????20???')
                time.sleep(20)

                num -= 1
        print('??????ip')
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
        print('get_html??????',proxies, e)
        return get_html(url)

def get_Html_IP_xq(url, headers):
    retry_count = 10
    while retry_count > 0:
        proxy = get_proxy()
        if "!" in str(proxy):
            print("??????ip, ??????60s")
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
                print("???????????????,????????????, ??????2???")
                time.sleep(2)
                continue

            if '??????' in response.text:
                t4 = "".join(re.findall("var t4=\'(.*)\';", response.text)[0])
                t3 = "".join(re.findall('var t3=\'(.*)\';', response.text)[-2])
                url = t4 + '?' + t3
                continue

            if  '??????????????????' in response.text or '????????????' in response.text:
                print('????????????, ??????????????????')
                break
            return response

        # ??????3???, ????????????????????????
        delete_proxy(proxy)
        retry_count -= 1
    return None


def get_info_community(url, **kwargs):
    """
    ?????????????????????
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
        return "????????????????????????"
    html = etree.HTML(res.text)

    dd_list = html.xpath("//h3[@class='f16'][contains(text(), '????????????')]/../../div[@class='pdX16']//li")
    item_info = {}
    item_dd = { dd.xpath('string(.)').split('???', 1)[0].replace(' ', ''): dd.xpath('string(.)').split('???', 1)[-1].replace(' ', '') for dd in dd_list}

    item_info['????????????'] = item_dd.get('????????????', None)
    item_info['????????????'] = item_dd.get('????????????', None)
    item_info['????????????'] = item_dd.get('????????????', None)
    item_info['????????????'] = item_dd.get('????????????', None)

    item_info['????????????'] = item_dd.get('????????????', None)
    item_info['????????????'] = item_dd.get('????????????', None)
    item_info['?????????'] = item_dd.get('?????????', None)
    item_info['?????????'] = item_dd.get('?????????', None)
    item_info['?????????'] = item_dd.get('?????????', None)
    item_info['?????????'] = item_dd.get('?????????', None)

    description = "".join(html.xpath("/html/head/meta[@name='description']/@content"))
    item_info['????????????'] = "".join(re.findall("????????????(\d+\.?\d+)????????????", description))
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
    ?????????????????????
    :param city:  ??????
    :param GetType:  ??????(??????)
    :return:
    '''
    dist = make_url(city, 'https://{}.esf.fang.com/housing/{}/', GetType)
    return dist


def get_data(url, baseUrl, city, dist, pageNumber, currPage, item):
    """
    ?????????????????????
    :param url:         ????????????url
    :param baseUrl:     ???url
    :param city:        ??????
    :param dist:        ?????????
    :param pageNumber:  ?????????
    :param currPage:    ????????????
    :return: dataList
    """

    has_spider_urlList = []
    for has_spider_url in has_spider.find():
        has_spider_urlList.append(has_spider_url['??????'])
    if url in has_spider_urlList:
        # print('?????????????????????????????????')
        return

    headers["User-Agent"] = get_ua()
    # res = get_Html_IP_xq(url, headers)
    print('????????????url',url)
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
        print("?????????%s %s, ????????????????????????%s???????????????%d???,  %s" % (city, dist, pageNumber, currPage, url))

    for house in house_box:
        item_dict = {}
        item_dict["??????"] = house.xpath('./dl/dd/p[1]/a[1]/text()')[0]
        city_code = baseUrl.split('.')[0].split('//')[1]
        code = json.loads(house.xpath("./@data-bgcomare")[0]).get('newcode')

        item_dict['??????url'] = "https://m.fang.com/xiaoqu/{city_code}/{community_code}.html".format(
            city_code=city_code, community_code=code)
        item_dict['??????'] = house.xpath('./dl/dd/p[1]/span[1]/text()')[0]
        if item_dict['??????'] not in ['??????', '??????']:
            continue
        try:
            item_dict['??????'] = house.xpath('./div/p[1]/span/text()')[0].strip()
            item_dict['?????????'] = house.xpath('./div/p[2]/span/text()')[0].strip()
        except:
            item_dict['??????'] = None
            item_dict['?????????'] = None
        # item_dict['??????'] = house.xpath('./div/p[1]/span/text()')
        # item_dict['?????????'] = house.xpath('./div/p[2]/span/text()')
        item_dict['????????????'] = house.xpath('./dl/dd/ul/li[1]/a/text()')[0].strip()
        item_dict['????????????'] = house.xpath('./dl/dd/ul/li[2]/a/text()')[0].strip()
        try:
            item_dict['????????????'] = re.findall("\d+", house.xpath('./dl/dd/ul/li[3]/text()')[0])[0]
        except: item_dict['????????????'] = None
        if city == '?????????':
            item_dict['??????'] = dist
        else:
            item_dict['??????'] = city
        item_dict['??????'] = dist
        item_dict['id'] = uuid.uuid1(node=random.randint(1000, 99999))
        try:
            addr = "-".join(house.xpath("./dl/dd/p[2]//a/text()"))
        except:
            addr = ''
        try:
            addrInfo = "".join(house.xpath("./dl/dd/p[2]/text()")).strip().split(' ')[1]
        except:
            addrInfo = ''
        item_dict['??????'] = addr + '-' + addrInfo
        # item_dict['longitude'] = np.NaN
        # item_dict['latitude'] = np.NaN
        # item_dict['date'] = f'{year}-{month}-28'
        # item_dict['????????????'] = year
        # item_dict['????????????'] = month
        item_dict['????????????'] = '?????????'
        community_url = item_dict['??????url']
        item_dict['????????????'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # print("??????-??????: {}-{}, ??????: {}, ??????url: {}".format(city, dist, item_dict['??????'], item_dict['??????url']))
        get_info_community(community_url, Referer=item_dict['??????url'], item=item, item_dict=item_dict)
        print(item_dict)
        if info_base.count_documents({'??????url':item_dict['??????url']}) == 1:
            continue
        info_base.insert_one(item_dict)
    has_spider.insert_one({'??????': url})


def get_street_page(city, street_url, GetType, **kwargs):
    """
    ?????????????????????????????????
    """
    headers['Referer'] = kwargs['Referer']
    res = get_Html_IP_xq(url=street_url, headers=headers)
    if res:
        tree = etree.HTML(res.text)
    else:
        return
    page_number = tree.xpath("//span[@class='txt']/text()")
    # ?????? ???????????????
    if len(page_number) < 1:
        print("????????????")
        return

    page_number = int(page_number[0][1:-1])
    print(city, kwargs['dist'], kwargs['street'], '?????????: ', page_number)

    # ??????????????????url
    data, pools = [], []
    for i in range(1, page_number + 1):
        url = re.sub("0_0_\d+_0_0_0", "0_0_{}_0_0_0".format(i), street_url)

        # TODO ??????
        # get_data(url=url, baseUrl=kwargs['base_url'], city=city, pageNumber=page_number,
        # currPage=i, dist=kwargs['dist'], item=data)

        # ??????????????? url, baseUrl, city, dist, pageNumber, currPage, item
        done = pool.submit(get_data, url, kwargs['base_url'], city, kwargs['dist'], page_number, i, data)
        pools.append(done)
    [obj.result() for obj in pools]

    # try:
    #     print("data?????????", len(data))
    #     useTime = saveData(data, city, GetType)  # ????????????
    #     save_grab_dist(city, kwargs['street'], street_url, GetType)  # ???????????????
    #     print("??????????????????, ??????: ", useTime)
    # 
    # except Exception as e:
    #     print('??????: %s, ??????: %s, ??????????????????, %s' % (city, kwargs['street'], e))
    # finally:
    #     del data



def get_page(city, dist_dict, GetType):
    """
    ???????????????????????????
    """
    for dist_url, dist in dist_dict.items():
        # if dist in get_exists_dist(city, GetType):
        #     print(city, dist, '----->  ????????????')
        #     continue

        base_url = re.findall("https.*com", dist_url)[0]
        print("base_url: ", base_url, "dist_url: ", dist_url)

        # has_spider_urlList = []
        # for has_spider_url in has_spider.find():
        #     has_spider_urlList.append(has_spider_url['??????'])
        # if dist_url in has_spider_urlList:
        #     print('?????????????????????????????????')
        #     break

        # res = get_Html_IP_xq(url=dist_url, headers=headers)
        res = get_html(dist_url)
        if res:
            tree = etree.HTML(res.text)
            # print('res','tree',res,tree)
        else:
            print('????????????')
            break
        page_number = tree.xpath("//span[@class='txt']/text()")
        print('page',page_number)

        # ?????? ???????????????
        if len(page_number) < 1:
            # save_grab_dist(city, dist, dist_url, GetType)
            print("????????????")
            continue

        if '1000' in page_number[0]:
        # if True:
            print(page_number)
            print('??????????????????1000???, ????????????')
            # ??????????????????
            street_xpath = '//*[@id="shangQuancontain"]/a[not(contains(text(), "??????"))]'
            street_dict = dict(zip(tree.xpath(street_xpath + '/text()'), tree.xpath(street_xpath + '/@href')))
            for street, str_url in street_dict.items():
                street_url = base_url + str_url
                print('??????',street, street_url)

                # if street in get_exists_dist(city, GetType):
                #     print(city, street, '----->  ????????????')
                #     continue

                get_street_page(city, street_url, GetType, street=street,
                                Referer=dist_url, dist=dist, base_url=base_url)

        else:
            page_number = int(page_number[0][1:-1])
            print(city, dist, '?????????: ', page_number)

            # ??????????????????url
            data, pools = [], []
            for i in range(1, page_number + 1):
                url = re.sub("0_0_\d+_0_0_0", "0_0_{}_0_0_0".format(i), dist_url)
                done = pool.submit(get_data, url, base_url, city, dist, page_number, i, data)
                pools.append(done)
            [obj.result() for obj in pools]

            # try:
            #     print("data?????????", len(data))
            #     useTime = saveData(data, city, GetType)  # ????????????
            #     save_grab_dist(city, dist, dist_url, GetType)  # ???????????????
            #     print("??????????????????, ??????: ", useTime)
            # 
            # except Exception as e:
            #     print('??????: %s, ??????: %s, ??????????????????, %s' % (city, dist, e))
            # finally:
            #     print()
            #     del data


if __name__ == '__main__':
    # cities = [i.split("_")[1] for i in os.listdir("data1/??????")]
    # cities = [i.split("_")[1] for i in os.listdir("log/??????")]

    # TODO ??????????????????
    # TODO ?????? month?????????????????????
    # TODO ???????????????,?????? log/lose_dist, log/??????  ????????????
    year = 2021
    month = 4
    # city_map=getCity_Code()
    pool = ThreadPoolExecutor(30)
    name = []

    while True:
        data = random.sample(city_map.items(), 1)
        city, city_code = data[0][0], data[0][1]


    # for city, city_code in city_map.items():


        if city == '?????????': continue

        print(city, city_code)
        if city == '??????':
            city_code = 'shaoxing'

        # ??????, ??????  ??????????????????
        if city not in citylist: continue
        if city in ["??????", "??????", '??????', '??????', '??????', '??????', '??????', '??????','??????', '??????', '??????', '??????'
                    '??????', '??????', '??????', '??????', '??????', '??????', '??????', '??????', '??????', '??????', '??????', '??????',
                    '??????', '??????', '??????', '??????', '??????','??????']:
            continue

        # GetType="??????",   ????????????????????????
        dist = get_dist(city, GetType="??????")
        if not dist:
            name.append(city)
        # print('?????????????????????: ', name)

        get_page(city, dist, GetType="??????")

    pool.shutdown()

