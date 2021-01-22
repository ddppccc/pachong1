import math
import os
import time
import requests
import pandas as pd
from queue import Queue
from threading import Thread, Lock
from storage import run_sqlite


def fozu():
    print("                            _ooOoo_  ")
    print("                           o8888888o  ")
    print("                           88  .  88  ")
    print("                           (| -_- |)  ")
    print("                            O\\ = /O  ")
    print("                        ____/`---'\\____  ")
    print("                      .   ' \\| |// `.  ")
    print("                       / \\||| : |||// \\  ")
    print("                     / _||||| -:- |||||- \\  ")
    print("                       | | \\\\\\ - /// | |  ")
    print("                     | \\_| ''\\---/'' | |  ")
    print("                      \\ .-\\__ `-` ___/-. /  ")
    print("                   ___`. .' /--.--\\ `. . __  ")
    print("                ."" '< `.___\\_<|>_/___.' >'"".  ")
    print("               | | : `- \\`.;`\\ _ /`;.`/ - ` : | |  ")
    print("                 \\ \\ `-. \\_ __\\ /__ _/ .-` / /  ")
    print("         ======`-.____`-.___\\_____/___.-`____.-'======  ")
    print("                            `=---='  ")
    print("  ")
    print("         .............................................  ")
    print("                  佛祖镇楼                  BUG辟易  ")
    print("          佛曰:  ")
    print("                  写字楼里写字间，写字间里程序员；  ")
    print("                  程序人员写程序，又拿程序换酒钱。  ")
    print("                  酒醒只在网上坐，酒醉还来网下眠；  ")
    print("                  酒醉酒醒日复日，网上网下年复年。  ")
    print("                  但愿老死电脑间，不愿鞠躬老板前；  ")
    print("                  奔驰宝马贵者趣，公交自行程序员。  ")


class Geocoding():
    _queue = Queue()
    lock = Lock()

    def __init__(self, path, address, threadNumber, gdKey, dataBuffer, ID=None):
        self.path = path
        self.address = address
        self.ThreadNumber = threadNumber
        self.gdKey = gdKey
        self.dataBuffer = dataBuffer
        self.ID = ID
        print(self.ThreadNumber, self.gdKey, self.ID)


    def dispose_split_df(self, df):

        filed_list =[i for i in self.address.split('|')]
        if len(filed_list) == 1:
            df[self.address] = df[filed_list[0]]
        elif len(filed_list) == 2:
            df[self.address] = df[filed_list[0]] + '-' + df[filed_list[1]]
        elif len(filed_list) == 3:
            df[self.address] = df[filed_list[0]]+'-'+df[filed_list[1]]+'-'+df[filed_list[2]]
        else:
            df[self.address] = df[filed_list[0]]+'-'+df[filed_list[1]]+'-'+df[filed_list[2]]+'-'+df[filed_list[3]]

        # 生成 唯一ID   # TODO 需要ID时打开
        # if not self.ID:
        #     df['id'] = df[self.address].map(lambda x: uuid.uuid1(node=random.randint(999, 999999)))
        df[self.address] = df[self.address].map(lambda x: str(x).replace('#', '').replace('|', '').replace("、",''))

        # 拆分df
        for i in range(int(math.ceil(df.shape[0] / 10))):
            item = {}
            splitDf = df.iloc[i * 10: (i + 1) * 10]
            # TODO 需要ID时打开
            # if not self.ID:
            #     id_list = splitDf['id'].tolist()
            # else:
            #     id_list = splitDf[self.ID].tolist()
            # item['id'] = id_list

            address_str = "|".join(splitDf[self.address].tolist())
            item['addr'] = address_str
            item['value'] = splitDf.to_dict(orient='records')
            yield item


    def run(self, encoding='utf-8'):
        while True:
            if '.csv' in self.path:
                f = open(self.path, mode='r', encoding=encoding)
                df = pd.read_csv(f, low_memory=False)

                df = df.fillna('')
                f.close()

                # # 方法一: python直接连接sql库进行数据提取
                # conn = psycopg2.connect(database="Esf", user="postgres", password="1q2w3e4r", host="47.107.236.13",
                #                         port="54321")
                #
                # sql = """
                # select "城市", "区县", "标题url", "小区", "数据来源", "单价", "总价", "户型", "面积", "楼层", "建筑年份", "朝向", "抓取月份"
                #  FROM "Esf_2020".esf_2020 and 城市 in ('东莞','佛山','深圳','中山','广州','珠海','惠州','江门','肇庆');
                # """
                # df = pd.read_sql_query(sql, con=conn)

                # df = df.drop_duplicates('标题url')
                # df.loc[df['地址'].isnull(), '地址'] = df['标题']
                # df = df[["城市", "区县", "标题url", "小区", "数据来源", "单价", "总价", "户型", "面积", "楼层", "建筑年份", "朝向", "抓取月份"]]
                print(df.shape)
                break
            elif '.xlsx' in self.path or '.xls' in self.path:
                df = pd.read_excel(self.path)
                df = df.fillna('')
                break
            else:
                print('请输入 csv 或者 xlsx格式的文件')
                self.path = input("请重新输入: ")
                continue


        for item in self.dispose_split_df(df):
            self._queue.put(item)

        data_all = []
        for i in range(self.ThreadNumber):
            t = Thread(target=self.parse, args=(data_all))
            t.daemon = True
            t.start()
        self._queue.join()


    def get_html(self, item: dict):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
        }
        params = {
            'key': self.gdKey,
            'address': item['addr'],
            'batch': 'True'
        }
        url = 'https://restapi.amap.com/v3/geocode/geo'
        while True:
            try:
                res = requests.get(url=url, params=params, headers=headers, timeout=(2, 10)).json()
                return res
            except:
                time.sleep(2)
                continue

    def parse(self):
        while True:
            if self._queue.empty() == True:
                return
            size = self._queue.qsize()

            if size % 10 == 0:
                print('剩余执行次数: ', size)

            item = self._queue.get()
            # self._queue.task_done()
            res = self.get_html(item)

            # 判断 是否key 用尽
            data_all = []
            try:
                geocodes = res['geocodes']
            except:
                self._queue.task_done()
                continue
            for i in range(len(geocodes)):
                data_dict = {}
                province = geocodes[i]['province'] or ' '
                formatted_address = geocodes[i]['formatted_address'] or ' '
                if len(geocodes[i]['location']) != 0:
                    longitude = geocodes[i]['location'].split(',')[0] or ' '
                    latitude = geocodes[i]['location'].split(',')[1] or ' '
                else:
                    latitude = ' '
                    longitude = ''

                # data_dict['id_gd'] = id
                data_dict['province_gd'] = province
                data_dict['city_gd'] = "".join(geocodes[i].get('city', ''))
                data_dict['district_gd'] = "".join(geocodes[i].get('district', ''))
                data_dict['street_gd'] = "".join(geocodes[i].get('street', ''))
                data_dict['level_gd'] = "".join(geocodes[i].get('level', ''))
                data_dict['formatted_address'] = formatted_address
                data_dict['lon_gd'] = longitude
                data_dict['lat_gd'] = latitude
                item['value'][i].update(data_dict)
                data_all.append(item['value'][i])

            self.lock.acquire(True)
            self.dataBuffer['GD'] += data_all
            self.lock.release()
            self._queue.task_done()


