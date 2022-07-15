import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

'''
    最后成功提取了
    '电影排名','电影名','上映时间','导演','主演','电影类型','电影评分','评价人数','电影链接'
    最后将结果输出到了 豆瓣电影Top250.xlsx 
    但是还存在问题：就是提取语言和制片国家/地区时，出现没有selector的情况。
    要解决该问题可能需要xpath
'''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55'}

start_num = [i for i in range(0, 226, 25)]

list_url_mv = []  # 所有电影的URL
def get_proxy():
    while True:
        try:
            ip = requests.get('http://47.111.226.234:8000/getip2/')
            if ip.status_code ==200:
                return ip.text

            # return requests.get('http://1.116.204.248:5000/proxy').text
        except:
            # num = 3
            # while num:
            #     try:
            #         return requests.get('http://1.116.204.248:5000/proxy').text
            #     except:
            #         print('暂无ip，等待20秒')
            #         time.sleep(20)
            #         num -= 1
            print('暂无ip')

for start in start_num:
    url = 'https://movie.douban.com/top250?start={}&filter='.format(start)
    print('正在处理url：', url)
    proxies = get_proxy()
    response = requests.get(url=url, headers=headers,proxies=proxies)
    soup = BeautifulSoup(response.text, 'html.parser')

    url_mv_list = soup.select('#content > div > div.article > ol > li > div > div.info > div.hd > a')
    # print(url_mv_list)
    for index_url in range(len(url_mv_list)):
        url_mv = url_mv_list[index_url]['href']
        list_url_mv.append(url_mv)
        # print(url_mv)


# 对每部电影进行处理
def loading_mv(url, number):
    list_mv = []
    print('-----正在处理第{}部电影-----'.format(number + 1))
    list_mv.append(number + 1)  # 排名

    # 解析网页
    response_mv = requests.get(url=url, headers=headers)
    soup_mv = BeautifulSoup(response_mv.text, 'html.parser')

    # 爬取电影名
    try:
        mv_name = soup_mv.find_all('span', attrs={'property': 'v:itemreviewed'})  # 电影名
        mv_name = mv_name[0].get_text()
        list_mv.append(mv_name)
    except:
        pass
    # print(mv_name)

    # 爬取电影的上映时间
    mv_year = soup_mv.select('span.year')  # 电影上映时间
    mv_year = mv_year[0].get_text()[1:5]
    list_mv.append(mv_year)
    # print(mv_year)

    # 爬取导演信息
    list_mv_director = []  # 导演
    mv_director = soup_mv.find_all('a', attrs={'rel': "v:directedBy"})
    for director in mv_director:
        list_mv_director.append(director.get_text())
    string_director = '/'.join(list_mv_director)  # 重新定义格式
    list_mv.append(string_director)
    # print(list_mv_director)

    # 爬取主演信息
    list_mv_star = []  # 主演
    mv_star = soup_mv.find_all('span', attrs={'class': 'actor'})
    if mv_star == []:  # 在第210部时没有主演
        list_mv.append(None)
    else:
        mv_star = mv_star[0].get_text().strip().split('/')
        mv_first_star = mv_star[0].split(':')
        list_mv_star.append(mv_first_star[-1].strip())
        del mv_star[0]  # 去除'主演'字段
        for star in mv_star:
            list_mv_star.append(star.strip())
        string = '/'.join(list_mv_star)  # 重新定义格式
        list_mv.append(string)

    # 爬取电影类型
    list_mv_type = []  # 电影类型
    mv_type = soup_mv.find_all('span', attrs={'property': 'v:genre'})
    for type in mv_type:
        list_mv_type.append(type.get_text())
    string_type = '/'.join(list_mv_type)
    list_mv.append(string_type)
    # print(list_mv_type)

    # 爬取电影评分
    mv_score = soup_mv.select('strong.ll.rating_num')  # 评分
    mv_score = mv_score[0].get_text()
    list_mv.append(mv_score)

    # 爬取评价人数
    mv_evaluation_num = soup_mv.select('a.rating_people')  # 评价人数
    mv_evaluation_num = mv_evaluation_num[0].get_text().strip()
    list_mv.append(mv_evaluation_num)

    # 爬取剧情简介
    mv_plot = soup_mv.find_all('span', attrs={"class": "all hidden"})  # 剧情简介
    if mv_plot == []:
        list_mv.append(None)
    else:
        string_plot = mv_plot[0].get_text().strip().split()
        new_string_plot = ' '.join(string_plot)
        list_mv.append(new_string_plot)

    # 加入电影网址
    list_mv.append(url)

    return list_mv


# url1 = 'https://movie.douban.com/subject/1292052/'
# url2 = 'https://movie.douban.com/subject/26430107/'      # 210部
# a = loading_mv(url1,1)
# # b = loading_mv(url2,210)
# # list_all_mv.append(a)
# # list_all_mv.append(b)

#=======================================================================================================================

list_all_mv = []

dict_mv_info = {}
for number in range(len(list_url_mv)):
    mv_info = loading_mv(list_url_mv[number], number)
    list_all_mv.append(mv_info)
