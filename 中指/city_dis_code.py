import os
import json
import pandas as pd

file_name = os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(__file__))), "city_region_code.json")
with open(file_name, 'r', encoding='utf-8') as fp:
    city_region = json.load(fp)


def GetCityCode(city):
    """ 输入城市 获取城市编号id """
    c = [j for j in [i['city'] for i in city_region['Table']] if city in j]
    if city == '鞍山':
        a = '鞍山市'
    else:
        a = ''.join(c)
    df = pd.DataFrame(city_region['Table'])
    cityDf = df[df['city'] == a]
    return cityDf['cityid'].values[0]


def GetRegion(city):
    """区县, 根据城市获取区县id"""
    c = [j for j in [i['city'] for i in city_region['Table']] if city in j]
    if city == '鞍山':
        a = '鞍山市'
    else:
        a = "".join(c)

    df = pd.DataFrame(city_region['Table1'])
    cityDf = df[df['city'] == a]
    region_ID_str = ','.join(cityDf['sDistrictID'].astype(str).tolist())
    print(region_ID_str)
    return region_ID_str


if __name__ == '__main__':
    print(os.path.dirname(__file__))
