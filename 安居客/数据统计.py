from urllib import parse
import pymongo
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
    import psycopg2
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

def getnum():
    info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
        MONGODB_CONFIG['user'],
        MONGODB_CONFIG['password'],
        MONGODB_CONFIG['host'],
        MONGODB_CONFIG['port']),
        retryWrites="false")[database][f'{types}_数据_{date}']
    try:
        info_base.create_index('城市', unique=False)
    except Exception as e:
        print(e)
    for i in info_base.distinct('城市'):
        print(i,'正在统计数量')
        num=info_base.count_documents({'城市':i})
        pgsql(i, num)
if __name__ == '__main__':
    # database='安居客'
    # types='二手房'
    # date='202106'
    database=input('请输入数据库(如：安居客)')
    types=input('请输入类型(如：二手房)')
    date=input('请输入日期(如：202106)')
    getnum()
    print(database,types,date,'运行完毕...')





