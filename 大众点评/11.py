# coding=utf-8
import requests
import time
# for i in range(100):
#     print(requests.get('http://47.106.223.4:50002/get/').json().get('proxy'))
# for i in range(100):
#     print(requests.get('http://118.24.52.95:5010/get/').json().get('proxy'))


# for i in range(100):
#     print(requests.get('http://192.168.1.131:5010/get/').json().get('proxy'))

from selenium import webdriver
from selenium.webdriver import ChromeOptions
option = ChromeOptions()



from fake_useragent import UserAgent

print()

print(' ')
headers = {
        'Connection': 'keep-alive',
        'Host': 'www.dianping.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        # 'User-Agent':  UserAgent().chrome,
        # 'Cookie': 'fspop=test; cy=9; cye=chongqing; _lxsdk_cuid=179c01ab88cc8-0df2f0b9256ac1-2363163-1fa400-179c01ab88cc8; _lxsdk=179c01ab88cc8-0df2f0b9256ac1-2363163-1fa400-179c01ab88cc8; _hc.v=fb783b09-adc2-78df-f8a5-7b53f530416c.1622425648; s_ViewType=10; _dp.ac.v=19b24d59-781c-4e11-94fc-d848cfb75d8f; ctu=21fd3f032ee980c9b98bee37cc18e7671d5ddb8684865c57d85b840ce1fe7fff; aburl=1; cityid=9; default_ab=shopList%3AA%3A5; ua=dpuser_1966568564; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1622430936,1622599018,1622622578,1622684317; dper=989da530f9ae3713022e170efc199d424fbd595e54994bc85947fd9f29ed441d5ad1ab9e2e57880ec5c6d0064a0712390a38646ccaac0670ba2affafff2ddb2de5a6575b1004c83b5ae7f3395eba0ca6d9b132de2b248b53a54ceea5c6d51636; ll=7fd06e815b796be3df069dec7836c3df; uamo=18523046785; dplet=5f4edba1e07f6f53950ca9020d8c330d; _lxsdk_s=179cf85b559-dcb-2cd-df8%7C%7C262; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1622686321'
    }
while 1:
    url='http://www.dianping.com/'
    ip = requests.get('http://192.168.1.104:5010/get/').json().get('proxy')
    proxies = {"http": ip}
    try:
        # print('get',proxies)
        res=requests.get(url=url,headers=headers,proxies=proxies,timeout=2)
    except:continue
    print(res.status_code)
    if res.status_code==200:
        option.add_argument(('--proxy-server=' + ip))
        driver = webdriver.Chrome(options=option)
        driver.get(url='http://www.dianping.com/shop/k7vol23SSMrz1OIp')
        time.sleep(2)
        # driver.execute_script("window.scrollBy(0,100)")
        driver.execute_script('document.close()')
        try:
            driver.execute_script("document.write(window.sessionStorage._lxsdk_cuid)")
        except:
            driver.close()
            continue
        time.sleep(2)
        cuid = driver.find_elements_by_xpath('/html/body')[0].text
        time.sleep(2)
        driver.close()
        if cuid == 'undefined':
            driver.close()
            continue
        print(cuid)
        
    else:continue
    time.sleep(5)

import numpy as np
# x = np.array([1,3,5,7,9])
# z = x > 5
# a=np.where(z,x,5)
# print(a)
#
# y = np.array([19,35,15,25,10])
# z = y > 18
# a=np.where(z)
# print(a)


# x = np.array([[1,2],
#               [4,5],
#               [7,8]])
# print(np.cumsum(x,axis=1))
# print(np.cumprod(x,axis=0))

# x = np.array([[12,1,7],
#               [6,0,3],
#               [5,4,8]])
# print(np.argmin(x,axis=0))
# print(np.argmax(x,axis=1))

# x = np.array([[2,1,7],
#               [6,0,3],
#               [5,4,8]])
# print(np.sort(x))
# print(np.sort(x,axis=0))

# x = np.array([19,35,15,25,10,11,2,3,2,19,11])
# y = np.array([10,11,2,3,2])
# z = np.array([2,3,2,454,44,5,8,11])
# print(np.unique(x))
# print(np.in1d(x,y))
# print(np.intersect1d(x,z))
# print(np.union1d(x,z))
# print(np.setdiff1d(x,z))
# print(np.setxor1d(x,z))

