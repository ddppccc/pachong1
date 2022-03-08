import requests
import time
import random
from config import get_proxy,rancook
e = ['a', 'b', 'c', 'd', 'e', 'f']
n = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
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
headers={
    'Connection': 'keep-alive',
    # 'Cookie': '_lxsdk_cuid=179c01ab88cc8-0df2f0b9256ac1-2363163-1fa400-179c01ab88cc8; _hc.v=fb783b09-adc2-78df-f8a5-7b53f530416c.1622425648; s_ViewType=10; _dp.ac.v=19b24d59-781c-4e11-94fc-d848cfb75d8f; ctu=21fd3f032ee980c9b98bee37cc18e7671d5ddb8684865c57d85b840ce1fe7fff; aburl=1; cityid=9; ua=dpuser_1966568564; cityInfo=%7B%22cityId%22%3A9%2C%22cityName%22%3A%22%E9%87%8D%E5%BA%86%22%2C%22provinceId%22%3A0%2C%22parentCityId%22%3A0%2C%22cityOrderId%22%3A0%2C%22isActiveCity%22%3Afalse%2C%22cityEnName%22%3A%22chongqing%22%2C%22cityPyName%22%3Anull%2C%22cityAreaCode%22%3Anull%2C%22cityAbbrCode%22%3Anull%2C%22isOverseasCity%22%3Afalse%2C%22isScenery%22%3Afalse%2C%22TuanGouFlag%22%3A0%2C%22cityLevel%22%3A0%2C%22appHotLevel%22%3A0%2C%22gLat%22%3A0%2C%22gLng%22%3A0%2C%22directURL%22%3Anull%2C%22standardEnName%22%3Anull%7D; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1622711914; uuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; iuuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _lxsdk=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _ga=GA1.2.1975686433.1622713531; _lx_utm=utm_source%3Diphx; default_ab=shop%3AA%3A11%7CshopList%3AA%3A5; cye=ningguo; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1622684317,1622688482,1622770592,1623029851; _lxsdk_s=179e47dfeb2-3f7-1c2-6e8%7C%7C20; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7='+str(int(time.time())),
    # 'Cookie': 's_ViewType=10; _lxsdk_cuid=179d0b00c27c8-013205f9b94a1a-51361244-1fa400-179d0b00c27c8; _lxsdk=179d0b00c27c8-013205f9b94a1a-51361244-1fa400-179d0b00c27c8; _hc.v=e149a70e-039d-1da2-cc33-5281ba603bab.1622703869; fspop=test; cy=9; cye=chongqing; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1622703870,1622773377,1623048604; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7='+str(int(time.time()))+'; _lxsdk_s=179e53c45a4-ceb-e96-7ae%7C%7C19',


    # 'Cookie': '_lxsdk_cuid=179e95c99791-06ce75e4ff57fc-68151f7a-1fa400-179e95c997ac8; _lxsdk=179e95c99791-06ce75e4ff57fc-68151f7a-1fa400-179e95c997ac8; _hc.v=f50464d5-bd9d-07d4-fad0-7f7d20538c25.1623117832; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1623117832,1623132947; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1623132947; _lxsdk_s=179ea42f481-7a0-e3b-68c%7C%7C3',
    # 'Cookie': '_lxsdk_cuid=179c01ab88cc8-0df2f0b9256ac1-2363163-1fa400-179c01ab88cc8; _lxsdk=179e95c99791-06ce75e4ff57fc-68151f7a-1fa400-179e95c997ac8; _hc.v=f50464d5-bd9d-07d4-fad0-7f7d20538c25.1623117832; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1623117832,1623132947; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1623132947; _lxsdk_s=179ea42f481-7a0-e3b-68c%7C%7C3',
    # 'Cookie': '_lxsdk_cuid=179eafe5c57c8-0b7f93562b9806-f7f1939-1fa400-179eafe5c57c8; _lxsdk=179e95c99791-06ce75e4ff57fc-68151f7a-1fa400-179e95c997ac8; _hc.v=f50464d5-bd9d-07d4-fad0-7f7d20538c25.1623117832; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1623117832,1623132947; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1623132947; _lxsdk_s=179ea42f481-7a0-e3b-68c%7C%7C3',
    # 'Cookie': '_lxsdk_cuid=179eb0257e6c8-0ed98d26aac296-f7f1939-1fa400-179eb0257e7c8; _lxsdk=179e95c99791-06ce75e4ff57fc-68151f7a-1fa400-179e95c997ac8; _hc.v=f50464d5-bd9d-07d4-fad0-7f7d20538c25.1623117832; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1623117832,1623132947; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1623132947; _lxsdk_s=179ea42f481-7a0-e3b-68c%7C%7C3',
    # 'Cookie': '_lxsdk_cuid=179eb02c2bbc8-0f9f2fbe38479a-f7f1939-1fa400-179eb02c2bbc8; _lxsdk=179e95c99791-06ce75e4ff57fc-68151f7a-1fa400-179e95c997ac8; _hc.v=f50464d5-bd9d-07d4-fad0-7f7d20538c25.1623117832; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1623117832,1623132947; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1623132947; _lxsdk_s=179ea42f481-7a0-e3b-68c%7C%7C3',
    'Cookie': f'_lxsdk_cuid={cuid}; _lxsdk=179e95c99791-06ce75e4ff57fc-68151f7a-1fa400-179e95c997ac8; _hc.v=f50464d5-bd9d-07d4-fad0-7f7d20538c25.{str(int(time.time()))}; Hm_lvt_602b80cf8079ae6591966cc70a3940e7={str(int(time.time()))}; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1623132947; _lxsdk_s=179ea42f481-7a0-e3b-68c%7C%7C3',
    'Host': 'www.dianping.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
}
def rans(num):
    x=''
    for i in range(num):
        x += random.choice(s)
    return x

