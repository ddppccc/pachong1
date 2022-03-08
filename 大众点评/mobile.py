# encoding=utf-8
from config import get_proxy,getheaders,rancook
from concurrent.futures import ThreadPoolExecutor
from  获取token import token
from d import P
from 美食 import getpagedata
from 获取位置 import getmpos
import random
import time
from config import rans
import json
import requests
headers = {
        # 'Connection': 'keep-alive',
        'Content-Type': "application/json",
        'Content-Length': '1518',
        'Cookie': f'_lxsdk_cuid=179c01ab88cc8-0df2f0b9256ac1-2363163-1fa400-179c01ab88cc8; _hc.v=fb783b09-adc2-78df-f8a5-7b53f530416c.1622425648; s_ViewType=10; _dp.ac.v=19b24d59-781c-4e11-94fc-d848cfb75d8f; ctu=21fd3f032ee980c9b98bee37cc18e7671d5ddb8684865c57d85b840ce1fe7fff; aburl=1; cityid=9; Hm_lvt_233c7ef5b9b2d3d59090b5fc510a19ce=1622431578; ua=dpuser_1966568564; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1622711914; uuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; iuuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _lxsdk=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _ga=GA1.2.1975686433.1622713531; default_ab=shop%3AA%3A11%7CshopList%3AA%3A5; fspop=test; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1623377928,1623721805,1623807276,1623807383; cy=9; cye=chongqing; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1623809568; msource=default; logan_custom_report=; Hm_lvt_220e3bf81326a8b21addc0f9c967d48d=1622774935,1622775917,1623830756,1623830792; logan_session_token=2llbcafju38n1f5a3sgf; Hm_lpvt_220e3bf81326a8b21addc0f9c967d48d=1623830801; _lxsdk_s=17a13ce14bd-259-b9-d37%7C%7C578',
        'Host': 'm.dianping.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Mobile Safari/537.36',
    }
url='https://m.dianping.com/isoapi/module'

def gettoken():
    with open('token.txt','r') as f:
        token=f.read()
        return token
dd = {"pageEnName": "shopList",
      "moduleInfoList": [{"moduleName": "mapiSearch",
                          "query": {"search": {"start": 20,
                                               "categoryId": "10",
                                               "parentCategoryId": 10,
                                               "locateCityid": 0,
                                               "limit": 20,
                                               "sortId": "0",
                                               "cityId": 9,
                                               "range": "-1",
                                               "maptype": 0,
                                               "keyword": ""}}}],
      "_token": gettoken()
      }

