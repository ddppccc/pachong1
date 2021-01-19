import pandas as pd
import json
import re

import jieba
import pymongo

from wordcloud import WordCloud
import PIL.Image as image
import numpy as np
import os
Tiezi_data = pymongo.MongoClient(host='127.0.0.1', port=27017)['BaiduTieba']['Tiezi']
Comment_data = pymongo.MongoClient(host='127.0.0.1', port=27017)['BaiduTieba']['Comment']
Tiezi_data = Tiezi_data.find()
Comment_data = Comment_data.find()




def stop_words(path):
    with open(path, encoding='UTF-8') as f:
        return [l.strip() for l in f]


def get_TF(k,words,total_data):
    tf_dic = {}
    for i in words:
        tf_dic[i] = tf_dic.get(i,0)+1
    words = sorted(tf_dic.items(),key=lambda item:item[1],reverse=True)[:k]
    tf_dic = {}
    for i in range(len(words)):
            if words[i][0] not in total_data.keys():
                tf_dic[words[i][0]] = words[i][1]
    return tf_dic

# 生成词云
def create_wordcloud(path,string,img_path):
    font = r'C:\\Windows\\Fonts\\simhei.ttf'
    string = " ".join(jieba.cut(string))
    mask = np.array(image.open(path))
    wordcloud = WordCloud(
        mask=mask,
        font_path=font,
        background_color='white',
        colormap="Set2",
        # max_words=50,
        relative_scaling = 0,
        max_font_size=300,
    ).generate(string)
    image_produce = wordcloud.to_image()
    wordcloud.to_file(img_path)
    # image_produce.show()


# 获取停词处理后的字符串
def get_string(tz_list,keyword,total_data):
    string = ''
    for data in tz_list:
        try:
            if data['postsBar'] == keyword:
                string += (data['PostsTitle'] + str(str(data['data']).replace('[','').replace(']','').replace('None','').replace('\'','')))
        except:
            continue

    split_words = [x for x in jieba.cut(string) if x not in stop_words('stopwords.txt')]
    for i in range(3):
        for _ in split_words:
            if _ == ' ':
                split_words.remove(_)
    # print(split_words)
    city_dict = get_TF(50, split_words,total_data)
    string = ''
    for _ in split_words:
        string += _
    return string,city_dict


def get_data():
    df1 = pd.DataFrame(list(Tiezi_data))
    df2 = pd.DataFrame(list(Comment_data))

    po = []
    wo = []
    for i in range(len(df2)):
        data = []
        for j in range(len(df2['data'][i])):
            postsID = df2['data'][i][j]['postsID']
            data.append(df2['data'][i][j]['comment'])
        wo.append(data)
        po.append(postsID)
    df2 = pd.DataFrame({'postsID': po, 'data': wo})

    df3 = pd.merge(df1, df2)
    df3 = df3.drop(columns=['_id'])
    df3 = df3.to_dict('index')

    tz_list = []
    for i in df3:
        tz_list.append(df3[i])
    return tz_list



def get_total_data():
    string = ''
    for data in tz_list:
        try:
            string += (
                (data['PostsTitle'] + str(data['data'])).replace('[', '').replace(']', '').replace('None', '').replace(
                    '\'', ''))
        except:
            continue
    split_words = [x for x in jieba.cut(string) if x not in stop_words('stopwords.txt')]
    for i in range(3):
        for _ in split_words:
            if _ == ' ':
                split_words.remove(_)
    # print(split_words)
    tf_dic = {}
    for i in split_words:
        tf_dic[i] = tf_dic.get(i,0)+1
    words = sorted(tf_dic.items(),key=lambda item:item[1],reverse=True)[:50]
    tf_dic = {}
    for i in range(len(words)):
        tf_dic[words[i][0]] = words[i][1]
    return tf_dic


tz_list = get_data()
img_list = os.listdir('../img')

with open('city_map.json', encoding='utf-8') as fp:
    cities = ["{city}".format(city=i) for i in json.load(fp).keys()]
contact_list = {}
for city in cities:
    for img in img_list:
        find_img = re.search(city,img)
        if find_img:
            # count += 1
            contact_list[img] = city

tf_dic = get_total_data()
json_data = {'全国':tf_dic}

for key,value in contact_list.items():
    string,top50 = get_string(tz_list,value,tf_dic)
    json_data[value] = top50
    try:
        create_wordcloud('../img/{}'.format(key),string,'./word_cloudimg/{}'.format(key))
    except:
        print('无数据，无法生成词云...')
        continue
with open('全国分词词频.json','w') as f:
    json.dump(json_data,f)
    print('载入完成..')
