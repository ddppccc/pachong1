import pymongo
import time
from lxml import etree
import requests
from config import typedict,MONGODB_CONFIG,fheaders,headers,citylist,getheaders,get_proxy
from urllib import parse
MONGODB_CONFIG = {
   "host": "8.135.119.198",
   "port": "27017",
   "user": "hladmin",
   "password": parse.quote("Hlxkd3,dk3*3@"),
   "db": "dianping",
   "collections": "dianping_collections",
}


def getregion(city):
   url=f'http://www.dianping.com/{city}/{typ}'
   for ii in range(1000):
      proxies = {"http": get_proxy()}
      try:
         r = requests.get(url, headers=getheaders(), proxies=proxies, timeout=5)
      except Exception as e:
         # print(e)
         continue
      if r.status_code == 200:
         r.encoding = 'utf8'
      else:
         # print('获取页面失败',r.status_code)
         continue
      if '页面不存在' in r.text:
         # print('页面不存在')
         # time.sleep(10)
         continue
      if '无效用户' in r.text:
         # print('无效用户')
         continue
      # res=requests.get(url,headers=headers)
      try:
         html = etree.HTML(r.text)
         box = html.xpath('//*[@id="region-nav"]/a')
      except:
         continue
      regionlist = []
      for i in box:
         data = {}
         url = i.xpath('./@href')[0]
         region = i.xpath('./span/text()')[0]
         data[region] = url.split('/')[-1]
         regionlist.append(data)
      return regionlist
typ='ch10'

l=getregion('chongqing')
print(l)