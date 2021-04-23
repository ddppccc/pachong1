import base64
import json
import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import re

from selenium.webdriver.support.wait import WebDriverWait


from PIL import Image

from requests.adapters import HTTPAdapter

import pymongo
from urllib import parse

MONGODB_CONFIG = {
   "host": "8.135.119.198",
   "port": "27017",
   "user": "hladmin",
   "password": parse.quote("Hlxkd3,dk3*3@"),
   "db": "dianping",
   "collections": "dianping_collections",
}

# 建立连接
info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['中国房价网']['anjuke_xiaoqu']



xqxx_data = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['中国房价网']['小区信息']

jcsj_data = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['中国房价网']['小区基础数据']



url_data = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['中国房价网']['小区名查重']


s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))  # 设置重试次数为3次
s.mount('https://', HTTPAdapter(max_retries=3))


def part_screenshot(driver):
    driver.save_screenshot("hello1.png")
    return Image.open("hello1.png")


def get_image(driver):  # 对验证码所在位置进行定位，然后截取验证码图片
    img = driver.find_element_by_xpath('//span[@id="viewkey_wp"]/img')
    time.sleep(2)
    location = img.location
    print(location, 111)
    size = img.size
    left = location['x']
    top = location['y']
    right = left + size['width']
    bottom = top + size['height']
    page_snap_obj = part_screenshot(driver)
    image_obj = page_snap_obj.crop((left, top, right, bottom))
    return image_obj  # 得到的就是验证码


def getCode(img):
    with open(img, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": "viccy", "password": "123456", "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]


def yanzheng(chaxun):
    if chaxun.find_element_by_xpath("//div").text == '您的访问过于频繁，请输入验证码后继续浏览。':
        img = get_image(chaxun)
        img.save('E:/PIL_img/1.png')
        yzm = getCode('E:/PIL_img/1.png')
        chaxun.find_element_by_xpath('//input[@id="VerifyCode"]').click()
        time.sleep(2)
        chaxun.find_element_by_xpath('//input[@id="VerifyCode"]').send_keys(yzm)
        time.sleep(random.randint(2, 5))
        chaxun.find_element_by_xpath('//input[@class="umenub2 width70"]').click()
        chaxun = yanzheng(chaxun)  ##########################################################
    return chaxun


def get_proxy():
    try:
        return s.get('http://47.106.223.4:50002/get/').json().get('proxy')
    except:
        num = 3
        while num:
            try:
                return s.get('http://47.106.223.4:50002/get/').json().get('proxy')
            except:
                print('暂无ip，等待20秒')
                time.sleep(20)

                num -= 1
        print('暂无ip')


def ipget(url):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--proxy-server=http://' + get_proxy())
        gd = webdriver.Chrome(chrome_options=options)
        gd.get(url)
        gd = yanzheng(gd)
    except Exception:
        gd.quit()
        print('ip')
        gd = ipget(url)
    return gd


