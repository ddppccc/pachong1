import re
import time
import requests
import pymongo

from lxml import etree
from config import get_proxy,get_ua,delete_proxy,statis_output
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

def getCity_Url():
    response = requests.get('https://www.anjuke.com/sy-city.html', headers=headers, timeout=(5, 5))
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)
    lists=html.xpath('/html/body/div[3]/div/div[2]/ul/li/div/a')
    city_url={}
    for data in lists:
        city=data.xpath('./text()')[0]
        url=data.xpath('./@href')[0]
        city_url[city]=url
    return city_url

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
                print(403, "休息一分钟")
                time.sleep(60)
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
    try:
        new_url = html.xpath('//div[@id="glbNavigation"]/div/ul[@class="L_tabsnew"]/li[4]/a/@href')
        return new_url[0]
    except:
        return ""


if __name__ == '__main__':
    city_url = getCity_Url()
    for item in city_url:
        key = item
        # unuse_city = ['吉安', '达州', '鸡西', '陵水', '信阳', '泰州', '舟山', '周口', '赤峰', '湘西', '丽水', '威海', '普洱', '昆明', '晋中', '儋州', '岳阳', '日喀则', '保山', '长春', '澳门', '乐山', '固原', '宁波', '白山', '永州', '曲靖', '阿克苏', '黑河', '自贡', '景德镇', '齐齐哈尔', '锦州', '巴中', '武汉', '海南', '衢州', '石河子', '常德', '许昌', '合肥', '果洛', '铁岭', '怒江', '晋城', '大兴安岭', '屯昌', '石嘴山', '新余', '湘潭', '松原', '西双版纳', '常州', '通化', '丹东', '五家渠', '琼中', '嘉兴', '山南', '迪庆', '呼伦贝尔', '邵阳', '海东', '双鸭山', '银川', '潍坊', '临汾', '佳木斯', '温州', '葫芦岛', '大同', '朝阳', '泸州', '德宏', '娄底', '牡丹江', '抚州', '苏州', '林芝', '天门', '雅安', '大理', '鞍山', '营口', '张家界', '铜川', '文昌', '黄冈', '阿里', '济南', '本溪', '菏泽', '宜宾', '昌吉', '重庆', '吉林', '无锡', '乌鲁木齐', '鄂州', '南通', '吐鲁番', '昌都', '海西', '潜江', '绥化', '烟台', '和田', '长治', '渭南', '呼和浩特', '宿迁', '克拉玛依', '抚顺', '恩施', '保亭', '临沂', '广元', '遂宁', '眉山', '随州', '鹤岗', '榆林', '广安', '漯河', '宝鸡', '玉溪', '日照', '哈密', '萍乡', '孝感', '濮阳', '伊犁', '延安', '临沧', '咸宁', '辽阳', '莱芜', '博尔塔拉', '吴忠', '七台河', '德阳', '绍兴', '黄石', '中卫', '宜昌', '淮安', '金华', '新乡', '鹰潭', '定安', '乌海', '喀什', '怀化', '东方', '大庆', '滨州', '十堰', '襄阳', '朔州', '那曲', '徐州', '益阳', '沈阳', '天津', '聊城', '青岛', '文山', '楚雄', '延边', '绵阳', '荆州', '克孜勒苏', '商洛', '西宁', '包头', '伊春', '攀枝花', '神农架', '长沙', '衡阳', '运城', '九江', '湖州', '咸阳', '株洲', '盐城', '盘锦', '万宁', '汉中', '连云港', '大连', '南京', '黄南', '镇江', '宜春', '成都', '泰安', '太原', '资阳', '甘孜', '昭通', '乌兰察布', '荆门', '阜新', '安康', '西安', '红河', '琼海', '通辽', '赣州', '吕梁', '内江', '辽源', '忻州', '杭州', '东营', '上海', '凉山', '丽江', '哈尔滨', '台州', '香港', '南昌', '南充', '济宁', '驻马店', '拉萨', '扬州', '淄博', '图木舒克', '阳泉', '巴音郭楞', '阿坝', '台湾', '德州', '白城', '玉树', '枣庄', '仙桃', '四平', '上饶', '鄂尔多斯', '海北', '郴州', '阿拉尔']
        # if item not in unuse_city:
        #     continue
        url = city_url[item]
        new_url = get_zu_url(url)
        # print(new_url)
        # print(key,url)
        if new_url == "https://haiwai.anjuke.com" or (not new_url):
            continue
        get_parseInfo(key, new_url)
    print("已完成...")
    # statis_output('安居客_五城_{}_租房.csv'.format(time.strftime("%Y-%m-%d", time.localtime())),
    #
    #               ['城市','标题','标题url','户型','面积','楼层','小区','小区url','地址','数据来源','类型','朝向','特点','租金'], info_base)
