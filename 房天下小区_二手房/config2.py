import time

import requests
import time
def get_proxy():
    # return 'http://H041YJYT015P8T3D:0B6839D706F30F56@http-dyn.abuyun.com:9020'
    while True:
        try:
            response = requests.get('http://47.111.226.234:8000/getip2/')
            if response.status_code == 200:
                return response.text
            else:
                time.sleep(1)
        except:
            print('暂无ip')