import pymongo
import time
from lxml import etree
import requests
from config import typedict,MONGODB_CONFIG,fheaders,headers,citylist
from urllib import parse
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
            retryWrites="false")['大众点评']['休闲娱乐_列表页链接_202106']
def getcity():
    provinceid = [i for i in range(1,35)]
    # print(provinceid)
    url='http://www.dianping.com/ajax/citylist/getDomesticCityByProvince'
    citylist=[]
    for p in provinceid:
        json={'provinceId': p}
        time.sleep(1)
        res=requests.post(url,json=json,headers=headers)
        for d in res.json()['cityList']:
            data = {}
            data['cityId']=d['cityId']
            data['cityName']=d['cityName']
            data['cityPyName']=d['cityPyName']
            citylist.append(data)
    return citylist
def getlilteregion(url):
    time.sleep(1)
    res = requests.get(url, headers=headers)
    html = etree.HTML(res.text)
    box = html.xpath('//*[@id="region-nav-sub"]/a')[1:]
    lilteregionlist = []
    for i in box:
        data = {}
        url = i.xpath('./@href')[0]
        region = i.xpath('./span/text()')[0]
        data[region] = url
        lilteregionlist.append(data)
    return lilteregionlist

def getregion(url):
    time.sleep(1)
    res=requests.get(url,headers=headers)
    html=etree.HTML(res.text)
    box=html.xpath('//*[@id="region-nav"]/a')
    regionlist=[]
    for i in box:
        data={}
        url=i.xpath('./@href')[0]
        region=i.xpath('./span/text()')[0]
        data[region]=url
        regionlist.append(data)
    return regionlist
def getliltetype(url):
    res=requests.get(url,headers=headers)
    html=etree.HTML(res.text)
    box=html.xpath('//*[@id="classfy"]/a')
    litletypelist=[]
    for i in box:
        data={}
        url=i.xpath('./@href')[0]
        region=i.xpath('./span/text()')[0]
        data[region]=url
        litletypelist.append(data)
    return litletypelist
def getpagenum(url):
    res = requests.get(url, headers=headers)
    html = etree.HTML(res.text)
    try:
        pagenum = html.xpath('/html/body/div[2]/div[3]/div[1]/div[2]/a/text()')[-2]
    except:
        pagenum = '1'
    return pagenum


def savedata(cityname,cityid,type,pagenum,url):
    data={
        'cityname':cityname,
        'cityid':cityid,
        'type':type,
        'pagenum':pagenum,
        'url':url,
        'status':0
    }
    if not info_base.find_one({'url':url}):
        info_base.insert_one(data)
        print(data)
        # print('存储成功')
    else:
        print('该url已存在')


for city in citylist:
    print('抓取城市',city['cityName'])
    for typ in typedict.values():
        if typ not in ['ch30']:continue                       #选择需要的大类
        url='http://www.dianping.com/'+city['cityPyName']+'/'+typ
        regionlist=getregion(url)
        # print(regionlist)
        for regidict in regionlist:
            for k,v in regidict.items():
                # print(k,v)
                pagenum=getpagenum(v)
                # print('总页数',pagenum)
                if int(pagenum) == 50:
                    lilteregionlist=getlilteregion(v)
                    # print(lilteregionlist)
                    for lilteregiondict in lilteregionlist:
                        for lk,lv in lilteregiondict.items():
                            pagenum = getpagenum(lv)
                            if int(pagenum) == 50:
                                list=getliltetype(lv)
                                # print(list)
                                for liltetypedict in list:
                                    for ltk,ltv in liltetypedict.items():
                                        pagenum = getpagenum(ltv)

                                        savedata(city['cityName'],city['cityId'],typ,pagenum,ltv)
                            else:

                                savedata(city['cityName'], city['cityId'], typ, pagenum, lv)
                else:
                    savedata(city['cityName'], city['cityId'], typ, pagenum, v)


