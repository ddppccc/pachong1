import json
from urllib import parse
from lxml import  etree
import time
import requests
import random
import pymongo
from fake_useragent import UserAgent
MONGODB_CONFIG = {
   "host": "8.135.119.198",
   "port": "27017",
   "user": "hladmin",
   "password": parse.quote("Hlxkd3,dk3*3@"),
   "db": "dianping",
   "collections": "dianping_collections",
}
CookieList=[
        # 15736037945
        'fspop=test; cy=9; cye=chongqing; _lxsdk_cuid=17b0f1f65f5b0-0ecedb46b8f298-2343360-1fa400-17b0f1f65f6c8; _lxsdk=17b0f1f65f5b0-0ecedb46b8f298-2343360-1fa400-17b0f1f65f6c8; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1628046321; _hc.v=3aad3c48-8949-3c39-5fba-9ce91e9a3895.1628046321; dplet=03d49c83a33f2f089c0b67e9f0119de3; dper=429d454f760df76593f1310023fd9b4969b6001bf652b9c55f7c5b7fa0b5b974daf93e1e4549b0518baceb697c5b54580759053cb50dc94a3575227b0923f90bdc822895f917f88b38c5e60afc17a8e70536d5ccfc4617ae43a844d6c1652651; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_8857687679; ctu=2582e35ed32bc48d46e18c88d011ad71040a001309071f4f05a98df4bb8a085d; uamo=15736037945; s_ViewType=10; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1628046386; _lxsdk_s=17b0f1f65f6-d3f-07c-60d%7C%7C51',
        # 18523046785
        '_lxsdk_cuid=179c01ab88cc8-0df2f0b9256ac1-2363163-1fa400-179c01ab88cc8; _hc.v=fb783b09-adc2-78df-f8a5-7b53f530416c.1622425648; s_ViewType=10; _dp.ac.v=19b24d59-781c-4e11-94fc-d848cfb75d8f; ctu=21fd3f032ee980c9b98bee37cc18e7671d5ddb8684865c57d85b840ce1fe7fff; aburl=1; ua=dpuser_1966568564; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1622711914; uuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; iuuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _lxsdk=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _ga=GA1.2.1975686433.1622713531; switchcityflashtoast=1; default_ab=citylist%3AA%3A1%7Cshop%3AA%3A11%7Cindex%3AA%3A3%7CshopList%3AA%3A5%7Cmap%3AA%3A1; cityid=8; fspop=test; cy=219; cye=dongguan; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1627523423,1627873598,1627954039,1628041071; dper=989da530f9ae3713022e170efc199d428aac0573d693a4d093c1f2f39e7e7d20bb99cc4f07a07f24a5dc0266f4a458d5ef11e24a8ae6b5c0483dc0a951b9f38786fa0ed4cf339ad3264cd16995ed0afb4944d4cf1c9ff80f96f74f836faa3e50; ll=7fd06e815b796be3df069dec7836c3df; uamo=18523046785; dplet=05e0909fc0a55feb9e75176a40095f7b; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1628047001; _lxsdk_s=17b0f293742-7c3-ac9-6cc%7C%7C34',
        # 17830026366
        'fspop=test; cy=9; cye=chongqing; _lxsdk_cuid=17b0f262833c8-0e70a2955665cc8-4c3f2d73-1fa400-17b0f262834c8; _lxsdk_s=17b0f262834-620-570-96a%7C%7C42; _lxsdk=17b0f262833c8-0e70a2955665cc8-4c3f2d73-1fa400-17b0f262834c8; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1628046764; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1628047074; _hc.v=52a08788-2bb7-4a34-6a04-fbabe028f07c.1628046764; dplet=b47939460914f7200ce9a3d462fb4b63; dper=6d7a13cf88fead86c7818cb316eb317e2d153a9fc4f6f8c27a2588b400657e302df09975f12baa0495c47fe3c8bb5454e5a57955f3c08068d6e4b6251c90d6e4f71c245ce13ac0a68f75733cdc6d9e14de85f9bc850ecbd3410dfd8e512e4305; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_2931842226; ctu=93204e23fac6507842916042cfbe96b16a7fd43f465e198cbd19ef807e31ca8c; uamo=17830026366; s_ViewType=10',
        # 18580417558
        'fspop=test; cy=9; cye=chongqing; _lxsdk_cuid=17b0f272c2ac8-0ae9313f344207-4c3f2d73-1fa400-17b0f272c2ac8; _lxsdk_s=17b0f272c2a-ffd-940-db8%7C%7C40; _lxsdk=17b0f272c2ac8-0ae9313f344207-4c3f2d73-1fa400-17b0f272c2ac8; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1628046831; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1628047177; _hc.v=3294ae3a-d762-5407-b59f-f0ef9be10f26.1628046831; dplet=7ec7b53d4d77ca72757d79862e423eed; dper=3b9e16e23de913835827e6ac55971d9c87d98acc088d014df48e39db165340be5c6646a9c6af88d5b1e588b4f112f0a1d216d679b93337062aab0f369cff2a5609148eef6b8c0cc26df4525166e1e928e8cc47a1113cd436b79816d40434d55b; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_9409979560; ctu=c1b57e38ae728fc01ecee623966391b2220f22171063a8a6c3060be567823c56; uamo=18580417558; s_ViewType=10',
        # 13678479446
        'fspop=test; cy=9; cye=chongqing; _lxsdk_cuid=17b0f226fb64d-0e8c1dcd36c619-5e4d2f10-1fa400-17b0f226fb7c8; _lxsdk=17b0f226fb64d-0e8c1dcd36c619-5e4d2f10-1fa400-17b0f226fb7c8; _hc.v=cd257a2b-5211-0fcf-3551-1e9e0bfd3f34.1628046520; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1628046524; dplet=e83303f7b5960a74aaf6e01223ddc3bf; dper=cc697f7ae8e56752fd947b03d7658366470a6bcf04265124b1a69bfecaf440426e5f820030b75da014dba7a6b8b5f118a28ea666310ee61e473613ebd5415591e4edc11b55edd743297dd977992eccae34eca41244c9c0766c28944b25427880; ll=7fd06e815b796be3df069dec7836c3df; ua=Fy; ctu=e9c0ded0e8991a8ec5f801226c719cd680adb333f76f773520bbb53332a1a3fd; uamo=13678479446; s_ViewType=10; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1628047244; _lxsdk_s=17b0f226fb9-80d-478-c4c%7C%7C46',
        # 源哥
        'fspop=test; cy=9; cye=chongqing; _lxsdk_cuid=17b0f23d352c8-0b217dabfee66-5e4d2f10-1fa400-17b0f23d35245; _lxsdk=17b0f23d352c8-0b217dabfee66-5e4d2f10-1fa400-17b0f23d35245; _hc.v=8041ee21-b113-9c41-e435-a288f257e0cd.1628046612; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1628046612; dplet=a6319488c98785ac8c74f6acb5c6b495; dper=79651365e9aa2bad87079c033d89ea811b9884bb13a454d70911771325d35a62b67e28fcfd7b9ab59738e4fd89a1bb3b11f9300f74400c8ba1e532eff247ae098c1a0f9a3f8adee60ef7af3a96ef56bb2e63a4b18e604287e1e78294442e1d61; ll=7fd06e815b796be3df069dec7836c3df; ua=%E7%89%87%E7%89%87%E9%A2%9D; ctu=e6eac913442846979994e6dd366936deaf36c36d10add3771a12c4579d595e49; uamo=18983869992; s_ViewType=10; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1628047323; _lxsdk_s=17b0f23d355-4d6-2a9-76d%7C%7C43',
]
IpPool=[
        # "192.168.1.104:5010",
        # "192.168.1.130:5010",
        # "118.24.52.95:5010",
        "demo.spiderpy.cn",
        # "47.106.223.4:50002"
        ]
