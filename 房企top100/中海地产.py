import requests
import time
import pymongo
import re
from lxml import etree
from urllib import parse
from multiprocessing import Process,Pool
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
            retryWrites="false")['中海地产']['info']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['中海地产']['has_spider']
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
}
year=2021
month=4
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
    try:
        proxies = {"https": get_proxy()}
        response = requests.get(url, headers=headers,timeout=(10, 10))
        # encod = response.apparent_encoding
        # if encod.upper() in ['GB2312', 'WINDOWS-1254']:
        #     encod = 'gbk'
        # response.encoding = encod
        return response
    except Exception as e:
        print('geturl错误',url, e)
        return get_html(url)

def getUrlList():
    url='http://www.coli688.com/new-property'
    res=get_html(url)
    res.encoding='utf8'
    html=etree.HTML(res.text)
    urlList=html.xpath('//article/div/div[1]/a/@href')
    return urlList
def getInfo():
    urlList=getUrlList()
    for url in urlList:
        has_spider_urllist = []
        for has_spider_url in has_spider.find():
            has_spider_urllist.append(has_spider_url['标题url'])
        if url in has_spider_urllist:
            print('该页数据已爬取，下一页')
            continue
        uid=re.findall('project/(\d+)',url)[0]
        item={}
        res=get_html(url)
        res.encoding='utf8'
        html=etree.HTML(res.text)
        info=html.xpath('//*[@id="portfolio-post-'+uid+'"]/section/div[3]/div[1]/div[3]')[0]
        item['城市']=''
        item['区县']=''
        item['标题']=html.xpath('/html/head/title/text()')[0].strip()
        item['标题url']=url
        item['销售情况']=''
        item['分类']=info.xpath('.//text()')[20]
        item['装修']=''
        item['户型']=html.xpath('string(.//*[@id="portfolio-post-'+uid+'"]/section/div[3]/div[2]/div/div/div/div/div[3]/div[2])').replace(' ','').replace('\r\n',' ')
        item['单价']=''
        item['总价']=''
        item['建面']=''
        item['最小建面']=''
        item['最大建面']=''
        item['容积率']=''
        item['绿化率']=''
        item['楼栋总数']=''
        item['总户数']=''
        item['建筑面积']=info.xpath('.//text()')[10]
        item['地址']=info.xpath('.//text()')[4]
        item['标签']=html.xpath('//*[@id="portfolio-post-'+uid+'"]/section/div[3]/div[1]/div[2]/p/text()')[0]
        item['开盘时间']=''
        item['物业费']=''
        item['latitude']=''
        item['longitude']=''
        item['抓取年份']=year
        item['抓取月份']=month
        item['数据来源']='中海地产'
        item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        info_base.insert_one(item)
        has_spider.insert_one({'标题url': url})
        print(item)
if __name__ == '__main__':
    getInfo()