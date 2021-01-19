# 贝壳指数

运行时段:日更

运行前提:

拥有MongoDB数据库

拥有Beike下的city_map 该库用于判断城市是否爬取，城市是否有数据

拥有Beike下的info_new 该库用于存放数据

拥有Beike下的beike_second 用于存放二手房指数数据

1.Base_info_spider.py

第一次运行需要初始化city_map数据库，打开主函数下的get_cityMap()注释即可



2.Beike_second.py

大概半年运行一次，四五个月一次也行，因为一个月只有一条，网站上显示月份有半年，所以半年可以跑一次超过半年就会丢失数据。

直接跑，没有要求

