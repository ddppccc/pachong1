# import json
# import re
#
# import jieba
# import pymongo
#
# from wordcloud import WordCloud
# import PIL.Image as image
# import numpy as np
# import os
#
# def stop_words(path):
#     with open(path, encoding='UTF-8') as f:
#         return [l.strip() for l in f]
#
#
# def get_TF(k,words,total_data):
#     tf_dic = {}
#     for i in words:
#         tf_dic[i] = tf_dic.get(i,0)+1
#     words = sorted(tf_dic.items(),key=lambda item:item[1],reverse=True)[:k]
#     tf_dic = {}
#     for i in range(len(words)):
#             if words[i][0] not in total_data.keys():
#                 tf_dic[words[i][0]] = words[i][1]
#     return tf_dic
#
# # 生成词云
# def create_wordcloud(path,string,img_path):
#     font = r'C:\\Windows\\Fonts\\simhei.ttf'
#     string = " ".join(jieba.cut(string))
#     mask = np.array(image.open(path))
#     wordcloud = WordCloud(
#         mask=mask,
#         font_path=font,
#         background_color='white',
#         colormap="Set2",
#         # max_words=50,
#         relative_scaling = 0,
#         max_font_size=300,
#     ).generate(string)
#     image_produce = wordcloud.to_image()
#     wordcloud.to_file(img_path)
#     # image_produce.show()
#
#
# # 获取停词处理后的字符串
# def get_string(tz_list,keyword,total_data):
#     string = ''
#     for data in tz_list:
#         try:
#             if data['postsBar'] == keyword:
#                 string += (data['PostsTitle'] + str(str(data['data']).replace('[','').replace(']','').replace('None','').replace('\'','')))
#         except:
#             continue
#     split_words = [x for x in jieba.cut(string) if x not in stop_words('stopwords.txt')]
#     for i in range(3):
#         for _ in split_words:
#             if _ == ' ':
#                 split_words.remove(_)
#     # print(split_words)
#     city_dict = get_TF(50, split_words,total_data)
#     string = ''
#     for _ in split_words:
#         string += _
#     return string,city_dict
#
#
# def get_data():
#
#     tz_list = []
#
#     Tiezi_data = pymongo.MongoClient(host='127.0.0.1', port=27017)['BaiduTieba']['Tiezi']
#     Comment_data = pymongo.MongoClient(host='127.0.0.1', port=27017)['BaiduTieba']['Comment']
#
#     # 连接帖子和评论
#     for tz_data in Tiezi_data.find({},no_cursor_timeout=True):
#         for data in Comment_data.find({},no_cursor_timeout=True):
#             if len(data['data']):
#                 if data['data'][0]['postsID'] == tz_data['postsID']:
#                     data_list = []
#                     for i in range(len(data['data'])):
#                         data_list.append(data['data'][i]['comment'])
#                         tz_data['data'] = data_list
#                     print(tz_data)
#                     tz_list.append(tz_data)
#     Tiezi_data.close()
#     Comment_data.close()
#     return tz_list
#
#
# def get_total_data():
#     string = ''
#     for data in tz_list:
#         string += (data['PostsTitle'] + str(data['data'][0]))
#     split_words = [x for x in jieba.cut(string) if x not in stop_words('stopwords.txt')]
#     for i in range(3):
#         for _ in split_words:
#             if _ == ' ':
#                 split_words.remove(_)
#     # print(split_words)
#     tf_dic = {}
#     for i in split_words:
#         tf_dic[i] = tf_dic.get(i,0)+1
#     words = sorted(tf_dic.items(),key=lambda item:item[1],reverse=True)[:50]
#     tf_dic = {}
#     for i in range(len(words)):
#         tf_dic[words[i][0]] = words[i][1]
#     return tf_dic
#
#
# tz_list = get_data()
# img_list = os.listdir('../img')
#
# with open('city_map.json', encoding='utf-8') as fp:
#     cities = ["{city}".format(city=i) for i in json.load(fp).keys()]
# contact_list = {}
# for city in cities:
#     for img in img_list:
#         find_img = re.search(city,img)
#         if find_img:
#             # count += 1
#             contact_list[img] = city
#
# tf_dic = get_total_data()
# json_data = {'全国':tf_dic}
#
# for key,value in contact_list.items():
#     string,top50 = get_string(tz_list,value,tf_dic)
#     json_data[value] = top50
#     create_wordcloud('../img/{}'.format(key),string,'./word_cloudimg/{}'.format(key))
# with open('全国分词词频.json','w') as f:
#     json.dump(json_data,f)
#     print('载入完成..')
#
# # 处理停词
# # with open('stop.txt',encoding='utf-8') as fp:
# #     word = fp.read().replace('\n', ',').replace('[','').replace(']','').split(',')
# #
# # word_list = string.split(' ')
#
#
#
#
#
#
#
#
#
