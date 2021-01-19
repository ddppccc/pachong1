# 百度贴吧城市爬虫

运行时段:大概一两个月来一次就好，运行时先把“处理词云.py"全局注释。或者注释掉主函数中代码避免无数据时直接运行该文件

运行前提:需要若干个在文件中声明过的MongoDB数据库

1.BaiduTieba下的city数据库

2.BaiduTieba下的Tiezi数据库

3.BaiduTieba下的Comment数据库

city用于判断已经爬过的城市数据，避免中断重头运行

其余用于存储和处理词云生成词频

3.使用scrapy方式运行tieba即可