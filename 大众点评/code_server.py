# encoding=utf-8
import time
from  io import BytesIO
from PIL import Image
from flask_restful import Api, Resource, reqparse
import threading
import queue
from flask import Flask, request, send_from_directory,Response
from gevent import pywsgi
import base64
import pymongo
from urllib import parse
import os
MONGODB_CONFIG = {
   "host": "8.135.119.198",
   "port": "27017",
   "user": "hladmin",
   "password": parse.quote("Hlxkd3,dk3*3@"),
   "db": "dianping",
   "collections": "dianping_collections",
}
info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['大众点评']['cookie数据']






app = Flask(__name__,static_url_path='/static')
@app.route('/up',methods=['GET','POST'])
def func():
    parser = reqparse.RequestParser()  #方法二  从客户端获取数据
    parser.add_argument('image', type=str, required=True,help='imgString must be Base64 string')
    args = parser.parse_args()
    img = args['image']

    base_s1=base64.b64decode(img.encode())  #将str转换为bytes,并进行base64解码，得到bytes类型
    buf=BytesIO()   #内存中创建一个buf,用于存储图像文件内容
    buf.write(base_s1)  #将图像文件内容写入到该buf中，该buf相当于一个临时文件
    buf.seek(0)  #将文件指针放在文件开头
    data=Image.open(buf).convert('RGB')   #将buf作为文件名，读取该文件，并转换成RGB
    print(data)    #Image格式的文件数据
    data.save('static/code.png')
    return 'ok'

@app.route("/getcode")
def getcode():
    if info_base.find_one({'upload': 1}):
        with open("static/code.png", 'rb') as f:
            image = f.read()
        return Response(image, mimetype='image/jpeg')
    else:
        return '正在生成二维码，请不要离开本页面',200,[('refresh','2')]

@app.route('/')
def hello_world():
    return request.args.__str__()
if __name__ == '__main__':
    flag = False
    def a():
        while True:
            time.sleep(1)
            if info_base.find_one({'upload': 1}):
                print(info_base.find_one({'upload': 1}))
                flag = True
            print('0')
    t1 = threading.Thread(target=a)
    t1.start()
    # server = pywsgi.WSGIServer(('0.0.0.0', 5678), app)
    # server.serve_forever()

    # app.run('0.0.0.0:5678')
    time.sleep(100000)
