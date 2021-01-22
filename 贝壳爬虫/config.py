import datetime
import random
import uuid
import json
import pandas as pd


class Update_NewHouse:
    def __init__(self):
        pass

    def A(self, x):
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

    def check_data(self, x):
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

    def update(self, df_beike: pd.DataFrame):
        df_beike['销售情况'] = df_beike['销售情况'].map(lambda x: {'未开盘':'待售', '售罄': '售完'}.get(x, x))
        df_beike['单价'] = df_beike['均价'].map(lambda x: None if str(x) == '0' else x)
        df_beike['总价'] = df_beike['总价'].map(lambda x: None if str(x) == '0' else x)
        df_beike['建面'] = df_beike['建面'].map(lambda x: str(x).replace('㎡', '') if x else None)
        df_beike['最大建面'] = df_beike['最大建面'].map(lambda x: str(x).replace('㎡', '') if x else None)
        df_beike['最小建面'] = df_beike['最小建面'].map(lambda x: str(x).replace('㎡', '') if x else None)
        df_beike['latitude'] = df_beike['latitude'].map(lambda x: None if not x else x)
        df_beike['longitude'] = df_beike['longitude'].map(lambda x: None if not x else x)

        df_beike['容积率'] = None
        df_beike['绿化率'] = None
        df_beike['楼栋总数'] = 0
        df_beike['总户数'] = 0
        df_beike['物业费'] = None
        df_beike['建筑面积'] = None
        df_beike['占地面积'] = None
        df_beike['数据来源'] = '贝壳'
        df_beike['id'] = df_beike['数据来源'].map(lambda x: uuid.uuid1(node=random.randint(10000, 1000000)))

        df_beike['开盘时间'] = df_beike['开盘时间'].map(self.check_data)
        df_beike['分类'] = df_beike['分类'].map(self.A)

        a = ["id", "城市", "区县", "标题", "销售情况", "分类", "装修", "户型", "单价", "总价", "建面", "最小建面", "最大建面", "容积率", "绿化率", "楼栋总数",
             "总户数", "建筑面积", "地址", "标签", "开盘时间", "物业费", "latitude", "longitude", "抓取月份", "抓取年份", "数据来源", "标题url"]

        df2 = df_beike[a]
        return df2


# ================================读取新房和小区映射表============================================================
with open('bk_newHouse_map.json', 'r', encoding='utf-8') as fp:
    newHouse_map = json.load(fp)

with open("bk_city_map.json", 'r', encoding='utf-8') as fp:
    cities = json.loads(fp.read())


# ================================保存数据到数据库==========================================================================
def write_to_table(df, schema, table_name, password='123456', host='127.0.0.1', DB='House',
                   if_exists='append', port=5432):
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


# ======================================================================================================================
# TODO 每个月的抓取时间 可以自定义时间
def make_date():
    # month = datetime.datetime.now().month
    # day = datetime.datetime.now().day
    year = 2020
    month = 12
    day = 28
    return year, month, day