print('-----运行结束-----')

pd = DataFrame(list_all_mv, columns=['电影排名', '电影名', '上映时间', '导演', '主演', '电影类型', '电影评分', '评价人数', '电影简介', '电影链接'])
# print(pd)

pd.to_excel(r'e:\data\豆瓣电影Top250.xlsx')


#   数据分析 处理=====================================================数据分析 = ===========================================
'''
对爬取得到的豆瓣电影Top250进行数据分析
分析内容：
1. 对时间：对时间分析
            绘制直方图
            饼图
            折线图——电影
2.对类型： 电影类型随时间变化
            绘制电影类型随时间变化
            电影类型词云图
3.对主演或导演： 以电影评分分析演员或者导演
            前十名主演
            查询演员/导演出演信息
            所有演员导演出演信息
'''

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import wordcloud
import imageio


# csv_path = '豆瓣电影Top250.csv'     # 不能用csv进行处理，可能会出现错误

# 读取excel转换成dataframe，方便读取
def excel_to_dataframe(excel_path):
    df = pd.read_excel(excel_path, keep_default_na=False)  # keep_default_na=False 得到的结果是''，而不是nan
    return df


excel_path = r'C:\Users\86178\Desktop\豆瓣电影Top250.xlsx'
data_mv = excel_to_dataframe(excel_path)

dict_time = {}
for time in data_mv['上映时间']:
    dict_time[time] = dict_time.get(time, 0) + 1

list_time = list(dict_time.items())
list_time.sort(key=lambda x: x[1], reverse=True)
list_year = []  # 年份
list_times = []  # 出现次数
for t in list_time:
    list_year.append(t[0])
    list_times.append(t[1])


# 绘制直方图
def make_Histogram(list_x, list_y, color):
    # 解决中文显示问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.bar(list_x, list_y, width=1, color=color)
    plt.title('电影上映时间与所产电影部数直方图')
    plt.xlabel('电影上映时间')
    plt.ylabel('年产电影部数')
    plt.show()


# make_Histogram(list_year,list_times,color=['g','y','m'])     # 绘制电影年份出现次数直方图

# 绘制饼图
def make_Pie(list_times, list_year):
    mpl.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei', 'FangSong']  # 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体
    mpl.rcParams['font.size'] = 12  # 字体大小
    mpl.rcParams['axes.unicode_minus'] = False  # 正常显示负号

    plt.figure(figsize=(10, 10), dpi=100)  # 视图的大小
    plt.pie(list_times,  # 指定绘图数据
            labels=list_year,  # 添加饼图圈外的标签
            autopct='%1.2f%%',  # 设置百分比格式
            textprops={'fontsize': 10},  # 设置饼图中的属性字体大小、颜色
            labeldistance=1.05)  # 设置各扇形标签（图例）与圆心的距离
    # plt.legend(fontsize=7)                 # 设置饼图指示
    plt.title('年产电影部数占比')
    plt.show()


pie_other = len([i for i in list_time if i[1] == 1])  # 将年份电影为1的归为其它类
list_pie_year = []
list_pie_times = []

for i in list_time:
    if i[1] == 1:
        break
    else:
        list_pie_year.append(i[0])
        list_pie_times.append(i[1])
list_pie_year.append('其它电影为1的年份')
list_pie_times.append(pie_other)


#
# make_Pie(list_pie_times,list_pie_year)
# make_Pie(list_times,list_year)

# 绘制折现图
def make_Plot(list_year, list_times):
    # 解决中文显示问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.title('年产电影个数折现图')
    plt.xlabel('电影上映时间')
    plt.ylabel('年产电影部数')
    plt.plot(list_year, list_times)
    plt.show()


list_plot_year = []
list_plot_times = []
list_time.sort(key=lambda x: int(x[0]))
for t in list_time:
    list_plot_year.append(t[0])
    list_plot_times.append(t[1])
# make_Plot(list_plot_year,list_plot_times)

mv_type = data_mv['电影类型']
dict_type = {}
for type in mv_type:
    line = type.split('/')
    for t in line:
        dict_type[t] = dict_type.get(t, 0) + 1
list_type = list(dict_type.items())
list_type.sort(key=lambda x: x[1], reverse=True)


# 绘制词云图
def c_wordcloud(ls):
    # string1 = ' '.join(ls)
    gpc = []
    for i in ls:
        gpc.append(i[0])
    string1 = " ".join('%s' % i for i in gpc)
    color_mask = imageio.imread(r"logo.jpg")
    wc = wordcloud.WordCloud(random_state=30,
                             width=600,
                             height=600,
                             max_words=30,
                             background_color='white',
                             font_path=r'msyh.ttc',
                             mask=color_mask
                             )
    wc.generate(string1)
    plt.imshow(wc)
    plt.show()
    # wc.to_file(path)


# c_wordcloud(list_type)


# [年份，电影类型]
list_time_type = []
for i in range(250):
    line = data_mv['电影类型'][i].split('/')
    for j in line:
        time_type = []
        time_type.append(data_mv['上映时间'][i])
        time_type.append(j)
        list_time_type.append(time_type)

