import requests
import time
import pymongo
import re
import json
from lxml import etree
from urllib import parse
from multiprocessing import Process, Pool
import warnings
from selenium import webdriver
from selenium.webdriver.support.ui import Select
warnings.filterwarnings("ignore")
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
    retryWrites="false")['房企top100']['xuhuijituan_cjy']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['房企top100']['xuhuijituan_has_spider']
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    'Host': 'online.gemdale.com',
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
}
year = 2021
month = 4


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


def get_html(url):
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'UqZBpD3n3iPIDwJU9B2ooSw_=v1iNKvg8SctIP; PHPSESSID=4lg1t096ndkemij5dvtt4hiir0; zVUpZH_think_language=zh-CN; _pk_ses.5.8790=*; _pk_id.5.8790=0fd265bf3a2bf36e.1619497620.2.1619502495.1619501467.',
        'Host':'www.cifi.com.cn',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
    }
    try:
        proxies = {"https": get_proxy()}
        response = requests.get(url, headers=headers,timeout=(10, 10))
        # encod = response.apparent_encoding
        # if encod.upper() in ['GB2312', 'WINDOWS-1254']:
        #     encod = 'gbk'
        # response.encoding = encod
        return response
    except Exception as e:
        print('geturl错误', url, e)
        time.sleep(2)
        return get_html(url)
def getSearch(valArgs):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '362',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie':'UqZBpD3n3iPIDwJU9B2ooSw_=v1iNKvg8SctIP; PHPSESSID=4lg1t096ndkemij5dvtt4hiir0; _pk_ses.5.8790=*; zVUpZH_think_language=zh-CN; _pk_id.5.8790=0fd265bf3a2bf36e.1619497620.2.1619505457.1619501467.',
        'Host': 'www.cifi.com.cn',
        'Origin': 'https://www.cifi.com.cn',
        'Referer': 'https://www.cifi.com.cn/product/house.html',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    url='https://www.cifi.com.cn/index.php?g=Contents&m=Index&a=public_ajax_search'
    form={
        'attrArgs': 'N17OarsNYUUf2lCOf/ggoHfMc91265MuJh/wb4DY4By7xSFRJZi7w6apDKTxYlua',
        # 'valArgs': 'Xa9DMcv4nVbxDaLVMFOHNN9yIRQeHg8YGd+quPahIY6t368Pz2NJj4szdIt5+mFwD5SCtv9d61XkE6sCRe8z2/onG2WZ0KCwrubjNUiFWYsd8AUmHua5rlK5PFpCIMnyQ6Y4X7l5bErRmdQSeCzLFp6Z4sYA+NJ0gbxTFXY1oqvUxKfgpkZLaO/9QsshsccP1qGroASQFd9Cour6mdZzW91LuwZlKzbKwUUFy3jMWgH1bNdXr4Cp48tpRz5eejnWi5ic2uRxhHeql2PuYXpNiA=='
        # 'valArgs': 'Xa9DMcv4nVbxDaLVMFOHNN9yIRQeHg8YGd quPahIY6t368Pz2NJj4szdIt5 mFwD5SCtv9d61XkE6sCRe8z2/onG2WZ0KCwrubjNUiFWYst ncJoX/qAq1GB941NLuCbfLZAXRdjckiy 8JCklW56kbEKg0Jv4B1qvnz2ZxGv/GSj9kF3CLB1JY2Hr2qty JFOiNxB5VxPaqSIKa5aVsDKKSWeSLA3GhHvjl2jYG9oUkZaM6F9csoIxqyLfyIjFk4XVL5tWzvdZQNHwpdg9Lg=='
        'valArgs':valArgs
    }
    res=requests.post(url,headers=headers,data=form,timeout=10)
    res.encoding='utf8'
    # print(res.json()['data'])
    return res.json()['data']
