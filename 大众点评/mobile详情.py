# encoding=utf-8
import random
import time
import requests
from config import rancook,getrandomcookie
from d import P
from config import rans
from config import get_proxy
import re
def getheaders(shopid):
    headers = {

        'Host': 'm.dianping.com',
        'Connection': 'keep-alive',
        # 'Content-Length': '1929',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        # 'sec-ch-ua-mobile': '?1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Mobile Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://m.dianping.com',
        'Sec-Fetch-Site': 'same-origin',
        # 'Sec-Fetch-Mode': 'cors',
        # 'Sec-Fetch-Dest': 'empty',
        'Referer': f'https://m.dianping.com/shop/{shopid}',
        'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Cookie': getrandomcookie()
    }
    return headers
def gettoken():
    with open('token.txt','r') as f:
        token=f.read()
        return token

def getmdetail(shopid):
    print('正在获取号码')
    for i in range(10):
        h = {

            'Host': 'm.dianping.com',
            'Connection': 'keep-alive',
            # 'Content-Length': '1929',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            # 'sec-ch-ua-mobile': '?1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Mobile Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://m.dianping.com',
            'Sec-Fetch-Site': 'same-origin',
            # 'Sec-Fetch-Mode': 'cors',
            # 'Sec-Fetch-Dest': 'empty',
            'Referer': f'https://m.dianping.com/shop/{shopid}',
            'Accept-Encoding': 'gzip, deflate, br',
            # 'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': getrandomcookie()
        }
        # uuid = f'fb783b09-adc2-78df-f8a5-7b53f530416c.{str(int(time.time()))}'
        uuid = f'fb{rans(5)}9-adc2-78df-f8a5-7b53{rans(6)}6c.{str(int(time.time()))}'
        # shopid = 'k6sCyr1j8sKjRPVu'
        token = gettoken()
        data = f'pageEnName=shop&moduleInfoList%5B0%5D%5BmoduleName%5D=baseinfo&moduleInfoList%5B0%5D%5Bquery%5D%5BshopId%5D={shopid}&moduleInfoList%5B0%5D%5Bquery%5D%5BhideInfo%5D=true&moduleInfoList%5B1%5D%5BmoduleName%5D=address&moduleInfoList%5B1%5D%5Bquery%5D%5BshopId%5D={shopid}&moduleInfoList%5B1%5D%5Bquery%5D%5BhideInfo%5D=true&moduleInfoList%5B2%5D%5BmoduleName%5D=autoopenapp&moduleInfoList%5B2%5D%5Bconfig%5D%5BopenUTM%5D=&moduleInfoList%5B2%5D%5Bconfig%5D%5Butm%5D=&moduleInfoList%5B2%5D%5Bconfig%5D%5Bapp_utm%5D=w_mshop_auto&moduleInfoList%5B2%5D%5Bconfig%5D%5BdisableTopPage%5D=false&moduleInfoList%5B2%5D%5Bconfig%5D%5Bapp_link_android%5D=dianping%3A%2F%2Fshopinfo%3Fid%3D%7BshopId%7D%26utm%3D%7Butm%7D&moduleInfoList%5B2%5D%5Bconfig%5D%5BopenURL%5D=dianping%3A%2F%2Fshopinfo%3Fid%3D%7BshopId%7D%26utm%3D%7Butm%7D&moduleInfoList%5B2%5D%5Bconfig%5D%5Bapp_link_ios%5D=dianping%3A%2F%2Fshopinfo%3Fid%3D%7BshopId%7D%26utm%3D%7Butm%7D&moduleInfoList%5B2%5D%5Bconfig%5D%5Btimeout%5D=0&moduleInfoList%5B2%5D%5Bquery%5D%5BshopId%5D={shopid}&uuid={uuid}&platform=3&partner=150&optimusCode=10&originUrl=https%3A%2F%2Fm.dianping.com%2Fshop%2F{shopid}&_token={token}'
        url = 'https://m.dianping.com/index/api/module'
        proxy = get_proxy()
        proxies = {
            "http": proxy,
            "https": proxy
        }
        # rr = requests.post(url, data=data, headers=h)
        try:
            rr = requests.post(url, data=data,proxies=proxies,timeout=3, headers=getheaders(shopid))
        except:continue
        if rr.status_code != 200:
            continue
        rr.encoding='utf8'
        if not re.findall('"entity":"(.*?)"', rr.text):
            # time.sleep(1)
            if i > 5:
                print('获取号码次数过多')
                return ''
            continue
        print('获取号码成功')
        return rr.text
    print('获取号码次数过多')
    return ''

if __name__ == '__main__':
    # print(getmdetail('H5bE0Gp3yPBpIdnY'))
    print(getmdetail('l4zlvrhOqKhlpaAy'))


