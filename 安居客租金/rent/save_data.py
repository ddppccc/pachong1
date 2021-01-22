import pandas as pd

from rent.check_file import save_region



def write_to_table(df, schema, table_name, password='1q2w3e4r', host='127.0.0.1', DB='RENT',
                   if_exists='append', port='5432'):
    """
    :param df:          df表
    :param schema:      模式名
    :param table_name:  表名
    :param password:    postgre密码
    :param host:        主机
    :param DB:          数据库
    :param port         端口号
    :param if_exists:   append表存在追加, fail,表存在跳过, replace,表存在删除重建
    :return:
    """
    import io
    import pandas as pd
    from sqlalchemy import create_engine
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


# 保存数据
def save_data(data, city, region):
    try:
        df = pd.DataFrame(data=data)
        # 去重
        # df.drop_duplicates(['标题', '标题url'], inplace=True)
        df = df[["id", "城市", "区县", "标题", "小区", "户型", "面积", "楼层", "租金", "特点", "地址", "抓取年份", "抓取月份", "小区url", "标题url", "朝向", "类型", "数据来源"]]
        # 保存到NAS
        # write_to_table(df_id, schema='public', table_name='Rent_2020',password='123456', host='192.168.88.254',DB='RENT' ,port='15432')
        # 保存到本地
        write_to_table(df, schema='public', table_name='Rent_2020',password='1q2w3e4r', host='127.0.0.1',DB='RENT' )

        # 数据保存成功
        save_region(city, region)

    except Exception as  e:
        print("数据保存失败: ",e)









