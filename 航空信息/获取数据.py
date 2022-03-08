# coding=utf-8
import time

import pymongo
from urllib import parse
import requests
import re
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
            retryWrites="false")['民航']['民航_列表页链接2_202109']
headers={
    'Host': 'www.caac.gov.cn',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://www.caac.gov.cn/XXGK/XXGK/TJSJ/index_1215.html',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': '__FT10000021=2021-9-29-15-11-7; __NRU10000021=1632899467473; __RT10000021=2021-9-29-15-11-7; Hm_lvt_4014848c4e18723269ffe0193734e573=1632899468; caac=18686823; wzws_cid=6d12524da54c83d5b1a637d8b2b1a8c789aa9eb8f18e5133a12019aa16ad39fb6384faa02c87e53e68bff618b83b4f132e92bf720fa24c5b0d9c4fc815d3a432ba50553c0cad1c28be58935feb808b86; Hm_lpvt_4014848c4e18723269ffe0193734e573=1632899740'

}




def getpdfurl(url):
    # url='http://www.caac.gov.cn/XXGK/XXGK/TJSJ/202109/t20210922_209298.html'
    res=requests.get(url,headers=headers)
    res.encoding='utf8'
    try:
        pdfurl=re.findall('href="\.(/P\d+\.pdf)"',res.text.replace(' ','').replace('\n',''))[0]
    except:
        return

    baseurl=url.split('/')[-2]
    pdfurl = 'http://www.caac.gov.cn/XXGK/XXGK/TJSJ/' +baseurl + pdfurl
    print(pdfurl)
    return pdfurl


def download(url,title):
    time.sleep(3)
    res = requests.get(url, headers=headers)
    res.encoding = 'utf8'
    with open('pdf/'+title+'.pdf','wb') as f:
        f.write(res.content)
    print('保存成功')

for d in info_base.find():
    print(d['标题'])
    url='http://www.caac.gov.cn/XXGK/XXGK/TJSJ'+d['url'][1:]
    print(url)
    pdfurl=getpdfurl(url)
    if pdfurl:
        download(pdfurl,d['标题'])
        time.sleep(10)
    else:
        print('无pdf..')
        time.sleep(5)

