# encoding: utf-8
# @author: LQK
# @desc: 改用api 获取数据
# @version: 0.2
# @Time: 2020/06/24


import time
import os
import re
from concurrent.futures.thread import ThreadPoolExecutor

import requests
import pandas as pd
from datetime import datetime
from scrapy import Selector

from config import get_script_data
from map import categories, regionMap


# 56
def parseJob(url, **kwargs):
    while True:
        try:
            r = get_script_data(url)
            break
        except Exception as e:
            print('error!!', e)
            time.sleep(1)
            continue
    response = Selector(text=r)

    # 工作列表页
    job_list = response.xpath("//ul[@class='jobs-list']//li")

    if not job_list:
        print("城市: %s, 区县: %s, 主分类: %s, 次分类: %s,  没有数据" % (
            kwargs['city'], kwargs['region'], kwargs['category_first'], kwargs['category']))
        # 保存抓取过的 工作分类
        save_category_path = 'log/{}-{}_{}.txt'.format(year, month, kwargs['city'])
        with open(save_category_path, 'a', encoding='utf-8') as fp:
            word = '{}_{}'.format(kwargs['region'], kwargs['category'])
            fp.writelines([word, '\n'])
        return

    print("城市: %s, 区县: %s, 主分类: %s, 次分类: %s, 页数: %s" % (
        kwargs['city'], kwargs['region'], kwargs['category_first'], kwargs['category'], kwargs['page']))
    for jobs in job_list:
        item = {}
        item['城市'] = kwargs['city']
        item['区县'] = kwargs['region']
        item['主分类'] = kwargs['category_first']
        item['次分类'] = kwargs['category']
        item['职位名称'] = jobs.xpath(".//span[@class='job-name']/@title").get()
        item['职位url'] = jobs.xpath(".//a[@class='left-box']/@href").get()
        item['薪资'] = jobs.xpath(".//span[@class='salary']/text()").get()
        # item['发布时间'] = '20' + jobs.xpath(".//span[@class='release_time']/text()").get()

        item['企业名称'] = jobs.xpath(".//a[@class='right-box']/div[@class='title']/@title").get()
        item['企业url'] = jobs.xpath(".//a[@class='right-box']/@href").get()
        text = jobs.xpath(".//span[@class='salary']/following-sibling::span/text()").get()
        item['工作经验'] = text.split('|')[1].strip()
        item['学历'] = text.split('|')[2].strip()
        item['工作地点'] = text.split('|')[0].strip()

        text2 = jobs.xpath(".//a[@class='right-box']/div[@class='right-box-tag']/text()").get()
        item['公司规模'] = text2.split('|')[1].strip()
        item['公司性质'] = text2.split('|')[0].strip()
        kwargs['data'].append(item)
        print("item: " ,item)

    print()
    # 获取下一页的数据
    next_page = response.xpath("//span[@class='search_page_next']/a/@href").get()
    if not next_page:
        # 保存抓取过的 工作分类
        save_category_path = 'log/{}-{}_{}.txt'.format(year, month, kwargs['city'])
        with open(save_category_path, 'a', encoding='utf-8') as fp:
            word = '{}_{}'.format(kwargs['region'], kwargs['category'])
            fp.writelines([word, '\n'])

        # 保存数据
        df = pd.DataFrame(data=kwargs['data'])
        data_path = 'data/{}-{}_{}.csv'.format(year, month, kwargs['city'])
        if os.path.exists(data_path):
            df.to_csv(data_path, mode='a', header=False, encoding='utf-8', index=False)
        else:
            df.to_csv(data_path, mode='w', header=True, encoding='utf-8', index=False)


    else:
        page = re.findall("/p(\d+)/", next_page)[0]
        next_page_url = "http://jobs.zhaopin.com" + next_page
        parseJob(next_page_url, city=kwargs['city'], region=kwargs['region'],
                 category_first=kwargs['category_first'], category=kwargs['category'],
                 page=page, data=kwargs['data'])


def run():
    pool = ThreadPoolExecutor(5)
    print("regionMap: ", regionMap.keys())
    print("len(regionMap): ", len(regionMap.keys()))

    for city, regionDict in regionMap.items():
        print(city, regionDict)
        if city == '洋浦市': continue
        if city != '合肥': continue
        # if city in [os.path.splitext(i)[0].split('_')[1] for i in os.listdir('data')]:
        #     continue

        # 检测 当前分类是否抓取过
        save_category_path = 'log/{}-{}_{}.txt'.format(year, month, city)
        if os.path.exists(save_category_path):
            print("save_category_path: ", save_category_path)
            with open(save_category_path, 'r', encoding='utf-8', errors='ignore') as fp:
                category_log = fp.readlines()
        else:
            category_log = []

        for region, region_url in regionDict.items():
            print('城市: %s, 区县: %s' % (city, region))
            if region != '':continue

            # 拼接 招聘岗位
            for category_first, category_first_dict in categories.items():

                p = []
                for category, category_code in category_first_dict.items():
                    if region + '_' + category + '\n' in category_log:
                        continue
                    data = []
                    url = region_url + category_code + '/'
                    # print("城市: %s,  区县: %s, 一级分类: %s,  二级分类: %s, 链接: %s" %
                    #       (city, region, category_first, category, url))
                    # parseJob(url, city=city, region=region, category_first=category_first,
                    #          category=category, page=1, data=data)
                    done = pool.submit(parseJob, url, city=city, region=region, page=1, data=data,
                                       category_first=category_first, category=category)
                    p.append(done)
                [obj.result() for obj in p]
    pool.shutdown()


if __name__ == '__main__':
    # year, month = datetime.now().year, datetime.now().month
    year, month = 2020,  6
    os.path.exists('data') or os.makedirs('data')
    os.path.exists('log') or os.makedirs('log')
    run()
