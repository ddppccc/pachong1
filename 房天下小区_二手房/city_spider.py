# -*- coding: utf-8 -*-
# 这是分城市的爬虫的标准件

import json
import os
import re
import time
from datetime import datetime, timedelta
from scrapy.crawler import CrawlerProcess, Settings
from multiprocessing import Process


# ==========================检测当月数据是否爬取函数==============================
def check_crawled(city_name, save_dir='data1', save_name=''):

    # 当前时间 -
    the_month = datetime.now() - timedelta(days=datetime.now().day)
    os.path.exists(save_dir) or os.makedirs(save_dir)
    dir_list = os.listdir(save_dir)
    dir_info = [re.findall('\d\d-\d\d-\d\d', i) for i in dir_list if (city_name in i) and (save_name in i)]
    dir_info = [{'date': datetime.strptime(info[0], '%y-%m-%d', ),
                 'file_path': os.path.join(save_dir, file_name)
                 } for info, file_name in
                zip(dir_info, dir_list) if len(info) == 1]
    crawled_city = list(filter(lambda info: info['date'] > the_month, dir_info))
    return crawled_city



# 创建多爬虫
def crawl_task(Spider, settings):
    # 调用scrapy爬虫对象爬取一个城市

    # 配置爬虫项目参数
    settings.get('clear_buffer', False) and print('5秒后开始爬取，本次操作将删除上一次的缓存，若需要请修改终止脚本后clear_buffer参数')
    time.sleep(5)
    process = CrawlerProcess(settings)
    process.crawl(Spider)
    process.start()
    process.join()


# 进程任务, 返回一个爬虫任务的进程对象  更新settings 信息
def crawl_city_process(city_name, spider_class, params):
    """
    进程任务, 返回一个爬虫任务的进程对象
    :param city_name: 要爬的城市名
    :param spider_class: 爬虫类
    :param params:
    :return:
    """

    # 检查当月数据是否已爬取
    if check_crawled(city_name, save_dir=params.get('save_dir', 'data1'), save_name=params.get('save_name', '')):
        print('%s当月数据已存在' % city_name)
        return
    print('%s当月数据缺失，开始爬取' % city_name)

    # 配置参数
    default_settings = {

        # 谷歌浏览器代理，防止网站认为程序是爬虫
        "USER_AGENT": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',

        # 设置用户代理
        'ROBOTSTXT_OBAY': False,
        "AUTOTHROTTLE_ENABLED": True,
        "ITEM_PIPELINES": {'pipeline.ItemPipeline': 300},
        'city_name': city_name,
        'clear_buffer': True,           # 是否删除上次缓存
        'save_name': '',                # 保存的数据类名 例如 18-10-09_东莞_安居客租金.xlsx， ‘安居客租金’为保存的数据类名
        'save_dir': 'data1',             # 保存的路径
        'DOWNLOAD_TIMEOUT': 10,         # 设置下载超时时间
        "LOG_LEVEL": 'INFO',
    }
    params.get('ITEM_PIPELINES') and params['ITEM_PIPELINES'].update(default_settings['ITEM_PIPELINES'])
    default_settings.update(params)
    # Spider = Spider
    settings = Settings()
    settings.update(default_settings)       # 自定义的setting添加到settings中
    default_settings.update(settings)       # 将settings添加到自定义的setting


    # 开启进程
    p = Process(target=crawl_task, args=(spider_class, settings))
    return p




with open(os.path.join(os.path.dirname(__file__), "city_code.json"), 'r', encoding='utf-8') as f:
    cities = json.load(f)



def city_loop(callback, cities=()):
    """
    每次传入callback函数一个城市名， 默认遍历所有城市
    :param callback: 回调函数， 传入回调函数的值是城市中文名(city_name)和城市拼音(city_pinyin)如：cityname='青岛', city_pinyin='qingdao'
    :param cities: cities传入需要处理的城市，默认全部处理
    :return: None
    """
    # 如果传入字符串则只处理一个城市
    if type(cities) is str:
        cities = (cities, )

    # 没有传入则默认遍历所有城市
    if not cities:
        # globals() 函数会以字典类型返回当前位置的全部全局变量。
        cities = globals()['cities']

    for city_name in cities:
        callback(city_name)


if __name__ == '__main__':
    # city_loop(lambda x: print(x))
    pass

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
