import time
import requests
from bs4 import BeautifulSoup as bs
import pymongo

from lxml import etree
from config import get_proxy,get_ua,delete_proxy,statis_output
from capter_verify.captcha_run import AJK_Slide_Captcha
from urllib import parse

MONGODB_CONFIG = {
   "host": "8.135.119.198",
   "port": "27017",
   "user": "hladmin",
   "password": parse.quote("Hlxkd3,dk3*3@"),
   "db": "dianping",
   "collections": "dianping_collections",
}
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    'Connection': 'close',
    "referer": "https://www.anjuke.com/sy-city.html",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}



def get_url(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)

    cs_url = html.xpath('//div[@class="content"]/div[@class="city-itm"]/div[@class="letter_city"]/ul/li/div[@class="city_list"]/a/@href')# /div[@class="letter_city"]/a
    cs_name = html.xpath('//div[@class="content"]/div[@class="city-itm"]/div[@class="letter_city"]/ul/li/div[@class="city_list"]/a/text()')
    csurl_list = []
    for i in range(len(cs_name)):
        item = {}
        item['城市名'] = cs_name[i]
        item['url'] = cs_url[i]
        csurl_list.append(item)


    return csurl_list




if __name__ == '__main__':
    url = 'https://www.anjuke.com/sy-city.html'
    s = get_url(url)
    print(s)