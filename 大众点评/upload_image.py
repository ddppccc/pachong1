import requests
import base64
url = 'http://1.116.204.248:5678//up'
def upload():
    with open('static/1.png','rb') as f:
        base_s=base64.b64encode(f.read()).decode() # 将图片以二进制的形式读入，并编码成base64，最后转换为str
        data={'image':base_s}
        response=requests.post(url,data=data)
        print(response.text)

