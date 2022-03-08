from urllib import parse
import pymongo
from fontTools.ttLib import TTFont
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
from scrapy import Selector
import hashlib
import random
import time
import re
import datetime
from lxml import etree
import requests
from config import typedict,MONGODB_CONFIG,fheaders,headers,citylist


info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['大众点评']['二手房_数据_202105']
words = '1234567890店中美家馆小车大市公酒行国品发电金心业商司超生装园场食有新限天面工服海华水房饰城乐汽香部利子老艺花专东肉菜学福饭人百餐茶务通味所山区门药银农龙停尚安广鑫一容动南具源兴鲜记时机烤文康信果阳理锅宝达地儿衣特产西批坊州牛佳化五米修爱北养卖建材三会鸡室红站德王光名丽油院堂烧江社合星货型村自科快便日民营和活童明器烟育宾精屋经居庄石顺林尔县手厅销用好客火雅盛体旅之鞋辣作粉包楼校鱼平彩上吧保永万物教吃设医正造丰健点汤网庆技斯洗料配汇木缘加麻联卫川泰色世方寓风幼羊烫来高厂兰阿贝皮全女拉成云维贸道术运都口博河瑞宏京际路祥青镇厨培力惠连马鸿钢训影甲助窗布富牌头四多妆吉苑沙恒隆春干饼氏里二管诚制售嘉长轩杂副清计黄讯太鸭号街交与叉附近层旁对巷栋环省桥湖段乡厦府铺内侧元购前幢滨处向座下澩凤港开关景泉塘放昌线湾政步宁解白田町溪十八古双胜本单同九迎第台玉锦底后七斜期武岭松角纪朝峰六振珠局岗洲横边济井办汉代临弄团外塔杨铁浦字年岛陵原梅进荣友虹央桂沿事津凯莲丁秀柳集紫旗张谷的是不了很还个也这我就在以可到错没去过感次要比觉看得说常真们但最喜哈么别位能较境非为欢然他挺着价那意种想出员两推做排实分间甜度起满给热完格荐喝等其再几只现朋候样直而买于般豆量选奶打每评少算又因情找些份置适什蛋师气你姐棒试总定啊足级整带虾如态且尝主话强当更板知己无酸让入啦式笑赞片酱差像提队走嫩才刚午接重串回晚微周值费性桌拍跟块调糕'

def get_html(url, headers):
    try:
        rep = requests.get(url, headers=fheaders)
    except Exception as e:
        print(e)
    text = rep.text
    html = re.sub('\s', '', text)  # 去掉非字符数据
    return html
