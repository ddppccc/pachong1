import pymongo

# a = ['10月', '11月', '12月', '1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月']
# b = [14150, 14428, 15015, 8233, 2467, 16634, 22173, 22853, 19008, 19738, 19919, 18842]
# c = [88334, 100489, 107649, 49694, 825, 87501, 180992, 184796, 150455, 179045, 184468, 151710]
# city_map = pymongo.MongoClient(host='127.0.0.1', port=27017)['Beike']['city_map']
#
# pass_year = '2019' + '年'
#
# this_year = '2020' + '年'
# aaa = [pass_year+i if a.index(i) < a.index('1月') else this_year+i for i in a]
# print(aaa)


# print(dict(zip(b,zip(a,c))))
# d = dict(zip(b,zip(a,c)))
# for i in d.keys():
#     print(i)
#     print(d[i][0])
#     print(d[i][1])

# print(city_map.find({'city':'合肥'}))
# for info in city_map.find({'city':'合肥'}):
#     print(info['url'])
#
# d = []
# d.extend(a)
# d.extend(b)
# d.extend(c)
# print(d)

