# -*- coding: utf-8 -*-
import os
import re
import sqlite3


# 用于将数据保存到sqlite3数据库中，初始化后只需要调用insert_data即可将数据插入对应的表内（表不存在则自动创建表）
class DB:
    field_map = {int: 'integer',
                 float: 'float',
                 str: 'varchar(200)'}
    table_fields = {}

    def __init__(self, file_path='database.db'):
        if os.path.split(file_path)[0] and not os.path.exists(os.path.dirname(file_path)):
            os.mkdir(os.path.dirname(file_path))
        self.conn = sqlite3.connect(file_path, timeout=200)

        self.conn.text_factory = str  # 自己加的

        self.cursor = self.conn.cursor()

    def insert_data(self, table_name, items):
        """
         插入数据, item: 元组或字典, 例如: ({'field1': 'value1', 'field2': 'value2'}, {'field1': value1'})
        """
        fields, values, sample_item = self._like_csv(items)
        self._check_table(table_name, sample_item)
        # 插入数据
        fields = [field.join(['"', '"']) for field in fields]
        sql = "insert into %s(%s) values(%s)" % (table_name, ','.join(fields), ','.join(['?'] * len(fields)))
        self.cursor.executemany(sql, values)
        self.conn.commit()

    #         self.cursor.execute('select * from %s' % table_name)
    #         print(self.cursor.fetchall())

    def create_table(self, table_name, item):
        fields_list = []
        for key, value in item.items():
            field_type = self._fit_field_type(value)
            fields_list.append(' '.join([key.join(['"', '"']), field_type]))
        fields = ','.join(fields_list)
        create_table_sql = 'create table if not exists %s(%s);' % (table_name, fields)
        self.cursor.execute(create_table_sql)
        #         fields = item.keys()
        #         values = list(item.values())
        #         sql = 'insert into %s(%s) values(%s)' % (table_name, ','.join(fields), ','.join('?' * len(values)))
        #         self.cursor.execute(sql, tuple(values))
        #         self.cursor.execute('select * from %s' % (table_name))
        #         display(self.cursor.fetchall())
        #         self.cursor.execute('PRAGMA table_info(%s)' % (table_name))
        #         display(self.cursor.fetchall())
        #         self.cursor.execute('drop table %s' % (table_name))
        #         self.cursor.execute('PRAGMA table_info(%s)' % (table_name))
        #         fields = self.cursor.fetchall()
        return list(item.keys())

    def add_field(self, table_name, item):
        # 修改表结构，添加字段
        for field_name in [key for key in item if key not in self.table_fields[table_name]]:
            field_type = self._fit_field_type(item[field_name])
            sql = 'alter table %s add column "%s" %s' % (table_name, field_name, field_type)
            self.conn.execute(sql)
        self.table_fields[table_name] = self._get_fields(table_name)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def _fit_field_type(self, value):
        # 获取数值类型对应的数据库数据类型
        if type(value) is str and len(value) > 200:
            field_type = 'text'
        else:
            field_type = self.field_map.get(type(value), 'varchar(200)')
        return field_type

    def _get_fields(self, table_name):
        # 获取表字段列表
        self.cursor.execute('PRAGMA table_info(%s)' % (table_name))
        fields = [i[1] for i in self.cursor.fetchall()]
        return fields

    def _check_table(self, table_name, item):
        # 检查并自动创建表和添加字段
        # 检查表是否存在
        if table_name not in self.table_fields:
            fields = self._get_fields(table_name)
            if not fields:
                fields = self.create_table(table_name, item)
            self.table_fields[table_name] = fields
        # 检查字段是否存在， 不存在则添加字段
        if [key for key in item if key not in self.table_fields[table_name]]:
            self.add_field(table_name, item)

    def _like_csv(self, items):
        # 将字典列表制成csv样式,
        # 如： items： [{'id': 1, 'name': 'big', }, {'id': 2, 'name': 'small', 'age': 16}, {'id': 3, 'age': 18 }]
        # 返回 fields: ['id', 'name', 'age']
        #      values: [[1, 'big', None], [2, 'small', '16'], [3, None, 18]]
        #      sample_item: {'id': 3, 'name': 'small', 'age':18}
        if type(items) is dict:
            items = (items,)
        sample_item = {}
        #     for item in items:
        #         [sample_item.update({key: item[key]}) for key in item if key not in sample_item]
        #         sample_item.update(item)
        [sample_item.update(item) for item in items]
        # self.check_table(table_name, sample_item)
        fields = sample_item.keys()
        # values = [[item.get(key) for key in fields] for item in items]
        values = [[item.get(key) if type(item.get(key)) in self.field_map else str(item.get(key)) for key in fields] for
                  item in items]
        return fields, values, sample_item

    def drop_table(self, table_name):
        # 删除表
        if table_name in self.table_fields:
            del self.table_fields[table_name]
        sql = 'drop table %s' % table_name
        self.conn.execute(sql)

    def update(self, item, unique_field):
        # 更新数据库中的数据
        pass

    def select(self, table_name, number=0, fields=(), start=0):
        # 选择
        if not fields:
            fields = self._get_fields(table_name)
        sql = 'select %s from %s' % (','.join([field.join(['"', '"']) for field in fields]), table_name)
        if number:
            sql = ' '.join([sql, 'limit %s,%s' % (start, number)])
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return fields, data

    def row_number(self, table_name):
        # 获取行数
        sql = 'select count(*) from %s' % (table_name,)
        self.cursor.execute(sql)
        number = self.cursor.fetchall()[0][0]
        return number


