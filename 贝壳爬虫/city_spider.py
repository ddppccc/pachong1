# -*- coding: utf-8 -*-
# 这是分城市的爬虫的标准件
# =========爬取贝壳全部城市=========
import json
import os
import re
import time
from datetime import datetime, timedelta
from scrapy.crawler import CrawlerProcess, Settings
from multiprocessing import Process

from beike_map import get_esf_code_map


# 检查是否爬取过 [弃用]
def check_crawled(city_name, save_dir='data', save_name=''):
    the_month = datetime.now() - timedelta(days=datetime.now().day)
    os.path.exists(save_dir) or os.makedirs(save_dir)
    dir_list = os.listdir(save_dir)
    dir_info = [re.findall('\d\d-\d\d-\d\d', i) for i in dir_list if (city_name in i) and (save_name in i)]
    dir_info = [{'date': datetime.strptime(info[0], '%y-%m-%d', ),
                 'file_path': os.path.join(save_dir, file_name)
                 } for info, file_name in
                zip(dir_info, dir_list) if len(info) == 1]
    crawled_city = list(filter(lambda info: info['date'] > the_month, dir_info))
    return crawled_city  # [{'date': datetime.datetime(2019, 7, 24, 0, 0), 'file_path': './.idea'}]


# 开启爬虫任务
def crawl_task(Spider, settings):
    print('5秒后开始爬取，本次操作将删除上一次的缓存，若需要请修改终止脚本后clear_buffer参数')
    time.sleep(5)
    process = CrawlerProcess(settings)
    process.crawl(Spider)
    process.start()
    process.join()


# 开启爬虫
def crawl_city_process(city_name, spider_class):
    # 检查当月数据是否已爬取
    # if check_crawled(city_name, save_dir=params.get('save_dir', 'data'), save_name=params.get('save_name', '')):
    #     print('%s当月数据已存在' % city_name)
    #     return
    # print('%s当月数据缺失，开始爬取' % city_name)

    # 配置参数
    default_settings = {
        "USER_AGENT": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',

        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            # "Host": "www.ke.com",
            "Referer": "https://sz.ke.com/",
        },

        # 设置用户代理
        'ROBOTSTXT_OBAY': False,
        "AUTOTHROTTLE_ENABLED": True,
        "ITEM_PIPELINES": {'pipeline.ItemPipeline': 300},
        'city_name': city_name,
        'clear_buffer': False,  # 是否删除上次缓存
        'save_name': '',  # 保存的数据类名 例如 18-10-09_东莞_安居客租金.xlsx， ‘安居客租金’为保存的数据类名
        'save_dir': 'data',  # 保存的路径
        'DOWNLOAD_TIMEOUT': 10,  # 设置下载超时时间
        'HTTPERROR_ALLOWED_CODES': [302],
        "LOG_LEVEL": 'INFO',
    }
    # params.get('ITEM_PIPELINES') and params['ITEM_PIPELINES'].update(default_settings['ITEM_PIPELINES'])
    # default_settings.update(params)
    # Spider = Spider
    settings = Settings()
    settings.update(default_settings)
    default_settings.update(settings)

    p = Process(target=crawl_task, args=(spider_class, settings))
    return p


# ======================================================================================================================


# 城市 + 拼音映射表
with open("bk_city_map2.json", 'r', encoding='utf-8') as fp:
    cities = json.loads(fp.read())


# 返回城市列表
def city_loop(callback, cities=()):
    # 如果传入字符串则只处理一个城市
    if type(cities) is str:
        cities = (cities,)

    # 没有传入则默认遍历所有城市
    if not cities:
        cities = globals()['cities']  # globals() 函数会以字典类型返回当前位置的全部全局变量。

    for city_name in cities:
        callback(city_name)


if __name__ == '__main__':
    city_loop(lambda x: print(x))
    # pass

    # 调用爬虫process-spider例子
    # from city_spider import crawl_city_process
    # from city_spider import cities
    #
    # # cities = '沈阳'.split(',')
    # params = {
    #     'save_name': '智联',
    #     'DOWNLOAD_DELAY': .5,
    #     'COOKIES_ENABLED': True,
    #     'AUTOTHROTTLE_START_DELAY': .5,
    #     'DOWNLOADER_MIDDLEWARES': {
    #         '%s.ErrMiddleware' % (os.path.split(__file__)[-1].rsplit('.')[0]): 300,
    #     }
    #
    # }
    # for city_name in cities:
    #     p = crawl_city_process(city_name, JobSpiderSpider2, params)
    #     p and p.start()
    #     p and p.join()
    #
    # print("程序结束")
