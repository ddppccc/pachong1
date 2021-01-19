import json
import re
import time
import requests
from scrapy import Selector
from map import cities


def zhilian_cookie_factory(arg1):
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


# 获取所有岗位映射表
"""
url = 'http://jobs.zhaopin.com/'
res = get_script_data(url)

response = Selector(text=res)
content_list = response.xpath('//div[@class="content-list"]')

data = {}
for content in content_list:
    category_a_list = content.xpath('./div[@class="listcon"]/a')

    category_first = content.xpath('.//h2/text()').get()
    item = {}
    for a in category_a_list:

        category = a.xpath('./text()').get()
        category_code = a.xpath("./@href").get().replace('/','')
        item[category] = category_code
        print(category, category_code)
    data[category_first] = item
print(data)
"""


# 所有城市映射表
'''
a = """<a href="//jobs.zhaopin.com/guangdong/" target="_blank">广东</a>
<a href="//jobs.zhaopin.com/hubei/" target="_blank">湖北</a>
<a href="//jobs.zhaopin.com/shaanxi/" target="_blank">陕西</a>
<a href="//jobs.zhaopin.com/sichuan/" target="_blank">四川</a>
<a href="//jobs.zhaopin.com/liaoning/" target="_blank">辽宁</a>
<a href="//jobs.zhaopin.com/jilin/" target="_blank">吉林</a>
<a href="//jobs.zhaopin.com/jiangsu/" target="_blank">江苏</a>
<a href="//jobs.zhaopin.com/shandong/" target="_blank">山东</a>
<a href="//jobs.zhaopin.com/zhejiang/" target="_blank">浙江</a>
<a href="//jobs.zhaopin.com/guangxi/" target="_blank">广西</a>
<a href="//jobs.zhaopin.com/anhui/" target="_blank">安徽</a>
<a href="//jobs.zhaopin.com/hebei/" target="_blank">河北</a>
<a href="//jobs.zhaopin.com/shanxi/" target="_blank">山西</a>
<a href="//jobs.zhaopin.com/neimenggu/" target="_blank">内蒙</a>
<a href="//jobs.zhaopin.com/fujian/" target="_blank">福建</a>
<a href="//jobs.zhaopin.com/jiangxi/" target="_blank">江西</a>
<a href="//jobs.zhaopin.com/henan/" target="_blank">河南</a>
<a href="//jobs.zhaopin.com/hunan/" target="_blank">湖南</a>
<a href="//jobs.zhaopin.com/hainans/" target="_blank">海南</a>
<a href="//jobs.zhaopin.com/guizhou/" target="_blank">贵州</a>
<a href="//jobs.zhaopin.com/yunnan/" target="_blank">云南</a>
<a href="//jobs.zhaopin.com/tibet/" target="_blank">西藏</a>
<a href="//jobs.zhaopin.com/gansu/" target="_blank">甘肃</a>
<a href="//jobs.zhaopin.com/qinghai/" target="_blank">青海</a>
<a href="//jobs.zhaopin.com/ningxia/" target="_blank">宁夏</a>
<a href="//jobs.zhaopin.com/xinjiang/" target="_blank">新疆</a>
<a href="//jobs.zhaopin.com/heilongjiang/" target="_blank">黑龙江</a>"""
data = {}
for a_ in a.split('\n'):
    url = "http:" + re.findall('href="(.*)" target', a_)[0]
    province = re.findall('target="_blank">(.*)</a>', a_)[0]
    print(province, url)

    res = get_script_data(url)
    response = Selector(text=res)
    a_list = response.xpath("//h2[contains(text(), '主要城市')]/../following-sibling::div[1]//a[not(@class='currentlimit')]")

    item = {}
    for a in a_list:
        city = a.xpath('./text()').get()
        city_url = a.xpath('./@href').get()
        item[city] = city_url
    data[province] = item

print(data)
'''


# 获取所有城市区县映射表
data = {}
for province, province_code in cities.items():

    for city, city_url in province_code.items():
        print('省份: %s, 城市: %s' % (province, city))
        time.sleep(0.3)
        res = get_script_data(city_url)
        response = Selector(text=res)

        a_list = response.xpath("//h2[contains(text(), '热门地区')]/../following-sibling::div[1]//a[not(@class='currentlimit')]")

        item = {}
        for a in a_list:
            region = a.xpath('./text()').get()
            region_url = a.xpath('./@href').get()
            item[region] = region_url

        if not a_list:
            item[city] = city_url

        data[city] = item
        print(item)
print(data)

with open('region.json', 'w', encoding='utf-8') as fp:
    fp.write(json.dumps(data, ensure_ascii=False))