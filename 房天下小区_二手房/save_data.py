# -*- coding: utf-8 -*-
import io
import os
import random
import re
import time
import datetime
import pandas as pd
from sqlalchemy import create_engine


def write_to_table(df, schema, table_name, spiderType, password='123456', host='127.0.0.1', DB='House',
                   if_exists='append', port=5432):
    """
    插入数据到数据库
    :param df:          df表
    :param schema:      模式名
    :param table_name:  表名
    :param spiderType   爬虫类型    [二手房/新房]
    :param password:    postgre密码
    :param host:        主机
    :param DB:          数据库
    :param port:        端口号
    :param if_exists:   append表存在追加, fail,表存在跳过, replace,表存在删除重建
    :return:
    """
    data_type_columns = {
        'community': '"id", "城市", "区县", "小区", "类型", "单价", "在售套数", "在租套数", "建筑年份", "longitude", "latitude", "涨跌幅", "建筑面积", "占地面积",  "房屋总数", "楼栋总数", "绿化率", "容积率", "产权描述", "地址", "小区url", "抓取年份", "抓取月份", "数据来源", "date", "物业费", "停车位"',
        'esf' : '"id", "城市", "区县", "标题url", "小区", "地址", "数据来源", "单价", "总价", "户型", "面积", "楼层", "建筑年份", "朝向", "抓取时间", "抓取年份", "抓取月份", "关注人数", "标签"',
        'newhouse': '"id", "城市", "区县", "标题", "销售情况", "分类", "装修", "户型", "单价", "总价", "建面", "最小建面", "最大建面", "容积率", "绿化率", "楼栋总数", "总户数", "建筑面积", "地址", "标签", "开盘时间", "物业费", "latitude", "longitude", "抓取月份", "抓取年份", "数据来源", "标题url"'
    }

    # db_engine = create_engine('postgresql://postgres:1q2w3e4r@192.168.88.51/House')# 初始化引擎
    db_engine = create_engine('postgresql://postgres:{}@{}:{}/{}'.format(password, host, port, DB))  # 初始化引擎
    string_data_io = io.StringIO()
    df.to_csv(string_data_io, sep=',', index=False)
    pd_sql_engine = pd.io.sql.pandasSQL_builder(db_engine)
    table = pd.io.sql.SQLTable(table_name, pd_sql_engine, frame=df,
                               index=False, if_exists=if_exists, schema=schema)  # 模式名
    table.create()
    string_data_io.seek(0)
    # string_data_io.readline()  # remove header
    with db_engine.connect() as connection:
        with connection.connection.cursor() as cursor:
            if spiderType == '二手房':
                copy_cmd = '''COPY "%s"."%s"(%s) FROM STDIN HEADER DELIMITER ',' CSV''' % (schema, table_name, data_type_columns['esf'])
            elif spiderType == 'newhouse':
                copy_cmd = '''COPY "%s"."%s"(%s) FROM STDIN HEADER DELIMITER ',' CSV''' % (schema, table_name, data_type_columns['newhouse'])
            elif spiderType == '小区':
                copy_cmd = '''COPY "%s"."%s"( %s ) FROM STDIN HEADER DELIMITER ',' CSV''' % ( schema, table_name, data_type_columns['community'])
            else:
                copy_cmd = '''COPY "%s"."%s" FROM STDIN HEADER DELIMITER ',' CSV''' % (schema, table_name)
            cursor.copy_expert(copy_cmd, string_data_io)
        connection.connection.commit()


