import re
import time
import requests
import pymongo

from lxml import etree
from config import get_proxy,get_ua,delete_proxy,statis_output, city_url
from capter_verify.captcha_run import AJK_Slide_Captcha
from zujin_descde import decode_zujin,get_font
from urllib import parse


MONGODB_CONFIG = {
   "host": "8.135.119.198",
   "port": "27017",
   "user": "hladmin",
   "password": parse.quote("Hlxkd3,dk3*3@"),
   "db": "dianping",
   "collections": "dianping_collections",
}

info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['安居客租房']['info']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['安居客租房']['has_spider']




# city_url = {
#     '广州':'https://gz.zu.anjuke.com/fangyuan/lx4/',
#     '深圳':'https://sz.zu.anjuke.com/fangyuan/lx4/',
#     '北京':'https://bj.zu.anjuke.com/fangyuan/lx4/',
#     '成都':'https://cd.zu.anjuke.com/fangyuan/lx4/',
#     '上海':'https://sh.zu.anjuke.com/fangyuan/lx4/',
#             }


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
                # response = requests.get(url, headers=headers,
                #                         proxies={"https": "https://{}".format(proxy)}, timeout=(2, 5))

                response = requests.get(url, headers=headers, timeout=(2, 5))
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


def get_parseInfo(city,url):
    while 1:
        try:
            html, response, _ = get_html(url)
            font = get_font(response.text)
            break
        except:
            continue

    has_spider_urlList = []
    for has_spider_url in has_spider.find():
        has_spider_urlList.append(has_spider_url['标题'])
    if url in has_spider_urlList:
        next_page_url = html.xpath('string(//div[@class="multi-page"]/a[@class="aNxt"]/@href)')
        if next_page_url:
            print('该页数据已爬取，下一页')
            get_parseInfo(city, next_page_url)
        else:
            print('最后一页')
            return
    else:
        house_div = html.xpath("//div[@class='zu-itemmod']")
        if len(house_div) == 0:
            return
        for house in house_div:
            item = {}
            item['城市'] = city
            try:
                item['标题'] = decode_zujin(house.xpath(".//h3/a/b/text()")[0], font)
                item['标题url'] = house.xpath(".//h3/a/@href")[0]
            except:
                item['标题'] = ''
                item['标题url'] = ''
            info = decode_zujin(house.xpath("string(.//p[@class='details-item tag'])").replace(" ", ""), font)
            item['户型'] = "".join(re.findall("\d+室\d?厅", info))
            item['面积'] = "".join(re.findall("(\d+\.?\d+)平米", info))
            item['楼层'] = "".join(["".join(re.findall("(.*\))", i)) for i in info.split("|") if "层" in i])
            item['小区'] = "".join(house.xpath(".//address[@class='details-item']/a/text()"))
            item['小区url'] = "".join(house.xpath(".//address[@class='details-item']/a/@href"))
            item['地址'] = "".join(house.xpath(".//address[@class='details-item']/text()")).strip()
            item['数据来源'] = '安居客'
            item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            cate = []
            for i in house.xpath(".//p[@class='details-item bot-tag']//span/text()"):
                if '整租' in i or '合租' in i:
                    item['类型'] = i
                    continue
                elif [j for j in ['东', '南', '西', '北'] if j in i]:
                    item['朝向'] = i
                    continue
                else:
                    cate.append(i)
            item['特点'] = "|".join(cate)
            item['租金'] = str(decode_zujin("".join(house.xpath(".//div[@class='zu-side']//b/text()")), font))


            print(item)
            info_base.insert_one(item)

        has_spider.insert_one({'标题':url})

    next_page_url = html.xpath('string(//div[@class="multi-page"]/a[@class="aNxt"]/@href)')
    if next_page_url:
        get_parseInfo(city,next_page_url)
    else:
        print('最后一页')
        return
def get_zu_url(index_url):
    html, response, _ = get_html(index_url)
    new_url=html.xpath('//div[@id="glbNavigation"]/div/ul[@class="L_tabsnew"]/li[4]/a/@href')
    return new_url[0]



if __name__ == '__main__':
    for item in city_url:
        key = item
        url = city_url[item]
        new_url=get_zu_url(url)
        # print(new_url)
        # print(key,url)
        get_parseInfo(key, new_url)
    # statis_output('安居客_五城_{}_租房.csv'.format(time.strftime("%Y-%m-%d", time.localtime())),
    #
    #               ['城市','标题','标题url','户型','面积','楼层','小区','小区url','地址','数据来源','类型','朝向','特点','租金'], info_base)
