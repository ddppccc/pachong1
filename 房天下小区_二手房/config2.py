import requests
import time
def get_proxy():
    try:
        return requests.get('http://1.116.204.248:5454/proxy2').text
        # return requests.get('http://1.116.204.248:5000/proxy').text
        # return requests.get('http://demo.spiderpy.cn/get/').json()['proxy']
        # return requests.get('http://47.106.223.4:50002/get/').json()['proxy']
    except:
        num = 3
        while num:
            try:
                return requests.get('http://demo.spiderpy.cn/get/').json()['proxy']
            except:
                print('暂无ip，等待20秒')
                time.sleep(20)
                num -= 1
        print('暂无ip')