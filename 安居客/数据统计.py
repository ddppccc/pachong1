from urllib import parse
import pymongo
import re
import psycopg2
MONGODB_CONFIG = {
   "host": "8.135.119.198",
   "port": "27017",
   "user": "hladmin",
   "password": parse.quote("Hlxkd3,dk3*3@"),
   "db": "dianping",
   "collections": "dianping_collections",
}
def pgsql(city,number):
    ### pip install psycopg2

    ## 连接到一个给定的数据库
    conn = psycopg2.connect(database="pachong_count", user="urasrsql",
                            password="1q2w3e4r", host="8.135.124.125", port="5432")
    ## 建立游标，用来执行数据库操作
    cursor = conn.cursor()
    cursor.execute(f"""
        insert into count (source,source_type,date,category,number)
        values('{database}', '{types}', '{date}', '{city}', {str(number)});
    """)
    conn.commit()
    cursor.close()
    conn.close()

def getnum(database, tables):
    info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
        MONGODB_CONFIG['user'],
        MONGODB_CONFIG['password'],
        MONGODB_CONFIG['host'],
        MONGODB_CONFIG['port']),
        retryWrites="false")[database][tables]
    try:
        info_base.create_index('城市', unique=False)
    except Exception as e:
        print(e)
    for i in info_base.distinct('城市'):
        print(i,'正在统计数量')
        num=info_base.count_documents({'城市':i})
        pgsql(i, num)



def getchoice():
    while 1:
        print('请输入序号选择统计的数据')
        for i in range(len(databaselist)):
            print(i, '--------', databaselist[i])
        try:
            opt = int(input('请输入序号'))
            print('选择', databaselist[opt])
            break
        except:
            print('输入错误')
    database = databaselist[opt]
    db = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
        MONGODB_CONFIG['user'],
        MONGODB_CONFIG['password'],
        MONGODB_CONFIG['host'],
        MONGODB_CONFIG['port']),
        retryWrites="false")[database]
    coll_names = db.list_collection_names()
    list = []
    for i in coll_names:
        if '数据' not in i:
            continue
        if '清洗' in i:
            continue
        list.append(i)
    while 1:
        print('请输入序号选择统计的数据')
        for i in range(len(list)):
            print(i, '--------', list[i])
        try:
            opt = int(input('请输入序号'))
            print('选择', list[opt])
            tables = list[opt]
            types=tables.split('_')[0]
            date=re.findall('_(\d+)',tables)[0]
            return database, tables,types,date
        except:
            print('输入错误')


if __name__ == '__main__':
    # database='安居客'
    # types='二手房'
    # date='202106'
    # database=input('请输入数据库(如：安居客)')
    # types=input('请输入类型(如：二手房)')
    # date=input('请输入日期(如：202106)')

    # databaselist = ['安居客', '房天下']
    # database, tables,types,date=getchoice()
    #
    # getnum(database, tables)
    # print(database,tables,'运行完毕...')
    conn = psycopg2.connect(database="pachong_count", user="urasrsql",
                            password="1q2w3e4r", host="8.135.124.125", port="5432")
    ## 建立游标，用来执行数据库操作
    cursor = conn.cursor()
    sqlstr = 'select * from public.count  ORDER  BY "category" DESC'
    cursor.execute(sqlstr)
    res = cursor.fetchall()
    list6={}
    list10={}
    for i in res:
        # print(i[3],i[4],i[5])
        if i[1] != '房天下':continue
        if i[3] == '202109':
            list6[i[4]]=i[5]
        if i[3] == '202110':
            list10[i[4]]=i[5]
    print(list6)
    print(list10)

    for k,v in list10.items():
        try:
            if v < (list6[k]*0.7):
                print(10,k,v)
                print(6,k,list6[k])
        except Exception as e:
            # print(e)
            pass
    print(0)










