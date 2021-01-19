import os

import pandas as pd

d = []
for city in ['石家庄', '太原', '呼和浩特', '沈阳', '长春', '哈尔滨', '南京', '沈阳',
                    '杭州', '合肥', '福州', '南昌', '济南', '郑州', '武汉', '长沙', '广州', '南宁',
                    '海口', '成都', '贵阳', '昆明', '拉萨', '西安', '兰州', '西宁', '银川', '乌鲁木齐',
                    '深圳', '北京', '天津', '上海', '重庆', '全国']:
    #     if city != '上海': continue
    path_name_1 = os.path.join('国文临时', '{}_{}.xlsx'.format(city, 1))
    path_name_2 = os.path.join('国文临时', '{}_{}.xlsx'.format(city, 2))
    print(city)
    df1 = pd.read_excel(path_name_1)
    # df2 = pd.read_excel(path_name_2)

    df1 = df1.query('type == "all"')
    df1['keyword'] = df1['keyword'].map(lambda x: x.replace("[{'name': '", '').replace("', 'wordType': 1}]", ""))
    df1 = df1.pivot_table(values='index', columns='keyword', index='date', fill_value=0).reset_index()

    # df2 = df2.query('type == "all"')
    # df2['keyword'] = df2['keyword'].map(lambda x: x.replace("[{'name': '", '').replace("', 'wordType': 1}]", ""))
    # df2 = df2.pivot_table(values='index', columns='keyword', index='date', fill_value=0).reset_index()
    # print(df2.head())
    df1['城市'] = city
    df1 = df1[['date', '城市', 'ktv', '三国杀', '健身', '儿子', '儿童', '儿童乐园', '剧本杀', '台球', '夜店', '女儿',
       '女孩', '婴儿', '孙女', '孙子', '孩子', '密室', '密室逃脱', '小孩', '小孩子', '幼儿', '清吧',
       '游乐园', '游戏厅', '游泳', '狼人杀', '电玩', '电玩城', '男孩', '网吧', '网咖', '酒吧']]
    d.append(df1)

df = pd.concat(d)
print(df.shape)
df.to_excel(f'1/全国_省会_百度指数.xlsx', index=False)
    # df['城市'] = city
    #     df = pd.merge(left=df, right=dataDF, left_on='date', right_on='时间', how='outer').fillna(0)
    #     df = df[['时间', '买房', '卖房', '失业金', '房价', '招工', '招聘', '租房', '股票']]
    #
    #     if df_all.shape[0] == 0:
    #         df_all = df.copy()
    #     else:
    #         df_all = df_all.replace(0, np.NaN)
    #         df_all = pd.merge(df_all, df, on='时间', how='outer')
    #         df_all = df_all[
    #             ['时间', '买房_x', '买房_y', '卖房_x', '卖房_y', '失业金_x', '失业金_y', '房价_x', '房价_y', '招工_x', '招工_y', '招聘_x', '招聘_y',
    #              '租房_x', '租房_y', '股票_x', '股票_y']]
    #
    #         df_all = df_all.fillna(method="bfill", limit=1, axis=1).rename(columns=colu)
    #         df_all = df_all[['时间', '买房', '卖房', '失业金', '房价', '招工', '招聘', '租房', '股票']]
    #
    # # [['时间', '买房', '卖房', '失业金', '房价','招工', '招聘', '租房', '股票' ]]
    # df_all['月'] = df_all['时间'].map(lambda x: x[:7])
    # d = []
    # for column in ['买房', '卖房', '失业金', '房价', '招工', '招聘', '租房', '股票']:
    #     df_colu = df_all[['月', column]]
    #     df_colu_gr = df_colu.groupby('月')[[column]].sum()
    #     d.append(df_colu_gr)
    #
    # name = '1_百度指数_出布林线_data/{}_百度指数.xlsx'.format(city)
    # writer = pd.ExcelWriter(name)
    #
    # df_all_1 = df_all[['时间', '买房', '卖房', '失业金', '房价', '招工', '招聘', '租房', '股票']]
    # df_all_1.to_excel(writer, sheet_name='原始数据', index=False)
    #
    # d1 = pd.concat(d, axis=1).astype(int)
    # for col in d1.columns:
    #     ddd = pd.DataFrame()
    #     ddd[col] = d1[col]
    #     ddd['布林中轨'] = ddd[col].rolling(window=10).mean().fillna(0)
    #     ddd['布林上轨'] = ddd[col].rolling(window=10).mean().fillna(0) + 2 * ddd[col].rolling(window=10).std().fillna(0)
    #     ddd['布林下轨'] = ddd[col].rolling(window=10).mean().fillna(0) - 2 * ddd[col].rolling(window=10).std().fillna(0)
    #     ddd.to_excel(writer, sheet_name=col)
    #
    # writer.save()
    # writer.close()
