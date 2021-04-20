import base64
import json
import re
import time

import requests
from requests import Session


def get_proxy():
    try:
        return requests.get('http://47.106.223.4:50002/get/').json().get('proxy')
        # return '111.202.83.35:80'
    except:
        num = 3
        while num:
            try:
                return requests.get('http://47.106.223.4:50002/get/').json().get('proxy')
            except:
                print('暂无ip，等待20秒')
                time.sleep(20)

                num -= 1
        print('暂无ip')

def run1(url):
    while 1:
        proxy = get_proxy()
        cookie = TuDi().run_get_ip_cookie(proxy)
        print(proxy, cookie,url)
        proxies = {
            'http': 'http://{}'.format(proxy),
            'https': 'https://{}'.format(proxy),
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "zh-CN,zh;q=0.9",
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests':'1',
            'cookie': cookie,
            'Referer': url,
            'Host': 'www.landchina.com',
            'Origin': 'https://www.landchina.com'
        }
        try:
            # res = requests.get(url, headers=headers, proxies=proxies)
            res = requests.get(url, headers=headers, proxies=proxies,timeout=(10,10))
            res.encoding = 'gbk'

            return res
        except Exception as e:
            print('run1', e)
            continue


class TuDi:
    def __init__(self):
        pass

    def stringToHex(self, s):
        val = ""
        for k in s:
            if val == "":
                val = str(hex(ord(k)))
            else:
                val += str(hex(ord(k)))
        return val.replace("0x", "")

    def get_verify_code(self, pic):
        a = base64.b64decode(pic)
        r = requests.post('http://127.0.0.1:7788', data=a)
        code = json.loads(r.text)['code']
        return code

    def run_get_ip_cookie(self, proxy):
        proxies = {
            'http': 'http://{}'.format(proxy),
            'https': 'https://{}'.format(proxy),
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "zh-CN,zh;q=0.9",
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Referer': 'http://www.landchina.com/default.aspx?tabid=261',
            'Host': 'www.landchina.com',
            'Origin': 'https://www.landchina.com'
        }
        url = 'https://www.landchina.com/default.aspx?tabid=261'
        session = Session()
        res = session.get(url, proxies=proxy, timeout=(10,5))
        cookie = requests.utils.dict_from_cookiejar(res.cookies)
        cookie['srcurl'] = self.stringToHex(url)
        try:
            pic = re.findall('data:image/bmp;base64,(.*)"/></td></tr><tr><td colspan="3">', res.text)[0]
        except:
            return ''
        verify_code = self.get_verify_code(pic)
        url1 = 'https://www.landchina.com/?security_verify_img={}'.format('3' + "3".join(list(str(verify_code))))
        session.post(url1, headers=headers, cookies=cookie, proxies=proxies, timeout=(2,5))
        cookie_dict = session.cookies.get_dict()
        return "".join(['{k}={v};'.format(k=k,v=v) for k,v in cookie_dict.items()])

    def run(self):

        while True:
            # proxy = get_proxy()
            # if ':' not in str(proxy):
            #     time.sleep(2*60)
            #     continue
            number = 2
            while number > 0:
                try:

                    proxies = {"https": get_proxy()}
                    # cookie = self.run_get_ip_cookie(proxies)
                    cookie='ASP.NET_SessionId=w3a5ne3kmsfwg4f224j1ip3w; Hm_lvt_83853859c7247c5b03b527894622d3fa=1618816746; Hm_lpvt_83853859c7247c5b03b527894622d3fa=1618888646'
                    # print(proxies,cookie)
                    return proxies, cookie
                except Exception as e:
                    print(' 解析cookie时失败: ', e)

                    number -= 1
                    continue
            # if ty == 1:
            #     requests.get("http://47.106.223.4:50002/delete/?proxy={}".format(proxy))
            # else:
            #     requests.get("http://127.0.0.1:5014/delete/?proxy={}".format(proxy))

            continue

if __name__ == '__main__':
    # proxy = get_proxy()
    # cookie = TuDi(proxy).run_get_ip_cookie(proxy)
    # print('proxy: ', proxy)
    # print(cookie)
    TuDi = TuDi()
    TuDi.run()