username = 'lum-customer-hl_dd804c17-zone-data_center-route_err-pass_dyn'
password = '1cysg9ek1vvk'
port = 22225
session_id = random.random()
super_proxy_url = ('http://%s-country-cn-session-%s:%s@zproxy.lum-superproxy.io:%d' %
    (username, session_id, password, port))

s = ['a', 'b', 'c', 'd', 'e', 'f', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
cuid1 = '179e'
for i in range(8):
        cuid1 += random.choice(s)
cuid2 = '0'
for i in range(13):
        cuid2 += random.choice(s)
cuid3 = 'f'
for i in range(6):
        cuid3 += random.choice(s)
cuid4 = '1fa400'
cuid5 = cuid1
cuid = cuid1 + '-' + cuid2 + '-' + cuid3 + '-' + cuid4 + '-' + cuid5
# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"
# 代理隧道验证信息
proxyUser = "H6F2SWR51B5L56HD"
proxyPass = "0984F7A27D0598EB"
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}
def get_proxy():
    try:
        return requests.get('http://1.116.204.248:5454/proxy2').text
    except:
        num = 3
        while num:
            try:
                return requests.get('http://1.116.204.248:5000/proxy').text
            except:
                print('暂无ip，等待20秒')
                time.sleep(20)
                num -= 1
        print('暂无ip')
def gethtml(url):
    headers = {
        'Connection': 'keep-alive',
        'Host': 'www.dianping.com',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48',
        # 'User-Agent':  UserAgent().chrome,
        # 'Cookie': 'fspop=test; cy=9; cye=chongqing; _lxsdk_cuid=179c01ab88cc8-0df2f0b9256ac1-2363163-1fa400-179c01ab88cc8; _lxsdk=179c01ab88cc8-0df2f0b9256ac1-2363163-1fa400-179c01ab88cc8; _hc.v=fb783b09-adc2-78df-f8a5-7b53f530416c.1622425648; s_ViewType=10; _dp.ac.v=19b24d59-781c-4e11-94fc-d848cfb75d8f; ctu=21fd3f032ee980c9b98bee37cc18e7671d5ddb8684865c57d85b840ce1fe7fff; aburl=1; cityid=9; default_ab=shopList%3AA%3A5; ua=dpuser_1966568564; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1622430936,1622599018,1622622578,1622684317; dper=989da530f9ae3713022e170efc199d424fbd595e54994bc85947fd9f29ed441d5ad1ab9e2e57880ec5c6d0064a0712390a38646ccaac0670ba2affafff2ddb2de5a6575b1004c83b5ae7f3395eba0ca6d9b132de2b248b53a54ceea5c6d51636; ll=7fd06e815b796be3df069dec7836c3df; uamo=18523046785; dplet=5f4edba1e07f6f53950ca9020d8c330d; _lxsdk_s=179cf85b559-dcb-2cd-df8%7C%7C262; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1622686321'
    }
    for i in range(100):
        proxies = {"http": get_proxy()}
        try:
            response = requests.get(url, headers=headers,proxies=proxies, timeout=10)
            encod = response.apparent_encoding
            if encod.upper() in ['GB2312', 'WINDOWS-1254']:
                encod = 'gbk'
            response.encoding = encod
            html = etree.HTML(response.text)
            if response.status_code ==200:
                return response
            print('获取页面失败',response.status_code, proxies)
        except Exception as e:
            print('get_html错误',proxies, e)
            time.sleep(2)
    return
def rans(num):
    s = ['a', 'b', 'c', 'd', 'e', 'f', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    x = ''
    for i in range(num):
        x += random.choice(s)
    return x
user_agent = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
              'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
              'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
              'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0',
              'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)']


def getmycookie():
    with open('cookie.txt','r') as f:
        token=f.read()
        return token
def getheaders():
        headers = {
                'Connection': 'keep-alive',
                'Host': 'www.dianping.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
                # 'Cookie':getmycookie()
                'Cookie':getrandomcookie()
                # 'Cookie': '_lxsdk_cuid=179c01ab88cc8-0df2f0b9256ac1-2363163-1fa400-179c01ab88cc8; _hc.v=fb783b09-adc2-78df-f8a5-7b53f530416c.1622425648; s_ViewType=10; _dp.ac.v=19b24d59-781c-4e11-94fc-d848cfb75d8f; ctu=21fd3f032ee980c9b98bee37cc18e7671d5ddb8684865c57d85b840ce1fe7fff; aburl=1; ua=dpuser_1966568564; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1622711914; uuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; iuuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _lxsdk=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _ga=GA1.2.1975686433.1622713531; cy=2; cye=beijing; switchcityflashtoast=1; default_ab=citylist%3AA%3A1%7Cshop%3AA%3A11%7Cindex%3AA%3A3%7CshopList%3AA%3A5%7Cmap%3AA%3A1; cityid=8; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1627270105,1627361338,1627523423,1627873598; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1627873598; _lxsdk_s=17b04d3d564-5b0-b53-de1%7C%7C21'
        }
        return headers
rancook=f'_lxsdk_cuid={cuid}; _lxsdk=179e9{rans(5)}91-06ce{rans(10)}-68151f7a-{rans(4)}00-179e{rans(7)}c8; _hc.v=f5{rans(4)}d5-{rans(4)}-07d4-fad0-7f7d{rans(5)}c25.{str(int(time.time()))}; Hm_lvt_602b80{rans(8)}659{rans(10)}940e7={str(int(time.time()))}; Hm_lpvt_602b{rans(8)}ae65{rans(10)}3940e7={str(int(time.time()))}; _lxsdk_s=179ea{rans(6)}-7a0-{rans(3)}-68c%7C%7C3'
def getrandomcookie():
        return f'_lxsdk_cuid={cuid}; _lxsdk=179e9{rans(5)}91-06ce{rans(10)}-68151f7a-{rans(4)}00-179e{rans(7)}c8; _hc.v=f5{rans(4)}d5-{rans(4)}-07d4-fad0-7f7d{rans(5)}c25.{str(int(time.time()))}; Hm_lvt_602b80{rans(8)}659{rans(10)}940e7={str(int(time.time()))}; Hm_lpvt_602b{rans(8)}ae65{rans(10)}3940e7={str(int(time.time()))}; _lxsdk_s=179ea{rans(6)}-7a0-{rans(3)}-68c%7C%7C3'
