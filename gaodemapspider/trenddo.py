import time
import pymongo
import jsonpath
import requests
from logsitc import *
import xlsxwriter

# 连接数据库
migrate_in_trend_data = pymongo.MongoClient(host='127.0.0.1', port=27017)['migrate_data']['migrate_in_trend_data']
migrate_in_peer_data = pymongo.MongoClient(host='127.0.0.1', port=27017)['migrate_data']['migrate_in_peer_data']
migrate_out_trend_data = pymongo.MongoClient(host='127.0.0.1', port=27017)['migrate_data']['migrate_out_trend_data']
migrate_out_peer_data = pymongo.MongoClient(host='127.0.0.1', port=27017)['migrate_data']['migrate_out_peer_data']

areacode_list = [100000, 1, 2, 3, 4, 130000, 140000, 150000, 210000, 220000, 230000, 320000, 330000,
                 340000, 350000, 360000, 370000, 410000, 420000, 430000, 440000, 450000, 460000,
                 510000, 520000, 530000, 610000, 620000, 630000, 640000, ]
citycode_list = [110000, 310000,
                 500000, 120000, 650100, 610100, 510100, 440300, 210100, 530100, 130900, 330100,
                 510600, 520100, 320100, 640100, 620100, 350100, 810000, 610100, 630100, 410700, 370800,
                 130600, 411300, 130100, 430100, 420100, 140200, 371300, 370200, 440100,
                 511300, 370700, 370100, 131000, 130200, 410300, 321300, 130300, 440500, 210200, 370900,
                 460100, 331000, 130500, 150100, 330600, 510700, 330300, 370600, 610400, 230100, 130400,
                 440400, 450200, 442000, 220100, 360100, 450300, 350200, 441800, 440800, 320300, 350600,
                 360700, 440600, 330400, 370300, 430400, 320200, 371400, 450100, 321000, 330200, 340100,
                 441900, 130700, 440900, 341100, 440200, 140100, 440700, 460200, 330800, 150600, 320400,
                 340200, 441300, 350500, 320500, 321100, 320700, 330500, 320900, 441200, 320800, 330700,
                 320600, 321200]
area_list = ["全国", "成渝", "京津冀", "长三角", "珠三角", "河北省", "山西省", "内蒙古自治区", "辽宁省", "吉林省", "黑龙江省", "江苏省", "浙江省", "安徽省", "福建省",
             "江西省",
             "山东省", "河南省", "湖北省", "湖南省", "广东省", "广西壮族自治区", "海南省", "四川省", "贵州省", "云南省", "陕西省",
             "甘肃省", "青海省", "宁夏回族自治区", ]
city_list = ["北京市", "上海市", "重庆市", "天津市", "乌鲁木齐", "西安市",
             "成都市", "深圳市","沈阳市", "昆明市", "沧州市", "杭州市", "德阳市", "贵阳市", "南京市", "银川市", "兰州市",
             "福州市", "香港", "郑州市", "西宁市", "新乡市", "济宁市", "保定市", "南阳市", "石家庄市", "长沙市", "武汉市", "大同市",
             "临沂市", "青岛市", "广州市", "南充市", "潍坊市", "济南市", "廊坊", "唐山市", "洛阳市", "宿迁市", "秦皇岛市", "汕头市",
             "大连市", "泰安市", "海口市", "台州市", "邢台市", "呼和浩特市", "绍兴市", "绵阳市", "温州市", "烟台市", "咸阳市", "哈尔滨市",
             "邯郸市", "珠海市", "柳州市", "中山市", "长春市", "南昌市", "桂林市", "厦门市", "清远市", "湛江市", "徐州市", "漳州市",
             "赣州市", "佛山市", "嘉兴市", "淄博市", "衡阳市", "无锡市", "德州市", "南宁市", "扬州市", "宁波市", "合肥市", "东莞市",
             "张家口市", "茂名市", "滁州市", "韶关市", "太原市", "江门市", "三亚市", "衢州市", "鄂尔多斯", "常州市", "芜湖市", "惠州市",
             "泉州市", "苏州市", "镇江市", "连云港市", "湖州市", "盐城市", "肇庆市", "淮安市", "金华市", "南通市", "泰州市",
             ]
