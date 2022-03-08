# encoding=utf-8
from selenium import webdriver
import time
from config import rans
import pymongo
from config import MONGODB_CONFIG


cookie_data = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['大众点评']['cookie数据']
def P():
    cV="fb6c360293843bd0dd3b6df27189a350"
    # cV = f"fb6c3{rans(16)}df27{rans(2)}9a350"
    d = "fffffffffffffffffffffffffffffffffffbfffffffffffffffffffffffffc-loading|0|0|" + str(int((time.time()) * 1000)) + "-{\"v\":\"0.1.1\",\"ts\":" + str(int((time.time()) * 1000)) + ",\"cts\":" + str(int((time.time()) * 1000)) + ",\"brVD\":[402,882],\"brR\":[[402,882],[402,882],24,24],\"bI\":[\"https://m.dianping.com\",\"\"],\"broP\":[],\"aM\":\"\",\"cV\":\"" + cV + "\",\"wVU\":\"Google Inc. (Intel)\",\"wRU\":\"ANGLE (Intel, Intel(R) HD Graphics 4600 Direct3D11 vs_5_0 ps_5_0, D3D11-20.19.15.4531)\",\"aF\":\"-\",\"dV\":\"1|1|1\",\"mT\":[],\"kT\":[],\"aT\":[],\"tT\":[],\"dT\":[],\"sT\":[]}"
    # d="ffffffe0007ffffffffffffffffffffffff83ffffffffffffffffffffffffc-loading|0|0|1624246457082-{\"v\":\"0.1.1\",\"ts\":1624246457118,\"cts\":1624246457196,\"brVD\":[402,882],\"brR\":[[402,882],[402,882],24,24],\"bI\":[\"http://m.dianping.com\",\"http://www.dianping.com/\"],\"broP\":[],\"aM\":\"\",\"cV\":\"fb6c360293843bd0dd3b6df27189a350\",\"wVU\":\"Google Inc. (Intel)\",\"wRU\":\"ANGLE (Intel, Intel(R) HD Graphics 4600 Direct3D11 vs_5_0 ps_5_0, D3D11-20.19.15.4531)\",\"aF\":\"-\",\"dV\":\"0|0|0\",\"mT\":[],\"kT\":[],\"aT\":[],\"tT\":[],\"dT\":[],\"sT\":[]}"
    l = []
    for i in d:
        l.append(ord(i))
    d= [0 for index in range(len(l))]
    ee = int((len(l) - len(l) % 8) / 8)
    f=[2,3,4,5]
    x=[]
    for e in range(ee):
        # print(e)
        e=e*8
        b = [0 for index in range(8)]
        for k in range(len(f)):
            b[k] = f[k] ^ l[e + k]
            ff=f[k] << 1
            b[k]=ff ^ b[k]
            b[k+4] = f[k] ^ l[e + k+4]
            b[k],b[k+4] = b[k+4],b[k]
        # print(b)
        x=x+b
    # print(x)
    # print(len(x))
    t=len(x)
    while t<len(l):
        x.append(l[t])
        t += 1
    # print(x)
    # print(len(x))
    s = ''
    for a in x:
        xa = ('00' + str(hex(a)[2:]))[-2:]
        s = s + xa
    l = len(s)
    t = 202                                             #t值不确定
    b = int(l / 2)
    data = s[0:b] + str(hex(t)[2:]) + s[b:]
    # print(data)

    # time.sleep(1)
    driver.execute_script('document.close()')
    # time.sleep(1)
    driver.execute_script("document.write(btoa(cjyfunction('%s', {'to': 'string'})))" % data)
    # time.sleep(1)
    token = driver.find_elements_by_xpath('/html/body')[0].text
    # print(token)
    # driver.close()
    return token
if __name__ == '__main__':
    driver = webdriver.Chrome()
    # driver = webdriver.Firefox()
    driver.get("http://1.116.204.248:1234/test/")
    print('窗口打开成功')
    while True:
        token=P()
        print('获取token成功',time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        cookiedata = cookie_data.find_one()
        cookie_data.update_one(cookiedata, {"$set": {'token':token}})
        with open('token.txt','w') as f:
            f.write(token)
        time.sleep(6)

import base64
# name = "javascript"
# print(base64.b64encode(name.encode()))
# print(base64.b64decode(b'Q2hpbmHvvIzkuK3lm70=').decode())

