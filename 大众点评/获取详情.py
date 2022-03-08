# encoding=utf8
from urllib import parse
import pymongo
from fontTools.ttLib import TTFont
from concurrent.futures import ThreadPoolExecutor
from 获取位置 import getpos, getmpos
from 获取评分 import getscore
from fake_useragent import UserAgent
from scrapy import Selector
import hashlib
import random
import time
import re
import os
import datetime
from lxml import etree
from mobile详情 import getmdetail
import requests
from fake_useragent import UserAgent
from config import typedict, MONGODB_CONFIG, fheaders, headers, citylist, get_proxy, gethtml, cookie_header, mycookie
from sendsms import sendsms
import warnings

warnings.filterwarnings("ignore")

pagebase = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['大众点评']['深圳_列表页链接_202109']
info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['大众点评']['深圳_数据_202109']
hasurl = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['大众点评']['深圳_去重_202109']
cookie_data = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['大众点评']['cookie数据']
words = '1234567890店中美家馆小车大市公酒行国品发电金心业商司超生装园场食有新限天面工服海华水房饰城乐汽香部利子老艺花专东肉菜学福饭人百餐茶务通味所山区门药银农龙停尚安广鑫一容动南具源兴鲜记时机烤文康信果阳理锅宝达地儿衣特产西批坊州牛佳化五米修爱北养卖建材三会鸡室红站德王光名丽油院堂烧江社合星货型村自科快便日民营和活童明器烟育宾精屋经居庄石顺林尔县手厅销用好客火雅盛体旅之鞋辣作粉包楼校鱼平彩上吧保永万物教吃设医正造丰健点汤网庆技斯洗料配汇木缘加麻联卫川泰色世方寓风幼羊烫来高厂兰阿贝皮全女拉成云维贸道术运都口博河瑞宏京际路祥青镇厨培力惠连马鸿钢训影甲助窗布富牌头四多妆吉苑沙恒隆春干饼氏里二管诚制售嘉长轩杂副清计黄讯太鸭号街交与叉附近层旁对巷栋环省桥湖段乡厦府铺内侧元购前幢滨处向座下澩凤港开关景泉塘放昌线湾政步宁解白田町溪十八古双胜本单同九迎第台玉锦底后七斜期武岭松角纪朝峰六振珠局岗洲横边济井办汉代临弄团外塔杨铁浦字年岛陵原梅进荣友虹央桂沿事津凯莲丁秀柳集紫旗张谷的是不了很还个也这我就在以可到错没去过感次要比觉看得说常真们但最喜哈么别位能较境非为欢然他挺着价那意种想出员两推做排实分间甜度起满给热完格荐喝等其再几只现朋候样直而买于般豆量选奶打每评少算又因情找些份置适什蛋师气你姐棒试总定啊足级整带虾如态且尝主话强当更板知己无酸让入啦式笑赞片酱差像提队走嫩才刚午接重串回晚微周值费性桌拍跟块调糕'


def get_html(url, headers):
    try:
        rep = requests.get(url, headers=fheaders)
    except Exception as e:
        print(e)
    text = rep.text
    html = re.sub('\s', '', text)  # 去掉非字符数据
    return html


