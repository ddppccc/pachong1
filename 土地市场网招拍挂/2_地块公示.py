# -*- coding: utf-8 -*-
import base64
import json
from lxml import etree

from selenium import webdriver
import os
import time
import datetime
import random
import re
import requests
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

url = 'https://www.landchina.com/publicDeal'

def base64_img(base):
    name = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
    imgdata = base64.b64decode(base.replace("data:image/bmp;base64,", ""))
    file = open('img/{}.jpg'.format(name), 'wb')
    file.write(imgdata)
    file.close()

    r = requests.post('http://127.0.0.1:7788', data=open('img/{}.jpg'.format(name), 'rb'))
    result = json.loads(r.text)['code']
    print(result)
    return result

def get_time_range_list(startdate, enddate):
    """
        切分时间段
    """
    date_range_list = []
    startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
    while 1:
        tempdate = startdate + datetime.timedelta(days=1)
        if tempdate > enddate:
            date_range_list.append((str(startdate.date()), str(enddate.date())))
            break
        date_range_list.append((str(startdate.date()), str((tempdate - datetime.timedelta(days=1)).date())))
        startdate = tempdate
    return date_range_list


def get_query(brows, time_part):
    time.sleep(1)
    for i in range(0, 10):
        try:
            mode_e = brows.find_elements_by_css_selector('input#TAB_queryTblEnumItem_210')
        except:
            continue
        if len(mode_e) == 0:
            time.sleep(1)
            continue
        else:
            break
    if len(mode_e) == 0:
        print('供应方式元素获取不到，无法输入')
        # sys.exit()

    win_handle = brows.window_handles
    for i in range(0, 10):
        try:
            mode_e[0].click()
        except:
            brows.refresh()
        time.sleep(1)
        new_win_handle = brows.window_handles
        if len(new_win_handle) >= 2:
            break
    for handle in new_win_handle:
        if handle not in win_handle:
            brows.switch_to.window(handle)
            time.sleep(0.5)
            try:
                np_e = brows.find_element_by_css_selector('a#treeDemo_3_a')
                np_e.click()
                time.sleep(0.5)
                btn = brows.find_element_by_css_selector('input.btnToolSmall')
                btn.click()
            except:
                if re.search('网站访问认证页面',brows.page_source):
                    img_src = etree.HTML(brows.page_source).xpath('string(//img[@class="verifyimg"]/@src)')
                    code = base64_img(img_src)
                    intext = brows.find_element_by_css_selector("#intext")
                    intext.send_keys(code)
                    time.sleep(0.5)
                    input_ = brows.find_element_by_xpath("//input[@type='submit']")
                    input_.click()
                    np_e = brows.find_element_by_css_selector('a#treeDemo_3_a')
                    np_e.click()
                    time.sleep(0.5)
                    btn = brows.find_element_by_css_selector('input.btnToolSmall')
                    btn.click()
                else:
                    brows.refresh()
                    np_e = brows.find_element_by_css_selector('a#treeDemo_3_a')
                    np_e.click()
                    time.sleep(0.5)
                    btn = brows.find_element_by_css_selector('input.btnToolSmall')
                    btn.click()
    win_handle = brows.window_handles
    brows.switch_to.window(win_handle[0])

    for i in range(0, 5):
        time_e_1 = brows.find_elements_by_css_selector('input#TAB_queryDateItem_79_1')
        if len(time_e_1) == 0:
            time.sleep(1)
            continue
        time_e_2 = brows.find_elements_by_css_selector('input#TAB_queryDateItem_79_2')
        if len(time_e_2) == 0:
            time.sleep(1)
            continue
        time_s = brows.find_elements_by_css_selector('input#TAB_QueryConditionItem79')
        if len(time_e_1) == 0 or len(time_e_2) == 0:
            print('不能输入时间')
            sys.exit()
        else:
            break

    #    time.sleep(0.5)
    try:
        time_e_1[0].clear()
    except:
        if re.search('网站访问认证页面', brows.page_source):
            img_src = etree.HTML(brows.page_source).xpath('string(//img[@class="verifyimg"]/@src)')
            code = base64_img(img_src)
            intext = brows.find_element_by_css_selector("#intext")
            intext.send_keys(code)
            time.sleep(0.5)
            input_ = brows.find_element_by_xpath("//input[@type='submit']")
            input_.click()
            time_e_1[0].clear()

        else:
            brows.refresh()
            time_e_1[0].clear()

    time_e_1[0].click()
    time.sleep(0.1)
    time_s[0].click()
    time.sleep(0.1)
    time_s[0].click()
    time_e_1[0].send_keys(time_part[0])
    time.sleep(0.5)
    time_e_2[0].clear()
    time_e_2[0].send_keys(time_part[1])
    time.sleep(3)
    for i in range(0, 5):
        query_e = brows.find_elements_by_css_selector('input#TAB_QueryButtonControl')
        if len(query_e) == 0:
            time.sleep(1)
            continue
        else:
            break
    if len(query_e) == 0:
        print('不能点击查询')
        sys.exit()
    query_e[0].click()
    return brows


