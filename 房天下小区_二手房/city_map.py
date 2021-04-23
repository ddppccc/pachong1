# 该脚本获取城市的分区
import json
import re
import time
import requests
from lxml import etree
import os

""" 房天下 """

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
}
def getCity_Code():
    item={}
    response = requests.get('https://www.fang.com/SoufunFamily.htm', headers=headers, timeout=(5, 5))
    response.encoding = 'gbk'
    html = etree.HTML(response.text)
    lists=html.xpath('//div[@class="onCont"]/table//a')
    for i in lists:
        city=i.xpath('./text()')[0]
        url=i.xpath('./@href')[0]
        code=url.split('.')[0][7:]
        # print(city,code,url)
        if city in ['波士顿','保加利亚','昌吉','德国','海外','西雅图','广德','旧金山','洛杉矶','日本','塞浦路斯','西雅图','西班牙','希腊','悉尼','芝加哥','马来西亚','澳大利亚','美国','纽约','葡萄牙','蒙城','安陆','璧山','綦江','潜江','石河子']:
            continue
        item[city]=code
    return item
city_map=getCity_Code()
# with open(os.path.join(os.path.dirname(__file__), 'city_map.json'), 'r', encoding='utf-8') as f:
#     city_map = json.load(f)



# 下载请求页面
def get_html(url, headers):
    while True:
        try:
            proxies = {"https": get_proxy()}
            response = requests.get(url, headers=headers,proxies=proxies,timeout=(10, 10))
            encod = response.apparent_encoding
            if encod == 'GB2312':
                encod = 'gbk'
            response.encoding = encod
            html = etree.HTML(response.text)
            if '跳转' in "".join(html.xpath("//title/text()")):
                t4 = "".join(re.findall("var t4=\'(.*)\';", response.text)[0])
                t3 = "".join(re.findall('var t3=\'(.*)\';', response.text)[-2])
                url = t4 + '?' + t3
                print("二次验证: t4: ", t4, "\tt3: ", t3)
                continue
            return html
        except Exception as e:
            print("请求出错: ",proxies, e)
            continue


# 根据城市名获得行政区
def get_proxy():
    try:
            return requests.get('http://47.106.223.4:50002/get/').json().get('proxy')
    except:
        num = 3
        while num:
            try:
                return requests.get('http://47.106.223.4:50002/get/').json().get('proxy')
            except:
                print('暂无ip，等待20秒')
                time.sleep(20)
                num-=1
        print('暂无ip')
def get_regions(city_name, GetType):
    """
    根据城市名获得行政区
    :type  二手房抓取
    :param city_name:
    :return: {'guangming': '光明'}
    """
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "global_cookie=f1v4y6cur4h7034ieaxs84qnk17jxobmy8b; Integrateactivity=notincludemc; newhouse_user_guid=50E5E180-78E4-4D10-DD8D-77E13BC96848; lastscanpage=0; __utmc=147393320; logGuid=85ba8359-bbe3-40bf-a1b9-5fba4ba5e9c3; new_search_uid=409e38256dd50cc398a6ef44a4cf8ea6; __utmz=147393320.1564039746.31.23.utmcsr=gz.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; city=www; __utma=147393320.1256259835.1562223675.1564039746.1564054938.32; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; budgetLayer=1%7Cbj%7C2019-07-25%2019%3A47%3A37; resourceDetail=1; g_sourcepage=ehlist; unique_cookie=U_y46qm1gjou8nny4td442ktabo11jydqi82f*242; __utmb=147393320.30.10.1564054938",
        "Referer": "https://esf.fang.com/newsecond/esfcities.aspx",
        "upgrade-insecure-requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    }

    # 二手房
    if GetType == '二手房':
        url = 'https://{}.esf.fang.com/'.format(city_map[city_name])
        if city_name == '北京':
            url = 'https://esf.fang.com/'
        print('\n将在 %s 爬取行政区' % url)
        html = get_html(url, headers=headers)

        regions_xpath = "//span[contains(text(), '区域')]//following-sibling::ul//a"
        regions = dict(zip(html.xpath(regions_xpath + '/@href'), html.xpath(regions_xpath + '/text()')))
        regions = {key.rsplit('/', 2)[-2]: value for key, value in regions.items() if
                   '周边' not in value and '全部' not in value}

        return regions

    else:  # 小区
        url = 'https://{}.esf.fang.com/housing/'.format(city_map[city_name])
        if city_name == '北京':
            url = 'https://esf.fang.com/housing/'
        if city_name == '绍兴':
            url = 'https://shaoxing.esf.fang.com/housing/'
        print('\n将在 %s 爬取行政区' % url)

        html = get_html(url=url, headers=headers)

        regions_xpath = "//*[@id='houselist_B03_02']/div[@class='qxName']/a"
        regions = dict(zip(html.xpath(regions_xpath + '/@href'), html.xpath(regions_xpath + '/text()')))
        regions = {key.rsplit('/', 2)[-2]: value for key, value in regions.items() if
                   '不限' not in value and '全部' not in value and '周边' not in value}

        return regions


