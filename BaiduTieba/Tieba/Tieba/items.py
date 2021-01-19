# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Posts(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    getdate = scrapy.Field()
    getYear = scrapy.Field()
    getMonth = scrapy.Field()
    postsBar = scrapy.Field()
    postsID = scrapy.Field()
    author_nickname = scrapy.Field()
    author_name = scrapy.Field()
    postsNum = scrapy.Field()
    PostsTitle = scrapy.Field()

class Comment(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    postsID = scrapy.Field()
    getYear = scrapy.Field()
    getMonth = scrapy.Field()
    getdate = scrapy.Field()
    comment = scrapy.Field()
    floor = scrapy.Field()
    pubData = scrapy.Field()