def getfont(cssurl):
    css_url = cssurl
    # 获取字体文件链接的网页数据
    font_html = get_html(css_url, headers)
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
        # woff = requests.get(font_dics[key], headers=headers).content
        r = requests.get(url=font_dics[key], headers=fheaders)
        if r.status_code == 200:
            woff = r.content
        # print(woff)
        with open(f'{key}.woff', 'wb')as f:
            f.write(woff)
    # 修改三类字体映射关系
    real_list = {}
    for key in font_dics.keys():
        # 打开本地字体文件
        font_data = TTFont(f'{key}.woff')
        # font_data.saveXML('shopNum.xml')
        # 获取全部编码，前2个非有用字符去掉
        uni_list = font_data.getGlyphOrder()[2:]
        # 请求数据中是 "" 对应 编码中为"uniF8A1",我们进行替换，以请求数据为准
        real_list[key] = ['&#x' + uni[3:] for uni in uni_list]
    # print(real_list)
    # 字符串
    words = '1234567890店中美家馆小车大市公酒行国品发电金心业商司超生装园场食有新限天面工服海华水房饰城乐汽香部利子老艺花专东肉菜学福饭人百餐茶务通味所山区门药银农龙停尚安广鑫一容动南具源兴鲜记时机烤文康信果阳理锅宝达地儿衣特产西批坊州牛佳化五米修爱北养卖建材三会鸡室红站德王光名丽油院堂烧江社合星货型村自科快便日民营和活童明器烟育宾精屋经居庄石顺林尔县手厅销用好客火雅盛体旅之鞋辣作粉包楼校鱼平彩上吧保永万物教吃设医正造丰健点汤网庆技斯洗料配汇木缘加麻联卫川泰色世方寓风幼羊烫来高厂兰阿贝皮全女拉成云维贸道术运都口博河瑞宏京际路祥青镇厨培力惠连马鸿钢训影甲助窗布富牌头四多妆吉苑沙恒隆春干饼氏里二管诚制售嘉长轩杂副清计黄讯太鸭号街交与叉附近层旁对巷栋环省桥湖段乡厦府铺内侧元购前幢滨处向座下澩凤港开关景泉塘放昌线湾政步宁解白田町溪十八古双胜本单同九迎第台玉锦底后七斜期武岭松角纪朝峰六振珠局岗洲横边济井办汉代临弄团外塔杨铁浦字年岛陵原梅进荣友虹央桂沿事津凯莲丁秀柳集紫旗张谷的是不了很还个也这我就在以可到错没去过感次要比觉看得说常真们但最喜哈么别位能较境非为欢然他挺着价那意种想出员两推做排实分间甜度起满给热完格荐喝等其再几只现朋候样直而买于般豆量选奶打每评少算又因情找些份置适什蛋师气你姐棒试总定啊足级整带虾如态且尝主话强当更板知己无酸让入啦式笑赞片酱差像提队走嫩才刚午接重串回晚微周值费性桌拍跟块调糕'
    return words,real_list

def get_proxy():
    try:
        return requests.get('http://192.168.1.131:5010/get/').json().get('proxy')
    except:
        num = 3
        while num:
            try:
                return requests.get('http://192.168.1.131:5010/get/').json().get('proxy')
            except:
                print('暂无ip，等待20秒')
                time.sleep(20)

                num -= 1
        print('暂无ip')
def gethtml(url):
    headers = {
        'Connection': 'keep-alive',
        'Host': 'www.dianping.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        # 'User-Agent':  UserAgent().chrome,
        # 'Cookie': 'fspop=test; cy=9; cye=chongqing; _lxsdk_cuid=179c01ab88cc8-0df2f0b9256ac1-2363163-1fa400-179c01ab88cc8; _lxsdk=179c01ab88cc8-0df2f0b9256ac1-2363163-1fa400-179c01ab88cc8; _hc.v=fb783b09-adc2-78df-f8a5-7b53f530416c.1622425648; s_ViewType=10; _dp.ac.v=19b24d59-781c-4e11-94fc-d848cfb75d8f; ctu=21fd3f032ee980c9b98bee37cc18e7671d5ddb8684865c57d85b840ce1fe7fff; aburl=1; cityid=9; default_ab=shopList%3AA%3A5; ua=dpuser_1966568564; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1622430936,1622599018,1622622578,1622684317; dper=989da530f9ae3713022e170efc199d424fbd595e54994bc85947fd9f29ed441d5ad1ab9e2e57880ec5c6d0064a0712390a38646ccaac0670ba2affafff2ddb2de5a6575b1004c83b5ae7f3395eba0ca6d9b132de2b248b53a54ceea5c6d51636; ll=7fd06e815b796be3df069dec7836c3df; uamo=18523046785; dplet=5f4edba1e07f6f53950ca9020d8c330d; _lxsdk_s=179cf85b559-dcb-2cd-df8%7C%7C262; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1622686321'
    }
    for i in range(100):
        proxies = {"http": get_proxy()}
        try:
            response = requests.get(url, headers=headers,proxies=proxies, timeout=10)
            encod = response.apparent_encoding
            if encod.upper() in ['GB2312', 'WINDOWS-1254']:
                encod = 'gbk'
            response.encoding = encod
            html = etree.HTML(response.text)
            if response.status_code ==200:
                return response
            print('获取页面失败',response.status_code, proxies)
        except Exception as e:
            print('get_html错误',proxies, e)
            time.sleep(2)
    return
