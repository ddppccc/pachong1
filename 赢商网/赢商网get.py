import random
import re
import json
import pymongo
import requests
from lxml import etree
import time
from urllib import parse
from lxml import etree

from 赢商网 import lists
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
    retryWrites="false")['赢商网']['数据_202110']

url_data = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['赢商网']['url_202110']


def get_proxy():
    try:
        return requests.get('http://1.116.204.248:5000/proxy').text
    except:
        print('暂无ip，等待20秒')
        time.sleep(20)


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'UM_distinctid=17b0fe2d2c61cb-0a90bac3145132-2343360-1fa400-17b0fe2d2c7269; winfanguser=uid=shen17772430852&nid=shen17772430852_430633575&logNum=1&err163=790025af03774d94&pwd=55d1ba829242569228eee1e425f253&headerImg=&sex=0&Email=&IsCompany=0; eyeuser=uid%3dshen17772430852%26nid%3dshen17772430852_430633575%26logNum%3d1%26err163%3d790025af03774d94%26pwd%3d55d1ba829242569228eee1e425f253%26headerImg%3d%26sex%3d0%26Email%3d%26IsCompany%3d0; CNZZDATA1277846263=97093927-1628055844-http%253A%252F%252Fwww.winshangdata.com%252F%7C1628061811; Hm_lvt_f48055ef4cefec1b8213086004a7b78d=1628040498,1628063527; Hm_lpvt_f48055ef4cefec1b8213086004a7b78d=1628063968',
    'Host': 'bizsearch.winshangdata.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
}
header = {
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'

}


def get_tree(url, headers):
    while True:
        try:
            prox = get_proxy()
            proxies = {'http': prox,
                       'https': prox}
            response = requests.get(url, headers=headers, proxies=proxies, timeout=(3, 5))
            response.encoding = response.apparent_encoding
            res = response.text
            tree = etree.HTML(res)
            return tree
        except:
            continue


# def get_nextUrl(qy_p, qy_c, qy_a):
#     pn = 1
#     js = 0
#     bj = 0
#     ipList = []
#     while True:
#         url = 'http://bizsearch.winshangdata.com/xiangmu/s%s-c%s-a%s-pn%s.html' % (qy_p, qy_c, qy_a, pn)
#         tree = get_tree(url, headers)
#         if js == 0:
#             ids = get_projectId(tree)
#             if ids == []:
#                 print('当前页面有问题：', url)
#                 bj += 1
#                 if bj < 5:
#                     continue
#             print(url)
#             ipList += ids
#         try:
#             next = tree.xpath('//div[@id="AspNetPager1"]/a')[-1]
#             nexts = ''.join(next.xpath('./@href'))
#             if nexts == '':
#                 break
#             pn += 1
#             js = 0
#         except Exception as e:
#             if js == 5:
#                 return ipList
#             js += 1
#             continue
#     return ipList
#
# def get_projectId(tree):
#     urlList = tree.xpath('//ul[@class="l-list clearfix"]//div[@class="l-logo fl"]/a/@href')
#     print(urlList)
#     ipList = []
#     for ur in urlList:
#         projectId = ''.join(re.findall('\d+', ur))
#         ipList.append(projectId)
#     return ipList
def get_nextUrl(qy_p, qy_c, qy_a):
    pn = 1
    ipList = []
    while True:
        headersl = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'appType': 'bigdata',
            'Authorization': '',
            'Content-Length': '160',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': '_uab_collina=162927528347933782884946; Hm_lvt_f48055ef4cefec1b8213086004a7b78d=1629275285; Hm_lpvt_f48055ef4cefec1b8213086004a7b78d=1629275285',
            'Host': 'www.winshangdata.com',
            'Origin': 'http://www.winshangdata.com',
            'platform': 'pc',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://www.winshangdata.com/projectList',
            'token': '',
            'uid': '',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73',
            'uuid': '123456'
        }
        data = {"pageNum": pn, "orderBy": "1", "pageSize": 60, "zsxq_yt1": "", "zsxq_yt2": "", "qy_p": qy_p,
                "qy_c": qy_c,
                "qy_a": qy_a, "xmzt": "", "key": "", "wuyelx": "", "isHaveLink": "", "ifdporyt": ""}
        url = 'http://www.winshangdata.com/wsapi/project/list3_4'
        while True:
            try:
                response = requests.post(url, headers=headersl, json=data, timeout=(3, 5)).json()
                break
            except:
                continue
        idit = response['data']['list']
        if idit == []:
            break
        for ids in idit:
            projectId = ids['projectId']
            ipList.append(projectId)
        pn += 1
    return ipList


