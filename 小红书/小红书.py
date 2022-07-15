import json
import os
import random
import time

import pandas as pd
import requests
import re
requests.packages.urllib3.disable_warnings()
from concurrent.futures.thread import ThreadPoolExecutor
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

# 建立连接
info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['小红书']['数据_202108']
url_data = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['小红书']['url_202108']

def get_proxy():
    return requests.get("http://47.106.223.4:50002/get/").json().get('proxy')
    # return requests.get("http://192.168.88.51:5010/get/").json().get('proxy')
    # return requests.get("http://127.0.0.1:5010/get/").json().get('proxy')


def delete_proxy(proxy):
    html = requests.get("http://47.106.223.4:50002/delete/?proxy={}".format(proxy))
    # html = requests.get("http://192.168.88.51:5010/delete/?proxy={}".format(proxy))
    # html = requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
    return html.text

# 创建UA池
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
    user_agent = random.choice(user_agents)  # random.choice(),从列表中随机抽取一个对象
    return user_agent


def get_(url, proxieslist):
    s = 0
    while True:
        try:
            headers = {
                'User-Agent': get_ua()
            }
            if len(proxieslist) > 0:
                proxies = proxieslist
            else:
                proxy = get_proxy()
                proxies = {"https": proxy ,"http": proxy}
            response = requests.get(url, headers=headers,proxies=proxies, verify=False, timeout=(2, 5))
            encod = response.apparent_encoding
            if encod.upper() in ['GB2312', 'WINDOWS-1254']:
                encod = 'gbk'
            response.encoding = encod
            if '正在加载' in response.text:
                print('详情信息: 出现验证', )
                proxieslist = []
                continue
            proxieslist = proxies
            print(s, proxies, '获取成功')
            return response, proxieslist
        except Exception as e:
            s += 1
            proxieslist = []

            # print('get_html错误', e)
            continue
# def get_(url):
#     # """
#     ip_number = 10
#     while ip_number > 0:
#         proxy = get_proxy()
#         if not proxy:
#             print("没有ip, 等待2分钟")
#             time.sleep(120)
#
#         number = 2
#         while number > 0:
#             headers = {
#                 'User-Agent': get_ua()
#             }
#             try:
#                 res = requests.get(url, headers=headers,proxies={
#                                            "https": "https://{}".format(proxy),
#                                            "http": "http://{}".format(proxy)
#                                         }, verify=False, timeout=(2, 5))
#                 if '正在加载' in res.text:
#                     print('详情信息: 出现验证', )
#                     break
#                 return res
#             except Exception as e:
#                 number -= 1
#                 # print('error!! ', e)
#                 continue
#         delete_proxy(proxy)
#         ip_number -= 1
#         continue
#     return ''
#     # """
#     """
#     while True:
#         headers = {
#             'Host': 'www.xiaohongshu.com',
#             'User-Agent': get_ua()
#         }
#         try:
#             res = requests.get(url, headers=headers, verify=False, timeout=(2, 5))
#             if '正在加载' in res.text:
#                 print('详情信息: 出现验证', )
#                 input('详情出现验证码: ')
#                 continue
#             return res
#         except Exception as e:
#             # print('详情error!! ', e)
#             continue
#         """

