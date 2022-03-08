
from urllib import parse
import pymongo

MONGODB_CONFIG = {
   "host": "8.135.119.198",
   "port": "27017",
   "user": "hladmin",
   "password": parse.quote("Hlxkd3,dk3*3@"),
   "db": "dianping",
   "collections": "dianping_collections",
}
cookie_data = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['大众点评']['cookie数据']
Cookie='_lxsdk_cuid=179c01ab88cc8-0df2f0b9256ac1-2363163-1fa400-179c01ab88cc8; _hc.v=fb783b09-adc2-78df-f8a5-7b53f530416c.1622425648; s_ViewType=10; _dp.ac.v=19b24d59-781c-4e11-94fc-d848cfb75d8f; ctu=21fd3f032ee980c9b98bee37cc18e7671d5ddb8684865c57d85b840ce1fe7fff; aburl=1; uuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; iuuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _lxsdk=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _ga=GA1.2.1975686433.1622713531; switchcityflashtoast=1; cityid=7; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1629444907; cy=9; cye=chongqing; fspop=test; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1631683812,1631842237,1632624328,1632706684; dplet=f936c5651e77e809d4a34c40522194a7; dper=ffc453d4de3fda2cc91b7aa202eb9f919c7bf8341cce158442e514a3278e39a20d86ae065ed22d99ab2a59e3899ebdfd1ccb324526d32a948d3096e298561064093118bfdd9b91c2ee8f43000c826a08501a29751f20f66c8afe2a6607a5f1f8; ll=7fd06e815b796be3df069dec7836c3df; ua=%E7%89%87%E7%89%87%E9%A2%9D; default_ab=index%3AA%3A3%7Cmyinfo%3AA%3A1; msource=default; chwlsource=default; pvhistory=6L+U5ZuePjo8L3N1Z2dlc3QvZ2V0SnNvbkRhdGE+OjwxNjMyNzIxNTU0NjY5XV9b; m_flash2=1; _lxsdk_s=17c25bca4eb-f9c-358-b6a%7C27839970%7C222; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1632722054'
cookiedata = cookie_data.find_one()
cookie_data.update_one(cookiedata, {"$set": {'Cookie':Cookie}})