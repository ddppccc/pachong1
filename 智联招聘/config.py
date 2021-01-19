import re

import requests


def zhilian_cookie_factory(arg1):
    """
    解析cookie
    :param arg1:
    :return:
    """
    key_array = [15, 35, 29, 24, 33, 16, 1, 38, 10, 9, 19, 31, 40, 27, 22, 23, 25, 13, 6, 11, 39, 18, 20, 8, 14, 21, 32, 26, 2, 30, 7, 4, 17, 5, 3, 28, 34, 37, 12, 36]
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


def get_script_data(url):
    """
    获取并返回网页数据
    :param url:
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    s = requests.Session()
    r = s.get(url, headers=headers, timeout=10)
    if 'arg1=' not in r.text:
        return r.text
    arg1 = re.search("arg1='([^']+)'", r.text).group(1)
    s.cookies['acw_sc__v2'] = zhilian_cookie_factory(arg1)
    r = s.get(url, headers=headers, timeout=10)
    return r.text