def get_html(page, label_id, label, lon, lat, proxieslist):
    s = 0
    url = 'https://www.xiaohongshu.com/web_api/sns/v1/page/poi/5a4b1086800086366cca864e/list?page={page}&page_size=20&req_type=nearby_filters&orig_filter_id={label_id}&latitude={lat}&longitude={lon}&search_id=b3187ee1-bc9f-4cae-a70d-f08aec08550f&sort_by=smart&category_id=&region_id='.format( page=page, label_id=label_id, lat=lat, lon=lon )
    print(url)

    # 根据url查重
    if url_data.find_one({'已爬取的url': url}):
        print('已爬取')
        return proxieslist

    count = 0
    ip_number = 10
    while ip_number > 0:
        headers = {
            'Referer': 'https://www.xiaohongshu.com/page/cities/5a4b1086800086366cca864e/nearby?naviHidden=yes',
            "Accept-Language": "zh-CN,zh;q=0.9",
            "upgrade-insecure-requests": "1",
            "Accept-Encoding": "gzip, deflate, br",
            'User-Agent': get_ua()
        }
        if count > 1:        #没有获取值的时候
            print('结束')
            return proxieslist     #将会返回前面得到的 proxieslist 值
        try:
            # print("proxy: ",proxy)

            if len(proxieslist) > 0:
                proxies = proxieslist
            else:
                proxy = get_proxy()
                proxies = {"https": proxy, "http": proxy}
            res = requests.get(url, headers=headers, proxies=proxies, verify=False, timeout=(2, 5))
            resJson = res.json()
            if not resJson['data']:
                count += 1           #没有获取值的时候 count=1 再次执行的时候 直接返回
                proxieslist = []
                print('没有data')
                s += 1
                continue

            yztext = res.text
            if 'data' not in yztext:
                s += 1
                ip_number -= 1
                print('出现滑动验证', ip_number, res.text, proxies)
                continue
            print(s, proxieslist)
            proxieslist = parse(resJson, label, proxieslist)
            url_data.insert_one({'已爬取的url':url})
            return proxieslist
        except Exception as e:
            # print('error!!!', e)
            proxieslist = []
            s += 1
            continue
    return proxieslist


def parse(response, label, proxieslist):
    data_list = response['data']
    if not data_list:
        print('没有数据')
        return proxieslist
    for data in data_list:
        item = {}
        item['_id'] = data['id']
        item['id'] = data['id']
        item['label'] = label
        item['page_id'] = data['page_id']
        item['名称'] = data.get('name')
        item['商区'] = data.get('hub')
        item['描述'] = data.get('desc')
        item['类别'] = data.get('sub_category')
        item['推荐人数'] = data.get('discuss_num')
        item['人均'] = data.get('price')
        item['特色'] = "|".join(data['recommend_dishes'])
        item['详情链接'] = 'https://www.xiaohongshu.com/page/restaurants/{}?naviHidden=yes'.format(item['page_id'])
        item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # get_info(item['详情链接'], item, data_all)
        # item.update(d)
        # print(item)
        # data_all.append(item)
        proxieslist = get_info(item['详情链接'], item, proxieslist)
    return proxieslist
    # return data_all

def get_info(url, item, proxieslist):
    res, proxieslist = get_(url, proxieslist)
    address = re.findall('"address":"(.*)","coordinate"', res.text)
    latitude = re.findall('"latitude":(.*),"longitude', res.text)
    longitude = re.findall('longitude":(.*)},"telephone', res.text)
    telephone = re.findall('telephone":(.*),"openingHours', res.text)
    openingHours = re.findall('openingHours":"(.*)","perCapitaPrice', res.text)
    # print(url)
    item['地址'] = "".join(address)
    item['latitude'] = "".join(latitude)
    item['longitude'] = "".join(longitude)
    item['电话'] = "".join(telephone)[2:-2]
    item['营业时间'] = "".join(openingHours)
    print(item)
    #保存数据
    info_base.insert_one(item)
    return proxieslist


def run(city, lon, lat, proxieslist):
    p = []
    label_dict = {
        "拍照地": "local.photo",
        "餐厅": "local.restaurant",
        "玩乐": "local.fun",
        "景点": "local.view",
        "周边游": "local.around",
        "逛街": "local.shop",
        "下午茶": "local.coffee",
        "展馆": "local.show",
        "变美": "local.beauty",
        "酒店": "local.hotel"
    }
    for label, label_id in label_dict.items():
        for page in range(1, 200):
            # if page != 100:continue

            print(city, '页数: ', page, label, label_id,)  # 获取到数据
            dd = pool.submit(get_html, page, label_id, label, lon, lat, proxieslist)
            # print(item)
            p.append(dd)
    proxieslist = [obj.result() for obj in p][-1]
    return proxieslist



