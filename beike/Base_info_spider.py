import csv
import random
import re
import time
import jsonpath
import pymongo
import requests
from bson import ObjectId
from lxml import etree

city_map_base = pymongo.MongoClient(host='127.0.0.1', port=27017)['Beike']['city_map']
info_base = pymongo.MongoClient(host='127.0.0.1', port=27017)['Beike']['info_new']

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'cookie': 'lianjia_ssid=38c77e0b-d46b-402f-917e-174595d13f1e; lianjia_uuid=e204ed92-d42b-4a6a-8fbd-6ef869d3886a; _smt_uid=5f8804cd.25b2ced1; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221752b52c1b53b6-03d9ed69788878-5b123211-2073600-1752b52c1b665f%22%2C%22%24device_id%22%3A%221752b52c1b53b6-03d9ed69788878-5b123211-2073600-1752b52c1b665f%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; select_city=340100; crosSdkDT2019DeviceId=-xf4acz-b283ki-nnhg81z5q0tllkp-e9qmx2qla; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiZjgyY2EwYjIwOWNlMjAwODYwNjE5ZmRlOTM4ZWNlNGJiYzYyYmJiMWE1NjRhNTc0NGVhZWZkZTg1NTgwMjhlM2I0YmNmMzBiZDNhNTA1OWVhMThhNjcxNGM2YzQ3OTM5MTYzYzMzZDZhOGU0OWEzOTdiNjFjYjU0N2ZmMjQ2MjExYWM3OTU2Y2M2YWM0YTRlZDRkMzFhM2JhMzUxYmVmMTE5ZGVhNzYzNDE2ZGVjOGEzMjY2NWQ3YTE5MTA5MDdiOGExYzRlNjJmNDQ4OWZiZmYzZWMwNWZhOTIzYmQwZTIwMmIxY2VhYjJlMWMxOGYwM2JmYzViYjViYzhiYWJkMGRhYjc0MTBlZjc5NDg1NmQxMzIxZjljYmE5MTkxZjFjYTZmNjlhNzFlOTBjNTRkNjdmZmJjYjEzNmJlMzY2Mzc2NGExY2JjYmRmOWQ3MzE2MDVlMTk0Yzg4NWJjMDY3ZFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJlZWFjZWVmYVwifSIsInIiOiJodHRwczovL3d3dy5rZS5jb20vY2l0eS8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ=='
}


def get_cityMap():
    count = 1
    sigle_info = {}
    city_map = {}
    url = 'https://www.ke.com/city/'
    resp = requests.get(url=url, headers=headers)
    city_map_source_code = resp.text
    tree = etree.HTML(city_map_source_code)
    li = tree.xpath('//ul[@class="city_list_ul"]/li')
    for citylist in li:
        city_li = citylist.xpath('./div[@class="city_list"]/div/ul/li')
        for info in city_li:
            city = info.xpath('string(./a)')
            url = info.xpath('./a/@href')[0]
            city_map['{}'.format(city)] = url
            sigle_info['_id'] = count
            sigle_info['city'] = city
            sigle_info['url'] = url
            sigle_info['sign'] = 1  # 未爬取城市
            if city in ['合肥', '北京', '厦门', '广州', '深圳', '佛山', '中山', '北海', '哈尔滨', '武汉', '长沙', '南京', '无锡', '沈阳', '大连', '太原',
                        '济南', '青岛', '烟台', '成都', '天津', '杭州']:
                sigle_info['has_data'] = 1
            else:
                sigle_info['has_data'] = 0  # 标记存在数据城市
            city_map_base.insert_one(sigle_info)
            count += 1
        if city == '诸暨':
            break
    return city_map


def statis_output(title, rowlist, database) -> object:
    csvfile = open('{}'.format(title), 'w+', newline='', encoding='utf-8')
    res_writer = csv.writer(csvfile, dialect='excel')
    res_writer.writerow(rowlist)
    for item in database.find():
        res_writer.writerow(list(item.values())[1:])