def make_url(city_name, url_fmt, GetType, city_code='suoxie'):
    # 获取城市中文名称
    # filter()
    # 函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表。
    # 该接收两个参数，第一个为函数，第二个为序列，序列的每个元素作为参数传递给函数进行判，然后将值为True的返回到新列表中
    city_name = list(filter(lambda x: city_name in x, city_map))[0]

    # 获取城市名称拼音
    code = city_map.get(city_name)

    print(code, code)
    if city_name == '绍兴' and GetType == '小区':
        code = 'shaoxing'
    if code:
        # 获取城市的行政区划分列表
        regions = {url_fmt.format(code, key): value for key, value in get_regions(city_name, GetType).items()}

        print(city_name, code, '\n提取到的分区: ', regions)
        return regions
    elif city_name == '北京':
        regions = {'https://{}esf.fang.com/{}/'.format(code, key): value for key, value in
                   get_regions(city_name, GetType).items()}
        if GetType != '二手房':
            regions = {'https://{}esf.fang.com/housing/{}/'.format(code, key): value for key, value in
                       get_regions(city_name, GetType).items()}

        print(city_name, code, '\n提取到的分区: ', regions)

        return regions
    else:
        return {}


if __name__ == '__main__':
    # {'https://nanyang.anjuke.com/community/wolongb/': '卧龙',
    # 'https://nanyang.anjuke.com/community/wanchengb/': '宛城',
    # ......,
    # 'https://nanyang.anjuke.com/community/nanzhaob/': '南召',
    # 'https://nanyang.anjuke.com/community/qitaabcdefghijklmnopqrs/': '其他'}

    #
    # make_url('深圳', 'https://{}.esf.fang.com/{}/')

    # get_regions('深圳')
    # data1 = open('test.html', 'r', encoding='utf-8').read()
    # import re
    # from selenium import webdriver
    # import time
    # url_city = dict(re.findall('<a href="([^"]+)">([^<]+)</a>', data1))
    # driver = webdriver.Chrome()
    # city_map = {}
    # for url in url_city:
    #     print(url)
    #     driver.get(url)
    #     if 'verify' in driver.current_url:
    #         input()
    #     # time.sleep(.1)
    #     elm = driver.find_element_by_xpath("//div[@id='header']//span[@class='city']")
    #     city_name = elm.text
    #     city_code = re.findall('https://([^\.]+)\.',driver.current_url)[0]
    #     city_map[city_name] = city_code
    #     print(city_name, city_code)
    # with open('city_code2.json', 'w', encoding='utf-8') as f:
    #     json.dump(city_map, f)
    # driver.close()

    # for city, city_code in city_map.items():
    #     if city != '深圳': continue
    #     # make_url(city_name=city, url_fmt='https://{}.esf.fang.com/housing/{}/', GetType="小区")
    #     make_url(city_name=city, url_fmt='https://{}.esf.fang.com/housing/{}/', GetType="小区")
    #     print()
    # print(city_map)
    # print(city_list)
    pass