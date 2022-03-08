# coding=utf-8
import pymongo
import time
from lxml import etree
import requests
from config import typedict,MONGODB_CONFIG,fheaders,headers,citylist,getheaders,get_proxy,cookie_header
from urllib import parse
MONGODB_CONFIG = {
   "host": "8.135.119.198",
   "port": "27017",
   "user": "hladmin",
   "password": parse.quote("Hlxkd3,dk3*3@"),
   "db": "dianping",
   "collections": "dianping_collections",
}

# info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
#             MONGODB_CONFIG['user'],
#             MONGODB_CONFIG['password'],
#             MONGODB_CONFIG['host'],
#             MONGODB_CONFIG['port']),
#             retryWrites="false")['大众点评']['美食_列表页链接_202106']
info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['大众点评']['深圳_列表页链接_202109']
cookie_data = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['大众点评']['cookie数据']
def gethtml(url):
    for ii in range(1000):
        time.sleep(10)
        # proxy = get_proxy()
        Cookinfo = cookie_data.find_one()
        Cookies = Cookinfo['Cookie']
        Cooknum = Cookinfo['号码']
        headers = cookie_header()
        headers['Cookie'] = Cookies
        # headers['Cookie']='_lxsdk_cuid=179c01ab88cc8-0df2f0b9256ac1-2363163-1fa400-179c01ab88cc8; _hc.v=fb783b09-adc2-78df-f8a5-7b53f530416c.1622425648; s_ViewType=10; _dp.ac.v=19b24d59-781c-4e11-94fc-d848cfb75d8f; ctu=21fd3f032ee980c9b98bee37cc18e7671d5ddb8684865c57d85b840ce1fe7fff; aburl=1; ua=dpuser_1966568564; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1622711914; uuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; iuuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _lxsdk=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _ga=GA1.2.1975686433.1622713531; switchcityflashtoast=1; default_ab=citylist%3AA%3A1%7Cshop%3AA%3A11%7Cindex%3AA%3A3%7CshopList%3AA%3A5%7Cmap%3AA%3A1; cy=219; cye=dongguan; fspop=test; m_flash2=1; cityid=7; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1628644029,1628731677,1628818276,1629077694; dper=989da530f9ae3713022e170efc199d425e7e60601d76eed2cc918ecc5d334a55b5415495914b1f8da18932ccae18f7a705e95ff6f0065ec6d99f871298db8ce1c264c082b16b2c2ea154f8cf4fc4a79aa6fc4fa1d1281e3553e0b47164a3a6ae; ll=7fd06e815b796be3df069dec7836c3df; uamo=18523046785; dplet=19cd5750f538a8ac4a9ac5232809ef3d; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1629089140; _lxsdk_s=17b4d43aa34-b76-0f9-308%7C%7C103'
        # proxies = {
        #     "https": proxy,
        #     "http": proxy,
        # }
        try:
            r = requests.get(url=url, headers=headers)
        except Exception as e:
            print(e)
            continue
        if r.status_code == 200:
            r.encoding = 'utf8'
        else:
            print('获取页面失败',r.status_code)
            continue
        if '页面不存在' in r.text:
            print('页面不存在')
            # time.sleep(10)
            continue
        if '无效用户' in r.text:
            print('无效用户')
            continue
        return r
def getcity():
    provinceid = [i for i in range(1,35)]
    # print(provinceid)
    url='http://www.dianping.com/ajax/citylist/getDomesticCityByProvince'
    citylist=[]
    for p in provinceid:
        json={'provinceId': p}
        time.sleep(1)
        res=requests.post(url,json=json,headers=cookie_header())
        for d in res.json()['cityList']:
            data = {}
            data['cityId']=d['cityId']
            data['cityName']=d['cityName']
            data['cityPyName']=d['cityPyName']
            citylist.append(data)
    return citylist