def get_city_info(data):
    for info in data:
        if info['sign'] == 0:
            continue
        item = {}
        item['id'] = ObjectId()
        city = info['city']
        city_url = info['url']
        url = 'https:' + city_url + '/fangjia/'

        # url = 'https://wuhu.ke.com/fangjia/'
        time.sleep(random.randint(10, 15) * 0.1 * 4)
        resp = requests.get(url=url, headers=headers)
        tree = etree.HTML(resp.text)
        tit = tree.xpath(
            'string(//div[@class="box-l"]/div[@class="box-l-t"]/div[@class="shuju"]/div/div[@class="tit"])')
        price = tree.xpath(
            'string(//div[@class="box-l"]/div[@class="box-l-t"]/div[@class="qushi"]/div[@class="qushi-2"]/span[@class="num"])')
        house_source = tree.xpath(
            'string(//div[@class="box-l"]/div[@class="box-l-t"]/div[@class="qushi"]/div[@class="qushi-2"]/span[last()]/a[1])')
        new_house = tree.xpath('string(//div[@class="box-l"]/div[@class="box-l-b"]/div[1]/div[@class="num"])')
        new_people = tree.xpath('string(//div[@class="box-l"]/div[@class="box-l-b"]/div[2]/div[@class="num"])')
        daikanliang = tree.xpath('string(//div[@class="box-l"]/div[@class="box-l-b"]/div[3]/div[@class="num"])')
        li = tree.xpath('string(//div[@class="menuLeft"]/ul/li[@data-action="click_name=地图找房"]/a/@href)')
        try:
            region_id = re.search(r'(\d+)', li).group(0)
        except:
            region_id = 0
        belong = city
        if tit == '':
            print('{}：该城市不存在该数据'.format(city))
            city_map_base.update_one({'city': city}, {"$set": {'sign': 0}})
            continue
        print(tit, price, house_source, new_house, new_people, daikanliang, belong, region_id)
        item['tit'], item['price'], item['house_source'], item['new_house'], item['new_people'], item[
            'daikanliang'], item['belong'], item[
            'region_id'] = tit, price, house_source, new_house, new_people, daikanliang, belong, region_id
        city_map_base.update_one({'city': city}, {"$set": {'has_data': 1}})
        info_base.insert_one(item)
        get_priceMap(city, city_url)


def get_priceMap(city, url):
    second_url = 'https:' + url + '/fangjia/priceMap/'
    time.sleep(random.randint(10, 15) * 0.1 * 4)
    json_resp = requests.get(url=second_url, headers=headers)
    try:
        quanpin_url = jsonpath.jsonpath(json_resp.json(), '$..quanpin_url')
        id_list = jsonpath.jsonpath(json_resp.json(), '$..id')
        cityMap = dict(zip(quanpin_url, id_list))
        for quanpin in cityMap.keys():
            quanpin_url = 'https:' + url + '/fangjia/{}/'.format(quanpin)
            time.sleep(random.randint(1, 15) * 0.1 * 4)
            resp = requests.get(url=quanpin_url, headers=headers)
            tree = etree.HTML(resp.text)
            tit = tree.xpath(
                'string(//div[@class="box-l"]/div[@class="box-l-t"]/div[@class="shuju"]/div/div[@class="tit"])')
            price = tree.xpath(
                'string(//div[@class="box-l"]/div[@class="box-l-t"]/div[@class="qushi"]/div[@class="qushi-2"]/span[@class="num"])')
            house_source = tree.xpath(
                'string(//div[@class="box-l"]/div[@class="box-l-t"]/div[@class="qushi"]/div[@class="qushi-2"]/span[last()]/a[1])')
            new_house = tree.xpath('string(//div[@class="box-l"]/div[@class="box-l-b"]/div[1]/div[@class="num"])')
            new_people = tree.xpath('string(//div[@class="box-l"]/div[@class="box-l-b"]/div[2]/div[@class="num"])')
            daikanliang = tree.xpath('string(//div[@class="box-l"]/div[@class="box-l-b"]/div[3]/div[@class="num"])')
            belong = city
            if tit == '':
                print('{}：该城市不存在该数据'.format(quanpin))
                continue
            city_local = {}
            city_local['tit'], city_local['price'], city_local['house_source'], city_local['new_house'], city_local[
                'new_people'], city_local['daikanliang'], city_local[
                'belong'], city_local[
                'region_id'] = tit, price, house_source, new_house, new_people, daikanliang, belong, cityMap[quanpin]

            print(tit, price, house_source, new_house, new_people, daikanliang, belong, cityMap[quanpin])
            city_map_base.update_one({'city': quanpin}, {"$set": {'has_data': 1}})
            info_base.insert_one(city_local)

        city_map_base.update_one({'city': city}, {"$set": {'sign': 0}})
    except:
        print("{}:该城市不存在数据集".format(city))


def fresh_city_map():
    for info in city_map_base.find():
        city_map_base.update_one({'city': info['city']}, {"$set": {'sign': 1}})


if __name__ == '__main__':
    # get_cityMap()
    fresh_city_map()
    while True:
        current_time = time.localtime(time.time())
        if (current_time.tm_hour == 10 and current_time.tm_min == 23 and current_time.tm_sec == 0):
            info_base.drop()
            count = 3
            # get_cityMap()  # 获取城市映射 运行一次即可
            has_data = city_map_base.find({'has_data': 1}, no_cursor_timeout=True)
            get_city_info(has_data)
            while count > 0:
                for city in has_data:
                    if city['sign'] == 1:
                        get_city_info(has_data)
                count -= 1
            has_data.close()
            statis_output('贝壳二手房_全国_{}_贝壳指数.csv'.format(time.strftime("%Y-%m-%d", time.localtime())),

                          ['地区', '单价', '在售房源', '新增房', '新增客', '带看量', '从属', 'ID'], info_base)

            has_data = city_map_base.find({'has_data': 0},no_cursor_timeout=True)
            get_city_info(has_data)
            while count > 0:
                for city in has_data:
                    if city['sign'] == 1:
                        get_city_info(has_data)
                count -= 1
            fresh_city_map()
            has_data.close()
