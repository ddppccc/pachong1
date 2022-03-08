# encoding=utf8
from urllib import parse
import pymongo
from fontTools.ttLib import TTFont
from concurrent.futures import ThreadPoolExecutor
from 获取位置 import getpos
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
import requests
from config import typedict,MONGODB_CONFIG,fheaders,headers,citylist,get_proxy,gethtml,getheaders


pagebase = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['大众点评']['美食_列表页链接_202106']
# info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
#             MONGODB_CONFIG['user'],
#             MONGODB_CONFIG['password'],
#             MONGODB_CONFIG['host'],
#             MONGODB_CONFIG['port']),
#             retryWrites="false")['大众点评']['休闲娱乐_数据_202106']
# hasurl = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
#             MONGODB_CONFIG['user'],
#             MONGODB_CONFIG['password'],
#             MONGODB_CONFIG['host'],
#             MONGODB_CONFIG['port']),
#             retryWrites="false")['大众点评']['休闲娱乐_去重_202106']
words = '1234567890店中美家馆小车大市公酒行国品发电金心业商司超生装园场食有新限天面工服海华水房饰城乐汽香部利子老艺花专东肉菜学福饭人百餐茶务通味所山区门药银农龙停尚安广鑫一容动南具源兴鲜记时机烤文康信果阳理锅宝达地儿衣特产西批坊州牛佳化五米修爱北养卖建材三会鸡室红站德王光名丽油院堂烧江社合星货型村自科快便日民营和活童明器烟育宾精屋经居庄石顺林尔县手厅销用好客火雅盛体旅之鞋辣作粉包楼校鱼平彩上吧保永万物教吃设医正造丰健点汤网庆技斯洗料配汇木缘加麻联卫川泰色世方寓风幼羊烫来高厂兰阿贝皮全女拉成云维贸道术运都口博河瑞宏京际路祥青镇厨培力惠连马鸿钢训影甲助窗布富牌头四多妆吉苑沙恒隆春干饼氏里二管诚制售嘉长轩杂副清计黄讯太鸭号街交与叉附近层旁对巷栋环省桥湖段乡厦府铺内侧元购前幢滨处向座下澩凤港开关景泉塘放昌线湾政步宁解白田町溪十八古双胜本单同九迎第台玉锦底后七斜期武岭松角纪朝峰六振珠局岗洲横边济井办汉代临弄团外塔杨铁浦字年岛陵原梅进荣友虹央桂沿事津凯莲丁秀柳集紫旗张谷的是不了很还个也这我就在以可到错没去过感次要比觉看得说常真们但最喜哈么别位能较境非为欢然他挺着价那意种想出员两推做排实分间甜度起满给热完格荐喝等其再几只现朋候样直而买于般豆量选奶打每评少算又因情找些份置适什蛋师气你姐棒试总定啊足级整带虾如态且尝主话强当更板知己无酸让入啦式笑赞片酱差像提队走嫩才刚午接重串回晚微周值费性桌拍跟块调糕'

def get_html(url, headers):
    try:
        rep = requests.get(url, headers=fheaders)
    except Exception as e:
        print(e)
    text = rep.text
    html = re.sub('\s', '', text)  # 去掉非字符数据
    return html

def getfont(cssurl,url):
    while True:
        css_url = cssurl
        # 获取字体文件链接的网页数据
        try:
            font_html = get_html(css_url,headers=headers)
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
        return words,real_list


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
def getdata(url,type,cityid):
    print(url)
    # if hasurl.find_one({'列表url':url}):
    #     print('该页已爬取')
    #     return
    for i in range(50):
        # time.sleep(5)
        proxy=get_proxy()
        # proxy='116.117.134.135:80'
        proxies = {"http": 'http://'+proxy,"https": 'https://'+proxy}
        try:
            # r = requests.get(url=url, headers=getheaders(),proxies=proxies,timeout=5)
            r = requests.get(url=url, headers=headers)
        except:continue
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
            # print('页面不存在',url)
            continue
        if '没有找到符合条件的商户' in r.text:
            print('没有找到符合条件的商户')
            return
        css = re.findall('href="//s3plus.meituan.net(.*?).css">', text.replace(' ', ''))[0]
        cssurl = 'http://s3plus.meituan.net' + css + '.css'
        'http://www.dianping.com/beijing/ch30/r1926'
        rname=url[24:].replace('/','')
        words, real_list = getfont(cssurl,rname)
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
            item['评论数量'] = i.xpath('string(./div[2]/div[2]/a[1]/b)')
            item['类型'] = i.xpath('string(./div[2]/div[3]/a[1]/span)')
            item['标签'] = i.xpath('string(./div[2]/div[3]/a[2]/span)')
            item['平均消费'] = i.xpath('string(./div[2]/div[2]/a[2])').replace('\n', '').replace(' ', '')
            item['地址'] = i.xpath('string(./div[2]/div[3]/span)')
            print(item)
            # getpagedata(item['标题url'], item,type)
            # done = pool.submit(getpagedata,item['标题url'], item,type,cityid)
            # l.append(done)
        # [obj.result() for obj in l]
            # break
        # hasurl.insert_one({'列表url': url})
        break
