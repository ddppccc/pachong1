# 高德地图迁徙指数

1.需要拥有以下MongoDB数据库

```python
migrate_in_trend_data = pymongo.MongoClient(host='127.0.0.1', port=27017)['migrate_data']['migrate_in_trend_data']
migrate_out_trend_data = pymongo.MongoClient(host='127.0.0.1', port=27017)['migrate_data']['migrate_out_trend_data']
migrate_in_peer_data = pymongo.MongoClient(host='127.0.0.1', port=27017)['migrate_data']['migrate_in_peer_data']
migrate_out_peer_data = pymongo.MongoClient(host='127.0.0.1', port=27017)['migrate_data']['migrate_out_peer_data']
in_city_info = pymongo.MongoClient(host='127.0.0.1', port=27017)['migrate_data']['city_migrate_in_data_test']
out_city_info = pymongo.MongoClient(host='127.0.0.1', port=27017)['migrate_data']['city_migrate_out_data_test']
```

2.运行时更改logistic.py中的star 和 end，这是运行时段。注意end不能是今天

3.运行in_out_city_spider 和 trenddo

4.运行outputData输出文件