# 650000
# "新疆维吾尔自治区",
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://trp.autonavi.com/migrate/index.do',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    # 'cookie': '_uab_collina=159797962670973574646665; UM_distinctid=1740f02100412c-0060d7142d7eea-6701b35-144000-1740f021005beb; __session:0.7035764361253245:state=111; user_unique_id=a184b07b741f1e0501741f8dd73906a9; SESSION=79dbebec-2361-40ea-8bc3-4676325b292b; CNZZDATA1256662931=1103843308-1597977235-https%253A%252F%252Ftrp.autonavi.com%252F%7C1598319841; user_unique_id=a187b9ae741f1d360174237a1d1070bf'
    'cookie': 'user_unique_id=a187b9ae7442ee10017452e8b7ac5d50; UM_distinctid=1741f9b2269fa-072bfdd46ac89d-5b123211-1fa400-1741f9b226a1c1; SESSION=817f1e2a-b054-458a-83f6-7cd5fe447ef6; CNZZDATA1256662931=255709660-1598254331-https%253A%252F%252Ftrp.autonavi.com%252F%7C1599122902'
}


def get_proxy():
    return requests.get("http://192.168.88.51:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://192.168.88.51:5010/delete/?proxy={}".format(proxy))


def getHtml(url):
    retry_count = 5
    proxy = get_proxy().get("proxy")
    proxies = {
        "http": "http://{}".format(proxy),
        "https": "https://{}".format(proxy)
    }
    if "!" in proxy:
        print('没有代理，等待2分钟')
        time.sleep(60 * 2)
    while retry_count > 0:
        try:
            html = requests.get(url, proxies=proxies, headers=headers)
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
            print(retry_count)
    # 出错5次, 删除代理池中代理
    delete_proxy(proxy)
    # getHtml(url)
    return None

# 获取地区数据
def get_localdata(url):
    response = requests.get(url, headers=headers)
    # response = getHtml(url)
    while response is None:
        time.sleep(10)
        # response = getHtml(url)
        response = requests.get(url, headers=headers)
    try:
        data = response.json()
    except:
        data = None
    willIdx = jsonpath.jsonpath(data, '$..willIdx')
    realIdx = jsonpath.jsonpath(data, '$..realIdx')
    dt = jsonpath.jsonpath(data, '$..dt')
    return willIdx, realIdx, dt

# 获取城市数据
def get_citydata(url):
    response = requests.get(url, headers=headers)
    # response = getHtml(url)
    while response is None:
        time.sleep(10)
        # response = getHtml(url)
        response = requests.get(url, headers=headers)
    try:
        data = response.json()
    except:
        data = None
    name = jsonpath.jsonpath(data, '$..name')
    willIdx = jsonpath.jsonpath(data, '$..willIdx')
    realIdx = jsonpath.jsonpath(data, '$..realIdx')
    dt = jsonpath.jsonpath(data, '$..dt')
    return name, willIdx, realIdx, dt





# in_city_list = []
# out_city_list = []
# in_willIdx_list = []
# out_willIdx_list = []
# in_realIdx_list = []
# out_realIdx_list = []
# in_time_list = []
# out_time_list = []

