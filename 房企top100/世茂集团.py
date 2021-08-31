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
            retryWrites="false")['房企top100']['世茂集团_数据_202107']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['房企top100']['世茂集团_去重_202107']
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
}

def get_proxy():
    try:
            return requests.get('http://demo.spiderpy.cn/get/').json().get('proxy')
            # return '111.202.83.35:80'
    except:
        num = 3
        while num:
            try:
                return requests.get('http://demo.spiderpy.cn/get/').json().get('proxy')
            except:
                print('暂无ip，等待20秒')
                time.sleep(20)

                num -= 1
        print('暂无ip')
def get_html(url):
    try:
        # proxies = {"https": get_proxy()}
        response = requests.get(url, headers=headers,timeout=(10, 10))
        # encod = response.apparent_encoding
        # if encod.upper() in ['GB2312', 'WINDOWS-1254']:
        #     encod = 'gbk'
        # response.encoding = encod
        return response
    except Exception as e:
        print('geturl错误',url, e)
        return get_html(url)

def getUrlList(page=1,list=[]):
    url = 'https://www.shimaogroup.com/smlist/list.php?tid=34&page=' + str(page)
    res = get_html(url)
    res.encoding = 'utf8'
    html = etree.HTML(res.text)
    urls = html.xpath('/html/body/div[5]/div/div[1]/div[1]/a/@href')
    pages=html.xpath('/html/body/div[5]/div/div[1]/div[2]/div/text()')[0]
    pages=re.findall('\d+',pages)[0]
    print('共%s页,当前第%d页' %(pages,page))
    for i in urls:
        url = 'https://www.shimaogroup.com' + i
        print(url)
        list.append(url)
    nextpage=page+1
    if page == int(pages):
    # if page == 5:
        return list
    return getUrlList(nextpage,list)
def getInfo():
    urlList=getUrlList()
    for url in urlList:
        has_spider_urllist = []
        for has_spider_url in has_spider.find():
            has_spider_urllist.append(has_spider_url['标题url'])
        if url in has_spider_urllist:
            print('该页数据已爬取，下一页')
            continue
        item={}
        res=get_html(url)
        res.encoding='utf8'
        # print(res.text)
        html=etree.HTML(res.text)
        item['城市']=re.findall('class="iconfont icon-zuobiaofill"></em>(.*?)</span>',res.text)[0]
        item['区县']=''
        item['标题']=re.findall('h1 style="margin-top:35px;"><p>(.*?)</p><span><em class="iconfont icon-zuobiaofill',res.text)[0]
        item['标题url']=url
        item['销售情况']=''
        item['分类']=html.xpath('//div[@class="hzhengwen"]//tr[1]/td[2]/text()')[0]
        try:
            item['装修']=html.xpath('//div[@class="hzhengwen"]//tr[2]/td[6]/text()')[0]
        except:
            item['装修'] =''
        item['户型'] = ''
        try:
            item['单价']=html.xpath('/html/body/div[4]/div[1]/div[2]/h3/text()')[0]
        except:
            item['单价'] =''
        item['总价']=''
        item['建面']=''
        item['最小建面']=''
        item['最大建面']=''
        try:
            item['容积率']=html.xpath('//div[@class="hzhengwen"]//tr[1]/td[4]/text()')[0]
        except:
            item['容积率'] =''
        try:
            item['绿化率']=html.xpath('//div[@class="hzhengwen"]//tr[2]/td[4]/text()')[0]
        except:
            item['绿化率'] = ''
        try:
            item['规划户数']=html.xpath('//div[@class="hzhengwen"]//tr[3]/td[2]/text()')[0]
        except:
            item['规划户数'] =''
        item['总户数']=''
        try:
            item['建筑面积']=html.xpath('//div[@class="hzhengwen"]//tr[2]/td[2]/text()')[0]
        except:
            item['建筑面积'] = ''
        item['地址']=re.findall('<h4><strong>项目地址：</strong><p>(.*?)</p></h4>',res.text)[0]
        tags=re.findall('<p class=bq.>(.*?)</p>',res.text)
        tag=''
        for i in tags:
            tag=tag+i+' '
        item['标签']=tag
        try:
            item['交房时间']=html.xpath('//div[@class="hzhengwen"]//tr[1]/td[6]/text()')[0]
        except:
            item['交房时间'] = ''
        item['物业费']=''
        item['latitude']=''
        item['longitude']=''
        item['数据来源']='世茂集团'
        item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        item['抓取年份'] = year
        item['抓取月份'] = month
        item['抓取日期'] = day
        info_base.insert_one(item)
        has_spider.insert_one({'标题url': url})
        print(item)
if __name__ == '__main__':
    year = 2021
    month = 7
    day = 15
    getInfo()