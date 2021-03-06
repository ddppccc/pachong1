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
        # ??????
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
# ???????????????
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"
# ????????????????????????
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
                print('??????ip?????????20???')
                time.sleep(20)
                num -= 1
        print('??????ip')
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
            print('??????????????????',response.status_code, proxies)
        except Exception as e:
            print('get_html??????',proxies, e)
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
    # '??????':'ch0',
    '??????':'ch10',                            #??????
    # '??????????????????':'ch25',
    '????????????':'ch30',                         #??????
    # '??????':'hotel',
    '??????':'ch50',
    'K???':'ch15',                        #??????
    '????????????':'ch45',                        #??????
    '??????/?????????':'ch35',
    # '??????':'ch70',
    # '??????':'ch55',
    '??????':'ch20',
    '??????':'ch95',
    '????????????':'ch80',                    #??????
    '????????????':'ch75',
    '??????/??????':'ch65',
    '????????????':'ch85',
    # '??????':'ch90',
    '????????????':'ch33954',
    '????????????':'ch34259',
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
        {'cityId': 2, 'cityName': '??????', 'cityPyName': 'beijing'},
        {'cityId': 10, 'cityName': '??????', 'cityPyName': 'tianjin'},
        {'cityId': 29, 'cityName': '??????', 'cityPyName': 'baoding'},
        {'cityId': 32, 'cityName': '??????', 'cityPyName': 'cangzhou'},
        {'cityId': 31, 'cityName': '??????', 'cityPyName': 'chengde'},
        {'cityId': 27, 'cityName': '??????', 'cityPyName': 'handan'},
        {'cityId': 34, 'cityName': '??????', 'cityPyName': 'hengshui'},
        {'cityId': 33, 'cityName': '??????', 'cityPyName': 'langfang'},
        {'cityId': 26, 'cityName': '?????????', 'cityPyName': 'qinhuangdao'},
        {'cityId': 24, 'cityName': '?????????', 'cityPyName': 'shijiazhuang'},
        {'cityId': 25, 'cityName': '??????', 'cityPyName': 'tangshan'},
        {'cityId': 28, 'cityName': '??????', 'cityPyName': 'xingtai'},
        {'cityId': 30, 'cityName': '?????????', 'cityPyName': 'zhangjiakou'},
        {'cityId': 38, 'cityName': '??????', 'cityPyName': 'changzhi'} ,
        {'cityId': 36, 'cityName': '??????', 'cityPyName': 'datong'} ,
        {'cityId': 39, 'cityName': '??????', 'cityPyName': 'jincheng'} ,
        {'cityId': 41, 'cityName': '??????', 'cityPyName': 'jinzhong'} ,
        {'cityId': 44, 'cityName': '??????', 'cityPyName': 'linfen'} ,
        {'cityId': 45, 'cityName': '??????', 'cityPyName': 'lvliang'} ,
        {'cityId': 40, 'cityName': '??????', 'cityPyName': 'shuozhou'} ,
        {'cityId': 35, 'cityName': '??????', 'cityPyName': 'taiyuan'} ,
        {'cityId': 43, 'cityName': '??????', 'cityPyName': 'xinzhou'} ,
        {'cityId': 37, 'cityName': '??????', 'cityPyName': 'yangquan'} ,
        {'cityId': 42, 'cityName': '??????', 'cityPyName': 'yuncheng'} ,              ########????????????????????????p1
        {'cityId': 57, 'cityName': '?????????', 'cityPyName': 'alashan'} ,
        {'cityId': 56, 'cityName': '????????????', 'cityPyName': 'bayannaoer'} ,
        {'cityId': 47, 'cityName': '??????', 'cityPyName': 'baotou'} ,
        {'cityId': 49, 'cityName': '??????', 'cityPyName': 'chifeng'} ,
        {'cityId': 51, 'cityName': '????????????', 'cityPyName': 'eerduosi'} ,
        {'cityId': 46, 'cityName': '????????????', 'cityPyName': 'huhehaote'} ,
        {'cityId': 52, 'cityName': '????????????', 'cityPyName': 'hulunbeier'} ,
        {'cityId': 50, 'cityName': '??????', 'cityPyName': 'tongliao'} ,
        {'cityId': 48, 'cityName': '??????', 'cityPyName': 'wuhai'} ,
        {'cityId': 55, 'cityName': '????????????', 'cityPyName': 'wulanchabu'} ,
        {'cityId': 54, 'cityName': '????????????', 'cityPyName': 'xilinguole'} ,
        {'cityId': 53, 'cityName': '?????????', 'cityPyName': 'xingan'} ,
        {'cityId': 58, 'cityName': '??????', 'cityPyName': 'anshan'} ,
        {'cityId': 60, 'cityName': '??????', 'cityPyName': 'benxi'} ,
        {'cityId': 68, 'cityName': '??????', 'cityPyName': 'chaoyang'} ,
        {'cityId': 19, 'cityName': '??????', 'cityPyName': 'dalian'} ,
        {'cityId': 61, 'cityName': '??????', 'cityPyName': 'dandong'} ,
        {'cityId': 59, 'cityName': '??????', 'cityPyName': 'fushun'} ,
        {'cityId': 64, 'cityName': '??????', 'cityPyName': 'fuxin'} ,
        {'cityId': 69, 'cityName': '?????????', 'cityPyName': 'huludao'} ,
        {'cityId': 62, 'cityName': '??????', 'cityPyName': 'jinzhou'} ,
        {'cityId': 65, 'cityName': '??????', 'cityPyName': 'liaoyang'} ,
        {'cityId': 66, 'cityName': '??????', 'cityPyName': 'panjin'} ,
        {'cityId': 18, 'cityName': '??????', 'cityPyName': 'shenyang'} ,
        {'cityId': 67, 'cityName': '??????', 'cityPyName': 'tieling'} ,
        {'cityId': 63, 'cityName': '??????', 'cityPyName': 'yingkou'} ,
        {'cityId': 77, 'cityName': '??????', 'cityPyName': 'baicheng'} ,
        {'cityId': 75, 'cityName': '??????', 'cityPyName': 'baishan'} ,
        {'cityId': 70, 'cityName': '??????', 'cityPyName': 'changchun'} ,
        {'cityId': 71, 'cityName': '??????', 'cityPyName': 'jilin'} ,
        {'cityId': 73, 'cityName': '??????', 'cityPyName': 'liaoyuan'} ,
        {'cityId': 72, 'cityName': '??????', 'cityPyName': 'siping'} ,
        {'cityId': 76, 'cityName': '??????', 'cityPyName': 'songyuan'} ,
        {'cityId': 74, 'cityName': '??????', 'cityPyName': 'tonghua'} ,
        {'cityId': 78, 'cityName': '??????', 'cityPyName': 'yanbian'} ,
        {'cityId': 84, 'cityName': '??????', 'cityPyName': 'daqing'} ,
        {'cityId': 91, 'cityName': '????????????', 'cityPyName': 'daxinganling'} ,
        {'cityId': 79, 'cityName': '?????????', 'cityPyName': 'haerbin'} ,
        {'cityId': 82, 'cityName': '??????', 'cityPyName': 'hegang'} ,
        {'cityId': 89, 'cityName': '??????', 'cityPyName': 'heihe'} ,
        {'cityId': 81, 'cityName': '??????', 'cityPyName': 'jixi'} ,
        {'cityId': 86, 'cityName': '?????????', 'cityPyName': 'jiamusi'} ,
        {'cityId': 88, 'cityName': '?????????', 'cityPyName': 'mudanjiang'} ,
        {'cityId': 87, 'cityName': '?????????', 'cityPyName': 'qitaihe'} ,
        {'cityId': 80, 'cityName': '????????????', 'cityPyName': 'qiqihaer'} ,
        {'cityId': 83, 'cityName': '?????????', 'cityPyName': 'shuangyashan'} ,
        {'cityId': 90, 'cityName': '??????', 'cityPyName': 'suihua'} ,
        {'cityId': 85, 'cityName': '??????', 'cityPyName': 'yichun'} ,
        {'cityId': 1, 'cityName': '??????', 'cityPyName': 'shanghai'} ,
        {'cityId': 93, 'cityName': '??????', 'cityPyName': 'changzhou'} ,
        {'cityId': 96, 'cityName': '??????', 'cityPyName': 'huaian'} ,
        {'cityId': 95, 'cityName': '?????????', 'cityPyName': 'lianyungang'} ,
        {'cityId': 5, 'cityName': '??????', 'cityPyName': 'nanjing'} ,
        {'cityId': 94, 'cityName': '??????', 'cityPyName': 'nantong'} ,
        {'cityId': 6, 'cityName': '??????', 'cityPyName': 'suzhou'} ,
        {'cityId': 100, 'cityName': '??????', 'cityPyName': 'suqian'} ,
        {'cityId': 99, 'cityName': '??????', 'cityPyName': 'taizhou'} ,
        {'cityId': 13, 'cityName': '??????', 'cityPyName': 'wuxi'} ,
        {'cityId': 92, 'cityName': '??????', 'cityPyName': 'xuzhou'} ,
        {'cityId': 97, 'cityName': '??????', 'cityPyName': 'yancheng'} ,
        {'cityId': 12, 'cityName': '??????', 'cityPyName': 'yangzhou'} ,
        {'cityId': 98, 'cityName': '??????', 'cityPyName': 'zhenjiang'} ,
        {'cityId': 3, 'cityName': '??????', 'cityPyName': 'hangzhou'} ,
        {'cityId': 103, 'cityName': '??????', 'cityPyName': 'huzhou'} ,
        {'cityId': 102, 'cityName': '??????', 'cityPyName': 'jiaxing'} ,
        {'cityId': 105, 'cityName': '??????', 'cityPyName': 'jinhua'} ,
        {'cityId': 109, 'cityName': '??????', 'cityPyName': 'lishui'} ,
        {'cityId': 11, 'cityName': '??????', 'cityPyName': 'ningbo'} ,
        {'cityId': 106, 'cityName': '??????', 'cityPyName': 'quzhou'} ,
        {'cityId': 104, 'cityName': '??????', 'cityPyName': 'shaoxing'} ,
        {'cityId': 108, 'cityName': '??????', 'cityPyName': 'taizhou'} ,
        {'cityId': 101, 'cityName': '??????', 'cityPyName': 'wenzhou'} ,
        {'cityId': 107, 'cityName': '??????', 'cityPyName': 'zhoushan'} ,
        {'cityId': 117, 'cityName': '??????', 'cityPyName': 'anqing'} ,
        {'cityId': 112, 'cityName': '??????', 'cityPyName': 'bengbu'} ,
        {'cityId': 124, 'cityName': '??????', 'cityPyName': 'bozhou'} ,
        {'cityId': 125, 'cityName': '??????', 'cityPyName': 'chizhou'} ,
        {'cityId': 119, 'cityName': '??????', 'cityPyName': 'chuzhou'} ,
        {'cityId': 120, 'cityName': '??????', 'cityPyName': 'fuyang'} ,
        {'cityId': 110, 'cityName': '??????', 'cityPyName': 'hefei'} ,
        {'cityId': 115, 'cityName': '??????', 'cityPyName': 'huaibei'} ,
        {'cityId': 113, 'cityName': '??????', 'cityPyName': 'huainan'} ,
        {'cityId': 118, 'cityName': '??????', 'cityPyName': 'huangshan'} ,
        {'cityId': 123, 'cityName': '??????', 'cityPyName': 'liuan'} ,
        {'cityId': 114, 'cityName': '?????????', 'cityPyName': 'maanshan'} ,
        {'cityId': 121, 'cityName': '??????', 'cityPyName': 'suzhou'} ,
        {'cityId': 116, 'cityName': '??????', 'cityPyName': 'tongling'} ,
        {'cityId': 111, 'cityName': '??????', 'cityPyName': 'wuhu'} ,
        {'cityId': 126, 'cityName': '??????', 'cityPyName': 'xuancheng'} ,
        {'cityId': 14, 'cityName': '??????', 'cityPyName': 'fuzhou'} ,
        {'cityId': 132, 'cityName': '??????', 'cityPyName': 'longyan'} ,
        {'cityId': 131, 'cityName': '??????', 'cityPyName': 'nanping'} ,
        {'cityId': 133, 'cityName': '??????', 'cityPyName': 'ningde'} ,
        {'cityId': 127, 'cityName': '??????', 'cityPyName': 'putian'} ,
        {'cityId': 129, 'cityName': '??????', 'cityPyName': 'quanzhou'} ,
        {'cityId': 128, 'cityName': '??????', 'cityPyName': 'sanming'} ,
        {'cityId': 15, 'cityName': '??????', 'cityPyName': 'xiamen'} ,
        {'cityId': 130, 'cityName': '??????', 'cityPyName': 'zhangzhou'} ,
        {'cityId': 143, 'cityName': '??????', 'cityPyName': 'fuzhou'} ,
        {'cityId': 140, 'cityName': '??????', 'cityPyName': 'ganzhou'} ,
        {'cityId': 141, 'cityName': '??????', 'cityPyName': 'jian'} ,
        {'cityId': 135, 'cityName': '?????????', 'cityPyName': 'jingdezhen'} ,
        {'cityId': 137, 'cityName': '??????', 'cityPyName': 'jiujiang'} ,
        {'cityId': 134, 'cityName': '??????', 'cityPyName': 'nanchang'} ,
        {'cityId': 136, 'cityName': '??????', 'cityPyName': 'pingxiang'} ,
        {'cityId': 144, 'cityName': '??????', 'cityPyName': 'shangrao'} ,
        {'cityId': 138, 'cityName': '??????', 'cityPyName': 'xinyu'} ,
        {'cityId': 142, 'cityName': '??????', 'cityPyName': 'yichun'} ,
        {'cityId': 139, 'cityName': '??????', 'cityPyName': 'yingtan'} ,
        {'cityId': 158, 'cityName': '??????', 'cityPyName': 'binzhou'} ,
        {'cityId': 156, 'cityName': '??????', 'cityPyName': 'dezhou'} ,
        {'cityId': 147, 'cityName': '??????', 'cityPyName': 'dongying'} ,
        {'cityId': 159, 'cityName': '??????', 'cityPyName': 'heze'} ,
        {'cityId': 22, 'cityName': '??????', 'cityPyName': 'jinan'} ,
        {'cityId': 150, 'cityName': '??????', 'cityPyName': 'jining'} ,
        {'cityId': 157, 'cityName': '??????', 'cityPyName': 'liaocheng'} ,
        {'cityId': 155, 'cityName': '??????', 'cityPyName': 'linyi'} ,
        {'cityId': 21, 'cityName': '??????', 'cityPyName': 'qingdao'} ,
        {'cityId': 153, 'cityName': '??????', 'cityPyName': 'rizhao'} ,
        {'cityId': 151, 'cityName': '??????', 'cityPyName': 'taian'} ,
        {'cityId': 152, 'cityName': '??????', 'cityPyName': 'weihai'} ,
        {'cityId': 149, 'cityName': '??????', 'cityPyName': 'weifang'} ,
        {'cityId': 148, 'cityName': '??????', 'cityPyName': 'yantai'} ,
        {'cityId': 146, 'cityName': '??????', 'cityPyName': 'zaozhuang'} ,
        {'cityId': 145, 'cityName': '??????', 'cityPyName': 'zibo'} ,
        {'cityId': 164, 'cityName': '??????', 'cityPyName': 'anyang'} ,
        {'cityId': 165, 'cityName': '??????', 'cityPyName': 'hebi'} ,
        {'cityId': 397, 'cityName': '??????', 'cityPyName': 'jiyuan'} ,
        {'cityId': 167, 'cityName': '??????', 'cityPyName': 'jiaozuo'} ,
        {'cityId': 161, 'cityName': '??????', 'cityPyName': 'kaifeng'} ,
        {'cityId': 162, 'cityName': '??????', 'cityPyName': 'luoyang'} ,
        {'cityId': 170, 'cityName': '??????', 'cityPyName': 'luohe'} ,
        {'cityId': 172, 'cityName': '??????', 'cityPyName': 'nanyang'} ,
        {'cityId': 163, 'cityName': '?????????', 'cityPyName': 'pingdingshan'} ,
        {'cityId': 168, 'cityName': '??????', 'cityPyName': 'puyang'} ,
        {'cityId': 171, 'cityName': '?????????', 'cityPyName': 'sanmenxia'} ,
        {'cityId': 173, 'cityName': '??????', 'cityPyName': 'shangqiu'} ,
        {'cityId': 166, 'cityName': '??????', 'cityPyName': 'xinxiang'} ,
        {'cityId': 174, 'cityName': '??????', 'cityPyName': 'xinyang'} ,
        {'cityId': 169, 'cityName': '??????', 'cityPyName': 'xuchang'} ,
        {'cityId': 160, 'cityName': '??????', 'cityPyName': 'zhengzhou'} ,
        {'cityId': 175, 'cityName': '??????', 'cityPyName': 'zhoukou'} ,
        {'cityId': 176, 'cityName': '?????????', 'cityPyName': 'zhumadian'} ,
        {'cityId': 181, 'cityName': '??????', 'cityPyName': 'ezhou'} ,
        {'cityId': 188, 'cityName': '??????', 'cityPyName': 'enshi'} ,
        {'cityId': 185, 'cityName': '??????', 'cityPyName': 'huanggang'} ,
        {'cityId': 177, 'cityName': '??????', 'cityPyName': 'huangshi'} ,
        {'cityId': 182, 'cityName': '??????', 'cityPyName': 'jinmen'} ,
        {'cityId': 184, 'cityName': '??????', 'cityPyName': 'jingzhou'} ,
        {'cityId': 190, 'cityName': '??????', 'cityPyName': 'qianjiang'} ,
        {'cityId': 404, 'cityName': '???????????????', 'cityPyName': 'shennongjia'} ,
        {'cityId': 178, 'cityName': '??????', 'cityPyName': 'shiyan'} ,
        {'cityId': 187, 'cityName': '??????', 'cityPyName': 'suizhou'} ,
        {'cityId': 191, 'cityName': '??????', 'cityPyName': 'tianmen'} ,
        {'cityId': 16, 'cityName': '??????', 'cityPyName': 'wuhan'} ,
        {'cityId': 189, 'cityName': '??????', 'cityPyName': 'xiantao'} ,
        {'cityId': 186, 'cityName': '??????', 'cityPyName': 'xianning'} ,
        {'cityId': 180, 'cityName': '??????', 'cityPyName': 'xiangyang'} ,
        {'cityId': 183, 'cityName': '??????', 'cityPyName': 'xiaogan'} ,
        {'cityId': 179, 'cityName': '??????', 'cityPyName': 'yichang'} ,
        {'cityId': 344, 'cityName': '??????', 'cityPyName': 'changsha'} ,
        {'cityId': 197, 'cityName': '??????', 'cityPyName': 'changde'} ,
        {'cityId': 200, 'cityName': '??????', 'cityPyName': 'chenzhou'} ,
        {'cityId': 194, 'cityName': '??????', 'cityPyName': 'hengyang'} ,
        {'cityId': 202, 'cityName': '??????', 'cityPyName': 'huaihua'} ,
        {'cityId': 203, 'cityName': '??????', 'cityPyName': 'loudi'} ,
        {'cityId': 195, 'cityName': '??????', 'cityPyName': 'shaoyang'} ,
        {'cityId': 193, 'cityName': '??????', 'cityPyName': 'xiangtan'} ,
        {'cityId': 204, 'cityName': '??????', 'cityPyName': 'xiangxi'} ,
        {'cityId': 199, 'cityName': '??????', 'cityPyName': 'yiyang'} ,
        {'cityId': 201, 'cityName': '??????', 'cityPyName': 'yongzhou'} ,
        {'cityId': 196, 'cityName': '??????', 'cityPyName': 'yueyang'} ,
        {'cityId': 198, 'cityName': '?????????', 'cityPyName': 'zhangjiajie'} ,
        {'cityId': 192, 'cityName': '??????', 'cityPyName': 'zhuzhou'} ,
        {'cityId': 221, 'cityName': '??????', 'cityPyName': 'chaozhou'} ,
        {'cityId': 219, 'cityName': '??????', 'cityPyName': 'dongguan'} ,
        {'cityId': 208, 'cityName': '??????', 'cityPyName': 'foshan'} ,
        {'cityId': 4, 'cityName': '??????', 'cityPyName': 'guangzhou'} ,
        {'cityId': 216, 'cityName': '??????', 'cityPyName': 'heyuan'} ,
        {'cityId': 213, 'cityName': '??????', 'cityPyName': 'huizhou'} ,
        {'cityId': 209, 'cityName': '??????', 'cityPyName': 'jiangmen'} ,
        {'cityId': 222, 'cityName': '??????', 'cityPyName': 'jieyang'} ,
        {'cityId': 211, 'cityName': '??????', 'cityPyName': 'maoming'} ,
        {'cityId': 214, 'cityName': '??????', 'cityPyName': 'meizhou'} ,
        {'cityId': 218, 'cityName': '??????', 'cityPyName': 'qingyuan'} ,
        {'cityId': 207, 'cityName': '??????', 'cityPyName': 'shantou'} ,
        {'cityId': 215, 'cityName': '??????', 'cityPyName': 'shanwei'} ,
        {'cityId': 205, 'cityName': '??????', 'cityPyName': 'shaoguan'} ,
        {'cityId': 7, 'cityName': '??????', 'cityPyName': 'shenzhen'} ,
        {'cityId': 217, 'cityName': '??????', 'cityPyName': 'yangjiang'} ,
        {'cityId': 223, 'cityName': '??????', 'cityPyName': 'yunfu'} ,
        {'cityId': 210, 'cityName': '??????', 'cityPyName': 'zhanjiang'} ,
        {'cityId': 212, 'cityName': '??????', 'cityPyName': 'zhaoqing'} ,
        {'cityId': 220, 'cityName': '??????', 'cityPyName': 'zhongshan'} ,
        {'cityId': 206, 'cityName': '??????', 'cityPyName': 'zhuhai'} ,
        {'cityId': 233, 'cityName': '??????', 'cityPyName': 'baise'} ,
        {'cityId': 228, 'cityName': '??????', 'cityPyName': 'beihai'} ,
        {'cityId': 394, 'cityName': '??????', 'cityPyName': 'chongzuo'} ,
        {'cityId': 229, 'cityName': '?????????', 'cityPyName': 'fangchenggang'} ,
        {'cityId': 231, 'cityName': '??????', 'cityPyName': 'guigang'} ,
        {'cityId': 226, 'cityName': '??????', 'cityPyName': 'guilin'} ,
        {'cityId': 235, 'cityName': '??????', 'cityPyName': 'hechi'} ,
        {'cityId': 234, 'cityName': '??????', 'cityPyName': 'hezhou'} ,
        {'cityId': 398, 'cityName': '??????', 'cityPyName': 'laibin'} ,
        {'cityId': 225, 'cityName': '??????', 'cityPyName': 'liuzhou'} ,
        {'cityId': 224, 'cityName': '??????', 'cityPyName': 'nanning'} ,
        {'cityId': 230, 'cityName': '??????', 'cityPyName': 'qinzhou'} ,
        {'cityId': 227, 'cityName': '??????', 'cityPyName': 'wuzhou'} ,
        {'cityId': 232, 'cityName': '??????', 'cityPyName': 'yulin'} ,
        {'cityId': 390, 'cityName': '??????', 'cityPyName': 'baisha'} ,
        {'cityId': 391, 'cityName': '??????', 'cityPyName': 'baoting'} ,
        {'cityId': 392, 'cityName': '??????', 'cityPyName': 'changjiang'} ,
        {'cityId': 393, 'cityName': '?????????', 'cityPyName': 'chengmai'} ,
        {'cityId': 358, 'cityName': '??????', 'cityPyName': 'danzhou'} ,
        {'cityId': 395, 'cityName': '?????????', 'cityPyName': 'dingan'} ,
        {'cityId': 396, 'cityName': '??????', 'cityPyName': 'dongfang'} ,
        {'cityId': 23, 'cityName': '??????', 'cityPyName': 'haikou'} ,
        {'cityId': 399, 'cityName': '??????', 'cityPyName': 'ledong'} ,
        {'cityId': 400, 'cityName': '?????????', 'cityPyName': 'lingao'} ,
        {'cityId': 401, 'cityName': '??????', 'cityPyName': 'lingshui'} ,
        {'cityId': 402, 'cityName': '??????', 'cityPyName': 'qionghai'} ,
        {'cityId': 403, 'cityName': '??????', 'cityPyName': 'qiongzhong'} ,
        {'cityId': 2310, 'cityName': '??????', 'cityPyName': 'sansha'} ,
        {'cityId': 345, 'cityName': '??????', 'cityPyName': 'sanya'} ,
        {'cityId': 406, 'cityName': '?????????', 'cityPyName': 'tunchang'} ,
        {'cityId': 407, 'cityName': '??????', 'cityPyName': 'wanning'} ,
        {'cityId': 408, 'cityName': '??????', 'cityPyName': 'wenchang'} ,
        {'cityId': 410, 'cityName': '?????????', 'cityPyName': 'wuzhishan'} ,
        {'cityId': 9, 'cityName': '??????', 'cityPyName': 'chongqing'} ,
        {'cityId': 255, 'cityName': '??????', 'cityPyName': 'aba'} ,
        {'cityId': 253, 'cityName': '??????', 'cityPyName': 'bazhong'} ,
        {'cityId': 8, 'cityName': '??????', 'cityPyName': 'chengdu'} ,
        {'cityId': 251, 'cityName': '??????', 'cityPyName': 'dazhou'} ,
        {'cityId': 241, 'cityName': '??????', 'cityPyName': 'deyang'} ,
        {'cityId': 256, 'cityName': '?????????', 'cityPyName': 'ganzi'} ,
        {'cityId': 250, 'cityName': '??????', 'cityPyName': 'guangan'} ,
        {'cityId': 243, 'cityName': '??????', 'cityPyName': 'guangyuan'} ,
        {'cityId': 246, 'cityName': '??????', 'cityPyName': 'leshan'} ,
        {'cityId': 257, 'cityName': '??????', 'cityPyName': 'liangshan'} ,
        {'cityId': 240, 'cityName': '??????', 'cityPyName': 'luzhou'} ,
        {'cityId': 248, 'cityName': '??????', 'cityPyName': 'meishan'} ,
        {'cityId': 242, 'cityName': '??????', 'cityPyName': 'mianyang'} ,
        {'cityId': 245, 'cityName': '??????', 'cityPyName': 'neijiang'} ,
        {'cityId': 247, 'cityName': '??????', 'cityPyName': 'nanchong'} ,
        {'cityId': 239, 'cityName': '?????????', 'cityPyName': 'panzhihua'} ,
        {'cityId': 244, 'cityName': '??????', 'cityPyName': 'suining'} ,
        {'cityId': 252, 'cityName': '??????', 'cityPyName': 'yaan'} ,
        {'cityId': 249, 'cityName': '??????', 'cityPyName': 'yibin'} ,
        {'cityId': 254, 'cityName': '??????', 'cityPyName': 'ziyang'} ,
        {'cityId': 238, 'cityName': '??????', 'cityPyName': 'zigong'} ,
        {'cityId': 261, 'cityName': '??????', 'cityPyName': 'anshun'} ,
        {'cityId': 264, 'cityName': '?????????', 'cityPyName': 'bijieshi'} ,
        {'cityId': 258, 'cityName': '??????', 'cityPyName': 'guiyang'} ,
        {'cityId': 259, 'cityName': '?????????', 'cityPyName': 'liupanshui'} ,
        {'cityId': 265, 'cityName': '?????????', 'cityPyName': 'qiandongnan'} ,
        {'cityId': 266, 'cityName': '??????', 'cityPyName': 'qiannan'} ,
        {'cityId': 263, 'cityName': '?????????', 'cityPyName': 'qianxinan'} ,
        {'cityId': 262, 'cityName': '??????', 'cityPyName': 'tongren'} ,
        {'cityId': 260, 'cityName': '??????', 'cityPyName': 'zunyi'} ,
        {'cityId': 270, 'cityName': '??????', 'cityPyName': 'baoshan'} ,
        {'cityId': 272, 'cityName': '?????????', 'cityPyName': 'chuxiongzhou'} ,
        {'cityId': 277, 'cityName': '?????????', 'cityPyName': 'dali'} ,
        {'cityId': 278, 'cityName': '??????', 'cityPyName': 'dehong'} ,
        {'cityId': 281, 'cityName': '??????', 'cityPyName': 'diqing'} ,
        {'cityId': 273, 'cityName': '??????', 'cityPyName': 'honghe'} ,
        {'cityId': 267, 'cityName': '??????', 'cityPyName': 'kunming'} ,
        {'cityId': 279, 'cityName': '??????', 'cityPyName': 'lijiang'} ,
        {'cityId': 282, 'cityName': '??????', 'cityPyName': 'linchang'} ,
        {'cityId': 280, 'cityName': '??????', 'cityPyName': 'nujiang'} ,
        {'cityId': 275, 'cityName': '??????', 'cityPyName': 'puer'} ,
        {'cityId': 268, 'cityName': '??????', 'cityPyName': 'qujing'} ,
        {'cityId': 274, 'cityName': '?????????', 'cityPyName': 'wenshan'} ,
        {'cityId': 276, 'cityName': '????????????', 'cityPyName': 'xishuangbanna'} ,
        {'cityId': 269, 'cityName': '??????', 'cityPyName': 'yuxi'} ,
        {'cityId': 271, 'cityName': '??????', 'cityPyName': 'zhaotong'} ,
        {'cityId': 288, 'cityName': '??????', 'cityPyName': 'ali'} ,
        {'cityId': 284, 'cityName': '?????????', 'cityPyName': 'changdudiqu'} ,
        {'cityId': 283, 'cityName': '??????', 'cityPyName': 'lasa'} ,
        {'cityId': 289, 'cityName': '?????????', 'cityPyName': 'linzhi'} ,
        {'cityId': 287, 'cityName': '??????', 'cityPyName': 'naqu'} ,
        {'cityId': 286, 'cityName': '?????????', 'cityPyName': 'rikaze'} ,
        {'cityId': 285, 'cityName': '??????', 'cityPyName': 'shannan'} ,
        {'cityId': 297, 'cityName': '??????', 'cityPyName': 'ankang'} ,
        {'cityId': 291, 'cityName': '??????', 'cityPyName': 'baoji'} ,
        {'cityId': 295, 'cityName': '??????', 'cityPyName': 'hanzhong'} ,
        {'cityId': 298, 'cityName': '??????', 'cityPyName': 'shangluo'} ,
        {'cityId': 290, 'cityName': '??????', 'cityPyName': 'tongchuan'} ,
        {'cityId': 293, 'cityName': '??????', 'cityPyName': 'weinan'} ,
        {'cityId': 17, 'cityName': '??????', 'cityPyName': 'xian'} ,
        {'cityId': 292, 'cityName': '??????', 'cityPyName': 'xianyang'} ,
        {'cityId': 294, 'cityName': '??????', 'cityPyName': 'yanan'} ,
        {'cityId': 296, 'cityName': '??????', 'cityPyName': 'yulin'} ,
        {'cityId': 302, 'cityName': '??????', 'cityPyName': 'baiyin'} ,
        {'cityId': 309, 'cityName': '??????', 'cityPyName': 'dingxi'} ,
        {'cityId': 312, 'cityName': '??????', 'cityPyName': 'gannan'} ,
        {'cityId': 300, 'cityName': '?????????', 'cityPyName': 'jiayuguan'} ,
        {'cityId': 301, 'cityName': '??????', 'cityPyName': 'jinchang'} ,
        {'cityId': 307, 'cityName': '??????', 'cityPyName': 'jiuquan'} ,
        {'cityId': 299, 'cityName': '??????', 'cityPyName': 'lanzhou'} ,
        {'cityId': 311, 'cityName': '?????????', 'cityPyName': 'linxiazhou'} ,
        {'cityId': 310, 'cityName': '??????', 'cityPyName': 'longnan'} ,
        {'cityId': 306, 'cityName': '??????', 'cityPyName': 'pingliang'} ,
        {'cityId': 308, 'cityName': '??????', 'cityPyName': 'qingyang'} ,
        {'cityId': 303, 'cityName': '??????', 'cityPyName': 'tianshui'} ,
        {'cityId': 304, 'cityName': '??????', 'cityPyName': 'wuwei'} ,
        {'cityId': 305, 'cityName': '??????', 'cityPyName': 'zhangye'} ,
        {'cityId': 318, 'cityName': '??????', 'cityPyName': 'guoluo'} ,
        {'cityId': 315, 'cityName': '??????', 'cityPyName': 'haibei'} ,
        {'cityId': 314, 'cityName': '??????', 'cityPyName': 'haidong'} ,
        {'cityId': 411, 'cityName': '?????????', 'cityPyName': 'hainanzhou'} ,
        {'cityId': 320, 'cityName': '??????', 'cityPyName': 'haixi'} ,
        {'cityId': 316, 'cityName': '??????', 'cityPyName': 'huangnan'} ,
        {'cityId': 313, 'cityName': '??????', 'cityPyName': 'xining'} ,
        {'cityId': 319, 'cityName': '??????', 'cityPyName': 'yushu'} ,
        {'cityId': 324, 'cityName': '??????', 'cityPyName': 'guyuan'} ,
        {'cityId': 322, 'cityName': '?????????', 'cityPyName': 'shizuishan'} ,
        {'cityId': 323, 'cityName': '??????', 'cityPyName': 'wuzhong'} ,
        {'cityId': 321, 'cityName': '??????', 'cityPyName': 'yinchuan'} ,
        {'cityId': 351, 'cityName': '??????', 'cityPyName': 'zhongwei'} ,
        {'cityId': 332, 'cityName': '???????????????', 'cityPyName': 'akesudiqu'} ,
        {'cityId': 389, 'cityName': '?????????', 'cityPyName': 'alaer'} ,
        {'cityId': 338, 'cityName': '???????????????', 'cityPyName': 'aletaidiqu'} ,
        {'cityId': 331, 'cityName': '????????????', 'cityPyName': 'bayinguoleng'} ,
        {'cityId': 346, 'cityName': '??????', 'cityPyName': 'beitun'} ,
        {'cityId': 330, 'cityName': '????????????', 'cityPyName': 'boertala'} ,
        {'cityId': 329, 'cityName': '?????????', 'cityPyName': 'changjizhou'} ,
        {'cityId': 2233, 'cityName': '?????????', 'cityPyName': 'hami'} ,
        {'cityId': 335, 'cityName': '????????????', 'cityPyName': 'hetiandiqu'} ,
        {'cityId': 4493, 'cityName': '????????????', 'cityPyName': 'huyangheshi'} ,
        {'cityId': 334, 'cityName': '????????????', 'cityPyName': 'kashidiqu'} ,
        {'cityId': 4490, 'cityName': '???????????????', 'cityPyName': 'kekedalashi'} ,
        {'cityId': 326, 'cityName': '????????????', 'cityPyName': 'kelamayi'} ,
        {'cityId': 333, 'cityName': '????????????', 'cityPyName': 'kezilesu'} ,
        {'cityId': 4489, 'cityName': '?????????', 'cityPyName': 'kunyushi'} ,
        {'cityId': 339, 'cityName': '?????????', 'cityPyName': 'shihezi'} ,
        {'cityId': 4488, 'cityName': '?????????', 'cityPyName': 'shuangheshi'} ,
        {'cityId': 337, 'cityName': '????????????', 'cityPyName': 'tachengdiqu'} ,
        {'cityId': 4472, 'cityName': '????????????', 'cityPyName': 'tiemenguan'} ,
        {'cityId': 405, 'cityName': '????????????', 'cityPyName': 'tumushuke'} ,
        {'cityId': 327, 'cityName': '????????????', 'cityPyName': 'tulufan'} ,
        {'cityId': 325, 'cityName': '????????????', 'cityPyName': 'wulumuqi'} ,
        {'cityId': 409, 'cityName': '?????????', 'cityPyName': 'wujiaqu'} ,
        {'cityId': 336, 'cityName': '??????', 'cityPyName': 'yili'} ,
        {'cityId': 341, 'cityName': '??????', 'cityPyName': 'xianggang'} ,
        {'cityId': 342, 'cityName': '??????', 'cityPyName': 'aomen'} ,
        {'cityId': 340, 'cityName': '??????', 'cityPyName': 'taiwan'}]