def get_data(sheng, city, qx, projectId):
    if url_data.count({'ID': projectId}):
        print('当前ID已爬取：', projectId)
        return
    item = {}
    url = 'https://www.winshangdata.com/projectDetail?projectId=' + str(projectId)
    item['省份'] = sheng
    item['城市'] = city
    item['区县'] = qx
    item['项目id'] = projectId
    tree = get_tree(url, header)
    item['项目名称'] = ''.join(tree.xpath('//h1[@class="detail-one-tit"]/text()')).replace(' ', '').replace('\n', '')
    mj = ''.join(
        tree.xpath('//ul[@class="detail-option border-b"]/li[3]/span[@class="detail-option-value"]/text()'))
    try:
        item['商业面积(万㎡)'] = float(''.join(re.findall('(.+)万平米', mj)))
    except:
        item['商业面积(万㎡)'] = 0
    item['地址'] = ''.join(
        tree.xpath('//ul[@class="detail-option border-b"]/li[6]/span[@class="detail-option-value"]/text()'))
    item['商业楼层'] = ''.join(
        tree.xpath('//ul[@class="detail-option border-b"]/li[4]/span[@class="detail-option-value"]/text()'))
    item['物业类型'] = ''.join(
        tree.xpath('//ul[@class="detail-option border-b"]/li[1]/span[@class="detail-option-value"]/text()'))
    item['项目状态'] = ''.join(tree.xpath('//div[@class="fl w-p-50"][1]/div[@class="detail-three-tit"]/text()'))
    item['招商状态'] = ''.join(tree.xpath('//div[@class="fl w-p-50"][2]/div[@class="detail-three-tit"]/text()'))
    text = ''.join(tree.xpath('//body/script/text()'))
    item['开业时间'] = ''.join(re.findall('kaiYeShiJianReal:"(\d+-?\d+?-?\d+?)",gaiZaoShijian', text))
    if item['开业时间'] == '':
        item['开业时间'] = ''.join(
            tree.xpath('//ul[@class="detail-option border-b"]/li[2]/span[@class="detail-option-value"]/text()'))
    item['longitude'] = ''.join(re.findall('gd_Lng:(\d+\.\d+)', text))
    item['latitude'] = ''.join(re.findall('gd_Lat:(\d+\.\d+)', text))
    # item['longitude'], item['latitude'] = get_zb(item['地址'], item['城市'])
    info_base.insert_one(item)
    url_data.insert_one({'ID': projectId})
    print(item)


def run(lists):
    for dicts in lists:
        sheng = dicts['text']
        qy_p = dicts['value']
        for cityDict in dicts['children']:
            city = cityDict['text']
            if url_data.count({city: '已爬取'}):
                print('当前城市已爬取：', city)
                continue
            elif url_data.count({city: '正在爬取12'}):
                print('当前城市正在爬取：', city)
                continue
            url_data.insert_one({city: '正在爬取12'})
            qy_c = cityDict['value']
            xcc = []
            for qxDict in cityDict['children']:
                qx = qxDict['text']
                qy_a = qxDict['value']
                print(city, qx, qy_p, qy_c, qy_a)
                ipList = get_nextUrl(qy_p, qy_c, qy_a)
                for ID in ipList:
                    xcc.append(pool.submit(get_data, sheng, city, qx, str(ID)))
            [obj.result() for obj in xcc]
            url_data.insert_one({city: '已爬取'})


