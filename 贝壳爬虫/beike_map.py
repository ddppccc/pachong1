import json
import re

import requests
from lxml import etree
#shen

# 生成最新的 映射表
def get_esf_code_map():
    """
    获取所有城市有二手房的城市
    :return: {'合肥': 'hf', '芜湖': 'wuhu',....
    """
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.ke.com",
        "Referer": "https://sz.ke.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
    esfDict = {}
    url = 'https://www.ke.com/city/'
    res = requests.get(url, headers=headers)
    res.encoding = res.apparent_encoding
    tree = etree.HTML(res.text)

    # url中包含fang,则没有二手房数据
    a_list = tree.xpath(
        "//div[@class='city-item VIEWDATA']//div[@class='city_province']/ul/li/a[not(contains(@href, 'fang'))]")     # 可以在这里设置需要爬取的城市区间  [x:y]
        # "//div[@class='city-item ']//div[@class='city_province']/ul/li/a[not(contains(@href, 'fang'))]")
        # "//div[@class='city_list_ul']//div[@class='city_province']/ul/li/a[not(contains(@href, 'fang'))]")
    for a in a_list:
        city = a.xpath("./text()")[0]
        city_code = a.xpath("./@href")[0].split(".")[0][2:]
        esfDict[city] = city_code
    print(esfDict)

    with open("bk_city_map.json", 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(esfDict, ensure_ascii=False))
    return esfDict

def get_cj_code_map():
    """
    获取所有城市有二手房的城市
    :return: {'合肥': 'hf', '芜湖': 'wuhu',....
    """
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.ke.com",
        "Referer": "https://sz.ke.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
    esfDict = {}
    url = 'https://www.ke.com/city/'
    res = requests.get(url, headers=headers)
    res.encoding = res.apparent_encoding
    tree = etree.HTML(res.text)

    # url中包含fang,则没有二手房数据
    a_list = tree.xpath(
        "//div[@class='city-item VIEWDATA']//div[@class='city_province']/ul/li/a[not(contains(@href, 'fang'))]")      # 可以在这里设置需要爬取的城市区间  [x:y]
        # "//div[@class='city-item ']//div[@class='city_province']/ul/li/a[not(contains(@href, 'fang'))]")
        # "//div[@class='city_list_ul']//div[@class='city_province']/ul/li/a[not(contains(@href, 'fang'))]")
    for a in a_list:
        city = a.xpath("./text()")[0]
        city_code = a.xpath("./@href")[0].split(".")[0][2:]
        esfDict[city] = city_code
    print(esfDict)

    with open("bk_city_map.json", 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(esfDict, ensure_ascii=False))
    return esfDict


# 获取 二手房区县
def get_regions(city_name, city_code_map):
    """
    根据城市名获得行政区
    :param city_name:
    :return: {'guangming': '光明'}, CHENFJIAO  [True/False]
    """
    url0 = 'https://{}.ke.com/ershoufang/'.format(city_code_map[city_name])


    CHENFJIAO = False
    tree0 = get_html(url0)
    urls = {}
    href = tree0.xpath('//div[@data-role="ershoufang"]/div/a')
    if "成交" in tree0.xpath("string(//div[@class='menuLeft']/ul)"):
        CHENFJIAO = True
    for ss in href:
        it1 = {}
        qx = ''.join(ss.xpath("./text()"))
        ur = ''.join(ss.xpath('./@href'))
        url1 = ''.join(re.findall('(.+)/ershoufang', url0)) + ur
        tree1 = get_html(url1)
        strnum = ''.join(tree1.xpath('//div[@class="resultDes clear"]/h2/span/text()'))
        length0 = int(strnum)
        numpg0 = int(length0/30) + 2
        if length0 > 3000:
            urlList = []
            for i in range(1, 9):
                it2 = {}
                url2 = url1 + 'p' + str(i)
                tree2 = get_html(url2)
                length1 = int(''.join(tree2.xpath('//div[@class="resultDes clear"]/h2/span/text()')))
                if length1 > 3000:
                    for j in range(1, 4):
                        it3 = {}
                        url3 = url1 + 'de' + str(j) + 'p' + str(i)
                        tree3 = get_html(url3)
                        length2 = int(''.join(tree3.xpath('//div[@class="resultDes clear"]/h2/span/text()')))
                        if length2 == length0:
                            continue
                        elif length2 == length1:
                            continue

                        if length2 > 3000:
                            url4ls = tree3.xpath('//div[@data-role="ershoufang"]/div[2]/a/@href')
                            for ur4 in url4ls:
                                it4 = {}
                                url4 = ''.join(re.findall('(.+)/ershoufang', url0)) + ur4
                                tree4 = get_html(url4)
                                length3 = int(''.join(tree4.xpath('//div[@class="resultDes clear"]/h2/span/text()')))
                                if length3 == length0:
                                    continue
                                elif length3 == length1:
                                    continue
                                elif length3 == length2:
                                    continue

                                numpg3 = int(length3 / 30) + 2
                                it4[url4] = numpg3
                                urlList.append(it4)
                                urls[qx] = urlList

                        else:
                            numpg2 = int(length2 / 30) + 2
                            it3[url3] = numpg2
                            urlList.append(it3)
                            urls[qx] = urlList
                elif length1 == length0:
                    continue
                else:
                    numpg1 = int(length1 / 30) + 2
                    it2[url2] = numpg1
                    urlList.append(it2)
                    urls[qx] = urlList
        else:
            it1[url1] = numpg0
            urls[qx] = [it1]
    return urls, CHENFJIAO

