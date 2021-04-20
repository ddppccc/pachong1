# 该脚本获取城市的分区
import json
import re
import time
import requests
from lxml import etree
import os

""" 房天下 """
city_list=[
 '滁州',
 '马鞍山',
 '安庆',
 '蚌埠',
 '巢湖',
 '池州',
 '阜阳',
 '淮北',
 '淮南',
 '黄山',
 '六安',
 '宿州',
 '铜陵',
 '芜湖',
 '宣城',
 '亳州',
 '合肥',
 '澳门',
 '北京',
 '福州',
 '厦门',
 '龙岩',
 '南平',
 '宁德',
 '莆田',
 '泉州',
 '三明',
 '漳州',
 '兰州',
 '白银',
 '定西',
 '甘南',
 '嘉峪关',
 '金昌',
 '酒泉',
 '临夏',
 '陇南',
 '平凉',
 '庆阳',
 '天水',
 '武威',
 '张掖',
 '深圳',
 '东莞',
 '惠州',
 '广州',
 '佛山',
 '潮州',
 '河源',
 '江门',
 '揭阳',
 '茂名',
 '梅州',
 '清远',
 '汕头',
 '汕尾',
 '韶关',
 '阳江',
 '云浮',
 '湛江',
 '肇庆',
 '中山',
 '珠海',
 '北海',
 '南宁',
 '桂林',
 '百色',
 '崇左',
 '防城港',
 '贵港',
 '河池',
 '贺州',
 '来宾',
 '柳州',
 '钦州',
 '梧州',
 '玉林',
 '贵阳',
 '安顺',
 '毕节',
 '六盘水',
 '黔东南',
 '黔南',
 '黔西南',
 '铜仁',
 '遵义',
 # '海口',
 '三亚',
 # '白沙',
 # '保亭',
 # '昌江',
 # '澄迈',
 # '定安',
 '东方',
 # '乐东',
 # '临高',
 # '陵水',
 '琼海',
 # '琼中',
 # '屯昌',
 '万宁',
 '文昌',
 '五指山',
 '儋州',
 '石家庄',
 '保定',
 '沧州',
 '承德',
 '邯郸',
 '衡水',
 '廊坊',
 '秦皇岛',
 '唐山',
 '邢台',
 '张家口',
 '郑州',
 '洛阳',
 '开封',
 '安阳',
 '鹤壁',
 '济源',
 '焦作',
 '南阳',
 '平顶山',
 '三门峡',
 '商丘',
 '新乡',
 '信阳',
 '许昌',
 '周口',
 '驻马店',
 '漯河',
 '濮阳',
 '哈尔滨',
 '大庆',
 '大兴安岭',
 '鹤岗',
 '黑河',
 '鸡西',
 '佳木斯',
 '牡丹江',
 '七台河',
 '齐齐哈尔',
 '双鸭山',
 '绥化',
 '伊春',
 '武汉',
 '鄂州',
 '孝感',
 '仙桃',
 '黄冈',
 '黄石',
 '荆门',
 '荆州',
 '潜江',
 '神农架',
 '十堰',
 '随州',
 '天门',
 '咸宁',
 '襄阳',
 '宜昌',
 '恩施',
 '长沙',
 '张家界',
 '常德',
 '郴州',
 '衡阳',
 '怀化',
 '娄底',
 '邵阳',
 '湘潭',
 '湘西',
 '益阳',
 '永州',
 '岳阳',
 '株洲',
 '长春',
 '吉林',
 '白城',
 '白山',
 '辽源',
 '四平',
 '松原',
 '通化',
 '延边',
 '南京',
 '南通',
 '扬州',
 '镇江',
 '苏州',
 '无锡',
 '常州',
 '淮安',
 '连云港',
 '宿迁',
 '泰州',
 '徐州',
 '盐城',
 '南昌',
 '抚州',
 '赣州',
 '吉安',
 '景德镇',
 '九江',
 '萍乡',
 '上饶',
 '新余',
 '宜春',
 '鹰潭',
 '沈阳',
 '大连',
 '鞍山',
 '本溪',
 '朝阳',
 '丹东',
 '抚顺',
 '阜新',
 '葫芦岛',
 '锦州',
 '辽阳',
 '盘锦',
 '铁岭',
 '营口',
 '呼和浩特',
 '阿拉善盟',
 '巴彦淖尔',
 '包头',
 '赤峰',
 '鄂尔多斯',
 '呼伦贝尔',
 '通辽',
 '乌海',
 '乌兰察布',
 '锡林郭勒盟',
 '大兴安岭',
 '银川',
 '固原',
 '石嘴山',
 '吴忠',
 '中卫',
 '西宁',
 '果洛',
 '海北',
 '海东',
 '海南',
 '海西',
 '黄南',
 '玉树',
 '济南',
 '德州',
 '济宁',
 '青岛',
 '滨州',
 '东营',
 '菏泽',
 '莱芜',
 '聊城',
 '临沂',
 '日照',
 '泰安',
 '威海',
 '潍坊',
 '烟台',
 '枣庄',
 '淄博',
 '太原',
 '长治',
 '大同',
 '晋城',
 '晋中',
 '临汾',
 '吕梁',
 '朔州',
 '忻州',
 '阳泉',
 '运城',
 '西安',
 '咸阳',
 '安康',
 '宝鸡',
 '汉中',
 '商洛',
 '铜川',
 '渭南',
 '延安',
 '榆林',
 '上海',
 '成都',
 '绵阳',
 '阿坝州',
 '巴中',
 '达州',
 '德阳',
 '甘孜',
 '广安',
 '广元',
 '乐山',
 '凉山',
 '眉山',
 '南充',
 '内江',
 '攀枝花',
 '遂宁',
 '雅安',
 '宜宾',
 '资阳',
 '自贡',
 '泸州',
 # '台湾',
 '天津',
 '拉萨',
 '阿里',
 '昌都',
 '林芝',
 '那曲',
 '日喀则',
 '山南',
 '香港',
 '乌鲁木齐',
 '阿克苏',
 '阿拉尔',
 # '巴音郭楞',
 '博尔塔拉',
 '昌吉',
 '哈密',
 '和田',
 '喀什',
 '克拉玛依',
 '克孜勒苏',
 '石河子',
 '图木舒克',
 '吐鲁番',
 '五家渠',
 '伊犁',
 '昆明',
 '怒江',
 '普洱',
 '丽江',
 '保山',
 '楚雄',
 '大理',
 '德宏',
 '迪庆',
 '红河',
 '临沧',
 '曲靖',
 '文山',
 '西双版纳',
 '玉溪',
 '昭通',
 '杭州',
 '温州',
 '湖州',
 '嘉兴',
 '台州',
 '金华',
 '丽水',
 '宁波',
 '绍兴',
 '舟山',
 '衢州',
 '重庆']
with open(os.path.join(os.path.dirname(__file__), 'city_map.json'), 'r', encoding='utf-8') as f:
    old_city_map = json.load(f)
    city_map = {}
    for i in range(len(city_list)):
        city_map[city_list[i]] = old_city_map[city_list[i]]


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