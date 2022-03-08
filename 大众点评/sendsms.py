# encoding=utf8
import requests
import hashlib
import time
import warnings
warnings.filterwarnings("ignore")
def sendsms(text):
    headers={
        'Content-Type':'application/json; charset="UTF-8"'
    }
    url='https://api-bj-shss01-mix2.zthysms.com/v2/sendSms'
    user='gxah666hy'
    pwd='HRLPdggg'
    ctime=str(int(time.time()))

    obj=hashlib.md5(pwd.encode('utf8'))         #MD5加密内容
    obj.update(''.encode('utf8'))                   #设置key值
    pwd1=obj.hexdigest()                           #加密
    obj=hashlib.md5(pwd1.encode('utf8'))         #MD5加密内容
    obj.update(ctime.encode('utf8'))                   #设置key值
    pwd2=obj.hexdigest()

    data={
        "username":user,
        "password":pwd2,
        "tKey":ctime,
        "mobile":"18523046785,18983869992",
        "content":text,
        "tine":"",
        "ext":"9999"
    }
    r=requests.post(url=url,json=data,headers=headers,verify=False)
    print(r.text)
    return
if __name__ == '__main__':
    # sendsms()
    obj = hashlib.md5(str(time.time()).encode('utf8'))  # MD5加密内容
    obj.update(''.encode('utf8'))  # 设置key值
    pid = obj.hexdigest()
    print(pid)