
import pymongo

has_spider = pymongo.MongoClient(host='127.0.0.1', port=27017)['安居客小区']['has_spider']



has_spider_list = has_spider.find()
for i in has_spider_list:
    print(i['金水'])