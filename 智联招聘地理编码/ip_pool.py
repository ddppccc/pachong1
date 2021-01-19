import re
import time

import requests

from crack_cookie import run1


def get_proxy():
    # return requests.get("http://127.0.0.1:5010/get/").json().get('proxy')
    return requests.get("http://47.106.223.4:50002/get/").json().get('proxy')


def delete_proxy(proxy):
    # html = requests.get("http://1127.0.0.1:5010/delete/?proxy={}".format(proxy))
    html = requests.get("http://47.106.223.4:50002/delete/?proxy={}".format(proxy))
    return html.text


# 解密数据
def zhilian_cookie_factory(arg1):
    """
    解析cookie
    :param arg1:
    :return:
    """
    key_array = [15, 35, 29, 24, 33, 16, 1, 38, 10, 9, 19, 31, 40, 27, 22, 23, 25, 13, 6, 11, 39, 18, 20, 8, 14, 21, 32,
                 26, 2, 30, 7, 4, 17, 5, 3, 28, 34, 37, 12, 36]
    data = "3000176000856006061501533003690027800375"

    step1 = []
    for i in range(len(arg1)):
        for ii in range(len(key_array)):
            if key_array[ii] == i + 1:
                step1.append(ii)

    cache = ""
    for i in range(len(step1)):
        ii = step1.index(i)
        cache += arg1[ii]

    iii = 0
    cookie = ""
    while iii < len(cache) and iii < len(data):
        a = int(cache[iii:iii + 2], 16)
        b = int(data[iii:iii + 2], 16)
        c = hex(a ^ b)[2:]
        if len(c) == 1:
            c = '0' + c
        cookie += c
        iii += 2
    return cookie


def get_script_data(url, proxy=None, headers=None):
    """
    获取并返回网页数据
    :param url:
    :return:
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Host': 'jobs.zhaopin.com',

        'Accept-Language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cookie': 'acw_tc=2760823b15866900164434294e5cfe118b1b122702a5643342c66c5963e821; x-zp-client-id=7dfbc5df-46fa-4fac-f5c1-56138d274728; sts_deviceid=1716e19daf5168-05abca6ba421f8-6701b35-1327104-1716e19daf692b; sts_sg=1; sts_chnlsid=Unknown; zp_src_url=https%3A%2F%2Fjobs.zhaopin.com%2FCC183970727J00236754910.htm; jobRiskWarning=true; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221716e19dad9d2-0bcdcbb98cbd7a-6701b35-1327104-1716e19dada121%22%2C%22%24device_id%22%3A%221716e19dad9d2-0bcdcbb98cbd7a-6701b35-1327104-1716e19dada121%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%7D; acw_sc__v2=5e93c8e8ea8f4d363a8bb42d0ef66c74526466c0; sts_sid=1717148cde93af-0c4036d132e7e5-6701b35-1327104-1717148cdea7b1; acw_sc__=5e93cbe212ae879323183038e01768581405a7ec; ZL_REPORT_GLOBAL={%22jobs%22:{%22recommandActionidShare%22:%226c8f0a78-798f-4188-9d7a-622cf06f9ea1-job%22}}; sts_evtseq=6'
        }
    s = requests.Session()
    print('dali: ', proxy)
    proxies = {
        "http": "http://{}".format(proxy),
        "https": "https://{}".format(proxy)
        }
    r = s.get(url, headers=header, timeout=10, proxies=proxies)

    if 'arg1=' not in r.text:
        print('没有arg1')
        return r
    arg1 = re.search("arg1='([^']+)'", r.text).group(1)
    s.cookies['acw_sc__v2'] = zhilian_cookie_factory(arg1)
    r = s.get(url, headers=header, timeout=10, proxies=proxies)
    r.encoding = r.apparent_encoding
    print('rs: ',url, r.text[:100])
    return r


def getHtml(url, headers):
    # ....
    retry_count = 2
    proxy = get_proxy()
    print("代理: ", proxy)
    if "!" in str(proxy):
        print("没有ip, 等待60s")
        time.sleep(60)
    number = 1
    a = 3
    while retry_count > 0:
        try:
            time.sleep(0.5)
            while True:
                html = get_script_data(url, proxy, headers)
                html.encoding = 'utf-8'
                if "arg1" in html.text:
                    a -= 1
                    # print(url, proxy, '重试...',a )
                else:
                    break
                if a > 0:
                    continue
                else:
                    return html, proxy
            # """
            if "arg1" in html.text:
                if not html:
                    number += 1
                    continue

            if "滑动验证页面" in "".join(re.findall("\<title\>(.*)\<\/title\>", html.text)):
                print("滑动页面", )
                retry_count = -1
                break
            # print("try:内, 当前ip: ", proxy)
            return html, proxy

        except Exception as e:
            print("报错, retry_count: %s , url: %s, 代理: %s, %s" % (retry_count, url, proxy, e))
            retry_count -= 1

    # 出错3次, 删除代理池中代理
    delete_proxy(proxy)
    # print("删除ip: ", (proxy, url))
    return None


