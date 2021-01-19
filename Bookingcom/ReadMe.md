# 缤客酒店爬虫

该爬虫应该不会被再次使用

1.需要拥有mangoDB数据库

Booking下的info_fin

2.需要代理，修改地址就行

3.就算有代理也很容易获取不到户型，需要隔一段时间检查一下，如果获取不到户型需要主动更换logstic.py中的Headers中的

```
X-Booking-Info
X-Booking-CSRF
```

字段

已经爬取过的国家放到一串国家列表中， 没有就全部清除

```python

```