if __name__ == '__main__':
    # info_base.delete_many({})
    # url_data.delete_many({})
    # url_data.insert_one({'西安':'已爬取'})
    pool = ThreadPoolExecutor()
    dicts = [
        {"value": 317, "text": "湖北", "children": [{"value": 569, "text": "武汉",
                                                    "children": [{"value": 11515, "text": "江岸区"},
                                                                 {"value": 11516, "text": "江汉区"},
                                                                 {"value": 11517, "text": "硚口区"},
                                                                 {"value": 11518, "text": "汉阳区"},
                                                                 {"value": 11519, "text": "武昌区"},
                                                                 {"value": 11520, "text": "青山区"},
                                                                 {"value": 11521, "text": "洪山区"},
                                                                 {"value": 11522, "text": "东西湖区"},
                                                                 {"value": 11523, "text": "汉南区"},
                                                                 {"value": 11524, "text": "蔡甸区"},
                                                                 {"value": 11525, "text": "江夏区"},
                                                                 {"value": 11526, "text": "黄陂区"},
                                                                 {"value": 11527, "text": "新洲区"}]},
                                                   {"value": 570, "text": "黄石",
                                                    "children": [{"value": 11528, "text": "黄石港区"},
                                                                 {"value": 11529, "text": "西塞山区"},
                                                                 {"value": 11530, "text": "下陆区"},
                                                                 {"value": 11531, "text": "铁山区"},
                                                                 {"value": 11532, "text": "阳新县"},
                                                                 {"value": 11533, "text": "大冶市"}]},
                                                   {"value": 571, "text": "十堰",
                                                    "children": [{"value": 11534, "text": "茅箭区"},
                                                                 {"value": 11535, "text": "张湾区"},
                                                                 {"value": 11536, "text": "郧阳区"},
                                                                 {"value": 11537, "text": "郧西县"},
                                                                 {"value": 11538, "text": "竹山县"},
                                                                 {"value": 11539, "text": "竹溪县"},
                                                                 {"value": 11540, "text": "房县"},
                                                                 {"value": 11541, "text": "丹江口市"}]},
                                                   {"value": 572, "text": "宜昌",
                                                    "children": [{"value": 11542, "text": "西陵区"},
                                                                 {"value": 11543, "text": "伍家岗区"},
                                                                 {"value": 11544, "text": "点军区"},
                                                                 {"value": 11545, "text": "猇亭区"},
                                                                 {"value": 11546, "text": "夷陵区"},
                                                                 {"value": 11547, "text": "远安县"},
                                                                 {"value": 11548, "text": "兴山县"},
                                                                 {"value": 11549, "text": "秭归县"},
                                                                 {"value": 11550, "text": "长阳土家族自治县"},
                                                                 {"value": 11551, "text": "五峰土家族自治县"},
                                                                 {"value": 11552, "text": "宜都市"},
                                                                 {"value": 11553, "text": "当阳市"},
                                                                 {"value": 11554, "text": "枝江市"}]},
                                                   {"value": 573, "text": "襄阳",
                                                    "children": [{"value": 11555, "text": "襄城区"},
                                                                 {"value": 11556, "text": "樊城区"},
                                                                 {"value": 11557, "text": "襄州区"},
                                                                 {"value": 11558, "text": "南漳县"},
                                                                 {"value": 11559, "text": "谷城县"},
                                                                 {"value": 11560, "text": "保康县"},
                                                                 {"value": 11561, "text": "老河口市"},
                                                                 {"value": 11562, "text": "枣阳市"},
                                                                 {"value": 11563, "text": "宜城市"}]},
                                                   {"value": 574, "text": "鄂州",
                                                    "children": [{"value": 11564, "text": "梁子湖区"},
                                                                 {"value": 11565, "text": "华容区"},
                                                                 {"value": 11566, "text": "鄂城区"}]},
                                                   {"value": 575, "text": "荆门",
                                                    "children": [{"value": 11567, "text": "东宝区"},
                                                                 {"value": 11568, "text": "掇刀区"},
                                                                 {"value": 11569, "text": "京山市"},
                                                                 {"value": 11570, "text": "沙洋县"},
                                                                 {"value": 11571, "text": "钟祥市"}]},
                                                   {"value": 576, "text": "孝感",
                                                    "children": [{"value": 11572, "text": "孝南区"},
                                                                 {"value": 11573, "text": "孝昌县"},
                                                                 {"value": 11574, "text": "大悟县"},
                                                                 {"value": 11575, "text": "云梦县"},
                                                                 {"value": 11576, "text": "应城市"},
                                                                 {"value": 11577, "text": "安陆市"},
                                                                 {"value": 11578, "text": "汉川市"}]},
                                                   {"value": 577, "text": "荆州",
                                                    "children": [{"value": 11579, "text": "沙市区"},
                                                                 {"value": 11581, "text": "公安县"},
                                                                 {"value": 11582, "text": "监利市"},
                                                                 {"value": 11583, "text": "江陵县"},
                                                                 {"value": 11584, "text": "石首市"},
                                                                 {"value": 11585, "text": "洪湖市"},
                                                                 {"value": 11586, "text": "松滋市"},
                                                                 {"value": 14835, "text": "荆州区"}]},
                                                   {"value": 578, "text": "黄冈",
                                                    "children": [{"value": 11587, "text": "黄州区"},
                                                                 {"value": 11588, "text": "团风县"},
                                                                 {"value": 11589, "text": "红安县"},
                                                                 {"value": 11590, "text": "罗田县"},
                                                                 {"value": 11591, "text": "英山县"},
                                                                 {"value": 11592, "text": "浠水县"},
                                                                 {"value": 11593, "text": "蕲春县"},
                                                                 {"value": 11594, "text": "黄梅县"},
                                                                 {"value": 11595, "text": "麻城市"},
                                                                 {"value": 11596, "text": "武穴市"}]},
                                                   {"value": 579, "text": "咸宁",
                                                    "children": [{"value": 11597, "text": "咸安区"},
                                                                 {"value": 11598, "text": "嘉鱼县"},
                                                                 {"value": 11599, "text": "通城县"},
                                                                 {"value": 11600, "text": "崇阳县"},
                                                                 {"value": 11601, "text": "通山县"},
                                                                 {"value": 11602, "text": "赤壁市"}]},
                                                   {"value": 580, "text": "随州",
                                                    "children": [{"value": 11603, "text": "曾都区"},
                                                                 {"value": 11604, "text": "随县"},
                                                                 {"value": 11605, "text": "广水市"}]},
                                                   {"value": 581, "text": "恩施",
                                                    "children": [{"value": 11606, "text": "恩施市"},
                                                                 {"value": 11607, "text": "利川市"},
                                                                 {"value": 11608, "text": "建始县"},
                                                                 {"value": 11609, "text": "巴东县"},
                                                                 {"value": 11610, "text": "宣恩县"},
                                                                 {"value": 11611, "text": "咸丰县"},
                                                                 {"value": 11612, "text": "来凤县"},
                                                                 {"value": 11613, "text": "鹤峰县"}]},
                                                   {"value": 582, "text": "仙桃",
                                                    "children": [{"value": 11614, "text": "仙桃市"}]},
                                                   {"value": 583, "text": "潜江",
                                                    "children": [{"value": 11615, "text": "潜江市"}]},
                                                   {"value": 584, "text": "天门",
                                                    "children": [{"value": 11616, "text": "天门市"}]},
                                                   {"value": 585, "text": "神农架",
                                                    "children": [{"value": 11617, "text": "神农架林区"}]}]
              },

             ]
    run(dicts)
    run(lists)
    input('爬取完成')

# url = 'http://bizsearch.winshangdata.com/xiangmu/s301-c401-a10001-pn1.html'
# tree = get_tree(url)
# nextUrl = tree.xpath('//div[@id="AspNetPager1"]/a')[-1].xpath('./@href')

# get_data('东城区', '4698')  # 2550