# 地区数据块
for adcode in areacode_list:
    trenddo_url = 'https://trp.autonavi.com/cityTravel/trend.do?adcode={}&inOut='.format(adcode)
    peerdata_url = 'https://trp.autonavi.com/cityTravel/getPeerData.do?adcode={}&inOut='.format(adcode)
    # peerdata_response = get_html(peerdata_url)
    # peerdata_response = requests.get(trenddo_url,headers=headers)
    # time.sleep(2)
    # peerdata_response = requests.get(peerdata_url,headers=headers)
    # time.sleep(2)
    # trenddo_response = getHtml(trenddo_url)
    # time.sleep(1.5)
    # peerdata_response = getHtml(peerdata_url)
    # time.sleep(1.5)


    willIdx, realIdx, dt = get_localdata(trenddo_url)
    if willIdx is False or realIdx is False:
        get_localdata(trenddo_url)
    else:
        # print(willIdx, '\n', realIdx, '\n', dt)
        # in_willIdx_list.extend(willIdx)
        # in_realIdx_list.extend(realIdx)
        # in_time_list.extend(dt)
        # for _ in range(len(dt)):
        #     in_city_list.append(area_dict[adcode])
        while len(willIdx) > 0:
            item = {}
            item['area'] = area_dict[adcode]
            item['date_time'] = dt.pop(0)
            item['in_willIdx'] = willIdx.pop(0)
            item['in_realIdx'] = realIdx.pop(0)
            migrate_in_trend_data.insert_one(item)


    #获取去年同比地区迁徙指数数据
    willIdx, realIdx, dt = get_localdata(peerdata_url)
    if willIdx is False or realIdx is False:
        get_localdata(peerdata_url)
    else:
        while len(willIdx) > 0:
            item = {}
            item['area'] = area_dict[adcode]
            item['date_time'] = dt.pop(0)
            item['in_willIdx'] = willIdx.pop(0)
            item['in_realIdx'] = realIdx.pop(0)
            migrate_out_peer_data.insert_one(item)
