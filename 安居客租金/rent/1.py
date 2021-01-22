import json

import psycopg2
import pandas as pd

def write_to_table(df, schema, table_name, password='1q2w3e4r', host='127.0.0.1', DB='RENT',
                   if_exists='append', port='5432'):
    """
    :param df:          df表
    :param schema:      模式名
    :param table_name:  表名
    :param spiderType   爬虫类型    [二手房/新房]
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

conn = psycopg2.connect(database='RENT',
                        user='postgres',
                        password='1q2w3e4r',  # lqk123456
                        host='127.0.0.1',     # 123.56.10.20
                        port=5432)
with open("city_dist.json", 'r', encoding='utf-8') as fp:
    city_dist = json.loads(fp.read())
city_list = []
for city, districts in city_dist.items():
    city_list.append(city)
for city in city_list:
    print(city)
    sql = f"""SELECT id, "城市", "区县", "标题", "小区", "户型", "面积", "楼层", "租金", "特点", "地址", "抓取年份", "抓取月份", "小区url", "标题url", "朝向", "类型", "数据来源"
    FROM public."Rent_2020" where 城市='{city}';"""

    df_id = pd.read_sql_query(sql, con=conn)
    print(df_id.shape)

    write_to_table(df_id, schema='public', table_name='Test',password='1q2w3e4r', host='127.0.0.1',DB='RENT' ,port='5432')
