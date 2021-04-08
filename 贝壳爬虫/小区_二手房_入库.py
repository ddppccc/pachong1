import os
import re
import uuid
import random
import pandas as pd


def write_to_table(df, schema, table_name, password='123456', host='127.0.0.1', DB='House',
                   if_exists='append', port=5432, sqlalchemy=None):
    """
    :param df:          df表
    :param schema:      模式名
    :param table_name:  表名
    :param password:    postgre密码
    :param host:        主机
    :param DB:          数据库
    :param if_exists:   append表存在追加, fail,表存在跳过, replace,表存在删除重建
    :return:
    """
    import io
    import pandas as pd
    from sqlalchemy import create_engine
    # db_engine = create_engine('postgresql://postgres:1q2w3e4r@192.168.88.51/House')# 初始化引擎
    db_engine = create_engine('postgresql://postgres:{}@{}:{}/{}'.format(password, host, port,DB))  # 初始化引擎
    string_data_io = io.StringIO()
    df.to_csv(string_data_io, sep=',', index=False)
    pd_sql_engine = pd.io.sql.pandasSQL_builder(db_engine)
    table = pd.io.sql.SQLTable(table_name, pd_sql_engine, frame=df,
                               index=False, if_exists=if_exists, schema=schema)  # 模式名
    table.create()
    string_data_io.seek(0)
    string_data_io.readline()  # remove header
    with db_engine.connect() as connection:
        with connection.connection.cursor() as cursor:
            copy_cmd = '''COPY "%s"."%s" FROM STDIN HEADER DELIMITER ',' CSV''' % (schema, table_name)
            cursor.copy_expert(copy_cmd, string_data_io)
        connection.connection.commit()


class Community_install_Postsql:

    def run(self, year, month):
        d = []
        p = 'data/小区'
        for i in os.listdir(p):
            path = os.path.join(p, i)
            print(i)
            f = open(path , 'r', encoding='utf-8')
            df = pd.read_csv(f)
            df['抓取时间'] = '2020-{}-28'.format(month)
            df['抓取年份'] = year
            df['抓取月份'] = month
            df['数据来源'] = '贝壳'
            f.close()
            d.append(df)

        df_beike_community = pd.concat(d)
        df_beike_community['楼栋总数'] = df_beike_community['楼栋总数'].map(lambda x: ''.join(re.findall('(\d+)', str(x))))
        df_beike_community['房屋总数'] = df_beike_community['房屋总数'].map(lambda x: ''.join(re.findall('(\d+)', str(x))))
        df_beike_community['在租套数'] = df_beike_community['再租套数']
        df_beike_community['物业费'] = df_beike_community['物业费用']
        df_beike_community['id'] = df_beike_community['楼栋总数'].map( lambda x: uuid.uuid1(node=random.randint(10000,1000000)))
        df_beike_community['在租套数'] = df_beike_community['在租套数'].map(lambda x: int(x) if str(x) != 'nan' else '')
        df_beike_community['建筑年份'] = df_beike_community['建筑年份'].map(lambda x: int(x) if str(x) != 'nan' else '')
        df_beike_community['类型'] = ''

        df_beike_community['涨跌幅'] = ''
        df_beike_community['产权描述'] = ''
        df_beike_community['建筑面积'] = ''
        df_beike_community['占地面积'] = ''
        df_beike_community['绿化率'] = ''
        df_beike_community['容积率'] = ''

        a = ["id", "城市", "区县", "小区", "类型", "单价", "在售套数", "在租套数", "建筑年份", "longitude", "latitude", "涨跌幅", "建筑面积", "占地面积", "房屋总数", "楼栋总数", "绿化率", "容积率", "产权描述", "地址", "小区url", "抓取年份", "抓取月份", "数据来源"]
        df_beike_community_1 = df_beike_community[a]
        print('数据量: ', df_beike_community_1.shape)
        write_to_table(df_beike_community_1, schema='public', table_name='Community_2020',password='123456', host='127.0.0.1', DB='Community' , port=5432)


if __name__ == '__main__':
    # TODO 弃用
    year, month = 2020, 11
    
    Community_install_Postsql().run(year, month)