def getpagedata(url,item,type,cityid):
    for ii in range(1000):
        # proxies = {"http": get_proxy()}
        proxy = get_proxy()
        # proxy='111.202.83.35:80'
        proxies = {"http": 'http://'+proxy,"https": 'https://'+proxy}
        try:
            r = requests.get(url, headers=getheaders(), proxies=proxies, timeout=5)
            r.encoding = 'utf8'
        except:
            # print('getpage error')
            continue
        # r = gethtml(url)
        if r.status_code == 200:
            text = r.text
        else:
            # print('获取页面失败',r.status_code)
            continue
        if '页面不存在' in r.text:
            # print('页面不存在')
            # time.sleep(10)
            continue
        if '无效用户' in r.text:
            # print('无效用户')
            continue
        if '"status":2003' in r.text:
            # print('"status":2003')
            continue
        if '大众点评网</title>' not in r.text:continue
        newtext = text.replace('&nbsp;', ',')
        try:
            css = re.findall('href="//s3plus.meituan.net(.*?).css">', text.replace(' ', ''))[0]
        except:return
        cssurl = 'http://s3plus.meituan.net' + css + '.css'
        shopId = item['标题url'].split('/')[-1]
        words, real_list = getfont(cssurl,shopId)

        for i in real_list.keys():         #review  dishname num  hours shopdesc
            if i in ['num']:continue
            newtext = dec(newtext, real_list,i)
        newtext = datanum(newtext, real_list)
        # print(newtext)
        html = etree.HTML(newtext)
        # item['营业时间'] = html.xpath('string(.//*[@id="basic-info"]/div[4]/p[1]/span[2])').replace(' ', '')
        item['营业时间'] = re.findall('<spanclass="info-name">营业时间：</span><spanclass="item">(.*?)</span>',newtext.replace(' ','')
                                  .replace('\n',''))[0].replace('<svgmtsiclass="shopdesc">','').replace('<svgmtsiclass="hours">','').replace('</svgmtsi>','')
        item['电话'] = html.xpath('string(.//*[@id="basic-info"]/p)').replace(' ', '')
        # item['各类评分'] = html.xpath('string(.//*[@id="comment_score"])').replace(' ', '')
        mainRegionId=re.findall('mainCategoryId:(\d+)',text)[0]
        mainCategoryId=re.findall('mainRegionId:(\d+)',text)[0]
        shopName=re.findall("shopName: ('.*?'),",text)[0]
        # print('开始获取pos')
        shop=getpos(shopId,cityid,mainRegionId, mainCategoryId,shopName)
        k,v=getscore(shopId,cityid,mainRegionId)
        if v:
            for i in range(len(v)):
                data=datanum(v[i], real_list).replace('<d class="num">','').replace('</d>','')
                item[k[i]]=data
        # print(k,shopId,cityid,mainRegionId)
        item['glng']=shop['glng']
        item['glat']=shop['glat']
        item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        try:
            print(item)
            # if not info_base.find_one({'标题url':url}):
            #     info_base.insert_one(item)
        except Exception as e:
            print(e,url)
        # time.sleep(2)
        break

if __name__ == '__main__':
    pool = ThreadPoolExecutor(15)
    pool2 = ThreadPoolExecutor(3)
    # x=info_base.delete_many({})
    # print(x.deleted_count,'个文档已删除')

    while pagebase.find_one({'status':0}):           #状态0未抓取  -1正在抓取  1已抓取
        page=pagebase.find_one({'status': 0})
        pagebase.update_one(page, {"$set": {'status':-1}})
        print(page)
        l=[]
        for i in range(1, int(page['pagenum']) + 1):
            url=page['url']+'p'+str(i)
            # getdata(url,page['type'])
            done = pool2.submit(getdata,url,page['type'],page['cityid'])
            l.append(done)
        [obj.result() for obj in l]
        pagebase.update_one(page, {"$set": {'status': 1}})