def get_regionscj(city_name, city_code_map):
    """
    根据城市名获得行政区
    :param city_name:
    :return: {'guangming': '光明'}, CHENFJIAO  [True/False]
    """
    url0 = 'https://{}.ke.com/chengjiao/'.format(city_code_map[city_name])


    CHENFJIAO = False
    tree0 = get_html(url0)
    urls = {}
    href = tree0.xpath('//div[@data-role="ershoufang"]/div/a')
    if "成交" in tree0.xpath("string(//div[@class='menuLeft']/ul)"):
        CHENFJIAO = True
    for ss in href:
        qx = ''.join(ss.xpath("./text()"))
        ur = ''.join(ss.xpath('./@href'))
        url1 = ''.join(re.findall('(.+)/chengjiao', url0)) + ur
        tree1 = get_html(url1)
        strnum = ''.join(tree1.xpath('//div[@class="total fl"]/span/text()'))
        try:
            length0 = int(strnum)
        except:
            length0 = 0
        if length0 > 3000:
            urlList = []
            for i in range(1, 9):
                url2 = url1 + 'p' + str(i)
                tree2 = get_html(url2)
                try:
                    length1 = int(''.join(tree2.xpath('//div[@class="total fl"]/span/text()')))
                except:
                    length1 = 0
                if length1 > 3000:
                    for j in range(1, 4):
                        url3 = url1 + 'de' + str(j) + 'p' + str(i)
                        tree3 = get_html(url3)
                        try:
                            length2 = int(''.join(tree3.xpath('//div[@class="total fl"]/span/text()')))
                        except:
                            length2 = 0
                        if length2 == length0:
                            continue
                        elif length2 == length1:
                            continue
                        urlList.append(url3)
                        urls[qx] = urlList
                elif length1 == length0:
                    continue
                else:
                    urlList.append(url2)
                    urls[qx] = urlList
        else:
            urls[qx] = [url1]
    return urls, CHENFJIAO


