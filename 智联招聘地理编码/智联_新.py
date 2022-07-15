import csv
import random
import re
import requests
import os
import time
import pandas as pd
from queue import Queue
from threading import Thread, Lock
from ip_pool import get_proxy, delete_proxy
import pymongo
MONGODB_CONFIG = {
    "host": "192.168.1.28",
    "port": "27017",
    "user": "admin",
    "password": '123123',
}

info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['智联']['地理数据_202207']
has_info = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['智联']['地理数据去重_202207']

def get_ua():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
        'Opera/8.0 (Windows NT 5.1; U; en)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) '
    ]
    user_agent = random.choice(user_agents)  # random.choice(),从列表中随机抽取一个对象
    return user_agent


def get_html(number: str):
    proxy = get_proxy()
    if "!" in str(proxy):
        print("没有ip, 等待60s")
        time.sleep(60)
    proxies = {
        "https": "https://{}".format(proxy),
        "http": "http://{}".format(proxy)
    }
    retry_count = 3
    while retry_count > 0:

        try:
            url = 'https://capi.zhaopin.com/capi/position/getPositionDetail'
            headers = {
                'user-agent': get_ua()
            }
            params = {
                "number": number,
                "at": "681c667dbe384f1e8103f435ea482172",
                "rt": "fbbd313fef49437995f723f6f9b58314",
                # 'at': '7a45cc942a2342d58a609f635bfda75a',
                # 'rt': '777630d9c5094f12b517382e33cd9d26',
                "channel": "wxxiaochengxu",
                "v": "1.0",
                "platform": "12",
                "d": "8F244A3B-AA8A-41E5-90B8-DADAB490A876",
                "version": "0.0.0"
            }
            res = requests.get(url, params=params, headers=headers, timeout=(2, 5),
                               proxies=proxies)
            return res.json()
        except Exception as E:
            retry_count -= 1
            print('error!!',  E)
            continue
    # 出错3次, 删除代理池中代理
    delete_proxy(proxy)
    return None


def check(dtime, city, **kwargs):
    """
    检查剩余条数
    :param city: 城市
    :return: 返回去除已经抓去过的url的 df
    """

    # 尚未获取
    path = os.path.join(kwargs['file_name'], '{}_{}.csv'.format(dtime, city))
    print(path)
    f = open(path, 'r', encoding='utf-8', errors='ignore')
    # df1 = pd.read_csv(f, names=['主分类','企业url','企业名称','公司性质','公司规模','区县','发布时间','城市','学历','工作地点','工作经验','次分类','职位url','职位名称','薪资'])
    df1 = pd.read_csv(f, names=['城市','区县','主分类','次分类','职位名称','职位url','薪资','工作地点','发布时间','企业名称','企业url','工作经验','学历','公司规模','公司性质'])
    f.close()
    df1 = df1.query('城市 != "城市"')

    df1['number'] = df1['职位url'].map(lambda x: ''.join(re.findall(r'\.com\/(.*)\.htm', str(x))))
    df1.rename(columns={'城市': 'city', '职位url': 'positionURL'}, inplace=True)
    print('未去重: ', df1.shape)
    df1 = df1.drop_duplicates(subset='number')
    df1 = df1[['city', 'number', 'positionURL']]
    print('去重后数据: ', df1.shape)

    # 已经获取的
    path = r'data_new/{}.csv'.format(city)
    if os.path.exists(path):
        f = open(path, mode='r', encoding='utf-8', errors='ignore',)
        df = pd.read_csv(f, error_bad_lines=False)
        f.close()
        print('已经获取的数据量: ', df.shape)

        df3 = df1[~df1['positionURL'].isin(df['url'].tolist())]
        print('尚未解析的数据量: ', df3.shape)
        return df3
    else:
        return df1