def getDetailInfo(city,data):
    url = 'https://www.cifi.com.cn'+data['url']
    has_spider_urllist = []
    for has_spider_url in has_spider.find():
        has_spider_urllist.append(has_spider_url['标题url'])
    if url in has_spider_urllist:
        print('该页数据已爬取，下一页')
        return
    res = get_html(url)
    res.encoding = 'utf8'
    if res.status_code == 502:
        print(url, '页面打开失败')
        return
    html = etree.HTML(res.text)
    # print(res.text)
    item = {}
    item['城市'] =city
    item['区县'] = ''
    item['标题'] =data['title']
    item['标题url'] = url
    item['销售情况'] = ''
    try:
        item['分类'] =html.xpath('/html/body/div[2]/div[2]/div[4]/div[1]/div/div/table/tbody/tr[4]/td[1]/div/p/text()')[0]
    except:
        item['分类'] = ''
    try:
        item['装修'] =''
    except:
        item['装修'] = ''
    item['户型'] =''
    try:
        item['单价'] =html.xpath('/html/body/div[2]/div[2]/div[4]/div[1]/div/div/table/tbody/tr[1]/td[1]/div/p/text()')[0]
    except:
        item['单价'] = ''
    item['总价'] = ''
    item['建面'] = ''
    item['最小建面'] = ''
    item['最大建面'] = ''
    try:
        item['容积率'] = html.xpath('/html/body/div[2]/div[2]/div[4]/div[1]/div/div/table/tbody/tr[3]/td[1]/div/p/text()')[0]
    except:
        item['容积率'] = ''
    try:
        item['绿化率'] = html.xpath('/html/body/div[2]/div[2]/div[4]/div[1]/div/div/table/tbody/tr[3]/td[2]/div/p/text()')[0]
    except:
        item['绿化率'] = ''
    item['楼栋户数'] =''
    try:
        item['总户数'] = html.xpath('/html/body/div[2]/div[2]/div[4]/div[1]/div/div/table/tbody/tr[2]/td[2]/div/p/text()')[0]
    except:
        item['总户数'] = ''
    try:
        item['建筑面积'] =html.xpath('/html/body/div[2]/div[2]/div[4]/div[1]/div/div/table/tbody/tr[2]/td[1]/div/p/text()')[0]
    except:
        item['建筑面积'] = ''
    item['地址'] =data['subtitle']
    # tags =
    # tag = ''
    # for i in tags:
    #     tag = tag + ' ' + i.strip()
    item['标签'] = ''
    try:
        item['开盘时间'] =html.xpath('//div[@class="house_banner_p"]/ul/li[3]/dl/dd/text()')[0]
    except:
        item['开盘时间'] = ''
    try:
        item['物业费'] = html.xpath('/html/body/div[2]/div[2]/div[4]/div[1]/div/div/table/tbody/tr[4]/td[2]/div/p/text()')[0]
    except:
        item['物业费'] =''
    item['latitude'] = data['source']
    item['longitude'] = data['author']
    item['抓取年份'] = year
    item['抓取月份'] = month
    item['数据来源'] = '旭辉集团'
    item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    info_base.insert_one(item)
    has_spider.insert_one({'标题url': url})
    print(item)

def getprovinceid():
    url='https://www.cifi.com.cn/product/house.html'
    res=get_html(url)
    res.encoding='utf8'
    html=etree.HTML(res.text)
    aidlist=html.xpath('//*[@id="province"]/dd/a')
    dict={}
    for i in aidlist:
        province=i.xpath('./@data-title')[0]
        cid=i.xpath('./@data-val')[0]
        dict[province]=cid
    # print(dict)
    return dict
def getcityjs(catid):
    # catid = '201'
    pageindex = '1'
    pagesize = '10000'
    pagecmd = "zhuzhai"
    where = '{"field":"catid","value":"' + str(catid) + '","symbol":"in","isRelationChild":0,"RelationField":""}'
    condition = '[{"condition":[' + where + '],"condition_type":1,"pagesize":' + pagesize + ',"pageindex":' + pageindex + '}]'
    valArgs = "getConditionResult" + "|search|" + pagecmd + "|search|" + condition
    driver.execute_script('document.close()')
    driver.execute_script("document.write(encryption('%s'))"%valArgs)
    time.sleep(2)
    js=driver.find_elements_by_xpath('/html/body')[0].text
    # print(js)
    return js
def getdatajs(relationid):
    # catid = '201'
    pageindex = '1'
    pagesize = '10000'
    pagecmd = "zhuzhaiAll"
    isRelationChild="0"
    where = '{"field":"relationid","value":"' + relationid + '","symbol":"in","isRelationChild":' + isRelationChild + '}'
    condition='[{"condition":[' + where + '],"condition_type":1,"pagesize":' + pagesize + ',"pageindex":' + pageindex + '}]'
    valArgs = "getConditionResult" + "|search|" + pagecmd + "|search|" + condition
    driver.execute_script('document.close()')
    driver.execute_script("document.write(encryption('%s'))"%valArgs)
    time.sleep(2)
    js=driver.find_elements_by_xpath('/html/body')[0].text
    # print(js)
    return js
if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('https://www.cifi.com.cn/product/house.html')
    time.sleep(3)
    dict=getprovinceid()
    for k,v in dict.items():
        valArgs=getcityjs(v)
        # print('val',valArgs)
        citydatalist=getSearch(valArgs)
        for i in citydatalist:
            # print(i['id'])
            city=i['title']
            js2=getdatajs(i['id'])
            # print('js2 ',js2)
            datalist=getSearch(js2)
            for data in datalist:
                getDetailInfo(city,data)
    print('执行成功')




