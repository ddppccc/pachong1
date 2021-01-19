import pymongo


def check_city(city):
    city_list = []
    citys = pymongo.MongoClient(host='127.0.0.1', port=27017)['BaiduTieba']['citys']
    for item in citys.find():
        city_list.append(item['city'])
    if city in city_list:
        return True
    else:
        return False

def save_city(city):
    print('正在保存已经爬取贴吧：{}'.format(city))
    citys = pymongo.MongoClient(host='127.0.0.1', port=27017)['BaiduTieba']['citys']
    item = {}
    item['city'] = city
    for _ in citys.find():
        if city == _['city']:
            return
    citys.insert_one(item)


def show_hasspider():
    city_list = []
    tiezi = pymongo.MongoClient(host='127.0.0.1', port=27017)['BaiduTieba']['Tiezi']
    for city in tiezi.find():
        city_list.append(city['postsBar'])
    print(list(set(city_list)))