# 用于临时保存在python中，
# 存储格式为： { table_name1: [item1, item2...], table_name2: [item1, item2...]}
# 若table_name不存在则自动创建table_name键，并初始化值为空列表(即list())
class DataBuffer(dict):
    def __init__(self, name='', cache_dir='__cached__', format='sqlite3', clear=False, *args, **kwargs):
        self.cache_dir = cache_dir
        self.cache_format = format
        if format == 'sqlite3':
            file_path = os.path.join(cache_dir, '.'.join(['_'.join([name, 'data_cache']), format]))
            if clear is True and os.path.exists(file_path):
                os.remove(file_path)
            self.db = DB(file_path)
            super(DataBuffer, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        super(DataBuffer, self).__setitem__(key, value)
        self.cache(10000)

    def __getitem__(self, item):
        if item not in self:
            super(DataBuffer, self).__setitem__(item, [])
        return super(DataBuffer, self).__getitem__(item)

    def cache(self, number=10000):
        for table_name in self:
            if len(self[table_name]) > number:
                table_data = self.pop(table_name)
                super(DataBuffer, self).__setitem__(table_name, [])
                self.db.insert_data(table_name, table_data)

    def to_excel(self, file_path='data1.xlsx', add_mode=False):
        import pandas as pd
        import xlrd
        ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]|\xef|\xbf')
        func = lambda x: x if type(x) is not str else ILLEGAL_CHARACTERS_RE.sub('', x.encode('gb2312',
                                                                                             errors='ignore').decode(
            'gb2312'))
        self.cache(0)
        # 从缓存中加载数据
        data = {}
        for table_name in self:
            table_fields, table_data = self.db.select(table_name)
            df = pd.DataFrame(table_data, columns=table_fields).applymap(func)
            data[table_name] = df

        # 追加模式, 追加数据
        if add_mode and os.path.exists(file_path):
            book = xlrd.open_workbook(file_path)
            # xlrd用于获取每个sheet的sheetname
            # count = len(book.sheets())
            for sheet in book.sheets():
                df = pd.read_excel(file_path, sheet.name, index_col=None)
                if sheet.name in data:
                    data[sheet.name] = df.append(data[sheet.name])
                else:
                    data[sheet.name] = df
        self._to_excel(file_path=file_path, data=data)

    def _to_excel(self, file_path, data):
        # 将数据写入excel
        import pandas as pd

        writer = pd.ExcelWriter(file_path)
        for sheet_name, sheet_data in data.items():
            print('saving %s row_number:%s' % (sheet_name, len(sheet_data)))
            df = pd.DataFrame(sheet_data)
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        writer.save()
        writer.close()

    def to_excel_div(self, file_path='data1.xlsx', add_mode=False, limit=200000):
        # 将数据分文件存储
        import pandas as pd
        ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]|\xef|\xbf')
        func = lambda x: x if type(x) is not str else ILLEGAL_CHARACTERS_RE.sub('', x.encode('gb2312',
                                                                                             errors='ignore').decode(
            'gb2312'))
        # 写入数据库
        self.cache(0)
        # 从缓存中加载数据
        row_number = max([self.db.row_number(table_name) for table_name in self])
        for start in range(0, row_number, limit):
            data = {}
            # 获取数据
            for table_name in self:
                table_fields, table_data = self.db.select(table_name, number=limit, start=start)
                df = pd.DataFrame(table_data, columns=table_fields).applymap(func)
                data[table_name] = df
            # 保存数据
            div_file_path = str(start).join(os.path.splitext(file_path))
            self._to_excel(file_path=div_file_path, data=data)

    def to_csv(self, file_prefix='data_', add_mode=False, format_data=False):
        import csv
        ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]|\xef|\xbf')
        func = lambda x: x if type(x) is not str else ILLEGAL_CHARACTERS_RE.sub('', x.encode('gb2312',
                                                                                             errors='ignore').decode(
            'gb2312'))
        self.cache(0)
        # 从缓存中加载数据
        for table_name in self:
            file_path = ''.join([file_prefix, table_name, '.csv'])
            with open(file_path, ('a' if add_mode else 'w'), encoding='gb2312', newline='\n', errors='ignore') as f:
                f_csv = csv.writer(f)
                for start in range(0, self.db.row_number(table_name), 100000):
                    # 从缓存中读取数据
                    table_fields, table_data = self.db.select(table_name, number=100000, start=start)
                    # 格式化数据
                    if format_data:
                        table_data = tuple(map(lambda x: tuple(map(func, x)), table_data))
                    # 添加表头
                    if start == 0 and not add_mode:
                        f_csv.writerow(table_fields)
                    # 写入数据
                    f_csv.writerows(table_data)

    # 写入到postgreSql
    def write_to_table(self, df, schema, table_name, spiderType, password='1q2w3e4r', host='127.0.0.1', DB='House',
                       if_exists='append'):
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
        db_engine = create_engine('postgresql://postgres:{}@{}/{}'.format(password, host, DB))  # 初始化引擎
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
                if spiderType == 'esf':
                    copy_cmd = '''COPY "%s"."%s"("id","城市", "区县", "标题url", "小区", "地址", "数据来源", "单价", "总价", "户型", "面积", "楼层", "建筑年份", "朝向", "抓取时间", "抓取年份", "抓取月份", "关注人数", "标签") FROM STDIN HEADER DELIMITER ',' CSV''' % (
                        schema, table_name)
                elif spiderType == 'chengjiao':
                    copy_cmd = '''COPY "%s"."%s"("城市", "区县", "标题", "标题url", "地址", "描述", "价格", "标签", "评论数量", "抓取时间", "抓取月份", "数据来源", "id") FROM STDIN HEADER DELIMITER ',' CSV''' % (
                        schema, table_name)
                else:
                    copy_cmd = '''COPY "%s"."%s" FROM STDIN HEADER DELIMITER ',' CSV''' % (schema, table_name)
                cursor.copy_expert(copy_cmd, string_data_io)
            connection.connection.commit()

    def to_postgreSql(self):
        import pandas as pd
        ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]|\xef|\xbf')
        func = lambda x: x if type(x) is not str else ILLEGAL_CHARACTERS_RE.sub('',
                                                                                x.encode('gb2312',
                                                                                         errors='ignore').decode(
                                                                                    'gb2312'))
        self.cache(0)
        # 从缓存中加载数据
        for table_name in self:
            table_fields, table_data = self.db.select(table_name)
            df = pd.DataFrame(table_data, columns=table_fields).applymap(func)
            print('saving row_number: ', df.shape)

            if table_name == 'beke_esf':  # 保存二手房(在售字段)数据库
                df = df[
                    ["id", "城市", "区县", "标题url", "小区", "地址", "数据来源", "单价", "总价", "户型", "面积", "楼层", "建筑年份", "朝向", "抓取时间",
                     "抓取年份", "抓取月份", "关注人数", "标签"]]

                # TODO 保存到大数据库
                # self.write_to_table(df, schema="Esf", table_name="esf", spiderType='esf',password='1q2w3e4r',host='192.168.88.51')
                # TODO 保存到本地
                self.write_to_table(df, DB='ESF', schema="public", table_name="Esf_2020", spiderType='esf', password='1q2w3e4r', host='127.0.0.1')

            if table_name == 'beke_chengjiao':  # 保存成交(成交字段)数据库
                self.write_to_table(df, schema="Esf", table_name="chengjiao", spiderType='chengjiao')

            if table_name == 'beke_xiaoqu':  # 保存小区(小区字段)数据库
                print(df.head(), df.shape)