def saveData(dataList, city, GetType):
    """
    保存到数据库
    """
    start = time.time()
    data = pd.DataFrame(dataList)
    if GetType == "二手房":
        data = data[
            ["id", "城市", "区县", "标题url", "小区", "地址", "数据来源", "单价", "总价", "户型", "面积", "楼层", "建筑年份", "朝向", "抓取时间", "抓取年份",
             "抓取月份", "关注人数", "标签"]]

        # TODO 保存二手房数据, 保存到NAS
        write_to_table(data, schema="public", table_name='Esf_2021', spiderType=GetType, password='1q2w3e4r', host='192.168.88.254',  DB='ESF', port=15432)

        # TODO 保存二手房数据, 保存到本地
        # write_to_table(data, DB="ESF", schema="public", table_name='Esf_2021', spiderType=GetType, password='123456',
        #                host='127.0.0.1')

        return time.time() - start

    else:
        a = ["id", "城市", "区县", "小区", "类型", "单价", "在售套数", "在租套数", "建筑年份", "longitude", "latitude", "涨跌幅", "建筑面积", "占地面积",
             "房屋总数", "楼栋总数", "绿化率", "容积率", "产权描述", "地址", "小区url", "抓取年份", "抓取月份", "数据来源", "date", "物业费", "停车位"]
        data = data[a]
        data['楼栋总数'] = data['楼栋总数'].map(lambda x: ''.join(re.findall('(\d+)', str(x))))
        data['房屋总数'] = data['房屋总数'].map(lambda x: ''.join(re.findall('(\d+)', str(x))))
        data['绿化率'] = data['绿化率'].map(lambda x: ''.join(re.findall('(\d+\.?\d+)', str(x))))

        # TODO 保存小区数据, 保存到Nas
        write_to_table(data, "public", 'Community_2021', GetType, password='1q2w3e4r', host='192.168.88.254', DB='Community', port=15432)

        # TODO 保存小区数据, 保存到本地
        # write_to_table(data, "public", 'Community_2021', GetType, password='123456', host='127.0.0.1', DB='Community', port=5432)

        return time.time() - start


def save_grab_dist(city, dist, url, GetType):
    """
    保存已经抓取的行政区
    """
    if GetType == "二手房":
        savePath = "log/lose_dist"
    else:
        savePath = "log\小区"
    file_prefix = os.path.join(savePath, '{}_{}_'.format(datetime.datetime.now().strftime('%y-%m'), city))
    save_filepath = ''.join([file_prefix, '{}.txt'.format("lose")])
    with open(save_filepath, 'a', encoding='utf-8') as fp:
        fp.writelines([city, ',', dist, ',', url, '\n'])


def get_exists_dist(city, GetType):
    """
    查看已经抓取的行政区
    """
    if GetType == "二手房":
        savePath = "log/lose_dist"
    else:
        savePath = "log/小区"
    for pathCity in os.listdir(savePath):
        if city in pathCity:
            pathCity = os.path.join(savePath, pathCity)
            with open(pathCity, 'r', encoding='utf-8') as fp:
                list_city = fp.readlines()
            dist_list = [i.split(',')[1] for i in list_city]
            return dist_list
    return []


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
    user_agent = random.choice(user_agents)
    return user_agent


