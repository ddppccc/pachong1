import pymongo
import csv

migrate_in_trend_data = pymongo.MongoClient(host='127.0.0.1', port=27017)['migrate_data']['migrate_in_trend_data']
migrate_out_trend_data = pymongo.MongoClient(host='127.0.0.1', port=27017)['migrate_data']['migrate_out_trend_data']
migrate_in_peer_data = pymongo.MongoClient(host='127.0.0.1', port=27017)['migrate_data']['migrate_in_peer_data']
migrate_out_peer_data = pymongo.MongoClient(host='127.0.0.1', port=27017)['migrate_data']['migrate_out_peer_data']
in_city_info = pymongo.MongoClient(host='127.0.0.1', port=27017)['migrate_data']['city_migrate_in_data_test']
out_city_info = pymongo.MongoClient(host='127.0.0.1', port=27017)['migrate_data']['city_migrate_out_data_test']


def statis_output(title, rowlist, database):
    csvfile = open('{}'.format(title), 'w+', newline='', encoding='utf-8')
    res_writer = csv.writer(csvfile, dialect='excel')
    res_writer.writerow(rowlist)
    for item in database.find():
        res_writer.writerow(list(item.values())[1:])


statis_output('高德地图_全国_2020-12-9_1-9_迁徙入规模指数.csv', ['地区', '时间', '迁徙意愿指数', '实际迁徙指数'], migrate_in_trend_data)
statis_output('高德地图_全国_2020-12-9_1-9_迁徙出规模指数.csv', ['地区', '时间', '迁徙意愿指数', '实际迁徙指数'], migrate_out_trend_data)
statis_output('高德地图_全国_2020-12-9_1-9_去年迁徙入规模指数.csv', ['地区', '时间', '迁徙意愿指数', '实际迁徙指数'], migrate_in_peer_data)
statis_output('高德地图_全国_2020-12-9_1-9_去年迁徙出规模指数.csv', ['地区', '时间', '迁徙意愿指数', '实际迁徙指数'], migrate_out_peer_data)
statis_output('高德地图_全国_2020-12-9_1-9_地区城市迁入指数表.csv', ['地区', '城市', '时间', '迁徙意愿指数', '实际迁徙指数'], in_city_info)
statis_output('高德地图_全国_2020-12-9_1-9_地区城市迁出指数表.csv', ['地区', '城市', '迁徙意愿指数', '实际迁徙指数', '时间'], out_city_info)