def daddr(text,real_list):
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
def dnum(text,real_list):
    def fnum(t):                #解密shopnum加密
        x=t.group(1)
        x1=re.findall('(&#x.*?;)',x)[0]
        x=x.replace(x1,x1[:-1])
        for j in range(10):
            x =x.replace(real_list['shopNum'][j], words[j])
        return x
    retext=re.compile('(<svgmtsi class="shopNum">.*?;</svgmtsi>)')
    newtext=retext.sub(fnum,text)
    return newtext
def dtag(text,real_list):
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
def datanum(text,real_list):
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
def dec(text,real_list,cla):
    def ftag(t):
        x = t.group(1)
        x1 = re.findall('(&#x.*?;)', x)[0]
        x = x.replace(x1, x1[:-1])
        for j in range(len(real_list[cla])):
            x = x.replace(real_list[cla][j], words[j])
        return x
    retext = re.compile('(<svgmtsi class="%s">.*?;</svgmtsi>)'%cla)
    newtext = retext.sub(ftag, text)
    return newtext
def getdata(url,type):
    while True:
        time.sleep(5)
        r = requests.get(url=url, headers=headers)
        # 如果状态码为200显示正常
        if r.status_code == 200:
            # print("访问成功")
            # text = r.text.encode("gbk", "ignore").decode("gbk", "ignore")  # 解决报错双重严格限制
            r.encoding = 'utf8'
            text = r.text
        else:
            print(r.status_code)
            continue
        if '页面不存在' in r.text:
            print('页面不存在',url)
            continue
        if '没有找到符合条件的商户' in r.text:
            print('没有找到符合条件的商户')
            return
        css = re.findall('href="//s3plus.meituan.net(.*?).css">', text.replace(' ', ''))[0]
        cssurl = 'http://s3plus.meituan.net' + css + '.css'
        words, real_list = getfont(cssurl)
        newtext = daddr(text,real_list)
        newtext = dnum(newtext,real_list)
        newtext = dtag(newtext,real_list)
        html = etree.HTML(newtext)
        box = html.xpath('//*[@id="shop-all-list"]/ul/li')
        l=[]
        for i in box:
            item = {}
            item['标题'] = i.xpath('.//h4/text()')[0]
            item['标题url'] = i.xpath('./div[1]/a/@href')[0]
            try:
                item['评分'] = i.xpath('./div[2]/div[2]/div/div[2]/text()')[0]
            except:
                item['评分'] = ''
            item['类型'] = i.xpath('string(./div[2]/div[3]/a[1]/span)')
            item['标签'] = i.xpath('string(./div[2]/div[3]/a[2]/span)')
            item['平均消费'] = i.xpath('string(./div[2]/div[2]/a[2])').replace('\n', '').replace(' ', '')
            item['地址'] = i.xpath('string(./div[2]/div[3]/span)')
            # print(item)
            # getpagedata(item['标题url'], item,type)
            done = pool.submit(getpagedata,item['标题url'], item,type)
            l.append(done)
        [obj.result() for obj in l]
            # break
        break
