import re
import time
from gridfs import GridFS
import pdfkit
import pymongo
import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
from urllib import parse
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
    'Host': 'www.innocom.gov.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
}
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
    retryWrites="false")['高新技术企业公示']['公示公告数据_202108']

url_data = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['高新技术企业公示']['url_202108']


def get_tree(url):
    while True:
        try:
            prox = get_proxy()
            proxies = {'http': prox,
                       'https': prox}
            response = requests.get(url, headers=headers, proxies=proxies, timeout=(3, 5))
            res = response.text
            tree = etree.HTML(res)
            return tree
        except:
            continue


def get_urOne(i):  # i=1 -> 公式的city url          i=2 -> 公告的 二级标题 url
    startUrl = 'http://www.innocom.gov.cn/gqrdw/index.shtml'
    tree = get_tree(startUrl)
    cityUrl = {}
    for li in tree.xpath('//div[@class="content"][%s]/a' % str(i)):
        key = ''.join(li.xpath('./text()')).replace(' ','')
        cityUrl[key] = 'http://www.innocom.gov.cn' + ''.join(li.xpath('./@href'))
    return cityUrl


def get_ggCityUrl(item):
    for ejKey in item:
        url = item[ejKey]
        tree = get_tree(url)
        cityUrl = {}
        for li in tree.xpath('//dd/a'):
            key = ''.join(li.xpath('./text()'))
            cityUrl[key] = 'http://www.innocom.gov.cn' + ''.join(li.xpath('./@href'))
        item[ejKey] = cityUrl
    return item


def get_url(url, urlList):
    while True:
        tree = get_tree(url)
        lis = tree.xpath('//ul[@class="list"]/li')
        for li in lis:
            item = {}
            item['url'] = 'http://www.innocom.gov.cn' + ''.join(li.xpath('./a/@href'))
            item['发布时间'] = ''.join(li.xpath('./span/text()')).replace('\n', '').replace(' ', '').replace('\r', '')
            item['标题'] = ''.join(li.xpath('./a/text()'))
            urlList.append(item)
        if lis == []:
            continue
        for page in range(2, 50):
            # try:
            nexturl = ''.join(re.findall('(.+)\.shtml', url)) + '_' + str(page) + '.shtml'
            tree = get_tree(nexturl)
            lis = tree.xpath('//ul[@class="list"]/li')
            if lis == []:
                return urlList
            for li in lis:
                item = {}
                item['url'] = 'http://www.innocom.gov.cn' + ''.join(li.xpath('./a/@href'))
                item['发布时间'] = ''.join(li.xpath('./span/text()')).replace('\n', '').replace(' ', '').replace('\r', '')
                item['标题'] = ''.join(li.xpath('./a/text()'))
                urlList.append(item)


def get_data(url,item):
    star = 0
    while True:
        if url_data.count({'url': url}):
            print('当前url已爬取')
            return
        tree = get_tree(url)
        text = ''.join(tree.xpath('//div[@id="detailContent"]//text()')).replace('扫一扫在手机打开当前页','').replace(' ','')
        pdfUr = ''.join(tree.xpath('//div[@id="detailContent"]//a/@href'))
        pdfName = ''.join(tree.xpath('//div[@id="detailContent"]//a/text()'))
        if pdfName == '' and text == '':
            text = ''.join(tree.xpath('//div[@id="content"]//text()'))
            pdfUr = ''.join(tree.xpath('//div[@id="content"]//a/@href'))
            pdfName = ''.join(tree.xpath('//div[@id="content"]//a/text()'))
        if '.pdf' in pdfName:
            pdfName = pdfName
        elif '.doc' in pdfName:
            pdfName = pdfName
        else:
            if '.pdf' in pdfUr:
                pdfName = pdfName + '.pdf'
            elif '.doc' in pdfUr:
                pdfName = pdfName + '.doc'

        item['pdf文件'] = pdfName
        item['text'] = text
        pdfUrl = ''.join(re.findall('(.+/)',item['url'])) + pdfUr
        urlfl = pdfUrl.split('/')
        if 'c' in urlfl:
            print('当前数据PDF文件无法获取，跳过')
            return
        item['pdf文件id'] = urlfl[-1][:-4]
        item['pdf文件url'] = pdfUrl
        if item['pdf文件'] == '':
            star += 1
            print('数据有误，请查看具体原因=>%s' % (str(item)))
            if star == 3:
                if item['pdf文件'] != '':
                    return
                info_base.insert_one(item)
                url_data.insert_one({'url': item['url']})
                return

        get_pdf(pdfUrl, item['pdf文件'])
        pdf_mongo(item['pdf文件'], item['pdf文件id'])
        info_base.insert_one(item)
        url_data.insert_one({'url': url})
        print(item)
        return