if __name__ == '__main__':
    # url_data.delete_many({})
    # info_base.delete_many({})
    pool = ThreadPoolExecutor(20)
    a = '''121.487899486 31.24916171 上海-上海市
100.092612914 23.8878061038 云南省-临沧市
100.229628399 26.8753510895 云南省-丽江市
99.1779956133 25.1204891962 云南省-保山市
100.223674789 25.5968996394 云南省-大理白族自治州
98.5894342874 24.441239663 云南省-德宏傣族景颇族自治州
98.8599320425 25.8606769782 云南省-怒江傈僳族自治州
104.246294318 23.3740868504 云南省-文山壮族苗族自治州
102.714601139 25.0491531005 云南省-昆明市
103.725020656 27.3406329636 云南省-昭通市
100.98005773 22.7887777801 云南省-普洱市
103.782538888 25.5207581429 云南省-曲靖市
101.529382239 25.0663556742 云南省-楚雄彝族自治州
102.545067892 24.3704471344 云南省-玉溪市
103.384064757 23.3677175165 云南省-红河哈尼族彝族自治州
100.803038275 22.0094330022 云南省-西双版纳傣族自治州
99.7136815989 27.8310294612 云南省-迪庆藏族自治州
113.112846391 41.0223629468 内蒙古自治区-乌兰察布市
106.831999097 39.6831770068 内蒙古自治区-乌海市
122.048166514 46.0837570652 内蒙古自治区-兴安盟
109.846238532 40.6471194257 内蒙古自治区-包头市
119.760821794 49.2016360546 内蒙古自治区-呼伦贝尔市
111.66035052 40.8283188731 内蒙古自治区-呼和浩特市
107.42380672 40.7691799024 内蒙古自治区-巴彦淖尔市
118.930761192 42.2971123203 内蒙古自治区-赤峰市
122.260363263 43.633756073 内蒙古自治区-通辽市
109.993706251 39.8164895606 内蒙古自治区-鄂尔多斯市
116.027339689 43.9397048423 内蒙古自治区-锡林郭勒盟
105.695682871 38.8430752644 内蒙古自治区-阿拉善盟
116.395645038 39.9299857781 北京-北京市
119.337634104 26.0911937119 台湾省-台中市
114.130474436 22.3748329286 台湾省-台北市
121.360525873 38.9658447898 台湾省-台南市
114.246701335 22.7288657203 台湾省-嘉义市
111.590952812 21.9464822541 台湾省-高雄市
126.564543989 43.8719883344 吉林省-吉林市
124.391382074 43.1755247011 吉林省-四平市
129.485901958 42.8964136037 吉林省-延边朝鲜族自治州
124.832994532 45.1360489701 吉林省-松原市
122.840776679 45.6210862752 吉林省-白城市
126.435797675 41.945859397 吉林省-白山市
125.133686052 42.9233026191 吉林省-辽源市
125.942650139 41.7363971299 吉林省-通化市
125.313642427 43.8983376071 吉林省-长春市
103.760824239 29.6009576111 四川省-乐山市
105.073055992 29.5994615348 四川省-内江市
102.259590803 27.8923929037 四川省-凉山彝族自治州
106.105553984 30.8009651682 四川省-南充市
104.633019062 28.7696747963 四川省-宜宾市
106.757915842 31.8691891592 四川省-巴中市
105.81968694 32.4410401584 四川省-广元市
106.635720331 30.4639838879 四川省-广安市
104.402397818 31.1311396527 四川省-德阳市
104.067923463 30.6799428454 四川省-成都市
101.722423152 26.5875712571 四川省-攀枝花市
105.443970289 28.8959298039 四川省-泸州市
101.969232063 30.0551441144 四川省-甘孜藏族自治州
103.841429563 30.0611150799 四川省-眉山市
104.705518975 31.5047012581 四川省-绵阳市
104.776071339 29.3591568895 四川省-自贡市
104.635930302 30.132191434 四川省-资阳市
107.494973447 31.2141988589 四川省-达州市
105.564887792 30.5574913504 四川省-遂宁市
102.228564689 31.9057628583 四川省-阿坝藏族羌族自治州
103.009356466 29.9997163371 四川省-雅安市
117.210813092 39.1439299033 天津-天津市
105.196754199 37.5211241916 宁夏回族自治区-中卫市
106.208254199 37.9935610029 宁夏回族自治区-吴忠市
106.285267996 36.0215234807 宁夏回族自治区-固原市
106.379337202 39.0202232836 宁夏回族自治区-石嘴山市
106.206478608 38.5026210119 宁夏回族自治区-银川市
115.787928245 33.8712105653 安徽省-亳州市
116.505252683 31.7555583552 安徽省-六安市
117.282699092 31.8669422607 安徽省-合肥市
117.058738772 30.5378978174 安徽省-安庆市
118.752096311 30.9516423543 安徽省-宣城市
116.988692412 33.6367723858 安徽省-宿州市
117.494476772 30.6600192482 安徽省-池州市
116.791447429 33.9600233054 安徽省-淮北市
117.018638863 32.6428118237 安徽省-淮南市
118.324570351 32.3173505954 安徽省-滁州市
118.384108423 31.3660197875 安徽省-芜湖市
117.357079866 32.9294989067 安徽省-蚌埠市
117.819428729 30.9409296947 安徽省-铜陵市
115.820932259 32.9012113306 安徽省-阜阳市
118.515881847 31.6885281589 安徽省-马鞍山市
118.293569632 29.7344348562 安徽省-黄山市
118.583926333 37.4871211553 山东省-东营市
118.340768237 35.0724090744 山东省-临沂市
122.093958366 37.5287870813 山东省-威海市
116.328161364 37.4608259263 山东省-德州市
119.507179943 35.4202251931 山东省-日照市
117.279305383 34.8078830784 山东省-枣庄市
117.089414917 36.1880777589 山东省-泰安市
117.024967066 36.6827847272 山东省-济南市
116.600797625 35.4021216643 山东省-济宁市
118.059134278 36.8046848542 山东省-淄博市
117.968292415 37.4053139418 山东省-滨州市
119.142633823 36.7161148731 山东省-潍坊市
121.30955503 37.5365615629 山东省-烟台市
115.986869139 36.4558285147 山东省-聊城市
117.684666912 36.2336541336 山东省-莱芜市
115.463359775 35.2624404961 山东省-菏泽市
120.384428184 36.1052149013 山东省-青岛市
111.538787596 36.0997454436 山西省-临汾市
111.143156602 37.527316097 山西省-吕梁市
113.290508673 40.1137444997 山西省-大同市
112.550863589 37.890277054 山西省-太原市
112.727938829 38.461030573 山西省-忻州市
112.7385144 37.6933615268 山西省-晋中市
112.867332758 35.4998344672 山西省-晋城市
112.479927727 39.3376719662 山西省-朔州市
111.006853653 35.0388594798 山西省-运城市
113.120292086 36.2016643857 山西省-长治市
113.569237602 37.8695294932 山西省-阳泉市
113.763433991 23.0430238154 广东省-东莞市
113.422060021 22.5451775145 广东省-中山市
112.050945959 22.9379756855 广东省-云浮市
113.134025635 23.0350948405 广东省-佛山市
113.307649675 23.1200491021 广东省-广州市
114.41065808 23.1135398524 广东省-惠州市
116.379500855 23.5479994669 广东省-揭阳市
116.126403098 24.304570606 广东省-梅州市
116.728650288 23.3839084533 广东省-汕头市
115.372924289 22.7787305002 广东省-汕尾市
113.078125341 22.5751167835 广东省-江门市
114.713721476 23.7572508505 广东省-河源市
114.025973657 22.5460535462 广东省-深圳市
113.040773349 23.6984685504 广东省-清远市
110.365067263 21.2574631038 广东省-湛江市
116.630075991 23.6618116765 广东省-潮州市
113.562447026 22.2569146461 广东省-珠海市
112.47965337 23.0786632829 广东省-肇庆市
110.931245331 21.6682257188 广东省-茂名市
111.977009756 21.8715173045 广东省-阳江市
113.594461107 24.8029603119 广东省-韶关市
109.122627919 21.472718235 广西壮族自治区-北海市
108.297233556 22.8064929356 广西壮族自治区-南宁市
107.357322038 22.4154552965 广西壮族自治区-崇左市
109.231816505 23.7411659265 广西壮族自治区-来宾市
109.42240181 24.3290533525 广西壮族自治区-柳州市
110.260920147 25.262901246 广西壮族自治区-桂林市
111.30547195 23.4853946367 广西壮族自治区-梧州市
108.069947709 24.6995207829 广西壮族自治区-河池市
110.151676316 22.6439736084 广西壮族自治区-玉林市
106.631821404 23.9015123679 广西壮族自治区-百色市
109.613707557 23.1033731644 广西壮族自治区-贵港市
111.552594179 24.4110535471 广西壮族自治区-贺州市
108.638798056 21.9733504653 广西壮族自治区-钦州市
108.351791153 21.6173984705 广西壮族自治区-防城港市
87.5649877411 43.8403803472 新疆维吾尔自治区-乌鲁木齐市
81.2978535304 43.9222480963 新疆维吾尔自治区-伊犁哈萨克自治州
76.1375644775 39.7503455778 新疆维吾尔自治区-克孜勒苏柯尔克孜自治州
84.8811801861 45.5943310667 新疆维吾尔自治区-克拉玛依市
82.0524362672 44.9136513743 新疆维吾尔自治区-博尔塔拉蒙古自治州
89.1815948657 42.9604700169 新疆维吾尔自治区-吐鲁番地区
79.9302386372 37.1167744927 新疆维吾尔自治区-和田地区
93.5283550928 42.8585963324 新疆维吾尔自治区-哈密地区
75.9929732675 39.4706271887 新疆维吾尔自治区-喀什地区
82.9748805837 46.7586836297 新疆维吾尔自治区-塔城地区
87.2960381257 44.0070578985 新疆维吾尔自治区-昌吉回族自治州
85.6148993383 42.1270009576 新疆维吾尔自治区-自治区直辖
80.2698461793 41.1717309015 新疆维吾尔自治区-阿克苏地区
88.1379154871 47.8397444862 新疆维吾尔自治区-阿勒泰地区
118.778074408 32.0572355018 江苏省-南京市
120.873800951 32.0146645408 江苏省-南通市
118.296893379 33.9520497337 江苏省-宿迁市
119.981861013 31.7713967447 江苏省-常州市
117.188106623 34.2715534311 江苏省-徐州市
119.427777551 32.4085052546 江苏省-扬州市
120.305455901 31.5700374519 江苏省-无锡市
119.919606016 32.4760532748 江苏省-泰州市
119.030186365 33.6065127393 江苏省-淮安市
120.148871818 33.3798618771 江苏省-盐城市
120.619907115 31.317987368 江苏省-苏州市
119.173872217 34.601548967 江苏省-连云港市
119.455835405 32.2044094436 江苏省-镇江市
117.955463877 28.4576225539 江西省-上饶市
115.999848022 29.7196395261 江西省-九江市
115.893527546 28.6895780001 江西省-南昌市
114.992038711 27.1138476502 江西省-吉安市
114.400038672 27.8111298958 江西省-宜春市
116.360918867 27.9545451703 江西省-抚州市
114.947117417 27.8223215586 江西省-新余市
117.186522625 29.3035627684 江西省-景德镇市
113.859917033 27.639544223 江西省-萍乡市
114.935909079 25.8452955363 江西省-赣州市
117.035450186 28.2413095972 江西省-鹰潭市
115.494810169 38.886564548 河北省-保定市
118.183450598 39.6505309225 河北省-唐山市
116.703602223 39.5186106251 河北省-廊坊市
114.89378153 40.8111884911 河北省-张家口市
117.933822456 40.9925210525 河北省-承德市
116.863806476 38.2976153503 河北省-沧州市
114.522081844 38.0489583146 河北省-石家庄市
119.604367616 39.9454615659 河北省-秦皇岛市
115.686228653 37.7469290459 河北省-衡水市
114.520486813 37.0695311969 河北省-邢台市
114.482693932 36.6093079285 河北省-邯郸市
111.181262093 34.7833199411 河南省-三门峡市
114.085490993 32.1285823075 河南省-信阳市
112.542841901 33.0114195691 河南省-南阳市
114.654101942 33.6237408181 河南省-周口市
115.641885688 34.4385886402 河南省-商丘市
114.351806508 36.1102667222 河南省-安阳市
113.300848978 33.7453014565 河南省-平顶山市
114.351642118 34.8018541758 河南省-开封市
113.912690161 35.3072575577 河南省-新乡市
112.447524769 34.6573678177 河南省-洛阳市
114.0460614 33.5762786885 河南省-漯河市
115.026627441 35.7532978882 河南省-濮阳市
113.211835885 35.234607555 河南省-焦作市
113.486804058 34.157183768 河南省-省直辖
113.83531246 34.0267395887 河南省-许昌市
113.64964385 34.7566100641 河南省-郑州市
114.049153547 32.9831581541 河南省-驻马店市
114.297769838 35.7554258742 河南省-鹤壁市
119.929575843 28.4562995521 浙江省-丽水市
121.440612936 28.6682832857 浙江省-台州市
120.760427699 30.7739922396 浙江省-嘉兴市
121.579005973 29.8852589659 浙江省-宁波市
120.219375416 30.2592444615 浙江省-杭州市
120.690634734 28.002837594 浙江省-温州市
120.137243163 30.8779251557 浙江省-湖州市
120.592467386 30.0023645805 浙江省-绍兴市
122.169872098 30.0360103026 浙江省-舟山市
118.875841652 28.9569104475 浙江省-衢州市
119.652575704 29.1028991054 浙江省-金华市
109.522771281 18.2577759149 海南省-三亚市
112.350383075 16.840062894 海南省-三沙市
110.330801848 20.022071277 海南省-海口市
109.733755488 19.1805008013 海南省-省直辖
110.801228917 32.6369943395 湖北省-十堰市
114.300060592 29.8806567577 湖北省-咸宁市
113.935734392 30.9279547842 湖北省-孝感市
111.310981092 30.732757818 湖北省-宜昌市
109.491923304 30.2858883166 湖北省-恩施土家族苗族自治州
114.316200103 30.5810841269 湖北省-武汉市
112.410562192 31.2093162501 湖北省-省直辖
112.241865807 30.332590523 湖北省-荆州市
112.217330299 31.0426112029 湖北省-荆门市
112.250092848 32.2291685915 湖北省-襄阳市
114.895594041 30.3844393228 湖北省-鄂州市
113.379358364 31.7178576082 湖北省-随州市
114.906618047 30.4461089379 湖北省-黄冈市
115.050683164 30.2161271277 湖北省-黄石市
111.996396357 27.7410733023 湖南省-娄底市
113.146195519 29.3780070755 湖南省-岳阳市
111.653718137 29.0121488552 湖南省-常德市
110.481620157 29.1248893532 湖南省-张家界市
109.986958796 27.5574829012 湖南省-怀化市
113.131695341 27.8274329277 湖南省-株洲市
111.614647686 26.4359716468 湖南省-永州市
112.935555633 27.835095053 湖南省-湘潭市
109.7457458 28.3179507937 湖南省-湘西土家族苗族自治州
112.366546645 28.5880877799 湖南省-益阳市
112.583818811 26.8981644154 湖南省-衡阳市
111.461525404 27.2368112449 湖南省-邵阳市
113.037704468 25.7822639757 湖南省-郴州市
112.979352788 28.2134782309 湖南省-长沙市
113.557519102 22.2041179884 澳门特别行政区-无堂区划分区域
113.566432335 22.1950041592 澳门特别行政区-澳门半岛
113.557519102 22.2041179884 澳门特别行政区-澳门离岛
103.215249178 35.5985143488 甘肃省-临夏回族自治州
103.823305441 36.064225525 甘肃省-兰州市
98.2816345853 39.8023973267 甘肃省-嘉峪关市
105.736931623 34.5843194189 甘肃省-天水市
104.626637601 35.5860562418 甘肃省-定西市
106.688911157 35.55011019 甘肃省-平凉市
107.644227087 35.7268007545 甘肃省-庆阳市
100.459891869 38.939320297 甘肃省-张掖市
102.640147343 37.9331721429 甘肃省-武威市
102.917442486 34.9922111784 甘肃省-甘南藏族自治州
104.171240904 36.5466817062 甘肃省-白银市
98.5084145062 39.7414737682 甘肃省-酒泉市
102.208126263 38.5160717995 甘肃省-金昌市
104.934573406 33.3944799729 甘肃省-陇南市
117.642193934 26.2708352794 福建省-三明市
118.181882949 26.6436264742 福建省-南平市
118.103886046 24.4892306125 福建省-厦门市
119.54208215 26.6565274192 福建省-宁德市
118.600362343 24.901652384 福建省-泉州市
117.676204679 24.5170647798 福建省-漳州市
119.330221107 26.0471254966 福建省-福州市
119.077730964 25.4484501367 福建省-莆田市
117.017996739 25.0786854335 福建省-龙岩市
91.7506438744 29.2290269317 西藏自治区-山南地区
91.111890896 29.6625570621 西藏自治区-拉萨市
88.8914855677 29.2690232039 西藏自治区-日喀则地区
97.18558158 31.1405756319 西藏自治区-昌都地区
94.3499854582 29.6669406258 西藏自治区-林芝地区
92.0670183689 31.4806798301 西藏自治区-那曲地区
81.1076686895 30.4045565883 西藏自治区-阿里地区
104.85208676 26.5918660603 贵州省-六盘水市
105.928269966 26.2285945777 贵州省-安顺市
105.333323371 27.4085621313 贵州省-毕节市
106.709177096 26.6299067414 贵州省-贵阳市
106.931260316 27.6999613771 贵州省-遵义市
109.168558028 27.6749026906 贵州省-铜仁市
107.985352573 26.5839917665 贵州省-黔东南苗族侗族自治州
107.52320511 26.2645359974 贵州省-黔南布依族苗族自治州
104.900557798 25.0951480559 贵州省-黔西南布依族苗族自治州
124.338543115 40.1290228266 辽宁省-丹东市
121.593477781 38.9487099383 辽宁省-大连市
123.929819767 41.8773038296 辽宁省-抚顺市
120.446162703 41.5718276679 辽宁省-朝阳市
123.77806237 41.3258376266 辽宁省-本溪市
123.432790922 41.8086447835 辽宁省-沈阳市
122.07322781 41.141248023 辽宁省-盘锦市
122.233391371 40.6686510665 辽宁省-营口市
120.860757645 40.7430298813 辽宁省-葫芦岛市
123.172451205 41.2733392656 辽宁省-辽阳市
123.854849615 42.2997570121 辽宁省-铁岭市
121.147748738 41.1308788759 辽宁省-锦州市
121.660822129 42.0192501071 辽宁省-阜新市
123.007763329 41.1187436822 辽宁省-鞍山市
106.530635013 29.5446061089 重庆-重庆市
108.707509278 34.345372996 陕西省-咸阳市
109.934208154 33.8739073951 陕西省-商洛市
109.038044563 32.70437045 陕西省-安康市
107.170645452 34.3640808097 陕西省-宝鸡市
109.500509757 36.6033203523 陕西省-延安市
109.745925744 38.2794392401 陕西省-榆林市
107.045477629 33.0815689782 陕西省-汉中市
109.483932697 34.5023579758 陕西省-渭南市
108.953098279 34.2777998978 陕西省-西安市
108.968067013 34.9083676964 陕西省-铜川市
100.223722769 34.4804845846 青海省-果洛藏族自治州
102.085206987 36.5176101677 青海省-海东地区
100.879802174 36.9606541011 青海省-海北藏族自治州
100.624066094 36.2843638038 青海省-海南藏族自治州
97.3426254153 37.3737990706 青海省-海西蒙古族藏族自治州
97.0133161374 33.0062399097 青海省-玉树藏族自治州
101.76792099 36.640738612 青海省-西宁市
102.007600308 35.5228515517 青海省-黄南藏族自治州
114.173291988 22.3072458588 香港特别行政区-九龙
114.146701965 22.4274312754 香港特别行政区-新界
114.183870524 22.2721034276 香港特别行政区-香港岛
131.019048047 45.7750053686 黑龙江省-七台河市
128.910765978 47.7346850751 黑龙江省-伊春市
130.284734586 46.8137796047 黑龙江省-佳木斯市
131.17140174 46.6551020625 黑龙江省-双鸭山市
126.657716855 45.7732246332 黑龙江省-哈尔滨市
124.19610419 51.991788968 黑龙江省-大兴安岭地区
125.02183973 46.59670902 黑龙江省-大庆市
129.608035396 44.5885211528 黑龙江省-牡丹江市
126.989094572 46.646063927 黑龙江省-绥化市
130.941767273 45.3215398866 黑龙江省-鸡西市
130.292472051 47.3386659037 黑龙江省-鹤岗市
127.500830295 50.2506900907 黑龙江省-黑河市
123.987288942 47.3476998134 黑龙江省-齐齐哈尔市'''
    # 123.987288942 47.3476998134 黑龙江省-齐齐哈尔市
    proxieslist = []
    for i in a.split('\n'):
        print(i)
        city = i.split(' ')[2].split('-')[1].strip()
        lon = i.split(' ')[0].strip()
        lat = i.split(' ')[1].strip()
        # print(city, lat, lon)
        if city in [
            '怒江傈僳族自治州','临沧市','文山壮族苗族自治州','西双版纳傣族自治州', '乌海市','阿拉善盟',
            '台中市', '台北市', '台南市', '台义市', '高雄市', '白城市', '辽源市','内江市','攀枝花市',
            '资阳市','阿坝藏族羌族自治州','中卫市','吴忠市','固原市','石嘴山市','铜陵市','莱芜市',
            '朔州市','阳泉市','宾市','百色市','克孜勒苏柯尔克孜自治州','克拉玛依市','喀什地区','和田地区',
            '塔城地区','自治区直辖','阿勒泰地区','鹰潭市','三门峡市','省直辖','驻马店市','鹤壁市','咸宁市',
            '鄂州市','堂区划分区域','澳门离岛','临夏回族自治州','天水市','定西市','平凉市','安庆市','白银市',
            '武威市','甘南藏族自治州','陇南市','金昌市','山南地区','那曲地区','昌都地区','铜仁市','商洛市',
            '安康市','延安市','铜川市','海北藏族自治州','果洛藏族自治州','海南藏族自治州','玉树藏族自治州',
            '黄南藏族自治州','九龙','新界','香港岛','伊春市','七台河市','大兴安岭地区','绥化市','鸡西市'
''        ]: continue
        if url_data.count({city: '已爬取'}):
            print('已爬取')
            continue
        elif url_data.count({city: '正在爬取'}):
            print('正在爬取')
            continue
        url_data.insert_one({city: '正在爬取'})
        proxieslist = run(city, lon, lat, proxieslist)
        url_data.insert_one({city: '已爬取'})
    pool.shutdown()