def rans(num):
    s = ['a', 'b', 'c', 'd', 'e', 'f', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    x = ''
    for i in range(num):
        x += random.choice(s)
    return x


def getheaders():
    s = ['a', 'b', 'c', 'd', 'e', 'f', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    cuid1 = '179e'
    for i in range(8):
        cuid1 += random.choice(s)
    cuid2 = '0'
    for i in range(13):
        cuid2 += random.choice(s)
    cuid3 = 'f'
    for i in range(6):
        cuid3 += random.choice(s)
    cuid4 = '1fa400'
    cuid5 = cuid1
    cuid = cuid1 + '-' + cuid2 + '-' + cuid3 + '-' + cuid4 + '-' + cuid5
    headers = {
        'Connection': 'keep-alive',
        'Cookie': f'_lxsdk_cuid={cuid}; _lxsdk=179e9{rans(5)}91-06ce{rans(10)}-68151f7a-1fa400-179e{rans(7)}c8; _hc.v=f50464d5-{rans(4)}-07d4-fad0-7f7d{rans(5)}c25.{str(int(time.time()))}; Hm_lvt_602b80cf8079ae659{rans(10)}940e7={str(int(time.time()))}; Hm_lpvt_602b80cf8079ae65{rans(10)}3940e7={str(int(time.time()))}; _lxsdk_s=179ea{rans(6)}-7a0-{rans(3)}-68c%7C%7C3',
        'Host': 'www.dianping.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        # 'User-Agent': UserAgent().chrome
    }
    return headers


def getfont(cssurl, url):
    while True:
        css_url = cssurl
        # 获取字体文件链接的网页数据
        try:
            font_html = get_html(css_url, headers=headers)
        except:
            print('获取css文件失败')
            continue
        # 正则表达式获取 字体信息列表
        font_list = re.findall(r'@font-face{(.*?)}', font_html)

        # 获取使用到的字体及其链接
        font_dics = {}
        for font in font_list:
            # 正则表达式获取字体文件名称
            font_name = re.findall(r'font-family:"PingFangSC-Regular-(.*?)"', font)[0]
            # 正则表达式获取字体文件对应链接
            font_dics[font_name] = 'http:' + re.findall(r',url\("(.*?)"\);', font)[0]
        for key in font_dics.keys():
            while True:
                # woff = requests.get(font_dics[key], headers=headers).content
                try:
                    r = requests.get(url=font_dics[key], headers=fheaders)
                except:
                    print('获取font文件失败')
                    continue
                if r.status_code == 200:
                    woff = r.content
                    with open(f'{key}{url}.woff', 'wb')as f:
                        f.write(woff)
                break
        # 修改三类字体映射关系
        real_list = {}
        for key in font_dics.keys():
            font_data = TTFont(f'{key}{url}.woff')
            os.remove(f'{key}{url}.woff')
            uni_list = font_data.getGlyphOrder()[2:]
            real_list[key] = ['&#x' + uni[3:] for uni in uni_list]
        words = '1234567890店中美家馆小车大市公酒行国品发电金心业商司超生装园场食有新限天面工服海华水房饰城乐汽香部利子老艺花专东肉菜学福饭人百餐茶务通味所山区门药银农龙停尚安广鑫一容动南具源兴鲜记时机烤文康信果阳理锅宝达地儿衣特产西批坊州牛佳化五米修爱北养卖建材三会鸡室红站德王光名丽油院堂烧江社合星货型村自科快便日民营和活童明器烟育宾精屋经居庄石顺林尔县手厅销用好客火雅盛体旅之鞋辣作粉包楼校鱼平彩上吧保永万物教吃设医正造丰健点汤网庆技斯洗料配汇木缘加麻联卫川泰色世方寓风幼羊烫来高厂兰阿贝皮全女拉成云维贸道术运都口博河瑞宏京际路祥青镇厨培力惠连马鸿钢训影甲助窗布富牌头四多妆吉苑沙恒隆春干饼氏里二管诚制售嘉长轩杂副清计黄讯太鸭号街交与叉附近层旁对巷栋环省桥湖段乡厦府铺内侧元购前幢滨处向座下澩凤港开关景泉塘放昌线湾政步宁解白田町溪十八古双胜本单同九迎第台玉锦底后七斜期武岭松角纪朝峰六振珠局岗洲横边济井办汉代临弄团外塔杨铁浦字年岛陵原梅进荣友虹央桂沿事津凯莲丁秀柳集紫旗张谷的是不了很还个也这我就在以可到错没去过感次要比觉看得说常真们但最喜哈么别位能较境非为欢然他挺着价那意种想出员两推做排实分间甜度起满给热完格荐喝等其再几只现朋候样直而买于般豆量选奶打每评少算又因情找些份置适什蛋师气你姐棒试总定啊足级整带虾如态且尝主话强当更板知己无酸让入啦式笑赞片酱差像提队走嫩才刚午接重串回晚微周值费性桌拍跟块调糕'
        return words, real_list


def daddr(text, real_list):
    def faddr(t):  # 地址
        x = t.group(1)
        x1 = re.findall('(&#x.*?;)', x)[0]
        x = x.replace(x1, x1[:-1])
        for j in range(len(real_list['address'])):
            x = x.replace(real_list['address'][j], words[j])
        return x

    retext = re.compile('(<svgmtsi class="address">.*?;</svgmtsi>)')
    newtext = retext.sub(faddr, text)
    return newtext


def dnum(text, real_list):
    def fnum(t):  # 解密shopnum加密
        x = t.group(1)
        x1 = re.findall('(&#x.*?;)', x)[0]
        x = x.replace(x1, x1[:-1])
        for j in range(10):
            x = x.replace(real_list['shopNum'][j], words[j])
        return x

    retext = re.compile('(<svgmtsi class="shopNum">.*?;</svgmtsi>)')
    newtext = retext.sub(fnum, text)
    return newtext


def dtag(text, real_list):
    def ftag(t):
        x = t.group(1)
        x1 = re.findall('(&#x.*?;)', x)[0]
        x = x.replace(x1, x1[:-1])
        for j in range(len(real_list['tagName'])):
            # str=re.findall('(&#x.*?);',t)[0]
            x = x.replace(real_list['tagName'][j], words[j])
        return x

    retext = re.compile('(<svgmtsi class="tagName">.*?;</svgmtsi>)')
    newtext = retext.sub(ftag, text)
    return newtext


def datanum(text, real_list):
    def ftag(t):
        x = t.group(1)
        x1 = re.findall('(&#x.*?;)', x)[0]
        x = x.replace(x1, x1[:-1])
        for j in range(10):
            x = x.replace(real_list['num'][j], words[j])
        return x

    retext = re.compile('(<d class="num">.*?;</d>)')
    newtext = retext.sub(ftag, text)
    return newtext


def dec(text, real_list, cla):
    def ftag(t):
        x = t.group(1)
        x1 = re.findall('(&#x.*?;)', x)[0]
        x = x.replace(x1, x1[:-1])
        for j in range(len(real_list[cla])):
            x = x.replace(real_list[cla][j], words[j])
        return x

    retext = re.compile('(<svgmtsi class="%s">.*?;</svgmtsi>)' % cla)
    newtext = retext.sub(ftag, text)
    return newtext


def getdata(url, type, cityid, cityname):
    print(url)
    if hasurl.find_one({'列表url': url}):
        print('该页已爬取')
        return
    while True:
        time.sleep(5)
        # proxy = get_proxy()
        Cookinfo = cookie_data.find_one()
        Cookies = Cookinfo['Cookie'].replace(' ', '')
        Cooknum = Cookinfo['号码']
        headers = cookie_header()
        headers['Cookie'] = Cookies
        # headers['Cookie']='_lxsdk_cuid=179c01ab88cc8-0df2f0b9256ac1-2363163-1fa400-179c01ab88cc8; _hc.v=fb783b09-adc2-78df-f8a5-7b53f530416c.1622425648; s_ViewType=10; _dp.ac.v=19b24d59-781c-4e11-94fc-d848cfb75d8f; ctu=21fd3f032ee980c9b98bee37cc18e7671d5ddb8684865c57d85b840ce1fe7fff; aburl=1; ua=dpuser_1966568564; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1622711914; uuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; iuuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _lxsdk=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _ga=GA1.2.1975686433.1622713531; switchcityflashtoast=1; default_ab=citylist%3AA%3A1%7Cshop%3AA%3A11%7Cindex%3AA%3A3%7CshopList%3AA%3A5%7Cmap%3AA%3A1; cy=219; cye=dongguan; fspop=test; m_flash2=1; cityid=7; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1628644029,1628731677,1628818276,1629077694; dper=989da530f9ae3713022e170efc199d425e7e60601d76eed2cc918ecc5d334a55b5415495914b1f8da18932ccae18f7a705e95ff6f0065ec6d99f871298db8ce1c264c082b16b2c2ea154f8cf4fc4a79aa6fc4fa1d1281e3553e0b47164a3a6ae; ll=7fd06e815b796be3df069dec7836c3df; uamo=18523046785; dplet=19cd5750f538a8ac4a9ac5232809ef3d; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1629089140; _lxsdk_s=17b4d43aa34-b76-0f9-308%7C%7C103'
        # proxies = {
        #     "https": proxy,
        #     "http": proxy,
        # }
        try:
            # r = requests.get(url=url,proxies=proxies, headers=getheaders())
            r = requests.get(url=url, headers=headers, verify=False)
            # r = requests.get(url=url,proxies=proxies,headers=cookie_header())
        except Exception as e:
            print(e)
            errorlog(e, time.strftime('%m-%d %H:%M:%S', time.localtime(time.time())), Cooknum)
            continue
        # 如果状态码为200显示正常
        if r.status_code == 503:
            print(503, Cookies)
            errorlog('503', time.strftime('%m-%d %H:%M:%S', time.localtime(time.time())), Cooknum)
            return
        if r.status_code == 404:
            print(404, Cookies)
            errorlog('404', time.strftime('%m-%d %H:%M:%S', time.localtime(time.time())), Cooknum)

            continue
        if r.status_code == 403:
            print(403, Cookies)
            errorlog('403', time.strftime('%m-%d %H:%M:%S', time.localtime(time.time())), Cooknum)
            continue
        if r.status_code == 200:
            # print("访问成功")
            # text = r.text.encode("gbk", "ignore").decode("gbk", "ignore")  # 解决报错双重严格限制
            r.encoding = 'utf8'
            text = r.text
        else:
            print(r.status_code, Cookies)
            errorlog('r.status_code', time.strftime('%m-%d %H:%M:%S', time.localtime(time.time())), Cooknum)
            continue
        if '页面不存在' in r.text:
            print('页面不存在', url)
            errorlog('页面不存在', time.strftime('%m-%d %H:%M:%S', time.localtime(time.time())), Cooknum)
            continue
        if '没有找到符合条件的商户' in r.text:
            print('没有找到符合条件的商户')
            return
        if len(r.text) < 100: continue
        try:
            css = re.findall('href="//s3plus.meituan.net(.*?).css">', text.replace(' ', ''))[0]
        except:
            print('获取css失败', len(r.text))
            return
        print('获取列表成功')
        cssurl = 'http://s3plus.meituan.net' + css + '.css'
        'http://www.dianping.com/beijing/ch30/r1926'
        rname = url[24:].replace('/', '')
        words, real_list = getfont(cssurl, rname)
        newtext = daddr(text, real_list)
        newtext = dnum(newtext, real_list)
        newtext = dtag(newtext, real_list)
        html = etree.HTML(newtext)
        box = html.xpath('//*[@id="shop-all-list"]/ul/li')
        l = []
        for i in box:
            item = {}
            item['标题'] = i.xpath('.//h4/text()')[0]
            item['城市'] = cityname
            # for k,v in typedict.items():
            #     if type == v:
            #         item['大类'] = k
            #         break
            item['大类'] = list(typedict.keys())[list(typedict.values()).index(type)]
            item['标题url'] = i.xpath('./div[1]/a/@href')[0]
            try:
                item['评分'] = i.xpath('./div[2]/div[2]/div/div[2]/text()')[0]
            except:
                item['评分'] = ''
            item['评论数量'] = i.xpath('string(./div[2]/div[2]/a[1]/b)')
            item['类型'] = i.xpath('string(./div[2]/div[3]/a[1]/span)')
            item['标签'] = i.xpath('string(./div[2]/div[3]/a[2]/span)')
            item['平均消费'] = i.xpath('string(./div[2]/div[2]/a[2])').replace('\n', '').replace(' ', '')
            item['地址'] = i.xpath('string(./div[2]/div[3]/span)')

            # shopId=item['标题url'].split('/')[-1]
            # mainRegionIdtxt=i.xpath('./div[2]/div[3]/a[1]/@href')[0].split('/')[-1]
            # mainRegionId=re.findall('(\d+)',mainRegionIdtxt)[0]
            # phtxt=getmdetail(shopId)
            # item['电话']=re.findall('"entity":"(.*?)"',phtxt)
            # shop = getmpos(shopId)
            # k, v = getscore(shopId, cityid, mainRegionId)
            # if v:
            #     for i in range(len(v)):
            #         data = datanum(v[i], real_list).replace('<d class="num">', '').replace('</d>', '')
            #         item[k[i]] = data
            # # print(k,shopId,cityid,mainRegionId)
            # item['glng'] = shop['glng']
            # item['glat'] = shop['glat']
            # item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            # print(item)
            # getpagedata(item['标题url'], item,type)

            done = pool.submit(getpagedata, item['标题url'], item, type, cityid)
            l.append(done)
        [obj.result() for obj in l]
        # break
        hasurl.insert_one({'列表url': url})
        break


def getpagedata(url, item, type, cityid):
    for ii in range(100):
        proxy = get_proxy()
        proxies = {
            "https": proxy,
            "http": proxy,
        }
        try:
            r = requests.get(url, headers=getheaders(), proxies=proxies, timeout=5)
        except:
            print('getpage error')
            continue
        # r = gethtml(url)
        if r.status_code == 200:
            r.encoding = 'utf8'
            text = r.text
        else:
            print('获取页面失败', r.status_code)
            continue
        if '页面不存在' in r.text:
            print('页面不存在')
            # time.sleep(10)
            continue
        if '无效用户' in r.text:
            # print('无效用户')
            continue
        if '"status":2003' in r.text:
            # print('"status":2003')
            continue
        if len(r.text) < 100: continue
        if '大众点评网</title>' not in r.text: continue
        newtext = text.replace('&nbsp;', ',')
        try:
            css = re.findall('href="//s3plus.meituan.net(.*?).css">', text.replace(' ', ''))[0]
        except:
            return
        cssurl = 'http://s3plus.meituan.net' + css + '.css'
        shopId = item['标题url'].split('/')[-1]
        words, real_list = getfont(cssurl, shopId)

        for i in real_list.keys():  # review  dishname num  hours shopdesc
            if i in ['num']: continue
            newtext = dec(newtext, real_list, i)
        newtext = datanum(newtext, real_list)
        # print(newtext)
        html = etree.HTML(newtext)
        # item['营业时间'] = html.xpath('string(.//*[@id="basic-info"]/div[4]/p[1]/span[2])').replace(' ', '')
        try:
            item['营业时间'] = \
            re.findall('<spanclass="info-name">营业时间：</span><spanclass="item">(.*?)</span>', newtext.replace(' ', '')
                       .replace('\n', ''))[0].replace('<svgmtsiclass="shopdesc">', '').replace('<svgmtsiclass="hours">',
                                                                                               '').replace('</svgmtsi>',
                                                                                                           '')
        except:
            item['营业时间'] = ''
        item['电话'] = html.xpath('string(.//*[@id="basic-info"]/p)').replace(' ', '')
        item['各类评分'] = html.xpath('string(.//*[@id="comment_score"])').replace(' ', '')
        mainRegionId = re.findall('mainCategoryId:(\d+)', text)[0]
        mainCategoryId = re.findall('mainRegionId:(\d+)', text)[0]
        shopName = re.findall("shopName: ('.*?'),", text)[0]
        # print('开始获取pos')
        shop = getpos(shopId, cityid, mainRegionId, mainCategoryId, shopName)
        # print('开始获取评分')
        if not item['各类评分']:
            v = None
        else:
            k, v, item['评分'] = getscore(shopId, cityid, mainRegionId)
        if v:
            for i in range(len(v)):
                data = datanum(v[i], real_list).replace('<d class="num">', '').replace('</d>', '')
                item[k[i]] = data
        # print(k,shopId,cityid,mainRegionId)
        # print('开始获取电话')
        if '无添加' in item['电话']:
            print('没有号码')
            phtxt = ''
        else:
            phtxt = getmdetail(shopId)
            x = phtxt
        item['详细电话'] = ','.join(re.findall('"entity":"(.*?)"', phtxt))
        item['glng'] = shop['glng']
        item['glat'] = shop['glat']
        item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        try:
            if not info_base.find_one({'标题url': url}):
                info_base.insert_one(item)
            print(item)
        except Exception as e:
            print(e, url)
        # time.sleep(2)
        break


def errorlog(text, times, cookie):
    print('cookie错误')
    cookiecount[0] += 1
    if cookiecount[0] < 10:
        return
    print('cookie错误次数过多')
    cookiecount[0] = 0

    pagebase.update_one(page, {"$set": {'status': 0}})
    texts = text + ',' + times + ',' + str(cookie) + '\n'
    with open('errorlog.txt', 'a') as f:
        f.write(texts)
    cookiedata = cookie_data.find_one()
    cookie_data.update_one(cookiedata, {"$set": {'status': 0}})
    while True:
        time.sleep(20)
        if cookie_data.find_one({'status': 1}):
            return


if __name__ == '__main__':
    pool = ThreadPoolExecutor(15)
    pool2 = ThreadPoolExecutor(3)
    cookiecount = [0]
    # x=info_base.delete_many({})
    # print(x.deleted_count,'个文档已删除')

    while pagebase.find_one({'status': 0}):  # 状态0未抓取  -1正在抓取  1已抓取
        page = pagebase.find_one({'status': 0})
        pagebase.update_one(page, {"$set": {'status': -1}})
        print(page)
        page['status'] = -1
        l = []
        for i in range(1, int(page['pagenum']) + 1):
            # for i in range(1,2):
            if i == 1:
                url = page['url']
            else:
                url = page['url'] + 'p' + str(i)
            # getdata(url,page['type'])
            done = pool2.submit(getdata, url, page['type'], page['cityid'], page['cityname'])
            l.append(done)
        [obj.result() for obj in l]
        pagebase.update_one(page, {"$set": {'status': 1}})