def getlilteregion(url):
    # time.sleep(1)
    for ii in range(1000):
        # proxies = {"http": get_proxy()}
        try:
            # r = requests.get(url, headers=getheaders(), proxies=proxies, timeout=5)
            r=gethtml(url)
        except Exception as e:
            print(e)
            continue
        if r.status_code == 200:
            r.encoding = 'utf8'
        else:
            print('获取页面失败',r.status_code)
            continue
        if '页面不存在' in r.text:
            print('页面不存在')
            # time.sleep(10)
            continue
        if '无效用户' in r.text:
            print('无效用户')
            continue
        try:
            html = etree.HTML(r.text)
            box = html.xpath('//*[@id="region-nav-sub"]/a')[1:]
        except:continue
        lilteregionlist = []
        for i in box:
            data = {}
            url = i.xpath('./@href')[0]
            region = i.xpath('./span/text()')[0]
            data[region] = url
            lilteregionlist.append(data)
        return lilteregionlist

def getregion(url):
    # time.sleep(1)
    for ii in range(1000):
        # proxies = {"http": get_proxy()}
        try:
            # r = requests.get(url, headers=getheaders(), proxies=proxies, timeout=3)
            r = gethtml(url)
        except Exception as e:
            print(e)
            continue
        if r.status_code == 200:
            r.encoding = 'utf8'
        else:
            # print('获取页面失败',r.status_code)
            continue
        if '页面不存在' in r.text:
            print('页面不存在')
            # time.sleep(10)
            continue
        if '无效用户' in r.text:
            print('无效用户')
            continue
        # res=requests.get(url,headers=headers)
        try:
            html=etree.HTML(r.text)
            box=html.xpath('//*[@id="region-nav"]/a')
        except:continue
        regionlist=[]
        for i in box:
            data={}
            url=i.xpath('./@href')[0]
            region=i.xpath('./span/text()')[0]
            data[region]=url
            regionlist.append(data)
        return regionlist
def getliltetype(url):
    for ii in range(1000):
        # proxies = {"http": get_proxy()}
        try:
            # r = requests.get(url, headers=getheaders(), proxies=proxies, timeout=5)
            r = gethtml(url)
        except Exception as e:
            # print(e)
            continue
        if r.status_code == 200:
            r.encoding = 'utf8'
        else:
            # print('获取页面失败',r.status_code)
            continue
        if '页面不存在' in r.text:
            # print('页面不存在')
            # time.sleep(10)
            continue
        if '无效用户' in r.text:
            # print('无效用户')
            continue
        try:
            html=etree.HTML(r.text)
            box=html.xpath('//*[@id="classfy"]/a')
        except:continue
        litletypelist=[]
        for i in box:
            data={}
            url=i.xpath('./@href')[0]
            region=i.xpath('./span/text()')[0]
            data[region]=url
            litletypelist.append(data)
        return litletypelist
def getpagenum(url):
    for ii in range(1000):
        # proxies = {"http": get_proxy()}
        try:
            # r = requests.get(url, headers=getheaders(), proxies=proxies, timeout=5)
            r = gethtml(url)
        except Exception as e:
            # print(e)
            continue
        if r.status_code == 200:
            r.encoding = 'utf8'
        else:
            # print('获取页面失败',r.status_code)
            continue
        if '页面不存在' in r.text:
            # print('页面不存在')
            # time.sleep(10)
            continue
        if '无效用户' in r.text:
            # print('无效用户')
            continue
        try:
            html = etree.HTML(r.text)
        except:continue
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

# x=info_base.distinct('cityname')
# print(x)



# x=info_base.delete_many({})
# print(x.deleted_count,'个文档已删除')

print(info_base.distinct('type'))

tag=False
for city in citylist:
    if city['cityName'] != '深圳':continue
    print('抓取城市',city['cityName'])
    for typ in typedict.values():
        if typ not in ['ch10','ch30','ch15','ch45','ch80']:continue                       #需要的大类
        # if typ not in ['ch80']:continue                       #需要的大类
        url='http://www.dianping.com/'+city['cityPyName']+'/'+typ
        regionlist=getregion(url)
        print(regionlist)
        for regidict in regionlist:
            for k,v in regidict.items():
                # if k == '寮步镇':
                #     tag=True
                # if not tag:continue
                print(k,v)
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