typedict={
    # '不限':'ch0',
    '美食':'ch10',                            #抓取
    # '电影演出赛事':'ch25',
    '休闲娱乐':'ch30',                         #抓取
    # '酒店':'hotel',
    '丽人':'ch50',
    'K歌':'ch15',                        #抓取
    '运动健身':'ch45',                        #抓取
    '景点/周边游':'ch35',
    # '亲子':'ch70',
    # '结婚':'ch55',
    '购物':'ch20',
    '宠物':'ch95',
    '生活服务':'ch80',                    #抓取
    '学习培训':'ch75',
    '养车/用车':'ch65',
    '医疗健康':'ch85',
    # '家居':'ch90',
    '民宿公寓':'ch33954',
    '交通设施':'ch34259',
}

headers = {
    'Connection': 'keep-alive',
    'Host': 'www.dianping.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Cookie':'_lxsdk_cuid=179c01ab88cc8-0df2f0b9256ac1-2363163-1fa400-179c01ab88cc8; _hc.v=fb783b09-adc2-78df-f8a5-7b53f530416c.1622425648; s_ViewType=10; _dp.ac.v=19b24d59-781c-4e11-94fc-d848cfb75d8f; ctu=21fd3f032ee980c9b98bee37cc18e7671d5ddb8684865c57d85b840ce1fe7fff; aburl=1; ua=dpuser_1966568564; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1622711914; uuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; iuuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _lxsdk=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _ga=GA1.2.1975686433.1622713531; cy=2; cye=beijing; switchcityflashtoast=1; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1625017013,1625219146,1625563435,1626835526; m_flash2=1; msource=default; source=m_browser_test_33; default_ab=citylist%3AA%3A1%7Cshop%3AA%3A11%7Cindex%3AA%3A3%7CshopList%3AA%3A5%7Cmap%3AA%3A1; pvhistory="6L+U5ZuePjo8L3N1Z2dlc3QvZ2V0SnNvbkRhdGE/Y2FsbGJhY2s9anNvbnBfMTYyNjg1NjU1MDk2N182NjE4Nz46PDE2MjY4NTY1NTA2NzldX1s="; fspop=test; chwlsource=default; cityid=8; noswitchcity=1; dper=989da530f9ae3713022e170efc199d42528fb04c1c5a2309d4a2efbe93b5573321d0512323e5ee6e288ef174bb8fefa9a79b638cf0a581e4a6f5268d58a5df475544201dd8c9b39987044f0a5ed0f1806aa4a26eba5cc4d211a463b749fcbfcf; ll=7fd06e815b796be3df069dec7836c3df; uamo=18523046785; dplet=bb1d80303c66ad8a223d1f04b042ebcd; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1626861401; _lxsdk_s=17ac814fffa-6fb-ea-bb9%7C0%7C1453'
    # 'Cookie': 'navCtgScroll=0; showNav=#nav-tab|0|0; _lxsdk_cuid=179c01ab88cc8-0df2f0b9256ac1-2363163-1fa400-179c01ab88cc8; _hc.v=fb783b09-adc2-78df-f8a5-7b53f530416c.1622425648; s_ViewType=10; _dp.ac.v=19b24d59-781c-4e11-94fc-d848cfb75d8f; ctu=21fd3f032ee980c9b98bee37cc18e7671d5ddb8684865c57d85b840ce1fe7fff; aburl=1; cityid=9; ua=dpuser_1966568564; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1622711914; uuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; iuuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _lxsdk=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _ga=GA1.2.1975686433.1622713531; default_ab=shop%3AA%3A11%7CshopList%3AA%3A5; fspop=test; cy=9; cye=chongqing; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1623201705,1623290813,1623377084,1623377928; dper=989da530f9ae3713022e170efc199d424b84b5589c1a94003f90d1dd64755f3594748ec3cb2c902af80c0cf9cde295f7a8ff7498ed1d26bac4d7ab27d0882184cecdddff1eecc97a58a16aac2963cdfca7dfedd2e3854141c0403900fc167b94; ll=7fd06e815b796be3df069dec7836c3df; uamo=18523046785; dplet=a1a259ec33df12d03dfd76a0c8569921; _lxsdk_s=179f98f6fbb-bf3-30d-629%7C%7C350; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1623394363'
    # 'Cookie': f'navCtgScroll=0; showNav=#nav-tab|0|0; _lxsdk_cuid=179c01{rans(7)}-0df2{rans(6)}6ac1-2363163-1fa400-179c01ab88cc8; _hc.v=fb783b09-adc2-78df-f8a5-7b53f530416c.1622425648; s_ViewType=10; _dp.ac.v=19b24d59-781c-4e11-94fc-d848cfb75d8f; ctu=21fd3f032ee9{rans(20)}1d5ddb8684865c57d85b840ce1fe7fff; aburl=1; cityid=2; ua=dpuser_1966568564; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1622711914; uuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; iuuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _lxsdk=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _ga=GA1.2.1975686433.1622713531; default_ab=shop%3AA%3A11%7CshopList%3AA%3A5; fspop=test; cy=2; cye=chongqing; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf{rans(16)}0a3940e7=1623201705,1623290813,1623377084,1623377928; dper=989da530f9ae3713022e170efc199d424b84b5589c1a94003f90d1dd64755f3594748ec3cb{rans(40)}d7ab27d0882184cecdddff1eecc97a58a16aac2963cdfca7dfedd2e3854141c0403900fc167b94; ll=7fd06e815b796be3df069dec7836c3df; uamo=18523046785; dplet=a1a259{rans(16)}a0c8569921; _lxsdk_s=179f98f6fbb-bf3-30d-629%7C%7C350; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7={str(int(time.time()))}'
}

def mycookie():
        with open('cookie.json','r') as f:
            lists=f.readlines()
        return random.choice(lists)




def cookie_header():
        headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept - Encoding': 'gzip, deflate',
                'Accept - Language': 'zh - CN, zh;q = 0.9',
                'Connection': 'keep-alive',
                'Host': 'www.dianping.com',
                'Upgrade - Insecure - Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                # 'Cookie': random.choice(CookieList)
        }
        return headers
fheaders = {
    'Connection': 'keep-alive',
    'Host': 's3plus.meituan.net',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',

}