dict_time_type = {}
for i in list_time_type:
    dict_time_type[tuple(i)] = dict_time_type.get(tuple(i), 0) + 1
list_num_time_type = list(dict_time_type.items())
list_num_time_type.sort(key=lambda x: x[1], reverse=True)


# 制作一种电影类型的发展史（以电影类型为单位）
def mv_time_type(type_name):
    list_mv_type = []
    for num in list_num_time_type:
        if num[0][1] == type_name:
            list_mv_type.append(num)
    list_mv_type.sort(key=lambda x: x[0][0], reverse=False)
    list_year = []
    list_times = []
    for t in list_mv_type:
        list_year.append(t[0][0])
        list_times.append(t[1])

    # 解决中文显示问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.title('电影类型"{}"的发展史'.format(type_name))
    plt.xlabel('年份')
    plt.ylabel('每年出现的次数')
    plt.plot(list_year, list_times)
    plt.show()


# mv_time_type('剧情')
# mv_time_type('科幻')      # 主要集中在2000以后


# 计算导演和主演的每部作品的得分和总得分
def people_score(peo_dir_star):
    list = []
    for num in range(250):
        if data_mv[peo_dir_star][num] == '':
            continue
        else:
            peoples = data_mv[peo_dir_star][num].split('/')
        for people in peoples:
            list_p_s = []
            list_p_s.append(people)
            list_p_s.append(data_mv['电影评分'][num])
            list_p_s.append(data_mv['电影排名'][num])
            list_p_s.append(data_mv['电影名'][num])
            list.append(list_p_s)
    return list


list_director = people_score('导演')
list_star = people_score('主演')


# 最佳导演或者演员----根据总分求得
def best_people(list_people):
    dict_people = {}
    for i in list_people:
        dict_people[i[0]] = dict_people.get(i[0], []) + [(i[1], i[2], i[3])]

    for i in dict_people.items():
        i[1].append(float('{:.2f}'.format(sum([j[0] for j in i[1]]))))
    # ('巩俐', [(9.6, 2, '霸王别姬'), (9.3, 30, '活着'), (8.7, 109, '唐伯虎点秋香 唐伯虎點秋香'), '27.60'])

    list_new_people = list(dict_people.items())
    list_new_people.sort(key=lambda x: x[1][-1], reverse=True)

    print('搜索结束，请开始您的操作（输入数字）!\n---输入1排名前十的主演---\n---输入2搜索演员的出演情况---\n---输入3输出所有演员---')
    print('-----输入enter退出-----')

    select_number = input('开始输入操作：')
    while select_number != '':

        if select_number == '1':
            print('前十演员出演信息:')
            list_all_score = []  # 总分
            list_prople_name = []
            for i in list_new_people[0:10]:
                print(i)

                list_prople_name.append(i[0])
                list_all_score.append(i[1][-1])

            # 解决中文显示问题
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['axes.unicode_minus'] = False

            # plt.figure(figsize=(10, 10), dpi=100)  # 视图的大小
            plt.title('前十演员总评分')
            plt.xlabel('演员')
            plt.ylabel('总评分')
            plt.bar(list_prople_name, list_all_score, width=0.5)
            plt.show()

        elif select_number == '2':
            # star_name = input('输入您想要知道的演员名：')
            star_name = ' '
            while star_name != '':
                star_name = input('输入您想要知道的演员名：')
                list_mv_name = []  # 电影名
                list_mv_score = []  # 电影评分
                for number, i in enumerate(list_new_people):
                    if star_name == i[0]:
                        all_score = i[1][-1]  # 总分
                        del i[1][-1]
                        for j in i[1]:
                            list_mv_name.append(j[2])
                            list_mv_score.append(j[0])
                            print('{} 主演豆瓣电影Top250中排名{}的《{}》评分为 {}'.format(star_name, j[1], j[2], j[0]))
                        print("{}共主演了{}部电影，所有总分为{}，在所有演员中排名第{}".format(star_name, len(i[1]), all_score, number + 1))
                        print('查询结束！')

                        # 计算饼图
                        def pie_mv_score():
                            mpl.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei',
                                                               'FangSong']  # 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体
                            mpl.rcParams['font.size'] = 12  # 字体大小
                            mpl.rcParams['axes.unicode_minus'] = False  # 正常显示负号

                            plt.figure(figsize=(10, 10))
                            plt.pie(list_mv_score,
                                    labels=list_mv_name,
                                    autopct='%1.2f%%',  # 计算百分比，设置及格式
                                    textprops={'fontsize': 10})
                            plt.title('{}的主演电影总分比---总排名为{}'.format(star_name, number + 1))
                            plt.show()

                        pie_mv_score()

                        break

                else:
                    print('查无此人！')
                    break

        elif select_number == '3':
            for i in list_new_people:
                print(i)

        else:
            print('无此项操作！')

        select_number = input('查询结束，您还可以继续输入查询序号：')

    print('-----查询结束-----')


best_people(list_star)