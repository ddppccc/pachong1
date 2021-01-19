# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from .items import Posts,Comment

Comment_data = pymongo.MongoClient(host='127.0.0.1', port=27017)['BaiduTieba']['Comment']



class TiebaPipeline(object):
    def process_item(self, item, spider):
        Comment_data.insert_one(item)
        return item