citylist=[
        {'cityId': 2, 'cityName': '北京', 'cityPyName': 'beijing'},
        {'cityId': 10, 'cityName': '天津', 'cityPyName': 'tianjin'},
        {'cityId': 29, 'cityName': '保定', 'cityPyName': 'baoding'},
        {'cityId': 32, 'cityName': '沧州', 'cityPyName': 'cangzhou'},
        {'cityId': 31, 'cityName': '承德', 'cityPyName': 'chengde'},
        {'cityId': 27, 'cityName': '邯郸', 'cityPyName': 'handan'},
        {'cityId': 34, 'cityName': '衡水', 'cityPyName': 'hengshui'},
        {'cityId': 33, 'cityName': '廊坊', 'cityPyName': 'langfang'},
        {'cityId': 26, 'cityName': '秦皇岛', 'cityPyName': 'qinhuangdao'},
        {'cityId': 24, 'cityName': '石家庄', 'cityPyName': 'shijiazhuang'},
        {'cityId': 25, 'cityName': '唐山', 'cityPyName': 'tangshan'},
        {'cityId': 28, 'cityName': '邢台', 'cityPyName': 'xingtai'},
        {'cityId': 30, 'cityName': '张家口', 'cityPyName': 'zhangjiakou'},
        {'cityId': 38, 'cityName': '长治', 'cityPyName': 'changzhi'} ,
        {'cityId': 36, 'cityName': '大同', 'cityPyName': 'datong'} ,
        {'cityId': 39, 'cityName': '晋城', 'cityPyName': 'jincheng'} ,
        {'cityId': 41, 'cityName': '晋中', 'cityPyName': 'jinzhong'} ,
        {'cityId': 44, 'cityName': '临汾', 'cityPyName': 'linfen'} ,
        {'cityId': 45, 'cityName': '吕梁', 'cityPyName': 'lvliang'} ,
        {'cityId': 40, 'cityName': '朔州', 'cityPyName': 'shuozhou'} ,
        {'cityId': 35, 'cityName': '太原', 'cityPyName': 'taiyuan'} ,
        {'cityId': 43, 'cityName': '忻州', 'cityPyName': 'xinzhou'} ,
        {'cityId': 37, 'cityName': '阳泉', 'cityPyName': 'yangquan'} ,
        {'cityId': 42, 'cityName': '运城', 'cityPyName': 'yuncheng'} ,              ########包含运城之前只有p1
        {'cityId': 57, 'cityName': '阿拉善', 'cityPyName': 'alashan'} ,
        {'cityId': 56, 'cityName': '巴彦淖尔', 'cityPyName': 'bayannaoer'} ,
        {'cityId': 47, 'cityName': '包头', 'cityPyName': 'baotou'} ,
        {'cityId': 49, 'cityName': '赤峰', 'cityPyName': 'chifeng'} ,
        {'cityId': 51, 'cityName': '鄂尔多斯', 'cityPyName': 'eerduosi'} ,
        {'cityId': 46, 'cityName': '呼和浩特', 'cityPyName': 'huhehaote'} ,
        {'cityId': 52, 'cityName': '呼伦贝尔', 'cityPyName': 'hulunbeier'} ,
        {'cityId': 50, 'cityName': '通辽', 'cityPyName': 'tongliao'} ,
        {'cityId': 48, 'cityName': '乌海', 'cityPyName': 'wuhai'} ,
        {'cityId': 55, 'cityName': '乌兰察布', 'cityPyName': 'wulanchabu'} ,
        {'cityId': 54, 'cityName': '锡林郭勒', 'cityPyName': 'xilinguole'} ,
        {'cityId': 53, 'cityName': '兴安盟', 'cityPyName': 'xingan'} ,
        {'cityId': 58, 'cityName': '鞍山', 'cityPyName': 'anshan'} ,
        {'cityId': 60, 'cityName': '本溪', 'cityPyName': 'benxi'} ,
        {'cityId': 68, 'cityName': '朝阳', 'cityPyName': 'chaoyang'} ,
        {'cityId': 19, 'cityName': '大连', 'cityPyName': 'dalian'} ,
        {'cityId': 61, 'cityName': '丹东', 'cityPyName': 'dandong'} ,
        {'cityId': 59, 'cityName': '抚顺', 'cityPyName': 'fushun'} ,
        {'cityId': 64, 'cityName': '阜新', 'cityPyName': 'fuxin'} ,
        {'cityId': 69, 'cityName': '葫芦岛', 'cityPyName': 'huludao'} ,
        {'cityId': 62, 'cityName': '锦州', 'cityPyName': 'jinzhou'} ,
        {'cityId': 65, 'cityName': '辽阳', 'cityPyName': 'liaoyang'} ,
        {'cityId': 66, 'cityName': '盘锦', 'cityPyName': 'panjin'} ,
        {'cityId': 18, 'cityName': '沈阳', 'cityPyName': 'shenyang'} ,
        {'cityId': 67, 'cityName': '铁岭', 'cityPyName': 'tieling'} ,
        {'cityId': 63, 'cityName': '营口', 'cityPyName': 'yingkou'} ,
        {'cityId': 77, 'cityName': '白城', 'cityPyName': 'baicheng'} ,
        {'cityId': 75, 'cityName': '白山', 'cityPyName': 'baishan'} ,
        {'cityId': 70, 'cityName': '长春', 'cityPyName': 'changchun'} ,
        {'cityId': 71, 'cityName': '吉林', 'cityPyName': 'jilin'} ,
        {'cityId': 73, 'cityName': '辽源', 'cityPyName': 'liaoyuan'} ,
        {'cityId': 72, 'cityName': '四平', 'cityPyName': 'siping'} ,
        {'cityId': 76, 'cityName': '松原', 'cityPyName': 'songyuan'} ,
        {'cityId': 74, 'cityName': '通化', 'cityPyName': 'tonghua'} ,
        {'cityId': 78, 'cityName': '延边', 'cityPyName': 'yanbian'} ,
        {'cityId': 84, 'cityName': '大庆', 'cityPyName': 'daqing'} ,
        {'cityId': 91, 'cityName': '大兴安岭', 'cityPyName': 'daxinganling'} ,
        {'cityId': 79, 'cityName': '哈尔滨', 'cityPyName': 'haerbin'} ,
        {'cityId': 82, 'cityName': '鹤岗', 'cityPyName': 'hegang'} ,
        {'cityId': 89, 'cityName': '黑河', 'cityPyName': 'heihe'} ,
        {'cityId': 81, 'cityName': '鸡西', 'cityPyName': 'jixi'} ,
        {'cityId': 86, 'cityName': '佳木斯', 'cityPyName': 'jiamusi'} ,
        {'cityId': 88, 'cityName': '牡丹江', 'cityPyName': 'mudanjiang'} ,
        {'cityId': 87, 'cityName': '七台河', 'cityPyName': 'qitaihe'} ,
        {'cityId': 80, 'cityName': '齐齐哈尔', 'cityPyName': 'qiqihaer'} ,
        {'cityId': 83, 'cityName': '双鸭山', 'cityPyName': 'shuangyashan'} ,
        {'cityId': 90, 'cityName': '绥化', 'cityPyName': 'suihua'} ,
        {'cityId': 85, 'cityName': '伊春', 'cityPyName': 'yichun'} ,
        {'cityId': 1, 'cityName': '上海', 'cityPyName': 'shanghai'} ,
        {'cityId': 93, 'cityName': '常州', 'cityPyName': 'changzhou'} ,
        {'cityId': 96, 'cityName': '淮安', 'cityPyName': 'huaian'} ,
        {'cityId': 95, 'cityName': '连云港', 'cityPyName': 'lianyungang'} ,
        {'cityId': 5, 'cityName': '南京', 'cityPyName': 'nanjing'} ,
        {'cityId': 94, 'cityName': '南通', 'cityPyName': 'nantong'} ,
        {'cityId': 6, 'cityName': '苏州', 'cityPyName': 'suzhou'} ,
        {'cityId': 100, 'cityName': '宿迁', 'cityPyName': 'suqian'} ,
        {'cityId': 99, 'cityName': '泰州', 'cityPyName': 'taizhou'} ,
        {'cityId': 13, 'cityName': '无锡', 'cityPyName': 'wuxi'} ,
        {'cityId': 92, 'cityName': '徐州', 'cityPyName': 'xuzhou'} ,
        {'cityId': 97, 'cityName': '盐城', 'cityPyName': 'yancheng'} ,
        {'cityId': 12, 'cityName': '扬州', 'cityPyName': 'yangzhou'} ,
        {'cityId': 98, 'cityName': '镇江', 'cityPyName': 'zhenjiang'} ,
        {'cityId': 3, 'cityName': '杭州', 'cityPyName': 'hangzhou'} ,
        {'cityId': 103, 'cityName': '湖州', 'cityPyName': 'huzhou'} ,
        {'cityId': 102, 'cityName': '嘉兴', 'cityPyName': 'jiaxing'} ,
        {'cityId': 105, 'cityName': '金华', 'cityPyName': 'jinhua'} ,
        {'cityId': 109, 'cityName': '丽水', 'cityPyName': 'lishui'} ,
        {'cityId': 11, 'cityName': '宁波', 'cityPyName': 'ningbo'} ,
        {'cityId': 106, 'cityName': '衢州', 'cityPyName': 'quzhou'} ,
        {'cityId': 104, 'cityName': '绍兴', 'cityPyName': 'shaoxing'} ,
        {'cityId': 108, 'cityName': '台州', 'cityPyName': 'taizhou'} ,
        {'cityId': 101, 'cityName': '温州', 'cityPyName': 'wenzhou'} ,
        {'cityId': 107, 'cityName': '舟山', 'cityPyName': 'zhoushan'} ,
        {'cityId': 117, 'cityName': '安庆', 'cityPyName': 'anqing'} ,
        {'cityId': 112, 'cityName': '蚌埠', 'cityPyName': 'bengbu'} ,
        {'cityId': 124, 'cityName': '亳州', 'cityPyName': 'bozhou'} ,
        {'cityId': 125, 'cityName': '池州', 'cityPyName': 'chizhou'} ,
        {'cityId': 119, 'cityName': '滁州', 'cityPyName': 'chuzhou'} ,
        {'cityId': 120, 'cityName': '阜阳', 'cityPyName': 'fuyang'} ,
        {'cityId': 110, 'cityName': '合肥', 'cityPyName': 'hefei'} ,
        {'cityId': 115, 'cityName': '淮北', 'cityPyName': 'huaibei'} ,
        {'cityId': 113, 'cityName': '淮南', 'cityPyName': 'huainan'} ,
        {'cityId': 118, 'cityName': '黄山', 'cityPyName': 'huangshan'} ,
        {'cityId': 123, 'cityName': '六安', 'cityPyName': 'liuan'} ,
        {'cityId': 114, 'cityName': '马鞍山', 'cityPyName': 'maanshan'} ,
        {'cityId': 121, 'cityName': '宿州', 'cityPyName': 'suzhou'} ,
        {'cityId': 116, 'cityName': '铜陵', 'cityPyName': 'tongling'} ,
        {'cityId': 111, 'cityName': '芜湖', 'cityPyName': 'wuhu'} ,
        {'cityId': 126, 'cityName': '宣城', 'cityPyName': 'xuancheng'} ,
        {'cityId': 14, 'cityName': '福州', 'cityPyName': 'fuzhou'} ,
        {'cityId': 132, 'cityName': '龙岩', 'cityPyName': 'longyan'} ,
        {'cityId': 131, 'cityName': '南平', 'cityPyName': 'nanping'} ,
        {'cityId': 133, 'cityName': '宁德', 'cityPyName': 'ningde'} ,
        {'cityId': 127, 'cityName': '莆田', 'cityPyName': 'putian'} ,
        {'cityId': 129, 'cityName': '泉州', 'cityPyName': 'quanzhou'} ,
        {'cityId': 128, 'cityName': '三明', 'cityPyName': 'sanming'} ,
        {'cityId': 15, 'cityName': '厦门', 'cityPyName': 'xiamen'} ,
        {'cityId': 130, 'cityName': '漳州', 'cityPyName': 'zhangzhou'} ,
        {'cityId': 143, 'cityName': '抚州', 'cityPyName': 'fuzhou'} ,
        {'cityId': 140, 'cityName': '赣州', 'cityPyName': 'ganzhou'} ,
        {'cityId': 141, 'cityName': '吉安', 'cityPyName': 'jian'} ,
        {'cityId': 135, 'cityName': '景德镇', 'cityPyName': 'jingdezhen'} ,
        {'cityId': 137, 'cityName': '九江', 'cityPyName': 'jiujiang'} ,
        {'cityId': 134, 'cityName': '南昌', 'cityPyName': 'nanchang'} ,
        {'cityId': 136, 'cityName': '萍乡', 'cityPyName': 'pingxiang'} ,
        {'cityId': 144, 'cityName': '上饶', 'cityPyName': 'shangrao'} ,
        {'cityId': 138, 'cityName': '新余', 'cityPyName': 'xinyu'} ,
        {'cityId': 142, 'cityName': '宜春', 'cityPyName': 'yichun'} ,
        {'cityId': 139, 'cityName': '鹰潭', 'cityPyName': 'yingtan'} ,
        {'cityId': 158, 'cityName': '滨州', 'cityPyName': 'binzhou'} ,
        {'cityId': 156, 'cityName': '德州', 'cityPyName': 'dezhou'} ,
        {'cityId': 147, 'cityName': '东营', 'cityPyName': 'dongying'} ,
        {'cityId': 159, 'cityName': '菏泽', 'cityPyName': 'heze'} ,
        {'cityId': 22, 'cityName': '济南', 'cityPyName': 'jinan'} ,
        {'cityId': 150, 'cityName': '济宁', 'cityPyName': 'jining'} ,
        {'cityId': 157, 'cityName': '聊城', 'cityPyName': 'liaocheng'} ,
        {'cityId': 155, 'cityName': '临沂', 'cityPyName': 'linyi'} ,
        {'cityId': 21, 'cityName': '青岛', 'cityPyName': 'qingdao'} ,
        {'cityId': 153, 'cityName': '日照', 'cityPyName': 'rizhao'} ,
        {'cityId': 151, 'cityName': '泰安', 'cityPyName': 'taian'} ,
        {'cityId': 152, 'cityName': '威海', 'cityPyName': 'weihai'} ,
        {'cityId': 149, 'cityName': '潍坊', 'cityPyName': 'weifang'} ,
        {'cityId': 148, 'cityName': '烟台', 'cityPyName': 'yantai'} ,
        {'cityId': 146, 'cityName': '枣庄', 'cityPyName': 'zaozhuang'} ,
        {'cityId': 145, 'cityName': '淄博', 'cityPyName': 'zibo'} ,
        {'cityId': 164, 'cityName': '安阳', 'cityPyName': 'anyang'} ,
        {'cityId': 165, 'cityName': '鹤壁', 'cityPyName': 'hebi'} ,
        {'cityId': 397, 'cityName': '济源', 'cityPyName': 'jiyuan'} ,
        {'cityId': 167, 'cityName': '焦作', 'cityPyName': 'jiaozuo'} ,
        {'cityId': 161, 'cityName': '开封', 'cityPyName': 'kaifeng'} ,
        {'cityId': 162, 'cityName': '洛阳', 'cityPyName': 'luoyang'} ,
        {'cityId': 170, 'cityName': '漯河', 'cityPyName': 'luohe'} ,
        {'cityId': 172, 'cityName': '南阳', 'cityPyName': 'nanyang'} ,
        {'cityId': 163, 'cityName': '平顶山', 'cityPyName': 'pingdingshan'} ,
        {'cityId': 168, 'cityName': '濮阳', 'cityPyName': 'puyang'} ,
        {'cityId': 171, 'cityName': '三门峡', 'cityPyName': 'sanmenxia'} ,
        {'cityId': 173, 'cityName': '商丘', 'cityPyName': 'shangqiu'} ,
        {'cityId': 166, 'cityName': '新乡', 'cityPyName': 'xinxiang'} ,
        {'cityId': 174, 'cityName': '信阳', 'cityPyName': 'xinyang'} ,
        {'cityId': 169, 'cityName': '许昌', 'cityPyName': 'xuchang'} ,
        {'cityId': 160, 'cityName': '郑州', 'cityPyName': 'zhengzhou'} ,
        {'cityId': 175, 'cityName': '周口', 'cityPyName': 'zhoukou'} ,
        {'cityId': 176, 'cityName': '驻马店', 'cityPyName': 'zhumadian'} ,
        {'cityId': 181, 'cityName': '鄂州', 'cityPyName': 'ezhou'} ,
        {'cityId': 188, 'cityName': '恩施', 'cityPyName': 'enshi'} ,
        {'cityId': 185, 'cityName': '黄冈', 'cityPyName': 'huanggang'} ,
        {'cityId': 177, 'cityName': '黄石', 'cityPyName': 'huangshi'} ,
        {'cityId': 182, 'cityName': '荆门', 'cityPyName': 'jinmen'} ,
        {'cityId': 184, 'cityName': '荆州', 'cityPyName': 'jingzhou'} ,
        {'cityId': 190, 'cityName': '潜江', 'cityPyName': 'qianjiang'} ,
        {'cityId': 404, 'cityName': '神农架林区', 'cityPyName': 'shennongjia'} ,
        {'cityId': 178, 'cityName': '十堰', 'cityPyName': 'shiyan'} ,
        {'cityId': 187, 'cityName': '随州', 'cityPyName': 'suizhou'} ,
        {'cityId': 191, 'cityName': '天门', 'cityPyName': 'tianmen'} ,
        {'cityId': 16, 'cityName': '武汉', 'cityPyName': 'wuhan'} ,
        {'cityId': 189, 'cityName': '仙桃', 'cityPyName': 'xiantao'} ,
        {'cityId': 186, 'cityName': '咸宁', 'cityPyName': 'xianning'} ,
        {'cityId': 180, 'cityName': '襄阳', 'cityPyName': 'xiangyang'} ,
        {'cityId': 183, 'cityName': '孝感', 'cityPyName': 'xiaogan'} ,
        {'cityId': 179, 'cityName': '宜昌', 'cityPyName': 'yichang'} ,
        {'cityId': 344, 'cityName': '长沙', 'cityPyName': 'changsha'} ,
        {'cityId': 197, 'cityName': '常德', 'cityPyName': 'changde'} ,
        {'cityId': 200, 'cityName': '郴州', 'cityPyName': 'chenzhou'} ,
        {'cityId': 194, 'cityName': '衡阳', 'cityPyName': 'hengyang'} ,
        {'cityId': 202, 'cityName': '怀化', 'cityPyName': 'huaihua'} ,
        {'cityId': 203, 'cityName': '娄底', 'cityPyName': 'loudi'} ,
        {'cityId': 195, 'cityName': '邵阳', 'cityPyName': 'shaoyang'} ,
        {'cityId': 193, 'cityName': '湘潭', 'cityPyName': 'xiangtan'} ,
        {'cityId': 204, 'cityName': '湘西', 'cityPyName': 'xiangxi'} ,
        {'cityId': 199, 'cityName': '益阳', 'cityPyName': 'yiyang'} ,
        {'cityId': 201, 'cityName': '永州', 'cityPyName': 'yongzhou'} ,
        {'cityId': 196, 'cityName': '岳阳', 'cityPyName': 'yueyang'} ,
        {'cityId': 198, 'cityName': '张家界', 'cityPyName': 'zhangjiajie'} ,
        {'cityId': 192, 'cityName': '株洲', 'cityPyName': 'zhuzhou'} ,
        {'cityId': 221, 'cityName': '潮州', 'cityPyName': 'chaozhou'} ,
        {'cityId': 219, 'cityName': '东莞', 'cityPyName': 'dongguan'} ,
        {'cityId': 208, 'cityName': '佛山', 'cityPyName': 'foshan'} ,
        {'cityId': 4, 'cityName': '广州', 'cityPyName': 'guangzhou'} ,
        {'cityId': 216, 'cityName': '河源', 'cityPyName': 'heyuan'} ,
        {'cityId': 213, 'cityName': '惠州', 'cityPyName': 'huizhou'} ,
        {'cityId': 209, 'cityName': '江门', 'cityPyName': 'jiangmen'} ,
        {'cityId': 222, 'cityName': '揭阳', 'cityPyName': 'jieyang'} ,
        {'cityId': 211, 'cityName': '茂名', 'cityPyName': 'maoming'} ,
        {'cityId': 214, 'cityName': '梅州', 'cityPyName': 'meizhou'} ,
        {'cityId': 218, 'cityName': '清远', 'cityPyName': 'qingyuan'} ,
        {'cityId': 207, 'cityName': '汕头', 'cityPyName': 'shantou'} ,
        {'cityId': 215, 'cityName': '汕尾', 'cityPyName': 'shanwei'} ,
        {'cityId': 205, 'cityName': '韶关', 'cityPyName': 'shaoguan'} ,
        {'cityId': 7, 'cityName': '深圳', 'cityPyName': 'shenzhen'} ,
        {'cityId': 217, 'cityName': '阳江', 'cityPyName': 'yangjiang'} ,
        {'cityId': 223, 'cityName': '云浮', 'cityPyName': 'yunfu'} ,
        {'cityId': 210, 'cityName': '湛江', 'cityPyName': 'zhanjiang'} ,
        {'cityId': 212, 'cityName': '肇庆', 'cityPyName': 'zhaoqing'} ,
        {'cityId': 220, 'cityName': '中山', 'cityPyName': 'zhongshan'} ,
        {'cityId': 206, 'cityName': '珠海', 'cityPyName': 'zhuhai'} ,
        {'cityId': 233, 'cityName': '百色', 'cityPyName': 'baise'} ,
        {'cityId': 228, 'cityName': '北海', 'cityPyName': 'beihai'} ,
        {'cityId': 394, 'cityName': '崇左', 'cityPyName': 'chongzuo'} ,
        {'cityId': 229, 'cityName': '防城港', 'cityPyName': 'fangchenggang'} ,
        {'cityId': 231, 'cityName': '贵港', 'cityPyName': 'guigang'} ,
        {'cityId': 226, 'cityName': '桂林', 'cityPyName': 'guilin'} ,
        {'cityId': 235, 'cityName': '河池', 'cityPyName': 'hechi'} ,
        {'cityId': 234, 'cityName': '贺州', 'cityPyName': 'hezhou'} ,
        {'cityId': 398, 'cityName': '来宾', 'cityPyName': 'laibin'} ,
        {'cityId': 225, 'cityName': '柳州', 'cityPyName': 'liuzhou'} ,
        {'cityId': 224, 'cityName': '南宁', 'cityPyName': 'nanning'} ,
        {'cityId': 230, 'cityName': '钦州', 'cityPyName': 'qinzhou'} ,
        {'cityId': 227, 'cityName': '梧州', 'cityPyName': 'wuzhou'} ,
        {'cityId': 232, 'cityName': '玉林', 'cityPyName': 'yulin'} ,
        {'cityId': 390, 'cityName': '白沙', 'cityPyName': 'baisha'} ,
        {'cityId': 391, 'cityName': '保亭', 'cityPyName': 'baoting'} ,
        {'cityId': 392, 'cityName': '昌江', 'cityPyName': 'changjiang'} ,
        {'cityId': 393, 'cityName': '澄迈县', 'cityPyName': 'chengmai'} ,
        {'cityId': 358, 'cityName': '儋州', 'cityPyName': 'danzhou'} ,
        {'cityId': 395, 'cityName': '定安县', 'cityPyName': 'dingan'} ,
        {'cityId': 396, 'cityName': '东方', 'cityPyName': 'dongfang'} ,
        {'cityId': 23, 'cityName': '海口', 'cityPyName': 'haikou'} ,
        {'cityId': 399, 'cityName': '乐东', 'cityPyName': 'ledong'} ,
        {'cityId': 400, 'cityName': '临高县', 'cityPyName': 'lingao'} ,
        {'cityId': 401, 'cityName': '陵水', 'cityPyName': 'lingshui'} ,
        {'cityId': 402, 'cityName': '琼海', 'cityPyName': 'qionghai'} ,
        {'cityId': 403, 'cityName': '琼中', 'cityPyName': 'qiongzhong'} ,
        {'cityId': 2310, 'cityName': '三沙', 'cityPyName': 'sansha'} ,
        {'cityId': 345, 'cityName': '三亚', 'cityPyName': 'sanya'} ,
        {'cityId': 406, 'cityName': '屯昌县', 'cityPyName': 'tunchang'} ,
        {'cityId': 407, 'cityName': '万宁', 'cityPyName': 'wanning'} ,
        {'cityId': 408, 'cityName': '文昌', 'cityPyName': 'wenchang'} ,
        {'cityId': 410, 'cityName': '五指山', 'cityPyName': 'wuzhishan'} ,
        {'cityId': 9, 'cityName': '重庆', 'cityPyName': 'chongqing'} ,
        {'cityId': 255, 'cityName': '阿坝', 'cityPyName': 'aba'} ,
        {'cityId': 253, 'cityName': '巴中', 'cityPyName': 'bazhong'} ,
        {'cityId': 8, 'cityName': '成都', 'cityPyName': 'chengdu'} ,
        {'cityId': 251, 'cityName': '达州', 'cityPyName': 'dazhou'} ,
        {'cityId': 241, 'cityName': '德阳', 'cityPyName': 'deyang'} ,
        {'cityId': 256, 'cityName': '甘孜州', 'cityPyName': 'ganzi'} ,
        {'cityId': 250, 'cityName': '广安', 'cityPyName': 'guangan'} ,
        {'cityId': 243, 'cityName': '广元', 'cityPyName': 'guangyuan'} ,
        {'cityId': 246, 'cityName': '乐山', 'cityPyName': 'leshan'} ,
        {'cityId': 257, 'cityName': '凉山', 'cityPyName': 'liangshan'} ,
        {'cityId': 240, 'cityName': '泸州', 'cityPyName': 'luzhou'} ,
        {'cityId': 248, 'cityName': '眉山', 'cityPyName': 'meishan'} ,
        {'cityId': 242, 'cityName': '绵阳', 'cityPyName': 'mianyang'} ,
        {'cityId': 245, 'cityName': '内江', 'cityPyName': 'neijiang'} ,
        {'cityId': 247, 'cityName': '南充', 'cityPyName': 'nanchong'} ,
        {'cityId': 239, 'cityName': '攀枝花', 'cityPyName': 'panzhihua'} ,
        {'cityId': 244, 'cityName': '遂宁', 'cityPyName': 'suining'} ,
        {'cityId': 252, 'cityName': '雅安', 'cityPyName': 'yaan'} ,
        {'cityId': 249, 'cityName': '宜宾', 'cityPyName': 'yibin'} ,
        {'cityId': 254, 'cityName': '资阳', 'cityPyName': 'ziyang'} ,
        {'cityId': 238, 'cityName': '自贡', 'cityPyName': 'zigong'} ,
        {'cityId': 261, 'cityName': '安顺', 'cityPyName': 'anshun'} ,
        {'cityId': 264, 'cityName': '毕节市', 'cityPyName': 'bijieshi'} ,
        {'cityId': 258, 'cityName': '贵阳', 'cityPyName': 'guiyang'} ,
        {'cityId': 259, 'cityName': '六盘水', 'cityPyName': 'liupanshui'} ,
        {'cityId': 265, 'cityName': '黔东南', 'cityPyName': 'qiandongnan'} ,
        {'cityId': 266, 'cityName': '黔南', 'cityPyName': 'qiannan'} ,
        {'cityId': 263, 'cityName': '黔西南', 'cityPyName': 'qianxinan'} ,
        {'cityId': 262, 'cityName': '铜仁', 'cityPyName': 'tongren'} ,
        {'cityId': 260, 'cityName': '遵义', 'cityPyName': 'zunyi'} ,
        {'cityId': 270, 'cityName': '保山', 'cityPyName': 'baoshan'} ,
        {'cityId': 272, 'cityName': '楚雄州', 'cityPyName': 'chuxiongzhou'} ,
        {'cityId': 277, 'cityName': '大理州', 'cityPyName': 'dali'} ,
        {'cityId': 278, 'cityName': '德宏', 'cityPyName': 'dehong'} ,
        {'cityId': 281, 'cityName': '迪庆', 'cityPyName': 'diqing'} ,
        {'cityId': 273, 'cityName': '红河', 'cityPyName': 'honghe'} ,
        {'cityId': 267, 'cityName': '昆明', 'cityPyName': 'kunming'} ,
        {'cityId': 279, 'cityName': '丽江', 'cityPyName': 'lijiang'} ,
        {'cityId': 282, 'cityName': '临沧', 'cityPyName': 'linchang'} ,
        {'cityId': 280, 'cityName': '怒江', 'cityPyName': 'nujiang'} ,
        {'cityId': 275, 'cityName': '普洱', 'cityPyName': 'puer'} ,
        {'cityId': 268, 'cityName': '曲靖', 'cityPyName': 'qujing'} ,
        {'cityId': 274, 'cityName': '文山州', 'cityPyName': 'wenshan'} ,
        {'cityId': 276, 'cityName': '西双版纳', 'cityPyName': 'xishuangbanna'} ,
        {'cityId': 269, 'cityName': '玉溪', 'cityPyName': 'yuxi'} ,
        {'cityId': 271, 'cityName': '昭通', 'cityPyName': 'zhaotong'} ,
        {'cityId': 288, 'cityName': '阿里', 'cityPyName': 'ali'} ,
        {'cityId': 284, 'cityName': '昌都市', 'cityPyName': 'changdudiqu'} ,
        {'cityId': 283, 'cityName': '拉萨', 'cityPyName': 'lasa'} ,
        {'cityId': 289, 'cityName': '林芝市', 'cityPyName': 'linzhi'} ,
        {'cityId': 287, 'cityName': '那曲', 'cityPyName': 'naqu'} ,
        {'cityId': 286, 'cityName': '日喀则', 'cityPyName': 'rikaze'} ,
        {'cityId': 285, 'cityName': '山南', 'cityPyName': 'shannan'} ,
        {'cityId': 297, 'cityName': '安康', 'cityPyName': 'ankang'} ,
        {'cityId': 291, 'cityName': '宝鸡', 'cityPyName': 'baoji'} ,
        {'cityId': 295, 'cityName': '汉中', 'cityPyName': 'hanzhong'} ,
        {'cityId': 298, 'cityName': '商洛', 'cityPyName': 'shangluo'} ,
        {'cityId': 290, 'cityName': '铜川', 'cityPyName': 'tongchuan'} ,
        {'cityId': 293, 'cityName': '渭南', 'cityPyName': 'weinan'} ,
        {'cityId': 17, 'cityName': '西安', 'cityPyName': 'xian'} ,
        {'cityId': 292, 'cityName': '咸阳', 'cityPyName': 'xianyang'} ,
        {'cityId': 294, 'cityName': '延安', 'cityPyName': 'yanan'} ,
        {'cityId': 296, 'cityName': '榆林', 'cityPyName': 'yulin'} ,
        {'cityId': 302, 'cityName': '白银', 'cityPyName': 'baiyin'} ,
        {'cityId': 309, 'cityName': '定西', 'cityPyName': 'dingxi'} ,
        {'cityId': 312, 'cityName': '甘南', 'cityPyName': 'gannan'} ,
        {'cityId': 300, 'cityName': '嘉峪关', 'cityPyName': 'jiayuguan'} ,
        {'cityId': 301, 'cityName': '金昌', 'cityPyName': 'jinchang'} ,
        {'cityId': 307, 'cityName': '酒泉', 'cityPyName': 'jiuquan'} ,
        {'cityId': 299, 'cityName': '兰州', 'cityPyName': 'lanzhou'} ,
        {'cityId': 311, 'cityName': '临夏州', 'cityPyName': 'linxiazhou'} ,
        {'cityId': 310, 'cityName': '陇南', 'cityPyName': 'longnan'} ,
        {'cityId': 306, 'cityName': '平凉', 'cityPyName': 'pingliang'} ,
        {'cityId': 308, 'cityName': '庆阳', 'cityPyName': 'qingyang'} ,
        {'cityId': 303, 'cityName': '天水', 'cityPyName': 'tianshui'} ,
        {'cityId': 304, 'cityName': '武威', 'cityPyName': 'wuwei'} ,
        {'cityId': 305, 'cityName': '张掖', 'cityPyName': 'zhangye'} ,
        {'cityId': 318, 'cityName': '果洛', 'cityPyName': 'guoluo'} ,
        {'cityId': 315, 'cityName': '海北', 'cityPyName': 'haibei'} ,
        {'cityId': 314, 'cityName': '海东', 'cityPyName': 'haidong'} ,
        {'cityId': 411, 'cityName': '海南州', 'cityPyName': 'hainanzhou'} ,
        {'cityId': 320, 'cityName': '海西', 'cityPyName': 'haixi'} ,
        {'cityId': 316, 'cityName': '黄南', 'cityPyName': 'huangnan'} ,
        {'cityId': 313, 'cityName': '西宁', 'cityPyName': 'xining'} ,
        {'cityId': 319, 'cityName': '玉树', 'cityPyName': 'yushu'} ,
        {'cityId': 324, 'cityName': '固原', 'cityPyName': 'guyuan'} ,
        {'cityId': 322, 'cityName': '石嘴山', 'cityPyName': 'shizuishan'} ,
        {'cityId': 323, 'cityName': '吴忠', 'cityPyName': 'wuzhong'} ,
        {'cityId': 321, 'cityName': '银川', 'cityPyName': 'yinchuan'} ,
        {'cityId': 351, 'cityName': '中卫', 'cityPyName': 'zhongwei'} ,
        {'cityId': 332, 'cityName': '阿克苏地区', 'cityPyName': 'akesudiqu'} ,
        {'cityId': 389, 'cityName': '阿拉尔', 'cityPyName': 'alaer'} ,
        {'cityId': 338, 'cityName': '阿勒泰地区', 'cityPyName': 'aletaidiqu'} ,
        {'cityId': 331, 'cityName': '巴音郭楞', 'cityPyName': 'bayinguoleng'} ,
        {'cityId': 346, 'cityName': '北屯', 'cityPyName': 'beitun'} ,
        {'cityId': 330, 'cityName': '博尔塔拉', 'cityPyName': 'boertala'} ,
        {'cityId': 329, 'cityName': '昌吉州', 'cityPyName': 'changjizhou'} ,
        {'cityId': 2233, 'cityName': '哈密市', 'cityPyName': 'hami'} ,
        {'cityId': 335, 'cityName': '和田地区', 'cityPyName': 'hetiandiqu'} ,
        {'cityId': 4493, 'cityName': '胡杨河市', 'cityPyName': 'huyangheshi'} ,
        {'cityId': 334, 'cityName': '喀什地区', 'cityPyName': 'kashidiqu'} ,
        {'cityId': 4490, 'cityName': '可克达拉市', 'cityPyName': 'kekedalashi'} ,
        {'cityId': 326, 'cityName': '克拉玛依', 'cityPyName': 'kelamayi'} ,
        {'cityId': 333, 'cityName': '克孜勒苏', 'cityPyName': 'kezilesu'} ,
        {'cityId': 4489, 'cityName': '昆玉市', 'cityPyName': 'kunyushi'} ,
        {'cityId': 339, 'cityName': '石河子', 'cityPyName': 'shihezi'} ,
        {'cityId': 4488, 'cityName': '双河市', 'cityPyName': 'shuangheshi'} ,
        {'cityId': 337, 'cityName': '塔城地区', 'cityPyName': 'tachengdiqu'} ,
        {'cityId': 4472, 'cityName': '铁门关市', 'cityPyName': 'tiemenguan'} ,
        {'cityId': 405, 'cityName': '图木舒克', 'cityPyName': 'tumushuke'} ,
        {'cityId': 327, 'cityName': '吐鲁番市', 'cityPyName': 'tulufan'} ,
        {'cityId': 325, 'cityName': '乌鲁木齐', 'cityPyName': 'wulumuqi'} ,
        {'cityId': 409, 'cityName': '五家渠', 'cityPyName': 'wujiaqu'} ,
        {'cityId': 336, 'cityName': '伊犁', 'cityPyName': 'yili'} ,
        {'cityId': 341, 'cityName': '香港', 'cityPyName': 'xianggang'} ,
        {'cityId': 342, 'cityName': '澳门', 'cityPyName': 'aomen'} ,
        {'cityId': 340, 'cityName': '台湾', 'cityPyName': 'taiwan'}]