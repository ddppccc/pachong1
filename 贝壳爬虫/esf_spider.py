import datetime
import json
import os
import random
import re
import time
import uuid
import numpy as np
import scrapy

from beike_map import get_regions, get_esf_code_map
from city_spider import crawl_city_process
from city_spider import cities
from config import make_date

year, month, day = make_date()


class Spider(scrapy.Spider):
    name = "BeiKe_esf"

    def start_requests(self):

        self.city_name = self.settings.get("city_name", '全国')
        city_names = list(filter(lambda x: self.city_name in x, cities))
        print("city_names", city_names)

        if not city_names:
            print("没有找到城市: %s" % self.city_name)
            return

        # 有数据  生成区县字典
        regions, cj = get_regions(self.city_name, cities)
        city_name = self.city_name
        for region_name, base_url in regions.items():
            url = base_url

            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 meta={
                                     'item': {'base_url': base_url,
                                              'region_name': region_name,
                                              'city': city_name}
                                 })

    # 获取district详情信息
    def parse(self, response):
        item = response.meta['item']
        city = item['city']
        district = item['region_name']
        dist_url = item['base_url']

        if '人机认证' in response.text:
            print('需要人机验证: ', response.url)
            time.sleep(60*10)   # 等待自己消失

        houses = response.xpath("//ul[@log-mod='list']//li[@class='clear']")
        if houses:
            for house in houses:
                items = {}
                items['id'] = uuid.uuid1(node=random.randint(100, 9999999))
                items['城市'] = city
                items['区县'] = district
                items['标题url'] = house.xpath(".//div[@class='title']/a/@href").get()
                items['小区'] = house.xpath(".//div[@class='positionInfo']/a/text()").get()
                houseInfo = "".join(house.xpath("./div/div[2]/div[2]/text()").extract()).replace(" ", "").replace("\n", "")

                # 户型
                items['户型'] = "".join(re.findall('\d室\d{0,1}厅{0,1}', ''.join([type_info for type_info in houseInfo.split('|') if '室' in type_info])))
                if len(items['户型']) == 0:
                    items['户型'] = np.NaN

                # 面积
                area = "".join(re.findall('(\d+\.?\d+)平米', "".join([type_info for type_info in houseInfo.split('|') if '米' in type_info])))
                try:
                    items['面积'] = float(area)
                except:
                    items['面积'] = np.NaN

                # 楼层
                items['楼层'] = "".join(re.findall("(.*\))", "".join([type_info for type_info in houseInfo.split('|') if '层' in type_info])))
                if len(items['楼层']) == 0:
                    items['楼层'] = np.NaN

                # 建筑年份
                houseYear = "".join(re.findall('(\d+)年', ''.join( [type_info for type_info in houseInfo.split('|') if '建' in type_info])))
                try:
                    items['建筑年份'] = int(houseYear)
                except:
                    items['建筑年份'] = np.NaN

                # 朝向
                items['朝向'] = "".join(
                    ''.join([type_info for type_info in houseInfo.split('|') if '东' in type_info or '西' in type_info \
                             or '南' in type_info or '北' in type_info]))
                if len(items['朝向']) == 0:
                    items['朝向'] = np.NaN

                flower = "".join(house.xpath("./div/div[2]/div[3]/text()").extract()).replace(" ", "").replace("\n", "")
                items['关注人数'] = ''.join(re.findall('(\d+)人', flower))
                if len(items['关注人数']) == 0:
                    items['关注人数'] = np.NaN

                # 标签
                items['标签'] = "|".join(house.xpath("./div/div[2]/div[4]/span/text()").extract())
                if len(items['标签']) == 0:
                    items['标签'] = np.NaN

                # 总价
                totalPrice = house.xpath(".//div[@class='totalPrice']/span/text()").get() + \
                             house.xpath(".//div[@class='totalPrice']/text()").get()
                totalPrice = "".join(re.findall('(\d+\.?\d+)万', str(totalPrice)))
                try:
                    items['总价'] = float(totalPrice)
                except:
                    items['总价'] = np.NaN

                # 单价
                unitPrace = house.xpath(".//div[@class='unitPrice']/span/text()").get()
                unitPrace = "".join(re.findall('(\d+\.?\d+)元', unitPrace))
                try:
                    items['单价'] = float(unitPrace)
                except:
                    items['单价'] = np.NaN

                items['抓取时间'] = f'{year}-{month}-28'
                items['抓取年份'] = year
                items['抓取月份'] = month
                items['数据来源'] = '贝壳'

                items['地址'] = np.NaN
                yield items

            next_page = json.loads(response.xpath("//div[@class='page-box house-lst-page-box']/@page-data").get())
            totalPage = next_page['totalPage']
            curPage = next_page['curPage']

            for i in range(curPage, totalPage + 1):
                curPage = i + 1
                if curPage > totalPage:
                    print(f'{district}\t总页数：{totalPage}, 已经爬完')
                    return
                else:
                    print(f'当前城市：{city},\t当前区：{district},\t总页数：{totalPage}, 当前页：{curPage}')
                    next_page_url = dist_url + 'pg' + str(curPage) + '/'
                    yield scrapy.Request(next_page_url, callback=self.parse,meta={'item': item})
                break


if __name__ == '__main__':
    # TODO 每个月跑程序之前 清理下上个月缓存的数据 位置: data/esf
    # TODO 修改每月抓取时间(可自定义), 位置 config >> make_date

    # 生成最新的esf映射表
    get_esf_code_map()

    params = {
        'save_dir': "data/esf",  # 保存位置
        'save_name': 'beke_esf'  # 保存数据名,
       }

    for city_name in cities:  #
        print("城市: ", city_name)
        if city_name in [i.split('_')[1] for i in os.listdir('data/esf')]:
            continue
        p = crawl_city_process(city_name, Spider, params=params)
        if p:
            p.start()
            p.join()
