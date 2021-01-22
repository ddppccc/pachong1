import json
import os
import random
import re
import time
import uuid
import requests

from lxml import etree
from concurrent.futures.thread import ThreadPoolExecutor

from capter_verify.captcha_run import AJK_Slide_Captcha
from rent.check_file import save_region, delete_log_dir, check
from rent.ip_other import get_proxy, get_ua, delete_proxy
from rent.save_data import save_data
from rent.zujin_descde import decode_zujin, get_font

os.chdir(os.path.dirname(os.path.abspath(__file__)))


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    'Connection': 'close',
    "referer": "https://www.anjuke.com/sy-city.html",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}


# 获取页面信息
def get_html(url):
    ip_number = 100
    while ip_number > 0:
        proxy = get_proxy()
        if not proxy:
            print("没有ip, 等待2分钟")
            time.sleep(120)

        number = 3
        while number > 0:
            headers['user-agent'] = get_ua()
            try:
                response = requests.get(url, headers=headers,
                                        proxies={"https": "https://{}".format(proxy)}, timeout=(2, 5))
                response.encoding = 'utf-8'
                html = etree.HTML(response.text)
            except requests.exceptions.ProxyError:
                number = -1
                continue
            except requests.exceptions.ConnectionError:
                number = -1
                continue
            except Exception as  e:
                print("出错, 正在进行第%s尝试, ip: %s, %s" % (number, proxy, type(e)))
                number -= 1
                continue

            # 检查是否出现 58滑动验证
            if html.xpath("//div[@class='pop']/p[@class='title']"):
                print("出现滑动验证, 更改ip")
                number = -1
                continue

            # 安居客滑动验证, js破解
            if html.xpath('//*[@id="captchaForm"]'):
                proixy = "https://" + proxy
                try:
                    message = AJK_Slide_Captcha(proixy).run()
                    if message != '校验成功':
                        break
                except Exception as e:
                    print("错误原因: ", e)
                    continue

            # ip被封
            if "访问过于频繁" in "".join(html.xpath("//h2[@class='item']/text()")):
                print(proxy, "ip被封")
                number = -1
                continue

            if response.status_code in [403]:
                print(403)
                continue
            return html, response, proxy

        # 出错3次, 删除代理池中代理
        delete_proxy(proxy)
        ip_number -= 1
        continue
    print("全部出处")
    return '', '', ''


# 获取价格区间映射表,返回字典形式
# {'1000元以下': 'https://bj.zu.anjuke.com/fangyuan/chaoyang/zj5332/',
def get_price_map_dict(url):
    html, response, _ = get_html(url)
    if not response:
        print("链接请求出错, 丢弃")
        return

    if "没有找到" in "".join(html.xpath("//div[@id='zu-comhead']/p/text()")):
        print("当前没有房源数据")
        return

    houseList = html.xpath("//div[@class='zu-itemmod']")
    if houseList:
        price_xpath = "//div[@class='items ']//a"
        price_extent = {key: value for key, value in
                        dict(zip(html.xpath(price_xpath + "/text()"), html.xpath(price_xpath + "/@href"))).items() if
                        "全部" not in key or '周边' not in key}
        print("价格字典: ", price_extent)
        return price_extent