class Update_NewHouse_Df:
    def __init__(self):
        pass

    def A(self, x):
        """规范化 分类标准"""
        d = []
        x = str(x)
        if '普通住宅' in x or '住宅' in x or ('独栋' in x and '企业独栋' not in x) or 'LOFT' in x:
            d.append('住宅')
        if '写字' in x or '企业' in x:
            d.append('写字楼')
        if '公寓' in x:
            d.append('公寓')
        if '别墅' in x:
            d.append('别墅')
        if '商铺' in x or '购物中心' in x or ('商业' in x and '商业类' not in x):
            d.append('商铺')
        if '商业类' in x:
            d.append('商业类')
        if '底商' in x:
            d.append('底商')
        if '商品房' in x:
            d.append('商品房')
        if '车库' in x:
            d.append('车库')
        if '综合体' in x:
            d.append('综合体')
        if len(d) == 0:
            d.append('住宅')
        return ','.join(d)

    def replace_re(self, x):
        """规范化 户型"""
        x = str(x)
        if not x:
            return ''
        y = '/'.join(re.findall('(\d居[以上]{0,2})+', x)).replace('居', '')
        if len(y) == 0:
            return ''
        else:
            if '以上' in y:
                return y.replace('以上', '') + '居以上'
            return y + '居'

    def replace_area(self, x):
        """规范化 面积"""
        x = str(x)
        if not x:
            return ''
        y = ''.join(re.findall('(\d+~?\d+)平', x)).replace('~', '-')
        if len(y) == 0:
            return ''
        else:
            return y

    def change_date(self, x):
        """初次规范 开盘时间"""
        d = ''
        y = str(x)
        if '暂无资料' in y:
            return d
        r = '\d+[-|年|\.]?\d{1,2}[-|月|\.]?\d{0,2}[日]?'
        a = re.findall(r, y)
        try:
            d = a[0]
        except:
            d = ''
        d = d.replace('年', '-').replace('月', '-').replace('日', '').replace('.', '-').strip('-')
        if ('-' not in d and len(d) < 3) or '20' not in d:
            d = ''
        return d

    def check_data(self, x):
        """再次规范 开盘时间"""
        x = str(x)
        if 'n' in x or 'N' in x:
            return ''
        elif x.count('-') == 2:
            try:
                x = datetime.datetime.strptime(x, "%Y-%m-%d").date()
            except:
                x = ''
        elif x.count('-') == 1:
            try:
                x = datetime.datetime.strptime(x, "%Y-%m").date()
            except:
                x = ''
        else:
            x = ''
        return x

    def update(self, df):
        """更新 df"""
        df['销售情况'] = df['标签'].map(lambda x: str(x).split(' ')[0])
        df['分类'] = df['标签'].map(self.A)
        df['户型'] = df['描述'].map(self.replace_re)
        df['建面'] = df['描述'].map(self.replace_area)
        df['开盘时间'] = df['开盘时间'].map(self.change_date)
        df['开盘时间'] = df['开盘时间'].map(self.check_data)

        df['装修'] = ''
        df['标题'] = df['标题'].map(lambda x: str(x).replace('\r', '').replace('\n', ''))
        df['标签'] = df['标签'].map(lambda x: str(x).replace('\r', '').replace('\n', ''))

        df['单价'] = df['价格'].map(
            lambda x: '' if not x else ''.join(re.findall('\d+\.?\d+', str(x))) if '元/' in str(x) else '')
        df['总价'] = df['价格'].map(
            lambda x: '' if not x else ''.join(re.findall('\d+\.?\d+', str(x))) if '万' in str(x) else '')
        df['占地面积'] = df['占地面积'].map(lambda x: ''.join(re.findall('(\d+\.?\d+)', str(x))) if '平方米' in str(x) else '')
        df['建筑面积'] = df['建筑面积'].map(lambda x: ''.join(re.findall('(\d+\.?\d+)', str(x))) if '平方米' in str(x) else '')
        df['容积率'] = df['容积率'].map(lambda x: ''.join(re.findall('(\d+\.?\d+)', str(x))))
        df['绿化率'] = df['绿化率'].map(lambda x: ''.join(re.findall('(\d+\.?\d+)', str(x))))
        df['楼栋总数'] = df['楼栋总数'].map(lambda x: ''.join(re.findall('(\d+)', str(x))))
        df['总户数'] = df['总户数'].map(lambda x: ''.join(re.findall('(\d+)', str(x))))
        df['最小建面'] = df['建面'].map(lambda x: x if '-' not in str(x) else str(x).split('-')[0])
        df['最大建面'] = df['建面'].map(lambda x: x if '-' not in str(x) else str(x).split('-')[1])
        df['物业费'] = df['物业费'].map(lambda x: '' if '暂无' in str(x) or 'None' in str(x) else x)
        df['longitude'] = ''
        df['latitude'] = ''

        a1 = ['id', "城市", "区县", "标题", "销售情况", "分类", "装修", "户型", "单价", "总价", "建面", "最小建面", "最大建面",
              "容积率", "绿化率", "楼栋总数", "总户数", "建筑面积", "地址", "标签", "开盘时间", "物业费", 'latitude', 'longitude',
              "抓取月份", "抓取年份", "数据来源", "标题url"]
        df1 = df[a1]
        return df1


if __name__ == '__main__':
    pass