def parse_list(brows, d_list):
    for i in range(0, 5):
        tab = brows.find_elements_by_css_selector('table#TAB_contentTable')
        if len(tab) == 0:
            time.sleep(1)
            continue
    if len(tab) == 0:
        return d_list
    tr_list = tab[0].find_elements_by_css_selector('tbody>tr')
    for i in range(1, len(tr_list)):
        td = tr_list[i].find_elements_by_css_selector('td')
        try:
            region = td[1].find_element_by_css_selector('span').get_attribute('title')
        except:
            try:
                region = td[1].text
            except:
                continue

        try:
            title_publicity = td[2].find_element_by_css_selector('span').get_attribute('title')
        except:
            title_publicity = td[2].text
        date_publicity = td[3].text
        a_href = tr_list[i].find_element_by_css_selector('a')
        detail_url = a_href.get_attribute('href')
        row = region + ',' + title_publicity + ',' + date_publicity + ',' + detail_url
        d_list.append(row)
    return d_list


def parse_part_page(bs, time_part):
    data_list = []
    time.sleep(random.randint(1, 15) * 0.1 * 4)
    brs = get_query(bs, time_part)
    total_page_re = re.compile(r'共(\d+)页')
    total_page_s = total_page_re.search(brs.page_source)
    if total_page_s is not None:
        total_page = int(total_page_s.group().replace('共', '').replace('页', ''))
    else:
        total_page = 1
    print('共' + str(total_page) + '页')
    print('第1页')
    data_list = parse_list(brs, data_list)
    try:
        print(data_list[0])
    except:
        pass

    for page in range(2, total_page + 1):
        time.sleep(random.randint(2, 5))
        try:
            next_e = brs.find_element_by_link_text('下页')
        except:
            time.sleep(10)
            brs.refresh()
            next_e = brs.find_element_by_link_text('下页')
        next_e.click()
        #        time.sleep(1)
        print('第' + str(page) + '页/' + str(total_page))
        # f = open('./土地log/地块公示log.txt', 'a')
        # f.write('第' + str(page) + '页/' + str(total_page))
        # f.close()
        data_list = parse_list(brs, data_list)
    f = open('土地数据/地块公示.csv', 'a')
    for d in data_list:
        try:
            f.write(d + '\n')
        except:
            continue
    f.close()


def main(startdate, enddate):

    date_list = get_time_range_list(startdate, enddate)
    print(date_list)

    # op = webdriver.ChromeOptions()
    # op.add_argument('-headless')
    bs = webdriver.Firefox()
    bs.get(url)
    if '验证' in bs.page_source:
        print('等待验证')
        img_src = etree.HTML(bs.page_source).xpath('string(//img[@class="verifyimg"]/@src)')
        code = base64_img(img_src)
        intext = bs.find_element_by_css_selector("#intext")
        intext.send_keys(code)
        time.sleep(0.5)
        input_ = bs.find_element_by_xpath("//input[@type='submit']")
        input_.click()
        time.sleep(3)
        time.sleep(10)

    time.sleep(5)
    for i in range(0, len(date_list)):

        # 判断是否存在
        try:
            if str(date_list[i]) + '\n' in open(r'土地log/地块公示log.txt', mode='r', encoding='utf-8').readlines():
                print("已经存在", date_list[i], '\n')
                continue
        except:
            pass
        print('waiting...')
        time.sleep(random.randint(1, 15) * 0.1 * 4)
        bs.refresh()
        try:
            parse_part_page(bs, date_list[i])

        except:

            print('wating.......longtime')
            bs.refresh()
            time.sleep(30)

            parse_part_page(bs, date_list[i])

        f = open('./土地log/地块公示log.txt', 'a', encoding='utf-8')
        f.write(str(date_list[i]))
        f.write('\n')
        f.close()

    bs.quit()


if __name__ == '__main__':
    startdate, enddate = '2021-8-3', '2021-9-23'
    main(startdate, enddate)
