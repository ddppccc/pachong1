import time
import requests
import pymongo

from lxml import etree
from config import get_proxy,get_ua,delete_proxy,statis_output, city_url
from capter_verify.captcha_run import AJK_Slide_Captcha
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
            retryWrites="false")['安居客二手房']['info']
has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['安居客二手房']['has_spider']


# city_url = {
#     '广州':'https://guangzhou.anjuke.com/sale/t17/',
#     '深圳':'https://shenzhen.anjuke.com/sale/t13/',
#     '北京':'https://beijing.anjuke.com/sale/t7/',
#     '成都':'https://chengdu.anjuke.com/sale/t22/',
#     '上海':'https://shanghai.anjuke.com/sale/t1/',
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
                print("出现滑动验证, 更改ip")
                number = -1
                continue
                # proixy = "https://" + proxy
                # try:
                #     message = AJK_Slide_Captcha(proixy).run()
                #     if message != '校验成功':
                #         break
                # except Exception as e:
                #     print("错误原因: ", e)
                #     continue

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
    has_spider_urlList = []
    for has_spider_url in has_spider.find():
        has_spider_urlList.append(has_spider_url['标题'])


    if url in has_spider_urlList:
        html, response, _ = get_html(url)
        next_page_url = html.xpath('string(//a[@class="next next-active"]/@href)')
        if next_page_url:
            print('该页数据已爬取，下一页')
            get_parseInfo(city, next_page_url)
        else:
            print('最后一页')
            return
    else:
        html, response, _ = get_html(url)
        li_list = html.xpath('//*[@id="__layout"]//div[@class="property"]//div[@class="property-content"]')
        for li in li_list:
            item = {}
            item['城市'] = city
            item['标题'] = li.xpath('string(.//div[@class="property-content-detail"]/div[@class="property-content-title"]/h3)').replace('\n','').strip()
            item['户型'] = li.xpath('string(.//div[@class="property-content-info"]/p[1])').replace('\n','').strip()
            item['面积'] = li.xpath('string(.//div[@class="property-content-info"]/p[2])').replace('\n','').strip()
            item['楼层'] = li.xpath('string(.//div[@class="property-content-info"]/p[4])').replace('\n','').strip()
            item['建筑年份'] = li.xpath('string(.//div[@class="property-content-info"]/p[5])').replace('\n','').strip()
            item['地址'] = li.xpath('string(.//p[@class="property-content-info-comm-address"])').replace('\n','').replace('\xa0','').replace(' ','').strip()
            item['标签'] = li.xpath('string(.//div[@class="property-content-info"]/span[@class="property-content-info-tag"])').replace('\n','').replace('\xa0','').replace(' ','').strip()
            item['总价'] = li.xpath('string(.//div[@class="property-price"]/p[1])')
            item['单价'] = li.xpath('string(.//div[@class="property-price"]/p[2])')
            item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            num.append(1)
            print(len(num))
            print(item)
            info_base.insert_one(item)
        has_spider.insert_one({'标题': url})

    next_page_url = html.xpath('string(//div[@class="pagination"]/a[@class="next next-active"]/@href)')
    if next_page_url:
        print('下一页')
        get_parseInfo(city, next_page_url)
    else:
        return


if __name__ == '__main__':
    num = []
    for item in city_url:
        key = item
        url = city_url[item]
        get_parseInfo(key,url+"/sale/")
        # statis_output('安居客_五城_{}_二手房.csv'.format(time.strftime("%Y-%m-%d", time.localtime())),
        #
        #               ['城市','标题','户型','面积','楼层','建筑年份','地址','标签','总价','单价'], info_base,key)