def getpagedata(url,item,type):
    headers = {
        'Connection': 'keep-alive',
        'Host': 'www.dianping.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        # 'User-Agent':  UserAgent().chrome,
        # 'Cookie': 's_ViewType=10; _lxsdk_cuid=179d0b00c27c8-013205f9b94a1a-51361244-1fa400-179d0b00c27c8; _lxsdk=179d0b00c27c8-013205f9b94a1a-51361244-1fa400-179d0b00c27c8; _hc.v=e149a70e-039d-1da2-cc33-5281ba603bab.1622703869; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1622703870,1622773377; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1622773387; _lxsdk_s=179d4d4a554-7e0-df-fc5||32'
    }
    for ii in range(1000):
        s = requests.Session()
        proxies = {"http": get_proxy()}
        try:
            # r = s.get(url, headers=headers, proxies=proxies, timeout=10)
            r = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        except:continue
        # r = gethtml(url)
        if r.status_code == 200:
            r.encoding = 'utf8'
            text = r.text
        else:
            # print('获取页面失败',r.status_code)
            continue
        if '页面不存在' in r.text:
            # print('页面不存在')
            # time.sleep(10)
            continue
        if '无效用户' in r.text:continue
        if '"status":2003' in r.text:continue
        if '大众点评网</title>' not in r.text:continue
        newtext = text.replace('&nbsp;', ',')
        try:
            css = re.findall('href="//s3plus.meituan.net(.*?).css">', text.replace(' ', ''))[0]
            cssurl = 'http://s3plus.meituan.net' + css + '.css'
            words, real_list = getfont(cssurl)

            for i in real_list.keys():         #review  dishname num  hours shopdesc
                newtext = dec(newtext, real_list,i)
            newtext = datanum(newtext, real_list)
        except:
            pass
        # print(newtext)
        html = etree.HTML(newtext)
        if type in ['ch75']:
            try:
                item['电话']=re.findall('<span class="item J-phone-hide" data-phone="(.*?)">',newtext)[0]
            except:
                item['电话'] = '暂无'
            item['效果']=re.findall('<span class="item">效果：(.*?)</span>',newtext)[0]
            item['师资']=re.findall('<span class="item">师资：(.*?)</span>',newtext)[0]
            item['环境']=re.findall('<span class="item">环境：(.*?)</span>',newtext)[0]
        elif type in ['ch50']:
            try:
                item['电话'] = re.findall('<span class="item" itemprop="tel">(.*?)</span>',newtext)[0]
            except:
                item['电话'] = '无添加'
            item['营业时间'] = html.xpath('//*[@id="basic-info"]/div[3]/p[1]/span[2]/text()')[0].replace('\n','').replace(' ','')
            item['效果'] = re.findall('<span class="item">效果：(.*?)</span>',newtext)[0]
            item['环境'] = re.findall('<span class="item">环境：(.*?)</span>',newtext)[0]
            item['服务'] = re.findall('<span class="item">服务：(.*?)</span>',newtext)[0]
        else:
            item['营业时间'] = html.xpath('string(.//*[@id="basic-info"]/div[4]/p[1]/span[2])').replace(' ', '')
            item['电话'] = html.xpath('string(.//*[@id="basic-info"]/p)').replace(' ', '')
            item['各类评分'] = html.xpath('string(.//*[@id="comment_score"])').replace(' ', '')
            item['mainCategoryId']=re.findall('mainCategoryId:(\d+)',text)[0]
            item['mainRegionId']=re.findall('mainRegionId:(\d+)',text)[0]
            # item['shopName']=re.findall("shopName: ('.*?'),",text)[0]
        try:
            print(item)
        except Exception as e:
            print(e,url)
        # getpos(s,proxies,shopId,mainRegionId, mainCategoryId, shopName)
        # time.sleep(2)
        break
