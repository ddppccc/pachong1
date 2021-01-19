import math, os
import time

import pandas as pd
import requests
from concurrent.futures.thread import ThreadPoolExecutor
from map import cities_code, categories_new


def get_proxy():
    return requests.get("http://47.106.223.4:50002/get/").json().get('proxy')


def delete_proxy(proxy):
    html = requests.get("http://47.106.223.4:50002/delete/?proxy={}".format(proxy))
    return html.text


def get_html(page, keyword, cityCode):
    url = 'https://capi.zhaopin.com/capi/position/searchV2?pageIndex={page}&pageSize=90&order=4&eventScenario=wxmpZhaopinSearchV2&S_SOU_WORK_CITY={citycode}&S_SOU_POSITION_NAME_QUERY={keyword}&S_SOU_POSITION_TYPE=1%3B2%3B4&cvNumber=JM745412187R90250000000&at={at}&rt={rt}&channel=wxxiaochengxu&v=1.0&platform=12&d=8F244A3B-AA8A-41E5-90B8-DADAB490A876&version=0.0.0'.format(
        page=page, citycode=cityCode, keyword=keyword, at=at, rt=rt)
    headers = {
        'Host': 'capi.zhaopin.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'content-type': 'application/json',
        'Referer': 'https://servicewechat.com/wxb7718fb9257e4fd2/90/page-frame.html',
        # 'Accept-Encoding': 'gzip, deflate, br',
    }
    # res = requests.get(url, headers=headers, verify=False)

    proxy = get_proxy()
    if "!" in str(proxy):
        print("没有ip, 等待60s")
        time.sleep(60)
    proxies = {
        "https": "https://{}".format(proxy),
        "http": "http://{}".format(proxy)
    }
    retry_count = 3
    while retry_count > 0:
        try:
            # print(url)
            res = requests.get(url, headers=headers, timeout=(2, 5), proxies=proxies)
            res.encoding = 'utf-8'
            return res
        except Exception as E:
            retry_count -= 1
            print('error!!', E)
            continue
    # 出错3次, 删除代理池中代理
    delete_proxy(proxy)
    return None


def parse(page, category, data, **kwargs):
    res = get_html(page, category, kwargs['mate']['city_code'])
    if not res: return
    resJson = res.json()
    # print(resJson)
    try:
        countNumber = int(resJson['data']['count'])
    except:
        print(resJson)
        return

    print('城市: %s,  职位: %s,  页数: %s,  数据总量: %s' % (kwargs['mate']['city'], category, page, countNumber))
    for li in resJson['data']['list']:
        item = {}
        item['城市'] = kwargs['mate']['city']
        item['区县'] = li.get('cityDistrict')
        # item['一级分类'] = kwargs['mate']['category']['level_1']
        item['主分类'] = kwargs['mate']['category']['level_2']
        item['次分类'] = kwargs['mate']['category']['level_3']

        item['职位名称'] = li.get('name')
        item['职位url'] = li.get('positionURL')
        item['薪资'] = li.get('salary')
        item['工作地点'] = li.get('workCity')
        item['发布时间'] = li.get('publishTime')

        item['企业名称'] = li.get('companyName')
        item['企业url'] = li.get('companyUrl')
        item['工作经验'] = li.get('workingExp')
        item['学历'] = li.get('education')
        item['公司规模'] = li.get('companySize')
        item['公司性质'] = li.get('property')
        # print(item)
        data.append(item)

    if countNumber <= 90 or page * 90 > countNumber:
        return
    else:
        current_page = page + 1
        parse(current_page, category, data=data, mate=kwargs['mate'])


def parse_1(city, cate, category_log, data, city_code, category):
    if city + '_' + cate + '\n' in category_log:  return
    parse(1, cate, data, mate={'city': city, 'city_code': city_code, 'category': category})

    df = pd.DataFrame(data)
    data_path = '小程序_data/{}-{}_{}.csv'.format(year, month, city)
    os.path.exists('小程序_data') or os.makedirs('小程序_data')
    if os.path.exists(data_path):
        df.to_csv(data_path, mode='a', header=False, encoding='utf-8', index=False)
    else:
        df.to_csv(data_path, mode='a', header=True, encoding='utf-8', index=False)

    # 保存抓取过的 工作分类
    save_category_path = '小程序_log/{}-{}_{}.txt'.format(year, month, city)
    with open(save_category_path, 'a', encoding='utf-8') as fp:
        word = '{}_{}'.format(city, cate)
        fp.writelines([word, '\n'])


def run(year, month):
    for city, city_code in cities_code.items():
        print(city, city_code)
        # if city != '深圳': continue
        if city in [i.split('_')[1].split('.')[0] for i in os.listdir('小程序_data')]:
            print(city, '已经存在')
            continue

        # 检测 当前分类是否抓取过
        save_category_path = '小程序_log/{}-{}_{}.txt'.format(year, month, city)
        try:
            with open(save_category_path, 'r', encoding='utf-8', errors='ignore') as fp:
                category_log = fp.readlines()
        except:
            category_log = []

        p = []
        for category in categories_new:
            data = []
            cate = category.get('level_3')
            pl = pool.submit(parse_1, city, cate, category_log, data, city_code, category)
            p.append(pl)
        [i.result() for i in p]


if __name__ == '__main__':
    # TODO 修改url中的 at, rt  最新版已经不封账号, 此处不用再修改
    # at = '48386fde7d304ae0acdfddc8d3b9a5de'
    # rt = 'eba215ce887b4a228d507cda54f51b08'
    at = ''
    rt = ''
    year, month = 2020, 12  # TODO 修改此处 月份
    pool = ThreadPoolExecutor(20)
    run(year, month)
    pool.shutdown()
