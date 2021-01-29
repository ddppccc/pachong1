import time

import requests


def get_proxy():
    while True:
        try:
            pro = requests.get("http://47.106.223.4:50002/get/").json().get('proxy')
            return pro
        except:
            time.sleep(1)
            continue


def delete_proxy(proxy):
    while True:
        try:
            pro = requests.get("http://47.106.223.4:50002/delete/?proxy={}".format(proxy))
            return
        except:
            time.sleep(1)
            continue



def get_Html_IP(url, headers):

    retry_count = 10
    while retry_count > 0:
        proxy = get_proxy()

        if "!" in str(proxy) or not proxy:
            print("没有ip, 等待60s")
            time.sleep(60)
            continue
        number = 3
        while number > 0:
            try:
                response = requests.get(url, headers=headers, timeout=2, proxies={'http': 'http://%s'%proxy, 'https': 'https://%s'%proxy})
                encod = response.apparent_encoding
                if encod.upper() in ['GB2312', 'WINDOWS-1254']:
                    encod = 'gbk'
                response.encoding = encod

            except Exception as e:
                number -= 1
                continue

            if response.status_code == 502:
                print("服务器错误,重新请求, 等待2秒")
                time.sleep(2)
                continue
            if '跳转' in response.text:
                print('跳转页面')
                continue

            if  '璁块棶楠岃瘉' in response.text or '访问验证' in response.text:
                print('需要验证, 出现搜索引擎')
                break
            return response

        # 出错3次, 删除代理池中代理
        delete_proxy(proxy)
        print('删除IP: ', proxy, url)
        retry_count -= 1
    return None


if __name__ == '__main__':
    url = 'https://abazhou.newhouse.fang.com/house/s/xiaojinxian/'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "global_cookie=f1v4y6cur4h7034ieaxs84qnk17jxobmy8b; Integrateactivity=notincludemc; newhouse_user_guid=50E5E180-78E4-4D10-DD8D-77E13BC96848; lastscanpage=0; budgetLayer=1%7Cbj%7C2019-07-30%2011%3A26%3A08; resourceDetail=1; new_search_uid=fd91130e51ddd1f2d8e5a7847545c3d8; __utmc=147393320; __utma=147393320.184954923.1564457033.1564642303.1564646708.12; __utmz=147393320.1564646708.12.5.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-verify/redirect; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; logGuid=cb4c3441-3467-4c19-ba09-1dd86b143529; g_sourcepage=ehlist; city=anshan; unique_cookie=U_11rfckz759men2uard7dzzy1i1ejys2c6di*36; __utmb=147393320.15.10.1564646708",
        "Referer": "https://esf.fang.com/newsecond/esfcities.aspx",
        "upgrade-insecure-requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    }
    res = get_Html_IP(url, headers)
    print(res.text)