def parse(city, data_list: list):
    count = 1
    while True:
        count += 1
        if queue.empty():
            break
        df = queue.get()
        queue.task_done()
        number = df['number']
        nb = 2
        while nb > 0:
            resJson = get_html(number)

            if not resJson:
                nb -= 1
                continue
            break

        try:
            if resJson.get('statusCode') != 200:
                print('该岗位已经删除', number, resJson)
                continue
        except:
            continue

        data = resJson['data']
        if not data:
            print('没有data: ', resJson)
            input('请输入后继续:', )
            continue
        item = dict()
        item['城市'] = city
        # 企业
        item['企业名称'] = data['companyDetail']['name']
        item['企业number'] = data.get('companyDetail').get('number')
        item['企业ID'] = data.get('companyDetail').get('companyId')
        item['公司规模'] = data.get('companyDetail').get('companySize')
        item['公司性质'] = data.get('companyDetail').get('property')
        item['企业分类'] = data.get('companyDetail').get('industry')
        item['分类层级'] = data.get('companyDetail').get('industryLevel')
        item['企业url'] = data.get('companyDetail').get('companyUrl')

        # 工作岗位
        item['三级ID'] = data.get('positionDetail').get('subJobTypeLevel')
        item['二级ID'] = data.get('positionDetail').get('jobTypeLevel')
        item['职位名称'] = data.get('positionDetail').get('name')
        item['url'] = data.get('positionDetail').get('positionURL')
        item['区县'] = data.get('positionDetail').get('cityDistrict')
        item['学历'] = data.get('positionDetail').get('education')
        item['职位类型'] = data.get('positionDetail').get('emplType')
        item['工作经验'] = data.get('positionDetail').get('workingExp')
        item['地址'] = data.get('positionDetail').get('workAddress')
        item['工作地点'] = data.get('positionDetail').get('workCity')
        item['薪资'] = data.get('positionDetail').get('salary')
        item['发布时间'] = data.get('positionDetail').get('publishTime')
        item['招聘人数'] = data.get('positionDetail').get('recruitNumber')
        item['latitude'] = data.get('positionDetail').get('latitude')
        item['longitude'] = data.get('positionDetail').get('longitude')
        item['岗位描述'] = data.get('positionDetail').get('jobDesc').replace(',', '，')
        item['职位技能'] = [i.get('value', '') if i else '' for i in data.get('positionDetail').get('skillLabel')]
        item['职位亮点'] = [i.get('value', '') if i else '' for i in data.get('positionDetail').get('welfareLabel')]
        print(item)
        info_base.insert_one(item)   #  插入数据库========================================================================

        # 保存数据
        path = '{}.csv'.format(city)
        savePath = os.path.join('data_new', path)
        if not os.path.exists(savePath):  # 不存在文件夹
            with open(savePath, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                lock = Lock()
                lock.acquire()
                writer.writerow(item.keys())
                writer.writerow(item.values())
                lock.release()
        else:
            with open(savePath, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                lock = Lock()
                lock.acquire()
                writer.writerow(item.values())
                lock.release()


def run(city, dtime, threadNumber: int, **kwargs):
    data_list = []
    df = check(dtime, city, file_name=kwargs['file_name'])
    print(df.head())
    if df.shape[0] == 0:
        print('没有数据')
        return

    number = df.shape[0]
    for i in [df.iloc[i] for i in range(number)]:
        queue.put(i)

    for i in range(threadNumber):
        t = Thread(target=parse, args=(city, data_list))
        t.daemon = True
        t.start()
    queue.join()


def run1(file_name, threadNumber):
    """
    :param file_name: 未解析过的文件的位置
    :return:
    """
    for i in os.listdir(file_name):
        dtime, city_txt = i.split('_')
        city, _ = city_txt.split('.')
        # if city not in ['北京', '北海', '安庆', '安康', '安达', '安阳', '安顺', '宝鸡', '滨州',
        #                 '白城', '白银', '蚌埠', '阿克苏', '阿勒泰', '阿坝', '阿拉善盟', '阿拉尔', '阿里', '鞍山']: continue

        # if '{}_{}\n'.format(dtime, city) in open('geocity.txt', 'r', encoding='utf-8').readlines():
        #     print(city, '已经存在')
        #     continue

        print('当前城市: ', city, '\n')
        run(city, threadNumber=threadNumber, dtime=dtime, file_name=file_name)

        # 保存抓去过的城市
        with open('geocity.txt', 'a', encoding='utf-8') as fp:
            fp.write("{}_{}".format(dtime, city))
            fp.write('\n')
        time.sleep(10)
        print()


if __name__ == '__main__':
    # 解析详情
    file_name = r'Z:\李乾坤\爬虫程序\智联招聘\小程序_data'             # 没有解析详情前的数据所在路径
    save_file_name = r'Z:\李乾坤\爬虫程序\智联招聘地理编码\data_new'    # 解析后数据保存的位置
    df_map = pd.read_excel('行业映射表.xlsx')
    queue = Queue()
    threadNumber = 30   # 线程数量  30
    run1(file_name, threadNumber)

    d = []
    for i in os.listdir(file_name):
        i = i.split('.')[0].split('_')[1]
        if i not in [j.split('.')[0] for j in os.listdir(save_file_name) ]:
            d.append(i)
    print(d)