pool = ThreadPoolExecutor(1)
uuid = f'fb{rans(5)}9-adc2-78df-f8a5-7b53{rans(6)}6c.{str(int(time.time()))}'
dta={"uuid":"%s"%uuid,"platform":1,"partner":150,"optimusCode":10,"originUrl":"https://m.dianping.com/chongqing/ch10/d1?from=m_nav_1_meishi","pageEnName":"shopList","moduleInfoList":[{"moduleName":"mapiSearch","query":{"search":{"start":0,"categoryId":"10","parentCategoryId":10,"locateCityid":0,"limit":20,"sortId":"0","cityId":9,"range":"-1","maptype":0,"keyword":""}}},{"moduleName":"downloadlayer","query":{}},{"moduleName":"autoopen","query":{}},{"moduleName":"side-activity","query":{},"config":{"imageUrl":"https://p0.meituan.net/travelcube/701ffbb879778257dfd58a566dbedc435356.png","openUrl":"dianping://mycardcoupon?notitlebar=true","downloadUrl":"https://m.dianping.com/download/redirect?id=5524665","url":"https://h5.dianping.com/app/usercenter/coupon.html"}}],"_token":"%s"%gettoken()}
data='pageEnName=index&moduleInfoList%5B0%5D%5BmoduleName%5D=cnxh&moduleInfoList%5B0%5D%5Bversion%5D=0&moduleInfoList%5B0%5D%5Bconfig%5D%5Bbord%5D=true&moduleInfoList%5B0%5D%5Bconfig%5D%5BhideWelfare%5D=false&moduleInfoList%5B0%5D%5Bconfig%5D%5BmoreUTM%5D=pmx%3Aall%3Aindex_cnxhgengduo%3Am&moduleInfoList%5B0%5D%5Bconfig%5D%5BadId%5D=m_dacu_banner&moduleInfoList%5B0%5D%5Bconfig%5D%5BshowOverlay%5D=true&moduleInfoList%5B0%5D%5Bconfig%5D%5BcategoryType%5D=standard&moduleInfoList%5B0%5D%5Bconfig%5D%5Bmainwelfare_utm%5D=ulink_mainwelfare&moduleInfoList%5B0%5D%5Bconfig%5D%5Bmainwelfare_link_ios%5D=%2F%2Flink.dianping.com%2Funiversal-link%3ForiginalUrl%3Dhttp%253A%252F%252Fevt.dianping.com%252Fsynthesislink%252F10765.html%26schema%3Ddianping%253A%252F%252Fweb%253Furl%253Dhttps%25253A%25252F%25252Fh5.dianping.com%25252Fapp%25252Fdaily-benefits%25252Fstatic%25252Findex.html%252523%25252Findex%25253Futm_source%25253DMcnxh&moduleInfoList%5B0%5D%5Bconfig%5D%5BoneUTM%5D=pmx%3Aall%3Aindex_cnxhone%3Am&modul'
h={
    'Host': 'm.dianping.com',
    'Connection': 'keep-alive',
    # 'Content-Length': '2002',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Mobile Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://m.dianping.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://m.dianping.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie':"_lxsdk_cuid=179c01ab88cc8-0df2f0b9256ac1-2363163-1fa400-179c01ab88cc8; _hc.v=fb783b09-adc2-78df-f8a5-7b53f530416c.1622425648; s_ViewType=10; _dp.ac.v=19b24d59-781c-4e11-94fc-d848cfb75d8f; ctu=21fd3f032ee980c9b98bee37cc18e7671d5ddb8684865c57d85b840ce1fe7fff; aburl=1; Hm_lvt_233c7ef5b9b2d3d59090b5fc510a19ce=1622431578; uuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; iuuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _lxsdk=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _ga=GA1.2.1975686433.1622713531; switchcityflashtoast=1; cityid=7; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1629444907; cy=9; cye=chongqing; fspop=test; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1631683812,1631842237,1632624328,1632706684; dplet=f936c5651e77e809d4a34c40522194a7; dper=ffc453d4de3fda2cc91b7aa202eb9f919c7bf8341cce158442e514a3278e39a20d86ae065ed22d99ab2a59e3899ebdfd1ccb324526d32a948d3096e298561064093118bfdd9b91c2ee8f43000c826a08501a29751f20f66c8afe2a6607a5f1f8; ll=7fd06e815b796be3df069dec7836c3df; ua=%E7%89%87%E7%89%87%E9%A2%9D; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1632711030; msource=default; chwlsource=default; logan_custom_report=; Hm_lvt_220e3bf81326a8b21addc0f9c967d48d=1632711074; default_ab=index%3AA%3A3%7Cmyinfo%3AA%3A1; logan_session_token=p1cas9foqj53880hoylt; Hm_lpvt_220e3bf81326a8b21addc0f9c967d48d=1632711092; _lxsdk_s=17c25090cba-0a8-430-157%7C%7C298"
    # 'Cookie':rancook,
    # 'Cookie':'_lxsdk_cuid=179c01ab88cc8-0df2f0b9256ac1-2363163-1fa400-179c01ab88cc8; _hc.v=fb783b09-adc2-78df-f8a5-7b53f530416c.1622425648; s_ViewType=10; _dp.ac.v=19b24d59-781c-4e11-94fc-d848cfb75d8f; ctu=21fd3f032ee980c9b98bee37cc18e7671d5ddb8684865c57d85b840ce1fe7fff; aburl=1; cityid=9; Hm_lvt_233c7ef5b9b2d3d59090b5fc510a19ce=1622431578; ua=dpuser_1966568564; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1622711914; uuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; iuuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _lxsdk=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _ga=GA1.2.1975686433.1622713531; cy=2; cye=beijing; default_ab=shop%3AA%3A11%7Cindex%3AA%3A3%7CshopList%3AA%3A5%7Cmap%3AA%3A1; switchcityflashtoast=1; dp_pwa_v_=fe25b31c1e622e79b2c551c1b73fa76ba19c48e7; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1625017013,1625219146,1625563435,1626835526; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1626835539; logan_custom_report=; msource=default; Hm_lvt_220e3bf81326a8b21addc0f9c967d48d=1625557798,1626842582,1626842597,1626847372; chwlsource=default; source=m_browser_test_22; pvhistory="6L+U5ZuePjo8L3N1Z2dlc3QvZ2V0SnNvbkRhdGE/Xz0xNjI2ODQ4ODU4MjE5JmNhbGxiYWNrPVplcHRvMTYyNjg0ODg1NTEyNz46PDE2MjY4NDg4NTgwNzFdX1s="; m_flash2=1; logan_session_token=fc07dbmqspzu0oxinufh; Hm_lpvt_220e3bf81326a8b21addc0f9c967d48d=1626848870; _lxsdk_s=17ac7a80b78-225-662-7e3%7C%7C679',
    # 'Content-Length': '%d'%(len(data)-28),
}
while True:
    proxies = {
        "https": get_proxy(),
        "http": get_proxy(),
               }
    try:
        rr=requests.post(url=url,json=data,verify=False,headers=h)
        # rr=requests.post(url=url,data=data,headers=h)
    except Exception as e:
        print(e)
        continue
    if rr.status_code != 200:
        print('errpr',rr.status_code)
        continue
    rr.encoding=rr.apparent_encoding
    if '页面不存在' in rr.text:
        print('页面不存在')
        continue
    elif '网络好像不太给力' in rr.text:
        print('网络好像不太给力')
        continue
    else:
        print(rr.json()['code'])
        l=[]
        for i in rr.json()['data']['moduleInfoList'][0]['moduleData']['data']['listData']['list']:
            data={}
            try:
                adr=i['branchName']
            except:
                adr=''
            # print(i['name'],adr)

            data['标题']=i['name']+adr
            data['标题url']='http://www.dianping.com/shop/'+i['shopuuid']
            data['评论数量']=i['reviewCount']
            data['综合评分']=i['starScore']
            data['平均消费']=i['priceText']
            data['标签']=i['matchText']
            # data['shopuuid']=i['shopuuid']
            # shop = getmpos(i['shopuuid'])
            # data['glng'] = shop['glng']
            # data['glat'] = shop['glat']
            try:
                print(data)
            except:pass
            # getpagedata(data['标题url'],data,'ch10','9')
            # done = pool.submit(getpagedata,data['标题url'],data,'ch10','9')
            # l.append(done)
        # [obj.result() for obj in l]
    break