import pandas as pda
# 使用pandas生成数据
# Series代表某一串数据 index指定行索引名称，Series索引默认从零开始
# DataFrame代表行列整合出来的数据框,columns 指定列名
a = pda.Series([8, 9, 2, 1], index=['one', 'two', 'three', 'four'])
# 以列表的格式创建数据框
b = pda.DataFrame([[5,6,2,3],[3,5,1,4],[7,9,3,5]], columns=['onex', 'twox', 'threex', 'fourx'],index=['one', 'two', 'three'])
# 以字典的格式创建数据框
c = pda.DataFrame({
 'one':4, # 会自动补全
 'two':[6,2,3],
 'three':list(str(982))
})
# b.head(行数)# 默认取前5行头
# b.tail(行数)# 默认取后5行尾
# b.describe() 统计数据的情况  count mean std min 25% max
# e = b.head()
# f = b.describe()
# 数据的转置,及行变成列，列变成行
# g = b.T
print(a)
print(b)
print(c)



#  51 五python数据的导入
#  52     import pandas as pad
#  53     f = open('d:/大.csv','rb')
#  54     # 导入csv
#  55     a = pad.read_csv(f, encoding='python')
#  56     # 显示多少行多少列
#  57     a.shape()
#  58     a.values[0][2] #第一行第三列
#  59     # 描述csv数据
#  60     b = a.describe()
#  61     # 排序
#  62     c = a.sort_values()
#  63     # 导入excel
#  64     d = pad.read_excel('d:/大.xls')
#  65     print(d)
#  66     print(d.describe())
#  67     # 导入mysql
#  68     import pymysql
#  69     conn = pymysql.connect(host='localhost', user='root', passwd='root', db='')
#  70     sql = 'select * from mydb'
#  71     e = pad.read_sql(sql, conn)
#  72     # 导入html表格数据 需要先安装 html5lib和bs4
#  73     g = pad.read_html('https://book.douban.com/subject/30258976/?icn=index-editionrecommend')
#  74     # 导入文本数据
#  75     h = pad.read_table('d:/lianjie.txt','rb', engine='python')
#  76     print(h.describe())
#  77 六matplotlib的使用
#  78     # 折线图/散点图用plot
#  79     # 直方图用hist
#  80     import matplotlib.pylab as pyl
#  81     import numpy as npy
#  82     x = [1,2,4,6,8,9]
#  83     y = [5,6,7,8,9,0]
#  84     pyl.plot(x, y) #plot(x轴数据，y轴数据，展现形式)
#  85     # o散点图,默认是直线 c cyan青色 r red红色 m magente品红色 g green绿色 b blue蓝色 y yellow黄色 w white白色
#  86     # -直线  --虚线  -. -.形式  :细小虚线
#  87     # s方形 h六角形  *星星  + 加号  x x形式 d菱形 p五角星
#  88     pyl.plot(x, y, 'D')
#  89     pyl.title('name') #名称
#  90     pyl.xlabel('xname') #x轴名称
#  91     pyl.ylabel('yname') #y轴名称
#  92     pyl.xlim(0,20) #设置x轴的范围
#  93     pyl.ylim(2,22) #设置y轴的范围
#  94     pyl.show()
#  95     # 随机数的生成
#  96     data = npy.random.random_integers(1,20,100) #(最小值，最大值，个数)
#  97     # 生成具有正态分布的随机数
#  98     data2 = npy.random.normal(10.0, 1.0, 10000) #(均值，西格玛，个数)
#  99     # 直方图hist
# 100     pyl.hist(data)
# 101     pyl.hist(data2)
# 102     # 设置直方图的上限下限
# 103     sty = npy.arange(2,20,2) #步长也表示直方图的宽度
# 104     pyl.hist(data, sty, histtype='stepfilled') # 去除轮廓
# 105     # 子图的绘制和使用
# 106     pyl.subplot(2, 2, 2) # (行，列，当前区域)
# 107     x1 = [2,3,5,8,6,7]
# 108     y1 = [2,3,5,9,6,7]
# 109     pyl.plot(x1, y1)
# 110     pyl.subplot(2, 2, 1) # (行，列，当前区域)
# 111     x1 = [2,3,5,9,6,7]
# 112     y1 = [2,3,5,9,6,7]
# 113     pyl.plot(x1, y1)
# 114     pyl.subplot(2, 1, 2) # (行，列，当前区域)
# 115     x1 = [2,3,5,9,6,7]
# 116     y1 = [2,3,9,5,6,7]
# 117     pyl.plot(x1, y1)
# 118     pyl.show()