import os
import datetime
import shutil



# 删除非当月记录数据
def delete_log_dir():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'log')
    for cityDir in os.listdir(path):
        if datetime.datetime.now().strftime('%Y-%m') not in cityDir:
            print('删除上月记录: ',os.path.join(path,cityDir))
            shutil.rmtree(os.path.join(path,cityDir))


# 检查当月区县数据是否存在,
def check(city, region):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'log')
    file_dir = '{}_{}/{}'.format(city,datetime.datetime.now().strftime('%Y-%m'), region)
    path2 = os.path.join(path, file_dir)
    if os.path.exists(path2):
        return True
    return False


# 保存已经抓取过的区县
def save_region(city, region):
    path1 = os.path.dirname(os.path.dirname(__file__))
    path2 = '{}/log/{}_{}'.format(path1,city, datetime.datetime.now().strftime('%Y-%m'))
    os.path.exists(path2) or os.makedirs(path2)
    file_name = os.path.join(path2, region)
    os.mkdir(file_name)



if __name__ == '__main__':
    # save_region('北京','朝阳')

    print(check(path='', city='深圳', region='南山'))
    delete_log_dir()