# 按行政区/价格区间进行分析, 获取html, 并获取当前所有页面
def get_price_district_html(url, city, region, extent=None, dataAll=None):
    html, response, proxy = get_html(url=url)
    if not response:
        print('没有 response: ')
        return
    try:
        font = get_font(response.text)
    except:
        return

    house_div = html.xpath("//div[@class='zu-itemmod']")
    if len(house_div) == 0:
        return

    for house in house_div:
        houseData = {}
        houseData['id'] = uuid.uuid1(node=random.randint(10, 1000000000))
        houseData['城市'] = city
        houseData['区县'] = region
        houseData['抓取年份'] = 2020    # TODO
        houseData['抓取月份'] = month
        try:
            houseData['标题'] = decode_zujin(house.xpath(".//h3/a/b/text()")[0], font)
            houseData['标题url'] = house.xpath(".//h3/a/@href")[0]
        except:
            houseData['标题'] = ''
            houseData['标题url'] = ''

        info = decode_zujin(house.xpath("string(.//p[@class='details-item tag'])").replace(" ", ""), font)
        houseData['户型'] = "".join(re.findall("\d+室\d?厅", info))
        houseData['面积'] = "".join(re.findall("(\d+\.?\d+)平米", info))
        houseData['楼层'] = "".join(["".join(re.findall("(.*\))", i)) for i in info.split("|") if "层" in i])
        houseData['小区'] = "".join(house.xpath(".//address[@class='details-item']/a/text()"))
        houseData['小区url'] = "".join(house.xpath(".//address[@class='details-item']/a/@href"))
        houseData['地址'] = "".join(house.xpath(".//address[@class='details-item']/text()")).strip()
        houseData['数据来源'] = '安居客'

        cate = []
        for i in house.xpath(".//p[@class='details-item bot-tag']//span/text()"):
            if '整租' in i or '合租' in i:
                houseData['类型'] = i
                continue
            elif [j for j in ['东', '南', '西', '北'] if j in i]:
                houseData['朝向'] = i
                continue
            else:
                cate.append(i)
        houseData['特点'] = "|".join(cate)
        houseData['租金'] = str(decode_zujin("".join(house.xpath(".//div[@class='zu-side']//b/text()")), font))
        dataAll.append(houseData)

    next_url = html.xpath("//div[@class='multi-page']/a[@class='aNxt']/@href")
    if next_url:
        next_url = next_url[0]
        print("城市: %s, 区县: %s, 当前ip: %s, 数据: %s,下一页: %s " % (city, region, proxy, len(dataAll), next_url))
        get_price_district_html(next_url, city, region, extent=extent, dataAll=dataAll)


# 查看城市行政区是否有50页数据
def get_district_html(url, city, region):
    html, response, _ = get_html(url=url)
    if not response:
        print("没有response: , 退出")
        return

    # 没有数据, 防止推荐数据
    if "没有找到" in ''.join(html.xpath("//div[@id='zu-comhead']/p/text()")):
        print('很抱歉, %s: 没有找到房源' % region)
        save_region(city, region)
        return

    # 有数据
    house_div = html.xpath("//div[@class='zu-itemmod']")
    dataAll = []
    if len(house_div) == 0:
        # 第50页没有数据
        # 当前页从1开始索引抓取页面
        url_one = url[:-4]
        get_price_district_html(url_one, city, region, dataAll=dataAll)
        if len(dataAll) == 0:
            with open("grab_region.txt", 'a', encoding="utf-8") as fp:
                fp.writelines((city, "-", region))
    else:
        # 有数据, 获取价格区间,抓取页面
        price_extent = get_price_map_dict(url=url)  # 生成价格区间
        print("生成价格区间: ", price_extent)

        if not price_extent:
            return
        for extent, price_url in price_extent.items():
            print('城市: %s, 行政区: %s, 当前价格区间: %s' % (city, region, extent))
            get_price_district_html(price_url, city, region, extent, dataAll=dataAll)  # 抓取每一页页面信息

    if len(dataAll) == 0:
        print("城市: ", city, region, "没有数据:", len(dataAll))
        try:
            save_region(city, region)
        except:
            pass
        return

    print("城市: ", city, region, "开始保存数据......", len(dataAll))
    save_data(data=dataAll, city=city, region=region)
    del dataAll


if __name__ == '__main__':
    # TODO, 当前月份,
    month = 12

    # 删除上月记录
    delete_log_dir()

    pool = ThreadPoolExecutor(10)
    with open("city_dist.json", 'r', encoding='utf-8') as fp:
        city_dist = json.loads(fp.read())

    for city, districts in city_dist.items():
        print(city, districts)

        l = []
        for district, distUrl in districts.items():
            if '周边' in district: continue
            url = distUrl + "p50/"
            if check(city, district):
                print(city, district, '已经存在')
                continue
            print(city, district, url)
            done = pool.submit(get_district_html, url, city, district)
            l.append(done)
        [obj.result() for obj in l]

        print('等待10s 继续进行: ', city)
        time.sleep(1)
    pool.shutdown()