# 将数据保存到指定excel表格中，若add_mode为True, 则在表格中追加这些数据
def save2excel(data, excel_file='data1.xlsx', add_mode=False):
    import pandas as pd
    import xlrd

    if add_mode:
        book = xlrd.open_workbook(excel_file)
        # xlrd用于获取每个sheet的sheetname
        # count = len(book.sheets())
        for sheet in book.sheets():
            df = pd.read_excel(excel_file, sheet.name, index_col=None)
            if sheet.name in data:
                data[sheet.name] = df.append(data[sheet.name])
            else:
                data[sheet.name] = df
    writer = pd.ExcelWriter('data1.xlsx')
    if add_mode:
        pd.read_excel()
    for sheet_name, sheet_data in data.items():
        print('saving %s' % (sheet_name,))
        df = pd.DataFrame(sheet_data)
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    writer.save()
    writer.close()


if __name__ == '__main__':
    # 这个脚本用于输出爬虫缓存中的数据
    from datetime import datetime

    city_name = '来宾'
    cache_dir = r'G:\爬虫\智联招聘\zlzp\zlzp\spiders\__cached__'
    spider_name = 'job_spider2'
    save_name = '智联'
    save_dir = r'G:\爬虫\utils'
    limit = 100
    table_names = ['company', 'job']  # 所要保存的表名， 因为这里没有添加数据，所以没有表名在缓冲区中

    file_prefix = os.path.join(save_dir, '{}_{}_'.format(datetime.now().strftime('%y-%m-%d'), city_name, ))

    data = DataBuffer(name='_'.join([city_name, spider_name]), cache_dir=cache_dir)
    data.update({table_name: [] for table_name in table_names})
    data.to_excel_div(''.join([file_prefix, '{}.xlsx'.format(save_name)]), limit=100)
