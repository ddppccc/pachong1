# import pandas as pd
# from concurrent.futures import ThreadPoolExecutor
# def parse_info(url,item):
#
#     print('url:',url,'item:',item)
#
# f = open(r'出让公告.csv', encoding='gbk', mode='r')
# df = pd.read_csv(f, error_bad_lines=False,index_col='标题url')
# # 这里是筛选日期
# print(df['公示日期'])
# df['公示日期'] = df['公示日期'].map(lambda x: '' if '20' not in x or '公示' or 'https://' in x else x)
# df['公示日期'] = pd.to_datetime(df['公示日期'])
# df = df.query("公示日期 > '2020-08-01'")
# df['公示日期'] = df['公示日期'].map(lambda x: str(x).split(' ')[0])
# f.close()
# # print(df.head(5))
# threadPool = ThreadPoolExecutor(max_workers=8)
# p = []
# try:
#     f = open(r'出让公告_详情.csv',encoding='gbk',mode='r')
#     df2 = pd.read_csv(f,error_bad_lines=False)
#     f.close()
#     has_spider_list = df2['标题url'].tolist()
# except:
#     has_spider_list = []
# for url in df.index:
#     if url in has_spider_list:
#         continue
#     item = {}
#     item['标题url'] = url
#     item['行政区'] = df.loc[[url]]['行政区'][0]
#     item['供应标题'] = df.loc[[url]]['供应标题'][0]
#     item['省份'] = df.loc[[url]]['省份'][0]
#     item['城市'] = df.loc[[url]]['城市'][0]
#     item['公告类型'] = df.loc[[url]]['公告类型'][0]
#     item['发布时间'] = df.loc[[url]]['发布时间'][0]
#     # print(url)
#     future = threadPool.submit(parse_info,item['标题url'],item)
#     p.append(future)
# #
# [i.result() for i in p]
# #
# threadPool.shutdown()


if 'list index out of range' in 'list index out of range':
    print(1)