# 城市数据块
for adcode in citycode_list:
    in_trenddo_url = 'https://trp.autonavi.com/cityTravel/trend.do?adcode={}&inOut=IN'.format(adcode)
    out_trenddo_url = 'https://trp.autonavi.com/cityTravel/trend.do?adcode={}&inOut=OUT'.format(adcode)
    in_peerdata_url = 'https://trp.autonavi.com/cityTravel/getPeerData.do?adcode={}&inOut=IN'.format(adcode)
    out_peerdata_url = 'https://trp.autonavi.com/cityTravel/getPeerData.do?adcode={}&inOut=OUT'.format(adcode)
    # in_trenddo_response = get_citydata(in_trenddo_url)
    # out_trenddo_response = get_data(out_trenddo_url)

    # in_trenddo_response = requests.get(in_trenddo_url,headers=headers)
    # time.sleep(2)
    # out_trenddo_response = requests.get(out_trenddo_url,headers=headers)
    # time.sleep(2)

    # in_peerdata_response = requests.get(in_peerdata_url,headers=headers)
    # out_peerdata_response = requests.get(out_peerdata_url,headers=headers)
    # in_trenddo_response = getHtml(in_trenddo_url)
    # out_trenddo_response = getHtml(out_trenddo_url)
    # in_peerdata_response = getHtml(in_peerdata_url)
    # out_peerdata_response = getHtml(out_peerdata_url)
    # in_trenddo_url = 'https://trp.autonavi.com/cityTravel/trend.do?adcode={}&inOut='.format(100000)
    # in_peerdata_url = 'https://trp.autonavi.com/cityTravel/getPeerData.do?adcode={}&inOut='.format(100000)
    #     trenddo_response = requests.get(in_trenddo_url, headers=headers)
    #     peerdata_response = requests.get(in_peerdata_url, headers=headers)
    #     print(peerdata_response.text)
    # in_trendto_data = in_trenddo_response.json()
    # out_trendto_data = out_trenddo_response.json()
    # in_peerto_data = in_peerdata_response.json()
    # out_peerto_data = out_peerdata_response.json()
    # in_name = jsonpath.jsonpath(in_trenddo_response, '$..name')
    # in_willIdx = jsonpath.jsonpath(in_trenddo_response, '$..willIdx')
    # in_realIdx = jsonpath.jsonpath(in_trenddo_response, '$..realIdx')
    # in_dt = jsonpath.jsonpath(in_trenddo_response, '$..dt')


    in_name, in_willIdx, in_realIdx, in_dt = get_citydata(in_trenddo_url)
    out_name, out_willIdx, out_realIdx, out_dt = get_citydata(out_trenddo_url)



    if in_name is False or in_willIdx is False or in_realIdx is False or in_dt is False:
        print('存在False，重试中...')
        time.sleep(10)
        get_citydata(in_trenddo_url)
    if out_name is False or out_willIdx is False or out_realIdx is False or out_dt is False:
        print('存在False，重试中...')
        time.sleep(10)
        get_citydata(out_trenddo_url)
    else:
        while len(in_willIdx) > 0:
            in_item = {}
            in_item['area'] = in_name.pop(0)
            in_item['date_time'] = in_dt.pop(0)
            in_item['in_willIdx'] = in_willIdx.pop(0)
            in_item['in_realIdx'] = in_realIdx.pop(0)
            migrate_in_trend_data.insert_one(in_item)
        while len(out_willIdx) > 0:
            out_item = {}
            out_item['area'] = out_name.pop(0)
            out_item['date_time'] = out_dt.pop(0)
            out_item['out_willIdx'] = out_willIdx.pop(0)
            out_item['out_realIdx'] = out_realIdx.pop(0)
            migrate_out_trend_data.insert_one(out_item)

    # 获取去年同比城市迁徙指数数据

    in_peer_name, in_peer_willIdx, in_peer_realIdx, in_peer_dt = get_citydata(in_peerdata_url)
    out_peer_name, out_peer_willIdx, out_peer_realIdx, out_peer_dt = get_citydata(in_peerdata_url)

    if in_peer_name is False or in_peer_willIdx is False or in_peer_realIdx is False or in_peer_dt is False:
        print('存在False，重试中...')
        time.sleep(10)
        get_citydata(in_peerdata_url)
    if out_peer_name is False or out_peer_willIdx is False or out_peer_realIdx is False or out_peer_dt is False:
        print('存在False，重试中...')
        time.sleep(10)
        get_citydata(out_peerdata_url)
    else:
        while len(in_peer_willIdx) > 0:
            in_item = {}
            in_item['area'] = in_peer_name.pop(0)
            in_item['date_time'] = in_peer_dt.pop(0)
            in_item['in_willIdx'] = in_peer_willIdx.pop(0)
            in_item['in_realIdx'] = in_peer_realIdx.pop(0)
            migrate_in_peer_data.insert_one(in_item)
        while len(out_peer_willIdx) > 0:
            out_item = {}
            out_item['area'] = out_peer_name.pop(0)
            out_item['date_time'] = out_peer_dt.pop(0)
            out_item['out_willIdx'] = out_peer_willIdx.pop(0)
            out_item['out_realIdx'] = out_peer_realIdx.pop(0)
            migrate_out_peer_data.insert_one(out_item)




        # in_willIdx_list.extend(in_willIdx)
        # in_realIdx_list.extend(in_realIdx)
        # in_time_list.extend(in_dt)
        #
        # for _ in range(len(in_dt)):
        #     in_city_list.append(area_dict[adcode])
        # # out_name = jsonpath.jsonpath(out_trenddo_response, '$..name')
        # # out_willIdx = jsonpath.jsonpath(out_trenddo_response, '$..willIdx')
        # # out_realIdx = jsonpath.jsonpath(out_trenddo_response, '$..realIdx')
        # # out_dt = jsonpath.jsonpath(out_trenddo_response, '$..dt')
        # out_willIdx_list.extend(out_willIdx)
        # out_realIdx_list.extend(out_realIdx)
        # out_time_list.extend(out_dt)
        # for _ in range(len(out_dt)):
        #         out_city_list.append(area_dict[adcode])

# workbook = xlsxwriter.Workbook('迁徙规模指数.xlsx')
# worksheet_trend = workbook.add_worksheet('迁入规模指数')
#
# worksheet_peerdata = workbook.add_worksheet('迁出规模指数')
#
# headings = ['地区', '迁徙意愿指数', '实际迁徙指数', '时间']
# worksheet_trend.write_row('A1', headings)
# worksheet_peerdata.write_row('A1', headings)
#
# worksheet_trend.write_column('A2', in_city_list)
# worksheet_peerdata.write_column('A2', out_city_list)
# worksheet_trend.write_column('B2', in_willIdx_list)
# worksheet_peerdata.write_column('B2', out_willIdx_list)
# worksheet_trend.write_column('C2', in_realIdx_list)
# worksheet_peerdata.write_column('C2', out_realIdx_list)
# worksheet_trend.write_column('D2', in_time_list)
# worksheet_peerdata.write_column('D2', out_time_list)
#
# workbook.close()