def getheaders():
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
    headers = {
        'Connection': 'keep-alive',
        'Cookie': f'_lxsdk_cuid={cuid}; _lxsdk=179e9{rans(5)}91-06ce{rans(10)}-68151f7a-1fa400-179e{rans(7)}c8; _hc.v=f50464d5-{rans(4)}-07d4-fad0-7f7d{rans(5)}c25.{str(int(time.time()))}; Hm_lvt_602b80cf8079ae659{rans(10)}940e7={str(int(time.time()))}; Hm_lpvt_602b80cf8079ae65{rans(10)}3940e7={str(int(time.time()))}; _lxsdk_s=179ea{rans(6)}-7a0-{rans(3)}-68c%7C%7C3',
        'Host': 'www.dianping.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    }
    return headers
def getpos(shopId,cityId,mainRegionId, mainCategoryId, shopname):
    # print('正在获取pos')
    url = 'http://www.dianping.com/ajax/json/shopDynamic/shopAside'
    # cityId='2'
    data2 = {
        'shopId':shopId ,
        'cityId': str(cityId),
        'shopName': shopname,
        'power': '5',
        'mainCategoryId': mainCategoryId,
        'shopType': '30',
        'mainRegionId': mainRegionId,
        'cityEnName': 'beijing',
        'shopCityId': '2',
        # '_token': 'eJxVj1uPojAYhv9Lb4dIW1oK3qGCi6cZDjI4k7kQcLEqBwE5ONn/viXZudikyff07fMlb79BZSdgiiCEBEmgPVVgCtAETlQggaYWLyrGTNewEDCTQPx/xiCVQFQFCzD91JgiIcjY15i4IvhEOoYi0uCX9MNEMCbijJYtJHBumnIqy13XTRJ+zEuep5O4yOT6XJTyL9rNn/fFpjUdA95NU5QCYjPzx01NxRLBY1GmUEnRmCBKBSE2StdREvP4bzY/9634olBrnuaCTqsePWG97i7GfpbMG88OtnIUHKBz9nhX8LWhJv3rEbnNHe7awHfJhie1a82jYpOp6YJ39Bln8omjKDaSZfJxr02WtDfFXs9Jvz1rZne5bQ9pb/ZVMXTPSncDmptEuephvrKqzPLdltDqUQZvVPm9tJ0bOXwMr54xI08vIxdjZy2ujZcNj9hA9cB4fn/x/FUZFi+6YsNiIyrWa6KHNHYaxbntFeMwLMN9BqE/86x3wvs0dvhl3b8FPR0KxOBuX3rWQ4ve8UNWU6Lo1dkPmwzHVUhZL29UfD0aRzVovFhND9ES/PkLr1OjZA==',
        # 'uuid': 'fb783b09-adc2-78df-f8a5-7b53f530416c.1622425648',
        'platform': '1',
        'partner': '150',
        'optimusCode': '10',
        'originUrl': 'http://www.dianping.com/shop/'+shopId,
    }
    for i in range(100):
        try:
            proxy=get_proxy()
            proxies = {
                "http": proxy,
                "https": proxy
            }
            # proxies = {"http": '116.117.134.135:80'}
            # proxies = {"http": random.choice([requests.get('http://118.24.52.95:5010/get/').json().get('proxy'),requests.get('http://47.106.223.4:50002/get/').json().get('proxy'),requests.get('http://192.168.1.131:5010/get/').json().get('proxy')])}
            # print('正在获取坐标')
            r = requests.get(url, params=data2,proxies=proxies, headers=getheaders(),timeout=2)
            # r = requests.get(url, params=data2, headers=headers,timeout=2)
            if not r.status_code in [200]:continue
            data=r.json()['shop']
            # print('获取坐标成功', shopId, mainRegionId, mainCategoryId, shopname)
            print('获取坐标成功')
            return data
        except Exception as e:
            # print(e)
            # print(shopId, mainRegionId, mainCategoryId, shopname)
            continue
    print('获取坐标错误次数过多')
    return {'glng':0.0,'glat':0.0}



def getmpos(shopId):
    headers = {
        'Connection': 'keep-alive',
        'Cookie': rancook,
        'Host': 'www.dianping.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    }
    url = 'http://www.dianping.com/ajax/json/shopDynamic/shopAside'
    proxies = {"https": get_proxy()}
    data = {
        'shopId': shopId,
        'power': '5',
        'platform': '1',
        'partner': '150',
        'optimusCode': '10',
        'originUrl': 'http://www.dianping.com/shop/%s'%shopId,
    }
    # r = requests.get(url, params=data, headers=headers, timeout=2)
    # print(r.text)
    for i in range(100):
        try:
            proxy=get_proxy()
            proxies = {
                "http": proxy,
                "https": proxy
            }
            r = requests.get(url, params=data,proxies=proxies, headers=headers,timeout=2)
            if not r.status_code in [200]:continue
            data=r.json()['shop']
            return data
        except Exception as e:
            continue
    print('获取坐标错误次数过多')
    return {'glng':0.0,'glat':0.0}




if __name__ == '__main__':
    headers = {
        'Connection': 'keep-alive',
        # 'Cookie': f'_lxsdk_cuid={cuid}; _lxsdk=179e9{rans(5)}91-06ce{rans(10)}-68151f7a-1fa400-179e{rans(7)}c8; _hc.v=f50464d5-{rans(4)}-07d4-fad0-7f7d{rans(5)}c25.{str(int(time.time()))}; Hm_lvt_602b80cf8079ae659{rans(10)}940e7={str(int(time.time()))}; Hm_lpvt_602b80cf8079ae65{rans(10)}3940e7={str(int(time.time()))}; _lxsdk_s=179ea{rans(6)}-7a0-{rans(3)}-68c%7C%7C3',
        # 'Cookie': "_lxsdk_cuid=179c01ab88cc8-0df2f0b9256ac1-2363163-1fa400-179c01ab88cc8; _hc.v=fb783b09-adc2-78df-f8a5-7b53f530416c.1622425648; s_ViewType=10; _dp.ac.v=19b24d59-781c-4e11-94fc-d848cfb75d8f; ctu=21fd3f032ee980c9b98bee37cc18e7671d5ddb8684865c57d85b840ce1fe7fff; aburl=1; cityid=9; ua=dpuser_1966568564; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1622711914; uuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; iuuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _lxsdk=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _ga=GA1.2.1975686433.1622713531; fspop=test; cy=2; cye=beijing; default_ab=shop%3AA%3A11%7CshopList%3AA%3A5%7Cmap%3AA%3A1; msource=default; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1623893307,1623915079,1624005143,1624245053; _lxsdk_s=17a2c6f1257-b67-9e8-72c%7C%7C319; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1624245131",
        'Cookie': rancook,
        'Host': 'www.dianping.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    }
    shopname = '润<e class="address">&#xf842;</e><e class="address">&#xebbd;</e>'
    url = 'http://www.dianping.com/ajax/json/shopDynamic/shopAside'
    proxies = {"https": get_proxy()}
    data = {
        'shopId': 'k54bKG93AfgLwW5h',
        # 'cityId': '2',
        # 'shopName': shopname,
        'power': '5',
        # 'mainCategoryId': '141',
        # 'shopType': '30',
        # 'mainRegionId': '1484',
        # 'cityEnName': 'beijing',
        # 'shopCityId': '2',
        # '_token': 'eJxVj1uPojAYhv9Lb4dIW1oK3qGCi6cZDjI4k7kQcLEqBwE5ONn/viXZudikyff07fMlb79BZSdgiiCEBEmgPVVgCtAETlQggaYWLyrGTNewEDCTQPx/xiCVQFQFCzD91JgiIcjY15i4IvhEOoYi0uCX9MNEMCbijJYtJHBumnIqy13XTRJ+zEuep5O4yOT6XJTyL9rNn/fFpjUdA95NU5QCYjPzx01NxRLBY1GmUEnRmCBKBSE2StdREvP4bzY/9634olBrnuaCTqsePWG97i7GfpbMG88OtnIUHKBz9nhX8LWhJv3rEbnNHe7awHfJhie1a82jYpOp6YJ39Bln8omjKDaSZfJxr02WtDfFXs9Jvz1rZne5bQ9pb/ZVMXTPSncDmptEuephvrKqzPLdltDqUQZvVPm9tJ0bOXwMr54xI08vIxdjZy2ujZcNj9hA9cB4fn/x/FUZFi+6YsNiIyrWa6KHNHYaxbntFeMwLMN9BqE/86x3wvs0dvhl3b8FPR0KxOBuX3rWQ4ve8UNWU6Lo1dkPmwzHVUhZL29UfD0aRzVovFhND9ES/PkLr1OjZA==',
        # 'uuid': 'fb783b09-adc2-78df-f8a5-7b53f530416c.1622425648',
        'platform': '1',
        'partner': '150',
        'optimusCode': '10',
        'originUrl': 'http://www.dianping.com/shop/k54bKG93AfgLwW5h',
    }
    r = requests.get(url, params=data, headers=headers,timeout=2)
    # print(cuid)
    print(r.text)