def mn_click(chaxun, city, xq):
    item_df = {}
    item_df['小区名'] = xq
    item_df['城市'] = city
    item_df['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    WebDriverWait(chaxun, 30, 0.2)
    chaxun.find_element_by_xpath('//input[@class="search_bar"]').send_keys(city + xq)  # 输入
    chaxun = yanzheng(chaxun)
    time.sleep(random.randint(2, 5))
    chaxun.find_element_by_xpath('//input[@class="search_bar"]').send_keys(Keys.ENTER)  # 回车
    # WebDriverWait(cha, 30, 1)xun
    chaxun = yanzheng(chaxun)
    chaxun = yanzheng(chaxun)
    time.sleep(random.randint(5, 15))
    try:
        item_df['小区url'] = chaxun.find_element_by_xpath('//ul[@class="mt5"]/li/a').get_attribute('href')
        chaxun.find_element_by_xpath('//ul[@class="mt5"]/li/a').click()  # 点击第一个（可以用NPL分词来优化相关度）
    except:
        print('无点击')
    try:
        WebDriverWait(chaxun, 30, 0.2)
        time.sleep(5)
        chaxun = yanzheng(chaxun)
        chaxun = yanzheng(chaxun)
        # 选择近5年    有的没有近5年的数据
        chaxun.find_element_by_xpath('//a[@class="yearsel "]/following-sibling::a').click()
        WebDriverWait(chaxun, 30, 0.2)
        time.sleep(5)
        # 选择数据
        chaxun.find_element_by_xpath('//a[@id="a_chart_price_line_table"]').click()
        WebDriverWait(chaxun, 30, 0.2)
        time.sleep(5)
        try:
            ke = chaxun.find_element_by_xpath('//div[@id="chart_price_line_table"]/table/thead').text.split(' ')
            va = chaxun.find_element_by_xpath('//div[@id="chart_price_line_table"]/table/tbody').text.split('\n')
            lists = []
            for v in va:
                s = {}
                val = v.split(' ')
                for i in range(len(ke)):
                    s[ke[i]] = val[i]
                # 保存 房价走势
                lists.append(s)
            print(s)
            item_df['房价走势'] = lists
        except Exception as  e:
            print('无数据')
        try:
            chaxun.find_element_by_xpath('//a[@id="a_chart_price_bar_table"]').click()
            WebDriverWait(chaxun, 30, 0.2)
            time.sleep(5)
            ke = chaxun.find_element_by_xpath('//div[@id="chart_price_bar_table"]/table/thead').text.split(' ')
            va = chaxun.find_element_by_xpath('//div[@id="chart_price_bar_table"]/table/tbody').text.split('\n')
            lists = []
            for v in va:
                s = {}
                val = v.split(' ')
                for i in range(len(ke)):
                    s[ke[i]] = val[i]
                # 保存 房价结构
                lists.append(s)
            print(s)
            item_df['房价结构'] = lists
        except Exception as  e:
            print('无数据')
        try:
            chaxun.find_element_by_xpath('//div[@id="chart_total_line_title"]/span').click()
            WebDriverWait(chaxun, 30, 0.2)
            time.sleep(5)
            chaxun.find_element_by_xpath('//a[@id="a_chart_total_line_table"]').click()
            ke = chaxun.find_element_by_xpath('//div[@id="chart_total_line_table"]/table/thead').text.split(' ')
            va = chaxun.find_element_by_xpath('//div[@id="chart_total_line_table"]/table/tbody').text.split('\n')
            lists = []
            for v in va:
                s = {}
                val = v.split(' ')
                for i in range(len(ke)):
                    s[ke[i]] = val[i]
                # 保存 总价走势
                lists.append(s)
            print(s)
            item_df['总价走势'] = lists
        except Exception as  e:
            print('无数据')
        try:
            chaxun.find_element_by_xpath('//a[@id="a_chart_total_bar_table"]').click()
            WebDriverWait(chaxun, 30, 0.2)
            time.sleep(5)
            ke = chaxun.find_element_by_xpath('//div[@id="chart_total_bar_table"]/table/thead').text.split(' ')
            va = chaxun.find_element_by_xpath('//div[@id="chart_total_bar_table"]/table/tbody').text.split('\n')
            lists = []
            for v in va:
                s = {}
                val = v.split(' ')
                for i in range(len(ke)):
                    s[ke[i]] = val[i]
                # 保存 总价结构
                lists.append(s)
            print(s)
            item_df['总价结构'] = lists
        except Exception as  e:
            print('无数据')
        try:
            chaxun.find_element_by_xpath('//div[@id="chart_supply_line_title"]/span').click()
            WebDriverWait(chaxun, 30, 0.2)
            time.sleep(5)
            chaxun.find_element_by_xpath('//a[@id="a_chart_supply_line_table"]').click()
            ke = chaxun.find_element_by_xpath('//div[@id="chart_supply_line_table"]/table/thead').text.split(' ')
            va = chaxun.find_element_by_xpath('//div[@id="chart_supply_line_table"]/table/tbody').text.split('\n')
            lists = []
            for v in va:
                s = {}
                val = v.split(' ')
                for i in range(len(ke)):
                    s[ke[i]] = val[i]
                # 保存 出售供给
                lists.append(s)
            print(s)
            item_df['出售供给'] = lists
        except Exception as  e:
            print('无数据')
        try:
            chaxun.find_element_by_xpath('//div[@id="chart_huxing_line_title"]/span').click()
            WebDriverWait(chaxun, 30, 0.2)
            time.sleep(5)
            chaxun.find_element_by_xpath('//a[@id="a_chart_huxing_line_table"]').click()
            ke = chaxun.find_element_by_xpath('//div[@id="chart_huxing_line_table"]/table/thead').text.split(' ')
            va = chaxun.find_element_by_xpath('//div[@id="chart_huxing_line_table"]/table/tbody').text.split('\n')
            lists = []
            for v in va:
                s = {}
                val = v.split(' ')
                for i in range(len(ke)):
                    s[ke[i]] = val[i]
                # 保存 出售户型
                lists.append(s)
            print(s)
            item_df['出售户型'] = lists
        except Exception as  e:
            print('无数据')

        try:
            ls = chaxun.find_element_by_xpath('//div[@id="duibi"]/table/tbody').text.split('\n')
            lists = []
            for li in ls:
                item = {}
                t = li.split(' ')
                item['名称'] = t[0]
                item['位置(行政区+道路)'] = t[1] + ' ' + t[2]
                item['方位距离'] = t[3]
                item['用途'] = t[4]
                item['建筑类型'] = t[5]
                item['建筑年代'] = t[6]
                item['价格(元/㎡)'] = t[7]
                item['挂牌数量(套)'] = t[8]
                # 保存 附近楼盘
                # ys.fjlp_data.insert_one(s)
                lists.append(item)
            print(item)
            item_df['附近楼盘'] = lists
        except Exception as  e:
            print('无数据')
    except Exception as  e:
        print('无近5年数据')

    # 获取更多信息的页面url
    gd_url = chaxun.find_element_by_xpath('//a[@class="blue simsun"]').get_attribute('href')
    item_df['更多信息url'] = gd_url

    # 返回到最初页面
    chaxun.find_element_by_xpath('//img[@class="newHeader"]').click()
    return item_df, gd_url


def get_gd(url, item_dt):
    #     gd = webdriver.Chrome()
    #     gd.get(url)

    #     gd = webdriver.ChromeOptions()
    #     gd.add_argument('--proxy-server=http://'+get_proxy()+'')
    #     gd = webdriver.Chrome( chrome_options=options)
    #     gd.get(url)
    if url == 'http://www.fangchan.com/':
        return item_dt
    gd = ipget(url)

    WebDriverWait(gd, 30, 0.2)
    # gd = yanzheng(gd)
    ls = gd.find_elements_by_xpath('//ul[@class="assess-ul"]/li')
    for li in ls:
        t = li.text.split('：\n')
        item_dt[t[0]] = t[1]
    try:
        req = requests.get(
            'http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=Z8OaLxT8vIhoPHeAfp1ic1cbDBXMyZZu' %
            item_dt[
                '位置'])
        print(item_dt['位置'])
        jwd = req.json()['result']['location']
        item_dt['坐标'] = jwd
    except:
        wzaa = gd.find_elements_by_xpath("//div[@class='tbox clearfix']/h1")[0].text
        req = requests.get(
            'http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=Z8OaLxT8vIhoPHeAfp1ic1cbDBXMyZZu' % wzaa)
        print(wzaa)
        jwd = req.json()['result']['location']
        item_dt['坐标'] = jwd

    jj = gd.find_element_by_xpath('//div[@class="ha_infobox"]').text
    item_dt['简介'] = jj
    # 保存基础信息
    # jcsj_data.insert_one(jcitem)

    try:
        ls = gd.find_element_by_xpath('//div[@class="ucont1"]/table/tbody').text.split('\n')
        xqlist = []
        for li in ls:
            itema = {}
            t = li.split(' ')
            itema['周边小区名称'] = t[0]
            itema['行政区'] = t[1]
            itema['价格(元/㎡)'] = t[2]
            xqlist.append(itema)
        print(itema)
        item_dt['周边小区'] = xqlist
    except Exception as  e:
        print('无数据')

    gd.switch_to_frame('zbiframe')
    try:
        jt = gd.find_element_by_xpath('//ul[@class="bus_xx"]').text.replace('\n|\n', ',').replace('站\n', '站,').split(
            '\n')
        jtlist = []
        for li in jt:
            itemaa = {}
            t = li.split(',')
            itemaa['站名'] = t[0]
            itemaa['方向距离'] = t[1]
            itemaa['线路'] = t[2]
            jtlist.append(itemaa)
            # 保存 公共交通
        print(itemaa)
        item_dt['公共交通'] = jtlist
    except Exception as  e:
        print('无数据')

    titles = gd.find_element_by_xpath('//ul[@class="clearfix"]').text.split('\n|\n')
    lists = []
    for tit in titles:
        print(tit)
        gd.find_element_by_xpath("//li[@title='" + tit + "']").click()
        WebDriverWait(gd, 30, 0.2)
        time.sleep(5)
        st = gd.find_element_by_xpath("//ul[@id='map_right_tbody']").text
        ls = re.split(r'\n[A-Z]', st)
        ls[0] = ls[0][1:]

        for li in ls:
            try:
                itemaaa = {}
                t = li.split('\n')
                itemaaa[tit] = t[0]
                itemaaa['距离'] = t[1]
                # 保存 周边环境
                lists.append(itemaaa)
            except:
                print('无数据')
        print(itemaaa)
    item_dt['周边环境'] = lists
    gd.quit()
    return item_dt

def run1(chaxun, city_name, xq):
    try:
        item,url = mn_click(login, city_name, xq) # IP容易被封
        return item,url
    except Exception as e:
        print(e)
        chaxun1 = chaxun.find_element_by_xpath('//img[@class="newHeader"]').click()
        run1(chaxun, city_name, xq)
def run2(url, item):
    try:
        new_item = get_gd(url, item)
        return new_item
    except Exception as e:
        print(e)
        run2(url, item)


if __name__ == '__main__':
    logins = webdriver.ChromeOptions()
    logins.add_argument('HOSTS=119.167.208.147 www.creprice.cn')

    logins.add_argument(
        'User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36')
    login = webdriver.Chrome(chrome_options=logins)
    login.get("https://www.creprice.cn/")
    # browser = webdriver.Chrome()
    # browser.get("https://www.creprice.cn/")
    # # 登录
    login.find_element_by_xpath('//a[@class="link"]').click()
    time.sleep(2)
    # 切换iframe
    login.switch_to_frame('layui-layer-iframe1')
    login.find_element_by_xpath("//li[@class='i1 mb20']/input").send_keys('urasr')
    login.find_element_by_xpath("//li[@class='i2']/input").send_keys('urasr2018')
    login.find_element_by_xpath("//div[@class='mt20']/input").click()
    time.sleep(2)
    input()

    # 顺序取小区
    citys = info_base.find({}, {"city_name": 1, '标题': 1, "_id": 0})
    for length in range(citys.count()):
        city_name = citys[length]['city_name']
        xq = citys[length]['标题']
        # 判断是否爬取过
        if url_data.find_one({'已爬取的小区': xq}):
            continue
        # 把爬取的小区名存入

        item, url = run1(login, city_name, xq)  # IP容易被封
        new_item = run2(url, item)
        url_data.insert_one({'已爬取的小区': xq})
        if new_item == {}:
            continue
        xqxx_data.insert_one(new_item)

    # # 随机取小区
    # count = ys.info_base.find().count()
    # lis = []
    # for i in range(count):
    #     lis.append(i)
    # for i in range(count):
    #     length = random.choice(lis)
    #
    #     citys = ys.info_base.find({}, {"city_name": 1, '标题': 1, "_id": 0})[length]
    #     city_name = citys['city_name']
    #     xq = citys['标题']
    #     city = city_name + xq
    #     # 判断是否爬取过
    #     if ys.url_data.find_one({'已爬取的小区': city}):
    #         lis.remove(length)
    #         continue
    #     lis.remove(length)
    #     # 把爬取的小区名存入
    #     ys.url_data.insert_one({'已爬取的小区': city})
    #     url = mn_click(login, city)  # IP容易被封
    #     get_gd(url, city)