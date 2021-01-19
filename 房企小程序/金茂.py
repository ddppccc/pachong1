import re
import time

import requests
from jsonpath import jsonpath

headers = {
    'Host': 'dm-api.elab-plus.cn',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
    'content-type': 'application/json;charset=UTF-8',
    'customerId': '2094793',
    'elabBrandId': '1',
    'elabEnvironment': '3',
    'elabProjectName': 'jinmaofen',
    'elabSystem': '2',
    'tonken': '',
    'Referer': 'https://servicewechat.com/wx7fb636aad5c61fe0/99/page-frame.html',
    'Accept-Encoding': 'gzip, deflate, br',
}

url_cityMap = 'https://dm-api.elab-plus.cn/elab-marketing-content/cityHistory/queryCityData'

data = {
    "brandId": 1,
    "customerId": 2094793,
    "simplify": 'false',
    "terminal": "1"
}


def get_cityMap(url, headers, data):
    resp = requests.post(url=url, headers=headers, json=data)
    CityMap = jsonpath(resp.json(), '$.single.belongCityList')
    for cityInfo in CityMap[0]:
        get_queryNewsByCity(cityInfo['cityName'])
        break


def get_queryNewsByCity(city):
    url = 'https://dm-api.elab-plus.cn/elab-marketing-content/houseManagement/houseSort'
    data = {
        "cityName": city,
        "coordinateX": "",
        "coordinateY": "",
        "brandId": 1,
        "newPath": 1,
        "terminal": "1"
    }
    resp = requests.post(url=url, headers=headers, json=data)
    project_list = jsonpath(resp.json(), '$.list')[0]
    for project in project_list:
        item = {}
        item['城市'] = project['city']
        item['区县'] = project['district']
        item['标题'] = project['houseName']
        item['总价'] = str(project['totalPriceMin']) + '-' + str(project['totalPriceMax'])
        item['开盘时间'] = time.strftime('%Y-%m-%d', time.localtime(int(str(project['openTime'])[:-3])))
        item['标签'] = project['label']
        item['longitude'] = project['coordinateY']
        item['latitude'] = project['coordinateX']
        item['建面'] = str(project['areaMin']) + '-' + str(project['areaMin'])
        id = project['houseId']
        print(item,id)
        get_detailByhouseID(id,item)

def get_detailByhouseID(houseid,item):
    url = 'https://dm-api.elab-plus.cn/elab-marketing-content/master/brandXcxPageNew'
    headers = {
        'Host': 'dm-api.elab-plus.cn',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'elabEnvironment': '4',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'Origin': 'https://dm-mng.elab-plus.cn',
        'Content-Type': 'application/json;charset=UTF-8',
        'Referer': 'https://dm-mng.elab-plus.cn/touFangBao/index.html',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-us,en',
        'Cookie': 'acw_tc=2f624a1116062999806295935e2b99b2ee2184aa66c83dc0ae232b73f96c86',
    }
    data = {
        'houseId':houseid,
        'terminal':'1'
    }
    resp = requests.post(url=url,headers=headers,json=data)
    json_url = jsonpath(resp.json(),'$..url')[0]
    headers_json = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'if-none-match': 'FuE3BMrmaPgxzZdQx4I3kx_jgxbh.gz',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    }
    resp_get = requests.get(url=json_url,headers=headers_json)
    id = re.search(r'\?id=(\d+)&',resp_get.text).group(1)
    print(id)
    resp_post = requests.post(url='https://dm-api.elab-plus.cn/elab-marketing-tfb/template/content/detailById',headers=headers,json={'id':id})
    imgurl_list = re.findall(r'\\"https://.*?\\"',resp_post.text)
    l = []
    for url in imgurl_list:
        l.append(url.replace('\"','').replace('\\',''))
    print(l)
get_cityMap(url_cityMap, headers, data)