def getpos(s,proxies,shopId,mainRegionId,mainCategoryId,shopName):
    while True:
        url='http://www.dianping.com/ajax/json/shopDynamic/shopAside'
        # mainCategoryId=2754                          #分类id
        # mainRegionId=1615                            #地区id
        # shopId='H9ShAwbAd1p1BtEr'
        shopCityId=9
        shopType=30
        cityId=9
        data={
            'shopId': shopId,
            'cityId': cityId,
            # 'shopName': 'CDP < e class ="address" > &  # xe76e;</e><e class="address">&#xf684;</e>搜证探案<e class="address">&#xe000;</e>',
            'shopName': shopName,
            'power': 5,
            'mainCategoryId': mainCategoryId,
            'shopType': shopType,
            'mainRegionId': mainRegionId,
            'cityEnName': 'chongqing',
            'shopCityId': shopCityId,
            '_token': 'eJxVj92OokAQhd + lbyXS3QKKyVwgjC4KjkADw07mQpBtUH6lGZDNvvu2yc7FJpXUqa / qpKp + g7t5AWsEIZSQAL7SO1gDNIdzBQiAdbyjYCxLEEMoK6oAkv8YwhgLIL4HBlh / IIgVAUEkfT6Ry8kHUjHkaAU / hW8tcY0lHs8pkw + BjLFmLYrDMMwv + blq8orOk7oUu6xuxAL1j4OeHpMf8hinxOJXAe4sydPJN2IBq8snuT0Jz + d / mX3XNn + Iu7qcVlyl + 5H4rWweiTZ0VuySZTgFzvEx2cgb3EccmO + 3yiZ5xLqoSTy / OFi + 1JvRnvSUXp1JH98GWiZEvo / RQsy7WN1NmbuItl5SFa1XyuMlmOXvZcPaUG7DW1NyfT7X + zANA + teUicktmhNkHbTSrU2tJfk3AtqhY3TilluZowk1hdBktnTSn5kI7W3RIP29XWxobddo / ys5NTXMmc6Gv4y1MWT5ZsFIyw92KK2r8qt5GxWsM03 + iHwtKw + mcmg7g / x7OJ / YecEpfaGNtqvzrhGy0TqtUuuGoHp + kXpnEvW1ZqjLV6L2Y6 + vIA / fwHaR6UH',
            'uuid': 'fb783b09 - adc2 - 78df - f8a5 - 7b53f530416c.1622425648',
            'platform': 1,
            'partner': 150,
            'optimusCode': 10,
            'originUrl': 'http: // www.dianping.com / shop / '+shopId

        }
        headers = {
            'Connection': 'keep-alive',
            'Host': 'www.dianping.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            # 'User-Agent':  UserAgent().chrome,
            'Cookie': 's_ViewType=10; _lxsdk_cuid=179d0b00c27c8-013205f9b94a1a-51361244-1fa400-179d0b00c27c8; _lxsdk=179d0b00c27c8-013205f9b94a1a-51361244-1fa400-179d0b00c27c8; _hc.v=e149a70e-039d-1da2-cc33-5281ba603bab.1622703869; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1622703870,1622773377; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1622773387; _lxsdk_s=179d4d4a554-7e0-df-fc5||32'
        }
        try:
            # proxies = {"http": get_proxy()}
            # rr=requests.get(url,params=data,headers=headers,timeout=10)
            # rr=s.get(url,params=data,headers=headers,timeout=10)
            time.sleep(1)
            rr=requests.get(url,params=data,headers=headers,timeout=10)
        except:
            time.sleep(5)
            continue
        if rr.status_code == 200:
            rr.encoding = 'utf8'
            text = rr.text
        else:
            print('获取页面失败', rr.status_code)
            time.sleep(5)
            continue
        if '请稍后再试' in rr.text:
            print('网络不给力')
            time.sleep(10)
            continue
        rr.encoding='utf8'
        print(rr.json()['shop']['glng'],rr.json()['shop']['glat'])
        break


pool = ThreadPoolExecutor(15)
with open('page.txt', 'r') as f:
    for i in range(10):
        data=f.readline().strip()
        if not data:continue
        type=data.split('@_@')[1]
        pagenum=data.split('@_@')[2]
        turl=data.split('@_@')[3]
        # print(pagenum)
        print(turl)
        for i in range(1,int(pagenum)+1):
            url=turl+'p'+str(i)
            getdata(url,type)





# url = 'http://www.dianping.com/chongqing/ch30/r1615p2'
# getdata(url)
# citylist=getcity()
# print(citylist)
# print(len(citylist))




# for i in typedict.values():
# # # for i in ['ch33954']:
#     url='http://www.dianping.com/chongqing/'+i
#     print(url)
#     getdata(url)
#     time.sleep(10)

# url='http://www.dianping.com/shop/G5UxcoekDWG4bd1c'
# getpagedata(url,{})


# citylist=getcity()