def RunExE():
    print(fozu())
    print()
    print("""使用说明: 
    本程序的作用是 地址转经纬度
    
    若对解析结果经度要求不高,可以使用此程序, 同时地址越详细,则解析结果越准确. 假如要对项目解析, 比如说深圳小区名称, 或者某个医院名称,
    解析结果可能可能会出现偏差, 部分数据只能解析到市或者某个区 这个级别的经纬度.
    
    1. 线程数量 [可选]: 并发数量(解析速度),      若不输入默认为 5, 根据电脑, 建议不超过50
    2. 高德 KEY [可选]: 可自己选择.    默认 4fabbb7c9a939ee3942c67715f9a8f33, 每天调用次数 300W
    3. sql 缓存 [可选]: True/False     是否sql文件缓存, 默认为True, 可不用改.
    4. 保存格式 [可选]: csv/xlsx 
    5. 保存路径 [可选]: 绝对路径。     默认生成在 data文件夹下, 可以自己添加路径, 建议绝对路径
    
    6. 文件路径 [必选]: 文件绝对路径，若文件和程序处于同一目录下, 可使用相对路径, 必须为csv或者xlsx格式的文件
    7. 地址表头 [必选]: 文件中标识地址的表头, 一个或多个[最多4个],  若有多个字段,请用 | 隔开,按照(省>市>区县...)顺序填写
                        ex: one: 地址        more: 省份|城市|区县|地址
    *************************************************************************
    """)
    threadNumber = int(input('[可选] 1. 线程数量:  ') or 5)
    key = input('[可选] 2. 高德 KEY:  ') or '4fabbb7c9a939ee3942c67715f9a8f33'
    clear = input('[可选] 3. sql 缓存:  ') or 'True'
    saveFormat = input('[可选] 4. 保存格式: ') or 'csv'
    savePath = r'{}'.format(input('[可选] 5. 保存路径: ')) or 'data'
    print('↓' * 20)
    path = r'{}'.format(input('[必选] 6. 文件路径: '))
    address = input('[必选] 7. 地址表头: ')   # 城市板块名称
    # uniqueID = input('3. 请输入数据唯一ID:  ')

    print('请确认输入是否正确:   y: 继续, n: 停止')
    result = input('请输入: ')
    if result != 'y':
        print('程序结束')
        time.sleep(2)
        return

    # 这里执行 sqlite 脚本
    dataBuffer = run_sqlite(path, clear)

    start = time.time()
    Geocoding(path, address=address, threadNumber=threadNumber, gdKey=key, dataBuffer=dataBuffer).run()
    start1 = time.time()
    print('执行完毕, 正在保存数据..... ')
    if saveFormat == 'csv':
        dataBuffer.to_csv(os.path.join(savePath, os.path.splitext(os.path.basename(path))[0]))
    elif saveFormat == 'xlsx':
        dataBuffer.to_excel(os.path.join(savePath, os.path.splitext(os.path.basename(path))[0]))

    print('线程数量: ', threadNumber, '解析数据用时: ', start1-start, '储存数据用时: ',time.time() - start1)
    print('解析完毕, 任意输入后, 自动退出')
    input()


if __name__ == '__main__':
    # 打包
    RunExE()

    # 线程数量:  5 用时:  1.3434062004089355
    # 线程数量:  1 用时:  1.6705365180969238
    # 线程数量:  10 用时:  0.8886213302612305

    # path='房天下_昆明二手房_2020年.csv'
    # dataBuffer = run_sqlite(path, 'False')

    # dataBuffer.to_csv(os.path.join('data', os.path.splitext(os.path.basename(path))[0]))