if __name__ == '__main__':
    number = 1
    while True:
        url = 'http://jobs.zhaopin.com/CC120069275J00235315308.htm'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'cookie': 'acw_tc=2760821b15816894814778468efdfbab9419b1c9961e7c5f1b0cf12123bd78; x-zp-client-id=b7f53ea2-85fa-4517-addb-1ce1ebe7b5f6; sts_deviceid=170440e280942a-049775333a938c-6701b35-1327104-170440e280a326; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22170440a3062b7-05890bf6444ef2-6701b35-1327104-170440a3063353%22%2C%22%24device_id%22%3A%22170440a3062b7-05890bf6444ef2-6701b35-1327104-170440a3063353%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%7D; sts_sg=1; sts_chnlsid=Unknown; jobRiskWarning=true; zp_src_url=http%3A%2F%2Fjobs.zhaopin.com%2FCC692075226J00076116115.htm; sts_sid=170461573b045a-0b380f8705ef27-6701b35-1327104-170461573b1c1a; ZL_REPORT_GLOBAL={%22jobs%22:{%22recommandActionidShare%22:%22f5c41fa4-aee4-4f8e-82a2-b08e02f4c9d8-job%22}}; sts_evtseq=2; acw_sc__v2=5e47325c664ce497b3188c1edea6a3b4e66f0d98'
        }
        proxy = requests.get("http://127.0.0.1:5010/get/").text
        r = get_script_data(url, proxy=proxy)
        r.encoding = r.apparent_encoding
        print(r.text)
        number += 1
        if 'arg1=' not in r.text:
            break

        print(number)


    # a = requests.get(url, headers=headers)
    # # headers = {
    # #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    # #     'Host': 'jobs.zhaopin.com',
    # #
    # #     'Accept-Language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
    # #     'Cache-Control': 'max-age=0',
    # #     'Connection': 'keep-alive',
    # #     'Upgrade-Insecure-Requests': '1',
    # #     # 'Cookie': "_uab_collina=156335456885984443547376; sou_experiment=unexperiment; _qzja=1.2094130333.1563412887880.1563412887880.1563412887880.1563412887880.1563412887880.0.0.0.1.1; __jsluid_s=1ea211449e4e07192aa1cbf5d03375bd; x-zp-client-id=fc733252-e3a5-470b-900d-cc7a3794e7b6; sts_deviceid=16c65f0e2ec302-0da4c186c19144-e343166-1327104-16c65f0e2ed520; adfbid2=0; smidV2=20190730174414d3becc9f13a496f55ac21f1911ef558300eb76519c441d460; Hm_lvt_80e552e101e24fe607597e5f45c8d2a2=1568192874,1570701351; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216d1f9443d395b-0507f583b4cb5f-e343166-1327104-16d1f9443d4af4%22%2C%22%24device_id%22%3A%2216d1f9443d395b-0507f583b4cb5f-e343166-1327104-16d1f9443d4af4%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidupcpz%22%2C%22%24latest_utm_medium%22%3A%22cpt%22%7D%7D; dywez=95841923.1572342655.6.3.dywecsr=jobs.zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/cc844736870j00360376308.htm; __utma=269921210.1082725216.1568192874.1571973511.1572342655.6; __utmz=269921210.1572342655.6.3.utmcsr=jobs.zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct=/CC844736870J00360376308.htm; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1571297878,1571298071,1571909245,1572342655; acw_tc=2760825015750219055732388e69d5039d42f4d3507c73329f8f33f50fcd15; dywea=95841923.180064747159326750.1568192874.1572342655.1575028447.7; urlfrom2=121126445; adfcid2=none; sts_sg=1; sts_chnlsid=Unknown; zp_src_url=https%3A%2F%2Fjobs.zhaopin.com%2FCC485763789J00278369303.htm; jobRiskWarning=true; acw_sc__=5de9c035601fefc4d231096099dd29401b2e6fdb; ZL_REPORT_GLOBAL={%22jobs%22:{%22recommandActionidShare%22:%22921788bf-522f-4723-b488-3b3103bb3443-job%22%2C%22funczoneShare%22:%22dtl_best_for_you%22}}; sts_sid=16ed916d571723-00b6c0217a1a35-b363e65-1327104-16ed916d57274f; sts_evtseq=2"
    # #
    # #     }
    # # a, b = getHtml(url, headers)
    #
    # print(a.text)
