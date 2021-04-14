import pymysql
import os
import csv
import pymongo
from urllib import parse

MONGODB_CONFIG = {
   "host": "8.135.119.198",
   "port": "27017",
   "user": "hladmin",
   "password": parse.quote("Hlxkd3,dk3*3@"),
}

poi = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['gaode']['pos']
poi_use = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['gaode']['pos_use']



def list_dir(file_dir):
    '''
        通过 listdir 得到的是仅当前路径下的文件名，不包括子目录中的文件，如果需要得到所有文件需要递归
    '''
    dir_list = os.listdir(file_dir)
    for cur_file in dir_list:
        # 获取文件的绝对路径
        path = os.path.join(file_dir, cur_file)
        if os.path.isfile(path): # 判断是否是文件还是目录需要用绝对路径
            city = cur_file.split("_")[0]
            #print("{0} : is file!".format(cur_file))
            with open(file_dir+os.sep+cur_file, 'r') as f:
                reader = csv.reader(f)
                i = 0
                for row in reader:
                    i += 1
                    if i == 1:
                        continue
                    gridid = row[0]
                    ulbr = row[1].strip("(").strip(")")
                    ulbr_0 = row[2].strip("(").strip(")")
                    ulbr_1 = row[3].strip("(").strip(")")
                    ulbr_2 = row[4].strip("(").strip(")")
                    ulbr_3 = row[5].strip("(").strip(")")
                    # for r in row[2:]:
                    #     rectangle_pos = r.strip("(").strip(")")
                    #     use_pos_list = rectangle_pos.split(",")
                    #     use_pos = ",".join(str(('%.6f' % float(x))) for x in use_pos_list)
                    poi.insert_one({"gridid":gridid,"city":city,"ulbr":ulbr,"ulbr_0":ulbr_0,"ulbr_1":ulbr_1,"ulbr_2":ulbr_2,"ulbr_3":ulbr_3,"status":0})
                    #poi.update()
        # if os.path.isdir(path):
        #     print("{0} : is dir!".format(cur_file))
        #     list_dir(path)# 递归子目录

list_dir("D:\grids_csv\small")
print("over...")