def get_html(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        # "Host": "www.ke.com",
        "Referer": "https://sz.ke.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
    # prox = get_proxy()
    # proxies = {'http': 'http://%s' % prox, 'https': 'https://%s' % prox}
    # res = sre.get(url, headers=headers, proxies=proxies)
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    # print(res.text)
    tree = etree.HTML(res.text)
    return tree

# 生成新房url_map
def get_newHouse_url_map():
    newhouse = {'安国': 'https://ag.fang.ke.com/loupan', '阿拉善盟': 'https://alsm.fang.ke.com/loupan',
                '鞍山': 'https://as.fang.ke.com/loupan', '安达': 'https://ad.fang.ke.com/loupan',
                '安庆': 'https://aq.fang.ke.com/loupan', '安丘': 'https://anqiu.fang.ke.com/loupan',
                '安阳': 'https://ay.fang.ke.com/loupan', '安陆': 'https://anlu.fang.ke.com/loupan',
                '阿坝': 'https://ab.fang.ke.com/loupan', '安顺': 'https://anshun.fang.ke.com/loupan',
                '安宁': 'https://an.fang.ke.com/loupan', '安康': 'https://ak.fang.ke.com/loupan',
                '阿克苏': 'https://aks.fang.ke.com/loupan', '阿拉尔': 'https://alr.fang.ke.com/loupan',
                '北京': 'https://bj.fang.ke.com/loupan', '保定': 'https://baoding.fang.ke.com/loupan',
                '泊头': 'https://botou.fang.ke.com/loupan', '霸州': 'https://bazhou.fang.ke.com/loupan',
                '包头': 'https://baotou.fang.ke.com/loupan', '本溪': 'https://bx.fang.ke.com/loupan',
                '北票': 'https://bp.fang.ke.com/loupan', '白山': 'https://bs.fang.ke.com/loupan',
                '白城': 'https://bc.fang.ke.com/loupan', '北安': 'https://ba.fang.ke.com/loupan',
                '蚌埠': 'https://bf.fang.ke.com/loupan', '亳州': 'https://bozhou.fang.ke.com/loupan',
                '滨州': 'https://binzhou.fang.ke.com/loupan', '北海': 'https://bh.fang.ke.com/loupan',
                '北流': 'https://bl.fang.ke.com/loupan', '百色': 'https://baise.fang.ke.com/loupan',
                '保亭市': 'https://bt.fang.ke.com/loupan', '巴中': 'https://bz.fang.ke.com/loupan',
                '毕节': 'https://bijie.fang.ke.com/loupan', '保山': 'https://baoshan.fang.ke.com/loupan',
                '宝鸡': 'https://baoji.fang.ke.com/loupan', '白银': 'https://by.fang.ke.com/loupan',
                '博尔塔拉': 'https://brtl.fang.ke.com/loupan', '博乐': 'https://bole.fang.ke.com/loupan',
                '承德': 'https://chengde.fang.ke.com/loupan', '沧州': 'https://cangzhou.fang.ke.com/loupan',
                '长治': 'https://changzhi.fang.ke.com/loupan', '赤峰': 'https://cf.fang.ke.com/loupan',
                '朝阳': 'https://chaoyang.fang.ke.com/loupan', '长春': 'https://cc.fang.ke.com/loupan',
                '昌邑': 'https://cy.fang.ke.com/loupan', '常州': 'https://changzhou.fang.ke.com/loupan',
                '常熟': 'https://changshu.fang.ke.com/loupan', '慈溪': 'https://cixi.fang.ke.com/loupan',
                '滁州': 'https://cz.fang.ke.com/loupan', '池州': 'https://chizhou.fang.ke.com/loupan',
                '长葛': 'https://cg.fang.ke.com/loupan', '赤壁': 'https://cb.fang.ke.com/loupan',
                '常德': 'https://changde.fang.ke.com/loupan', '郴州': 'https://chenzhou.fang.ke.com/loupan',
                '潮州': 'https://chaozhou.fang.ke.com/loupan', '岑溪': 'https://cx.fang.ke.com/loupan',
                '崇左': 'https://chongzuo.fang.ke.com/loupan', '澄迈市': 'https://cm.fang.ke.com/loupan',
                '成都': 'https://cd.fang.ke.com/loupan', '崇州': 'https://chongzhou.fang.ke.com/loupan',
                '赤水': 'https://chishui.fang.ke.com/loupan', '楚雄': 'https://chuxiong.fang.ke.com/loupan',
                '昌都': 'https://changdu.fang.ke.com/loupan', '昌吉': 'https://cj.fang.ke.com/loupan',
                '重庆': 'https://cq.fang.ke.com/loupan', '长沙': 'https://cs.fang.ke.com/loupan',
                '定州': 'https://dingzhou.fang.ke.com/loupan', '大同': 'https://dt.fang.ke.com/loupan',
                '大连': 'https://dl.fang.ke.com/loupan', '丹东': 'https://dd.fang.ke.com/loupan',
                '东港': 'https://donggang.fang.ke.com/loupan', '大石桥': 'https://dsq.fang.ke.com/loupan',
                '灯塔': 'https://dengta.fang.ke.com/loupan', '德惠': 'https://dehui.fang.ke.com/loupan',
                '敦化': 'https://dunhua.fang.ke.com/loupan', '大庆': 'https://dq.fang.ke.com/loupan',
                '大兴安岭': 'https://dxal.fang.ke.com/loupan', '大丰': 'https://df.fang.ke.com/loupan',
                '东台': 'https://dongtai.fang.ke.com/loupan', '丹阳': 'https://danyang.fang.ke.com/loupan',
                '东阳': 'https://dongyang.fang.ke.com/loupan', '德兴': 'https://dx.fang.ke.com/loupan',
                '东营': 'https://dongying.fang.ke.com/loupan', '德州': 'https://dezhou.fang.ke.com/loupan',
                '登封': 'https://dengfeng.fang.ke.com/loupan', '邓州': 'https://dengzhou.fang.ke.com/loupan',
                '大冶': 'https://dazhi.fang.ke.com/loupan', '当阳': 'https://dangyang.fang.ke.com/loupan',
                '东莞': 'https://dg.fang.ke.com/loupan', '儋州': 'https://dz.fang.ke.com/loupan',
                '东方': 'https://dongfang.fang.ke.com/loupan', '定安市': 'https://da.fang.ke.com/loupan',
                '都江堰': 'https://djy.fang.ke.com/loupan', '德阳': 'https://dy.fang.ke.com/loupan',
                '达州': 'https://dazhou.fang.ke.com/loupan', '大理': 'https://dali.fang.ke.com/loupan',
                '德宏': 'https://dh.fang.ke.com/loupan', '迪庆': 'https://diqing.fang.ke.com/loupan',
                '敦煌': 'https://dunhuang.fang.ke.com/loupan', '定西': 'https://dingxi.fang.ke.com/loupan',
                '德令哈': 'https://dlh.fang.ke.com/loupan', '鄂尔多斯': 'https://eeds.fang.ke.com/loupan',
                '鄂州': 'https://ez.fang.ke.com/loupan', '恩施': 'https://es.fang.ke.com/loupan',
                '恩平': 'https://ep.fang.ke.com/loupan', '汾阳': 'https://fenyang.fang.ke.com/loupan',
                '抚顺': 'https://fushun.fang.ke.com/loupan', '凤城': 'https://fch.fang.ke.com/loupan',
                '阜阳': 'https://fy.fang.ke.com/loupan', '福州': 'https://fz.fang.ke.com/loupan',
                '福清': 'https://fuqing.fang.ke.com/loupan', '福安': 'https://fa.fang.ke.com/loupan',
                '福鼎': 'https://fd.fang.ke.com/loupan', '丰城': 'https://fengcheng.fang.ke.com/loupan',
                '抚州': 'https://fuzhou.fang.ke.com/loupan', '肥城': 'https://fc.fang.ke.com/loupan',
                '佛山': 'https://fs.fang.ke.com/loupan', '防城港': 'https://fcg.fang.ke.com/loupan',
                '福泉': 'https://fq.fang.ke.com/loupan', '阜康': 'https://fk.fang.ke.com/loupan',
                '高碑店': 'https://gbd.fang.ke.com/loupan', '古交': 'https://gujiao.fang.ke.com/loupan',
                '盖州': 'https://gaizhou.fang.ke.com/loupan', '公主岭': 'https://gzl.fang.ke.com/loupan',
                '甘南': 'https://gn.fang.ke.com/loupan', '高邮': 'https://gaoyou.fang.ke.com/loupan',
                '贵溪': 'https://gx.fang.ke.com/loupan', '赣州': 'https://ganzhou.fang.ke.com/loupan',
                '高密': 'https://gm.fang.ke.com/loupan', '广水': 'https://gs.fang.ke.com/loupan',
                '广州': 'https://gz.fang.ke.com/loupan', '高州': 'https://gaozhou.fang.ke.com/loupan',
                '桂林': 'https://gl.fang.ke.com/loupan', '贵港': 'https://gg.fang.ke.com/loupan',
                '桂平': 'https://gp.fang.ke.com/loupan', '广元': 'https://guangyuan.fang.ke.com/loupan',
                '广安': 'https://ga.fang.ke.com/loupan', '甘孜': 'https://ganzi.fang.ke.com/loupan',
                '贵阳': 'https://gy.fang.ke.com/loupan', '个旧': 'https://gejiu.fang.ke.com/loupan',
                '格尔木': 'https://grm.fang.ke.com/loupan', '固原': 'https://guyuan.fang.ke.com/loupan',
                '邯郸': 'https://hd.fang.ke.com/loupan', '黄骅': 'https://huanghua.fang.ke.com/loupan',
                '河间': 'https://hj.fang.ke.com/loupan', '衡水': 'https://hs.fang.ke.com/loupan',
                '侯马': 'https://houma.fang.ke.com/loupan', '霍州': 'https://huozhou.fang.ke.com/loupan',
                '呼和浩特': 'https://hhht.fang.ke.com/loupan', '呼伦贝尔': 'https://hlbr.fang.ke.com/loupan',
                '海城': 'https://haicheng.fang.ke.com/loupan', '葫芦岛': 'https://hld.fang.ke.com/loupan',
                '桦甸': 'https://huadian.fang.ke.com/loupan', '珲春': 'https://hunchun.fang.ke.com/loupan',
                '哈尔滨': 'https://hrb.fang.ke.com/loupan', '鹤岗': 'https://hegang.fang.ke.com/loupan',
                '海林': 'https://hl.fang.ke.com/loupan', '黑河': 'https://heihe.fang.ke.com/loupan',
                '海门': 'https://haimen.fang.ke.com/loupan', '淮安': 'https://ha.fang.ke.com/loupan',
                '杭州': 'https://hz.fang.ke.com/loupan', '海宁': 'https://haining.fang.ke.com/loupan',
                '湖州': 'https://huzhou.fang.ke.com/loupan', '合肥': 'https://hf.fang.ke.com/loupan',
                '淮南': 'https://huainan.fang.ke.com/loupan', '淮北': 'https://huaibei.fang.ke.com/loupan',
                '黄山': 'https://huangshan.fang.ke.com/loupan', '霍邱': 'https://hq.fang.ke.com/loupan',
                '海阳': 'https://haiyang.fang.ke.com/loupan', '菏泽': 'https://heze.fang.ke.com/loupan',
                '鹤壁': 'https://hb.fang.ke.com/loupan', '鹤山': 'https://hsh.fang.ke.com/loupan',
                '辉县': 'https://huixian.fang.ke.com/loupan', '黄石': 'https://huangshi.fang.ke.com/loupan',
                '洪湖': 'https://honghu.fang.ke.com/loupan', '黄冈': 'https://hg.fang.ke.com/loupan',
                '衡阳': 'https://hy.fang.ke.com/loupan', '怀化': 'https://hh.fang.ke.com/loupan',
                '洪江': 'https://hongjiang.fang.ke.com/loupan', '化州': 'https://huazhou.fang.ke.com/loupan',
                '河源': 'https://heyuan.fang.ke.com/loupan', '贺州': 'https://hezhou.fang.ke.com/loupan',
                '河池': 'https://hc.fang.ke.com/loupan', '合山': 'https://heshan.fang.ke.com/loupan',
                '海南': 'https://hn.fang.ke.com/loupan', '海口': 'https://hk.fang.ke.com/loupan',
                '华蓥': 'https://huaying.fang.ke.com/loupan', '仁怀': 'https://hr.fang.ke.com/loupan',
                '红河州': 'https://honghezhou.fang.ke.com/loupan', '韩城': 'https://hancheng.fang.ke.com/loupan',
                '汉中': 'https://hanzhong.fang.ke.com/loupan', '海东': 'https://haidong.fang.ke.com/loupan',
                '海西': 'https://haixi.fang.ke.com/loupan', '哈密': 'https://hm.fang.ke.com/loupan',
                '和田': 'https://ht.fang.ke.com/loupan', '惠州': 'https://hui.fang.ke.com/loupan',
                '冀州': 'https://jizhou.fang.ke.com/loupan', '晋城': 'https://jc.fang.ke.com/loupan',
                '晋中': 'https://jz.fang.ke.com/loupan', '锦州': 'https://jinzhou.fang.ke.com/loupan',
                '吉林': 'https://jl.fang.ke.com/loupan', '蛟河': 'https://jiaohe.fang.ke.com/loupan',
                '鸡西': 'https://jixi.fang.ke.com/loupan', '佳木斯': 'https://jms.fang.ke.com/loupan',
                '金坛': 'https://jt.fang.ke.com/loupan', '句容': 'https://jr.fang.ke.com/loupan',
                '靖江': 'https://jingjiang.fang.ke.com/loupan', '建德': 'https://jd.fang.ke.com/loupan',
                '嘉兴': 'https://jx.fang.ke.com/loupan', '嘉善': 'https://jiashan.fang.ke.com/loupan',
                '金华': 'https://jh.fang.ke.com/loupan', '建瓯': 'https://jo.fang.ke.com/loupan',
                '进贤': 'https://jinxian.fang.ke.com/loupan', '景德镇': 'https://jdz.fang.ke.com/loupan',
                '九江': 'https://jiujiang.fang.ke.com/loupan', '吉安': 'https://jian.fang.ke.com/loupan',
                '济南': 'https://jn.fang.ke.com/loupan', '胶州': 'https://jiaozhou.fang.ke.com/loupan',
                '济宁': 'https://jining.fang.ke.com/loupan', '焦作': 'https://jiaozuo.fang.ke.com/loupan',
                '济源': 'https://jiyuan.fang.ke.com/loupan', '荆门': 'https://jm.fang.ke.com/loupan',
                '荆州': 'https://jingzhou.fang.ke.com/loupan', '吉首': 'https://jishou.fang.ke.com/loupan',
                '江门': 'https://jiangmen.fang.ke.com/loupan', '揭阳': 'https://jieyang.fang.ke.com/loupan',
                '简阳': 'https://jianyang.fang.ke.com/loupan', '江油': 'https://jiangyou.fang.ke.com/loupan',
                '景洪': 'https://jinghong.fang.ke.com/loupan', '嘉峪关': 'https://jyg.fang.ke.com/loupan',
                '金昌': 'https://jinchang.fang.ke.com/loupan', '酒泉': 'https://jq.fang.ke.com/loupan',
                '开原': 'https://kaiyuan.fang.ke.com/loupan', '昆山': 'https://ks.fang.ke.com/loupan',
                '开封': 'https://kf.fang.ke.com/loupan', '开平': 'https://kp.fang.ke.com/loupan',
                '凯里': 'https://kaili.fang.ke.com/loupan', '昆明': 'https://km.fang.ke.com/loupan',
                '开远': 'https://ky.fang.ke.com/loupan', '克拉玛依': 'https://klmy.fang.ke.com/loupan',
                '库尔勒': 'https://krl.fang.ke.com/loupan', '克孜勒苏': 'https://kzls.fang.ke.com/loupan',
                '喀什': 'https://kashi.fang.ke.com/loupan', '奎屯': 'https://kt.fang.ke.com/loupan',
                '廊坊': 'https://lf.fang.ke.com/loupan', '潞城': 'https://lucheng.fang.ke.com/loupan',
                '临猗': 'https://lin.fang.ke.com/loupan', '临汾': 'https://linfen.fang.ke.com/loupan',
                '吕梁': 'https://lvliang.fang.ke.com/loupan', '辽阳': 'https://liaoyang.fang.ke.com/loupan',
                '凌源': 'https://lingyuan.fang.ke.com/loupan', '辽源': 'https://liaoyuan.fang.ke.com/loupan',
                '临江': 'https://linjiang.fang.ke.com/loupan', '龙井': 'https://longjing.fang.ke.com/loupan',
                '溧阳': 'https://liyang.fang.ke.com/loupan', '连云港': 'https://lyg.fang.ke.com/loupan',
                '兰溪': 'https://lanxi.fang.ke.com/loupan', '临海': 'https://lh.fang.ke.com/loupan',
                '丽水': 'https://lishui.fang.ke.com/loupan', '龙泉': 'https://lq.fang.ke.com/loupan',
                '六安': 'https://la.fang.ke.com/loupan', '连江': 'https://lianj.fang.ke.com/loupan',
                '龙海': 'https://longhai.fang.ke.com/loupan', '龙岩': 'https://ly.fang.ke.com/loupan',
                '乐平': 'https://lp.fang.ke.com/loupan', '莱西': 'https://laixi.fang.ke.com/loupan',
                '莱阳': 'https://laiyang.fang.ke.com/loupan', '莱州': 'https://laizhou.fang.ke.com/loupan',
                '莱芜': 'https://lw.fang.ke.com/loupan', '临沂': 'https://linyi.fang.ke.com/loupan',
                '乐陵': 'https://ll.fang.ke.com/loupan', '聊城': 'https://lc.fang.ke.com/loupan',
                '临清': 'https://linqing.fang.ke.com/loupan', '洛阳': 'https://luoyang.fang.ke.com/loupan',
                '林州': 'https://linzhou.fang.ke.com/loupan', '漯河': 'https://luohe.fang.ke.com/loupan',
                '老河口': 'https://lhk.fang.ke.com/loupan', '利川': 'https://lichuan.fang.ke.com/loupan',
                '浏阳': 'https://liuyang.fang.ke.com/loupan', '醴陵': 'https://liling.fang.ke.com/loupan',
                '临湘': 'https://linxiang.fang.ke.com/loupan', '娄底': 'https://loudi.fang.ke.com/loupan',
                '冷水江': 'https://lsj.fang.ke.com/loupan', '涟源': 'https://lianyuan.fang.ke.com/loupan',
                '乐昌': 'https://lechang.fang.ke.com/loupan', '廉江': 'https://lianjiang.fang.ke.com/loupan',
                '雷州': 'https://leizhou.fang.ke.com/loupan', '陆丰': 'https://lufeng.fang.ke.com/loupan',
                '连州': 'https://lianzhou.fang.ke.com/loupan', '罗定': 'https://luoding.fang.ke.com/loupan',
                '柳州': 'https://liuzhou.fang.ke.com/loupan', '来宾': 'https://lb.fang.ke.com/loupan',
                '临高市': 'https://lg.fang.ke.com/loupan', '乐东市': 'https://ld.fang.ke.com/loupan',
                '陵水市': 'https://ls.fang.ke.com/loupan', '泸州': 'https://luzhou.fang.ke.com/loupan',
                '乐山': 'https://leshan.fang.ke.com/loupan', '阆中': 'https://langzhong.fang.ke.com/loupan',
                '凉山': 'https://liangshan.fang.ke.com/loupan', '六盘水': 'https://lps.fang.ke.com/loupan',
                '丽江': 'https://lj.fang.ke.com/loupan', '临沧': 'https://lincang.fang.ke.com/loupan',
                '拉萨': 'https://lasa.fang.ke.com/loupan', '林芝': 'https://linzhi.fang.ke.com/loupan',
                '兰州': 'https://lz.fang.ke.com/loupan', '陇南': 'https://ln.fang.ke.com/loupan',
                '临夏': 'https://lx.fang.ke.com/loupan', '满洲里': 'https://mzl.fang.ke.com/loupan',
                '密山': 'https://mishan.fang.ke.com/loupan', '牡丹江': 'https://mdj.fang.ke.com/loupan',
                '马鞍山': 'https://mas.fang.ke.com/loupan', '明光': 'https://mingguang.fang.ke.com/loupan',
                '孟州': 'https://mengzhou.fang.ke.com/loupan', '麻城': 'https://mc.fang.ke.com/loupan',
                '茂名': 'https://mm.fang.ke.com/loupan', '梅州': 'https://meizhou.fang.ke.com/loupan',
                '绵竹': 'https://mianzhu.fang.ke.com/loupan', '绵阳': 'https://mianyang.fang.ke.com/loupan',
                '眉山': 'https://ms.fang.ke.com/loupan', '南宫': 'https://nangong.fang.ke.com/loupan',
                '讷河': 'https://nh.fang.ke.com/loupan', '宁安': 'https://ningan.fang.ke.com/loupan',
                '南京': 'https://nj.fang.ke.com/loupan', '南通': 'https://nt.fang.ke.com/loupan',
                '宁波': 'https://nb.fang.ke.com/loupan', '宁国': 'https://ng.fang.ke.com/loupan',
                '南安': 'https://na.fang.ke.com/loupan', '南平': 'https://np.fang.ke.com/loupan',
                '宁德': 'https://nd.fang.ke.com/loupan', '南昌': 'https://nc.fang.ke.com/loupan',
                '南康': 'https://nk.fang.ke.com/loupan', '南阳': 'https://ny.fang.ke.com/loupan',
                '南宁': 'https://nn.fang.ke.com/loupan', '内江': 'https://neijiang.fang.ke.com/loupan',
                '南充': 'https://nanchong.fang.ke.com/loupan', '怒江': 'https://nujiang.fang.ke.com/loupan',
                '那曲': 'https://nq.fang.ke.com/loupan', '普兰店': 'https://pld.fang.ke.com/loupan',
                '盘锦': 'https://pj.fang.ke.com/loupan', '邳州': 'https://pz.fang.ke.com/loupan',
                '平湖': 'https://ph.fang.ke.com/loupan', '莆田': 'https://pt.fang.ke.com/loupan',
                '萍乡': 'https://pingxiang.fang.ke.com/loupan', '平度': 'https://pd.fang.ke.com/loupan',
                '平顶山': 'https://pds.fang.ke.com/loupan', '濮阳': 'https://py.fang.ke.com/loupan',
                '普宁': 'https://pn.fang.ke.com/loupan', '攀枝花': 'https://pzh.fang.ke.com/loupan',
                '普洱': 'https://pr.fang.ke.com/loupan', '平凉': 'https://pl.fang.ke.com/loupan',
                '迁安': 'https://qa.fang.ke.com/loupan', '秦皇岛': 'https://qhd.fang.ke.com/loupan',
                '清徐': 'https://qx.fang.ke.com/loupan', '齐齐哈尔': 'https://qqhr.fang.ke.com/loupan',
                '七台河': 'https://qth.fang.ke.com/loupan', '栖霞': 'https://qixia.fang.ke.com/loupan',
                '启东': 'https://qidong.fang.ke.com/loupan', '衢州': 'https://quzhou.fang.ke.com/loupan',
                '泉州': 'https://quanzhou.fang.ke.com/loupan', '青岛': 'https://qd.fang.ke.com/loupan',
                '青州': 'https://qingzhou.fang.ke.com/loupan', '曲阜': 'https://qf.fang.ke.com/loupan',
                '沁阳': 'https://qinyang.fang.ke.com/loupan', '潜江': 'https://qianjiang.fang.ke.com/loupan',
                '清远': 'https://qy.fang.ke.com/loupan', '钦州': 'https://qinzhou.fang.ke.com/loupan',
                '琼海': 'https://qh.fang.ke.com/loupan', '琼中市': 'https://qz.fang.ke.com/loupan',
                '邛崃': 'https://ql.fang.ke.com/loupan', '清镇': 'https://qingzhen.fang.ke.com/loupan',
                '黔西南': 'https://qianxinan.fang.ke.com/loupan', '黔东南': 'https://qdn.fang.ke.com/loupan',
                '黔南': 'https://qn.fang.ke.com/loupan', '曲靖': 'https://qj.fang.ke.com/loupan',
                '庆阳': 'https://qingyang.fang.ke.com/loupan', '青铜峡': 'https://qtx.fang.ke.com/loupan',
                '任丘': 'https://rq.fang.ke.com/loupan', '如皋': 'https://rg.fang.ke.com/loupan',
                '瑞安': 'https://ra.fang.ke.com/loupan', '瑞昌': 'https://rc.fang.ke.com/loupan',
                '瑞金': 'https://rj.fang.ke.com/loupan', '荣成': 'https://rongcheng.fang.ke.com/loupan',
                '日照': 'https://rz.fang.ke.com/loupan', '汝州': 'https://ruzhou.fang.ke.com/loupan',
                '瑞丽': 'https://rl.fang.ke.com/loupan', '日喀则': 'https://rkz.fang.ke.com/loupan',
                '上海': 'https://sh.fang.ke.com/loupan', '三河': 'https://sanhe.fang.ke.com/loupan',
                '深州': 'https://shenzhou.fang.ke.com/loupan', '四平': 'https://sp.fang.ke.com/loupan',
                '松原': 'https://songyuan.fang.ke.com/loupan', '尚志': 'https://shangzhi.fang.ke.com/loupan',
                '双鸭山': 'https://sys.fang.ke.com/loupan', '绥芬河': 'https://sfh.fang.ke.com/loupan',
                '绥化': 'https://suihua.fang.ke.com/loupan', '苏州': 'https://su.fang.ke.com/loupan',
                '宿迁': 'https://sq.fang.ke.com/loupan', '沭阳': 'https://shuyang.fang.ke.com/loupan',
                '绍兴': 'https://sx.fang.ke.com/loupan', '嵊州': 'https://shengzhou.fang.ke.com/loupan',
                '宿州': 'https://suzhou.fang.ke.com/loupan', '三明': 'https://sm.fang.ke.com/loupan',
                '石狮': 'https://shishi.fang.ke.com/loupan', '邵武': 'https://shaowu.fang.ke.com/loupan',
                '上饶': 'https://sr.fang.ke.com/loupan', '寿光': 'https://shouguang.fang.ke.com/loupan',
                '商丘': 'https://shangqiu.fang.ke.com/loupan', '十堰': 'https://shiyan.fang.ke.com/loupan',
                '石首': 'https://shishou.fang.ke.com/loupan', '松滋': 'https://songzi.fang.ke.com/loupan',
                '韶山': 'https://ss.fang.ke.com/loupan', '邵阳': 'https://shaoyang.fang.ke.com/loupan',
                '韶关': 'https://shaoguan.fang.ke.com/loupan', '深圳': 'https://sz.fang.ke.com/loupan',
                '汕头': 'https://st.fang.ke.com/loupan', '顺德': 'https://sd.fang.ke.com/loupan',
                '汕尾': 'https://sw.fang.ke.com/loupan', '三亚': 'https://san.fang.ke.com/loupan',
                '什邡': 'https://sf.fang.ke.com/loupan', '遂宁': 'https://sn.fang.ke.com/loupan',
                '商洛': 'https://sl.fang.ke.com/loupan', '石嘴山': 'https://szs.fang.ke.com/loupan',
                '石家庄': 'https://sjz.fang.ke.com/loupan', '沈阳': 'https://sy.fang.ke.com/loupan',
                '天津': 'https://tj.fang.ke.com/loupan', '唐山': 'https://ts.fang.ke.com/loupan',
                '太原': 'https://ty.fang.ke.com/loupan', '通辽': 'https://tongliao.fang.ke.com/loupan',
                '铁岭': 'https://tieling.fang.ke.com/loupan', '通化': 'https://tonghua.fang.ke.com/loupan',
                '铁力': 'https://tieli.fang.ke.com/loupan', '泰州': 'https://tz.fang.ke.com/loupan',
                '泰兴': 'https://tx.fang.ke.com/loupan', '桐乡': 'https://tongxiang.fang.ke.com/loupan',
                '台州': 'https://taizhou.fang.ke.com/loupan', '铜陵': 'https://tl.fang.ke.com/loupan',
                '桐城': 'https://tc.fang.ke.com/loupan', '天长': 'https://tianchang.fang.ke.com/loupan',
                '滕州': 'https://tengzhou.fang.ke.com/loupan', '泰安': 'https://ta.fang.ke.com/loupan',
                '天门': 'https://tm.fang.ke.com/loupan', '台山': 'https://taishan.fang.ke.com/loupan',
                '铜仁': 'https://tr.fang.ke.com/loupan', '铜川': 'https://tongchuan.fang.ke.com/loupan',
                '天水': 'https://tianshui.fang.ke.com/loupan', '吐鲁番': 'https://tlf.fang.ke.com/loupan',
                '无极': 'https://wj.fang.ke.com/loupan', '武安': 'https://wa.fang.ke.com/loupan',
                '乌海': 'https://wuhai.fang.ke.com/loupan', '乌兰察布': 'https://wlcb.fang.ke.com/loupan',
                '瓦房店': 'https://wfd.fang.ke.com/loupan', '五常': 'https://wuchang.fang.ke.com/loupan',
                '五大连池': 'https://wdlc.fang.ke.com/loupan', '温州': 'https://wz.fang.ke.com/loupan',
                '温岭': 'https://wl.fang.ke.com/loupan', '芜湖': 'https://wuhu.fang.ke.com/loupan',
                '潍坊': 'https://wf.fang.ke.com/loupan', '威海': 'https://weihai.fang.ke.com/loupan',
                '舞钢': 'https://wugang.fang.ke.com/loupan', '卫辉': 'https://weihui.fang.ke.com/loupan',
                '武汉': 'https://wh.fang.ke.com/loupan', '武穴': 'https://wuxue.fang.ke.com/loupan',
                '武冈': 'https://wg.fang.ke.com/loupan', '吴川': 'https://wuchuan.fang.ke.com/loupan',
                '梧州': 'https://wuzhou.fang.ke.com/loupan', '五指山': 'https://wzs.fang.ke.com/loupan',
                '文昌市': 'https://wc.fang.ke.com/loupan', '万宁': 'https://wn.fang.ke.com/loupan',
                '万源': 'https://wy.fang.ke.com/loupan', '文山': 'https://ws.fang.ke.com/loupan',
                '渭南': 'https://weinan.fang.ke.com/loupan', '武威': 'https://ww.fang.ke.com/loupan',
                '吴忠': 'https://wuzhong.fang.ke.com/loupan', '乌鲁木齐': 'https://wlmq.fang.ke.com/loupan',
                '无锡': 'https://wx.fang.ke.com/loupan', '新乐': 'https://xl.fang.ke.com/loupan',
                '邢台': 'https://xt.fang.ke.com/loupan', '忻州': 'https://xinzhou.fang.ke.com/loupan',
                '锡林郭勒盟': 'https://xlglm.fang.ke.com/loupan', '锡林浩特': 'https://xlht.fang.ke.com/loupan',
                '新民': 'https://xinmin.fang.ke.com/loupan', '兴城': 'https://xingcheng.fang.ke.com/loupan',
                '徐州': 'https://xz.fang.ke.com/loupan', '新沂': 'https://xiny.fang.ke.com/loupan',
                '宣城': 'https://xuancheng.fang.ke.com/loupan', '厦门': 'https://xm.fang.ke.com/loupan',
                '新余': 'https://xinyu.fang.ke.com/loupan', '新泰': 'https://xintai.fang.ke.com/loupan',
                '荥阳': 'https://xingyang.fang.ke.com/loupan', '新密': 'https://xinmi.fang.ke.com/loupan',
                '新乡': 'https://xinxiang.fang.ke.com/loupan', '许昌': 'https://xc.fang.ke.com/loupan',
                '信阳': 'https://xinyang.fang.ke.com/loupan', '项城': 'https://xiangcheng.fang.ke.com/loupan',
                '襄阳': 'https://xy.fang.ke.com/loupan', '孝感': 'https://xg.fang.ke.com/loupan',
                '咸宁': 'https://xn.fang.ke.com/loupan', '仙桃': 'https://xiantao.fang.ke.com/loupan',
                '湘潭': 'https://xiangtan.fang.ke.com/loupan', '湘乡': 'https://xiangxiang.fang.ke.com/loupan',
                '湘西': 'https://xx.fang.ke.com/loupan', '兴宁': 'https://xingning.fang.ke.com/loupan',
                '西昌': 'https://xichang.fang.ke.com/loupan', '兴义': 'https://xingyi.fang.ke.com/loupan',
                '宣威': 'https://xw.fang.ke.com/loupan', '西双版纳': 'https://xsbn.fang.ke.com/loupan',
                '西安': 'https://xa.fang.ke.com/loupan', '咸阳': 'https://xianyang.fang.ke.com/loupan',
                '兴平': 'https://xp.fang.ke.com/loupan', '西宁': 'https://xining.fang.ke.com/loupan',
                '阳泉': 'https://yq.fang.ke.com/loupan', '运城': 'https://yuncheng.fang.ke.com/loupan',
                '永济': 'https://yongji.fang.ke.com/loupan', '营口': 'https://yk.fang.ke.com/loupan',
                '榆树': 'https://yushu.fang.ke.com/loupan', '延边': 'https://yb.fang.ke.com/loupan',
                '延吉': 'https://yj.fang.ke.com/loupan', '伊春': 'https://yichun.fang.ke.com/loupan',
                '宜兴': 'https://yixing.fang.ke.com/loupan', '盐城': 'https://yc.fang.ke.com/loupan',
                '扬州': 'https://yz.fang.ke.com/loupan', '仪征': 'https://yizheng.fang.ke.com/loupan',
                '余姚': 'https://yr.fang.ke.com/loupan', '义乌': 'https://yw.fang.ke.com/loupan',
                '永康': 'https://yongkang.fang.ke.com/loupan', '永安': 'https://yongan.fang.ke.com/loupan',
                '鹰潭': 'https://yingtan.fang.ke.com/loupan', '宜春': 'https://ych.fang.ke.com/loupan',
                '烟台': 'https://yt.fang.ke.com/loupan', '禹城': 'https://yucheng.fang.ke.com/loupan',
                '偃师': 'https://yanshi.fang.ke.com/loupan', '鄢陵': 'https://yanling.fang.ke.com/loupan',
                '禹州': 'https://yuzhou.fang.ke.com/loupan', '永城': 'https://yongcheng.fang.ke.com/loupan',
                '宜昌': 'https://yichang.fang.ke.com/loupan', '宜都': 'https://yd.fang.ke.com/loupan',
                '应城': 'https://yingcheng.fang.ke.com/loupan', '岳阳': 'https://yy.fang.ke.com/loupan',
                '益阳': 'https://yiyang.fang.ke.com/loupan', '沅江': 'https://yuanjiang.fang.ke.com/loupan',
                '永州': 'https://yongzhou.fang.ke.com/loupan', '阳江': 'https://yangjiang.fang.ke.com/loupan',
                '阳春': 'https://yangchun.fang.ke.com/loupan', '英德': 'https://yingde.fang.ke.com/loupan',
                '玉林': 'https://yl.fang.ke.com/loupan', '宜州': 'https://yizhou.fang.ke.com/loupan',
                '宜宾': 'https://yibin.fang.ke.com/loupan', '雅安': 'https://yaan.fang.ke.com/loupan',
                '玉溪': 'https://yx.fang.ke.com/loupan', '延安': 'https://ya.fang.ke.com/loupan',
                '榆林': 'https://yulin.fang.ke.com/loupan', '玉门': 'https://ym.fang.ke.com/loupan',
                '银川': 'https://yinchuan.fang.ke.com/loupan', '伊犁': 'https://yili.fang.ke.com/loupan',
                '伊宁': 'https://yining.fang.ke.com/loupan', '赵县': 'https://zhaoxian.fang.ke.com/loupan',
                '遵化': 'https://zhunhua.fang.ke.com/loupan', '涿州': 'https://zhuozhou.fang.ke.com/loupan',
                '张家口': 'https://zjk.fang.ke.com/loupan', '庄河': 'https://zhuanghe.fang.ke.com/loupan',
                '肇东': 'https://zhaodong.fang.ke.com/loupan', '张家港': 'https://zjg.fang.ke.com/loupan',
                '镇江': 'https://zj.fang.ke.com/loupan', '诸暨': 'https://zhuji.fang.ke.com/loupan',
                '舟山': 'https://zhoushan.fang.ke.com/loupan', '漳州': 'https://zhangzhou.fang.ke.com/loupan',
                '樟树': 'https://zhangshu.fang.ke.com/loupan', '章丘': 'https://zhangqiu.fang.ke.com/loupan',
                '淄博': 'https://zb.fang.ke.com/loupan', '枣庄': 'https://zaozhuang.fang.ke.com/loupan',
                '招远': 'https://zhaoyuan.fang.ke.com/loupan', '诸城': 'https://zhucheng.fang.ke.com/loupan',
                '邹城': 'https://zc.fang.ke.com/loupan', '周口': 'https://zk.fang.ke.com/loupan',
                '驻马店': 'https://zmd.fang.ke.com/loupan', '枝江': 'https://zhijiang.fang.ke.com/loupan',
                '枣阳': 'https://zaoyang.fang.ke.com/loupan', '钟祥': 'https://zhongxiang.fang.ke.com/loupan',
                '株洲': 'https://zhuzhou.fang.ke.com/loupan', '张家界': 'https://zjj.fang.ke.com/loupan',
                '资兴': 'https://zx.fang.ke.com/loupan', '珠海': 'https://zh.fang.ke.com/loupan',
                '湛江': 'https://zhanjiang.fang.ke.com/loupan', '肇庆': 'https://zq.fang.ke.com/loupan',
                '中山': 'https://zs.fang.ke.com/loupan', '自贡': 'https://zg.fang.ke.com/loupan',
                '资阳': 'https://ziyang.fang.ke.com/loupan', '遵义': 'https://zunyi.fang.ke.com/loupan',
                '昭通': 'https://zt.fang.ke.com/loupan', '周至': 'https://zhouzhi.fang.ke.com/loupan',
                '张掖': 'https://zy.fang.ke.com/loupan',
                '中卫': 'https://zw.fang.ke.com/loupan',
                '郑州': 'https://zz.fang.ke.com/loupan'}
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    }

    item = {}
    for city, city_url in newhouse.items():
        # if city != '郑州': continue
        print(city, city_url)
        res = requests.get(city_url, headers=headers)
        tree = etree.HTML(res.text)

        region = tree.xpath("//ul[@class='district-wrapper']/li/text()")
        region_spell = tree.xpath("//ul[@class='district-wrapper']/li/@data-district-spell")
        region_dict = dict(zip(region, region_spell))

        url = city_url + '/' + "-".join(region_dict.values())
        # print("url: ", url )
        # headers = {
        #     "Accept": "application/json, text/javascript, */*; q=0.01",
        #     "Accept-Encoding": "gzip, deflate, br",
        #     "Accept-Language": "zh-CN,zh;q=0.9",
        #     "Cache-Control": "no-cache",
        #     "Connection": "keep-alive",
        #     "Pragma": "no-cache",
        #     "Sec-Fetch-Mode": "cors",
        #     "Sec-Fetch-Site": "same-origin",
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        #     "X-Requested-With": "XMLHttpRequest",
        # }
        # params = { "_t": "1" }
        # res = requests.get(url, headers=headers, params=params).json()
        # print(res)

        # 生成所有城市映射表
        item[city] = url

    with open("bk_newHouse_map.json", 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(item, ensure_ascii=False))


if __name__ == '__main__':
    # 城市映射表
    # city_code_map = get_esf_code_map()
    # # print(city_code_map)
    # regions, cj = get_regions("清远", city_code_map)
    # print(regions, cj)

    get_newHouse_url_map()
