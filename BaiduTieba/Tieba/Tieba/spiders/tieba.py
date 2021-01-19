# -*- coding: utf-8 -*-
import json
import re
import arrow
import pymongo
import scrapy
from scrapy import Selector
from bson import ObjectId
from .logistics import save_city, check_city
from ..items import Posts, Comment

Tiezi_data = pymongo.MongoClient(host='127.0.0.1', port=27017)['BaiduTieba']['Tiezi']


class TiebaSpider(scrapy.Spider):
    name = 'tieba'

    allowed_domains = ['tieba.baidu.com']

    def start_requests(self):
        with open('city_map.json', encoding='utf-8') as fp:
            cities = ["{city}".format(city=i) for i in json.load(fp).keys()]
            # cities = {"深圳": "sz"}
        for city in cities:
            print('当前贴吧: ', city)

            if check_city(city):
                print('已经抓取过: ', city)
                continue
            # 页数
            for page in range(1):
                url = 'https://tieba.baidu.com/f?kw={city}&ie=utf-8&pn={page}'.format(city=city, page=page * 50)
                yield scrapy.Request(url=url, callback=self.parse_tiezi_info,
                                     meta={'city': city, 'page': page})

    def parse_tiezi_info(self, response):
        if '抱歉' in response.xpath('/html/body/div[2]/div/div[2]/div[1]/h2/text()').get(''): return
        city, page = response.meta['city'], response.meta['page']
        # print(response.body.decode('utf-8'))
        forum_posts_li = Selector(text=re.findall('<ul id="thread_list".*>', response.body.decode('utf-8'), re.S)[0]).xpath('.//li')

        for li in forum_posts_li:
            postsData = json.loads(li.xpath('./@data-field').get()) if li.xpath('./@data-field').get() else {}
            if postsData:
                Post = Posts()
                Post['getdate'] = arrow.now().strftime("%Y-%m-%d")
                Post['getYear'] = arrow.now().date().year
                Post['getMonth'] = arrow.now().date().month
                Post['postsBar'] = city
                Post['postsID'] = postsData['id']
                Post['author_nickname'] = postsData['author_nickname']
                Post['author_name'] = postsData['author_name']
                Post['postsNum'] = postsData['reply_num']
                # 详情
                url = 'https://tieba.baidu.com/p/{}'.format(postsData['id'])
                # url = 'https://tieba.baidu.com/p/6424375276'
                yield scrapy.Request(url=url, callback=self.info_parse, meta={'data': Post, "city": city})
        # 保存抓取的
        save_city(city)

    def info_parse(self, response):
        Post = response.meta['data']
        city = response.meta['city']
        title = response.xpath('//*[@id="j_core_title_wrap"]//h1/@title').get() \
                or response.xpath('//*[@id="j_core_title_wrap"]//h3/@title').get()

        Postes = Posts()
        Postes['_id'] = ObjectId()
        Postes['PostsTitle'] = title
        Postes['getdate'] = arrow.now().strftime("%Y-%m-%d")
        Postes['postsBar'] = Post['postsBar']
        Postes['postsID'] = Post['postsID']
        Postes['author_nickname'] = Post['author_nickname']
        Postes['author_name'] = Post['author_name']
        Postes['postsNum'] = Post['postsNum']
        Postes['getYear'] = arrow.now().date().year
        Postes['getMonth'] = arrow.now().date().month
        Tiezi_data.insert_one(Postes)
        # yield {'data':[Postes]}

        # 回复内容
        totalPage = response.xpath('//*[@id="thread_theme_5"]/div[1]/ul/li[2]/span[2]/text()').get() or '1'
        reply_div = response.xpath("//*[@id='j_p_postlist']/div[@data-pid]")
        # comment_data = {}
        allData = []
        for reply in reply_div:
            comment = Comment()
            comment['postsID'] = Post['postsID']
            comment['getYear'] = Post['getYear']
            comment['getMonth'] = Post['getMonth']
            comment['getdate'] = Post['getdate']
            comment['comment'] = reply.xpath(".//cc//div[@id]/text()").get().strip()
            # 以表情或者图片开头
            if comment['comment'] == '':
                comment['comment'] = reply.xpath(".//cc//div[@id]/img/text()").get()
            content_data = json.loads(reply.xpath("./@data-field").get())
            comment['floor'] = content_data['content']['post_no']
            try:
                comment['pubData'] = content_data['content']['date']
            except:
                comment['pubData'] = reply.xpath(".//div[@class='post-tail-wrap']/span[last()]/text()").get()

            allData.append(comment)
        if int(totalPage) > 1:
            print('当前贴吧: %s, 标题: %s, 回复页数: %s ' % (city, title, totalPage))
            # comment_data['comment_data'] = allData
            # print(comment_data)
            # Comment_data.insert_one(comment_data)
            yield {'data': allData}
        else:
            for i in range(1, int(totalPage) + 1):
                url = response.url + '?pn={}'.format(totalPage)
                yield scrapy.Request(url=url, callback=self.info_parse_page,
                                     meta={'postsID': Post['postsID'],
                                           'city': city,
                                           'title': title,
                                           'page': i,
                                           })

    def info_parse_page(self, response):
        postsID = response.meta['postsID']
        page = response.meta['page']
        title = response.meta['title']
        city = response.meta['city']

        print('当前贴吧: %s, 标题: %s, 回复页数: %s ' % (city, title, page))
        # 回复内容
        reply_div = response.xpath("//*[@id='j_p_postlist']/div[@data-pid]")
        # comment_data = {}
        allData = []
        for reply in reply_div:
            comment = Comment()
            comment['postsID'] = postsID
            comment['getYear'] = arrow.now().date().year
            comment['getMonth'] = arrow.now().date().month
            comment['getdate'] = arrow.now().strftime("%Y-%m-%d")
            comment['comment'] = reply.xpath(".//cc//div[@id]/text()").get().strip()
            content_data = json.loads(reply.xpath("./@data-field").get())
            comment['floor'] = content_data['content']['post_no']
            try:
                comment['pubData'] = content_data['content']['date']
            except:
                comment['pubData'] = reply.xpath(".//div[@class='post-tail-wrap']/span[last()]/text()").get()
            allData.append(comment)
            # comment_data['comment_data'] = allData
            # Comment_data.insert_one(comment_data)
        yield {'data': allData}