# ej = requests.get('http://www.innocom.gov.cn/gqrdw/c101466/201903/a52749c2de2941668a90f6b2bb2e3be0/files/fcb5bfa2cced4718b7ddb168a15efe0a.pdf')


def get_pdf(pdfurl, pdfname):
    pdflj = 'PDF文件/' + pdfname
    while True:
        try:
            prox = get_proxy()
            proxies = {'http': prox,
                       'https': prox}
            res = requests.get(pdfurl, headers=headers, proxies=proxies, timeout=(3,5))
            res.encoding = res.apparent_encoding
            with open(pdflj, 'wb') as f:
                f.write(res.content)
            tree = etree.HTML(res.text)
            if tree.xpath('//title/text()') != []:
                continue
            if tree.xpath('//h1/text()') != []:
                continue
            if tree.xpath('//a/text()') != []:
                continue
            return
        except Exception as e:
            print(e)
            continue


# from pymongo import Connection



# db = Connection().text_database


def pdf_mongo(file_name,id):  # 本地文件名
    pdflj = 'PDF文件/' + file_name
    file_coll = 'pdf_202108'
    db = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
        MONGODB_CONFIG['user'],
        MONGODB_CONFIG['password'],
        MONGODB_CONFIG['host'],
        MONGODB_CONFIG['port']),
        retryWrites="false")['高新技术企业公示']
    filter_condition = {"filename": file_name, 'pdfID': id, 'version': 2}
    gridfs_col = GridFS(db, collection=file_coll)
    query = {"pdfID": ""}
    query["pdfID"] = id

    if gridfs_col.exists(query):
        print(query,'=============================================================')
        print('已经存在该文件')
    else:
        with open(pdflj, 'rb') as file_r:
            file_data = file_r.read()
            gridfs_col.put(data=file_data, **filter_condition)  # 上传到gridfs

def run():
    cityUrl = get_urOne(1)  # {城市：url}
    titleUrl = get_urOne(2)  # {二级标题：url}
    ggCityUrl = get_ggCityUrl(titleUrl)  # {二级标题：{城市：url}}
    for ejbt in ggCityUrl:
        dec = ggCityUrl[ejbt]
        for city in dec:
            urlList = get_url(dec[city], [])
            print(ejbt, city, urlList)
            for item in urlList:
                item['分类'] = '公告'
                item['二级标题'] = ejbt
                item['城市'] = city
                # get_data(item['url'], item)  # dataurl
                pool.submit(get_data, item['url'], item)
    for city in cityUrl:
        urlList = get_url(cityUrl[city], [])
        print(city, urlList)
        for item in urlList:
            item['分类'] = '公示'
            item['城市'] = city
            # get_data(item['url'], item)  # dataurl
            pool.submit(get_data, item['url'], item)





if __name__ == '__main__':
    # get_data('http://www.innocom.gov.cn/gqrdw/c101523/202012/f1950a648d9e4cb3b637ad8c541837ce.shtml',{'分类':'asdasd','url':'http://www.innocom.gov.cn/gqrdw/c101523/202012/f1950a648d9e4cb3b637ad8c541837ce.shtml'})
    # pdf_mongo('关于取消天津魔幻动力科技有限公司高新技术企业资格的公告.pdf','1f9b06e669c4480d82f48fd815dc1b1c')
    # get_pdf('http://www.innocom.gov.cn/gqrdw/c101407/202007/de15e2c92a0b48f296f2d8422c68dffc/files/1c359d35573d4413a901f72932c90b0e.pdf','北京市2020年第一批拟认定高新技术企业名单.pdf')
    pool = ThreadPoolExecutor()
    # info_base.delete_many({'分类': {"$exists": True}})
    # url_data.delete_many({'url':  {"$exists": True}})
    # # print(get_url('http://www.innocom.gov.cn/gqrdw/c101407/list_gsgg_l3.shtml', []))
    run()
    # print(info_base.find_one({'pdf文件id':'c/ee0ce9f85784437bbc7cecf8d851ac8c'}))

