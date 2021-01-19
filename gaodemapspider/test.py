# # # #
# # # import requests
# # #
# # # response = requests.get('https://api.xiaoxiangdaili.com/ip/get?appKey=615462072872226816&appSecret=nLukzeho&cnt=1&wt=json')
# # #
# # # print(response.text)
# # #
# # #
# # # #
import time

import jsonpath

area_list = ["全国", "成渝", "京津冀", "长三角", "珠三角", "河北省", "山西省", "内蒙古自治区", "辽宁省", "吉林省", "黑龙江省", "江苏省", "浙江省", "安徽省", "福建省",
             "江西省",
             "山东省", "河南省", "湖北省", "湖南省", "广东省", "广西壮族自治区", "海南省", "四川省", "贵州省", "云南省", "陕西省",
             "甘肃省", "青海省", "宁夏回族自治区", "新疆维吾尔自治区", ]
city_list = ["北京市", "上海市", "重庆市", "天津市", "乌鲁木齐", "西安市",
             "成都市", "深圳市", "伊犁", "沈阳市", "昆明市", "沧州市", "杭州市", "德阳市", "贵阳市", "南京市", "银川市", "兰州市",
             "福州市", "香港", "郑州市", "西宁市", "新乡市", "济宁市", "保定市", "南阳市", "石家庄市", "长沙市", "武汉市", "大同市",
             "临沂市", "青岛市", "广州市", "南充市", "潍坊市", "济南市", "廊坊", "唐山市", "洛阳市", "宿迁市", "秦皇岛市", "汕头市",
             "大连市", "泰安市", "海口市", "台州市", "邢台市", "呼和浩特市", "绍兴市", "绵阳市", "温州市", "烟台市", "咸阳市", "哈尔滨市",
             "邯郸市", "珠海市", "柳州市", "中山市", "长春市", "南昌市", "桂林市", "厦门市", "清远市", "湛江市", "徐州市", "漳州市",
             "赣州市", "佛山市", "嘉兴市", "淄博市", "衡阳市", "无锡市", "德州市", "南宁市", "扬州市", "宁波市", "合肥市", "东莞市",
             "张家口市", "茂名市", "滁州市", "韶关市", "太原市", "江门市", "三亚市", "衢州市", "鄂尔多斯", "常州市", "芜湖市", "惠州市",
             "泉州市", "苏州市", "镇江市", "连云港市", "湖州市", "盐城市", "肇庆市", "淮安市", "金华市", "南通市", "泰州市",
             ]


print(len(area_list)+len(city_list))
# import re
#
#
import requests
# from lxml import etree
#
#
# def get_community_area(url):
# headers = {
#     'accept': 'application/json, text/plain, */*',
#     'accept-encoding': 'gzip, deflate, br',
#     'accept-language': 'zh-CN,zh;q=0.9',
#     'cache-control': 'no-cache',
#     'pragma': 'no-cache',
#     'referer': 'https://trp.autonavi.com/migrate/index.do',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
#     'cookie': '_uab_collina=159797962670973574646665; UM_distinctid=1740f02100412c-0060d7142d7eea-6701b35-144000-1740f021005beb; __session:0.7035764361253245:state=111; user_unique_id=a184b07b741f1e0501741f8dd73906a9; SESSION=79dbebec-2361-40ea-8bc3-4676325b292b; CNZZDATA1256662931=1103843308-1597977235-https%253A%252F%252Ftrp.autonavi.com%252F%7C1598319841; user_unique_id=a187b9ae741f1d360174237a1d1070bf'
# }
# #     res = requests.get(url=url, headers=headers)
#     res.encoding = 'gbk'
#     tree = etree.HTML(res.text)
#     item, data = [], {}
#
#     # 销售信息
#     sales_message = tree.xpath("//div[@class='main-item']/h3[contains(text(), '销售信息')]/../ul/li")
#     for sales in sales_message:
#         txt = re.sub('\s' ,'', sales.xpath('string(.)')).split('：')
#         item.append(dict(zip(txt[0::2], txt[1::2])))
#
#     # 小区规划
#     # Community_planning = tree.xpath('//ul[@class="list clearfix"]/li')
#     Community_planning = tree.xpath("//div[@class='main-item']/h3[contains(text(), '基本信息')]/following-sibling::ul/li")
#     print( len(Community_planning))
#     for plan in Community_planning:
#         print(plan)
#         # print('plan: ', plan.xpath('string(.)'))
#         txt = re.sub('\s' ,'', plan.xpath('string(.)')).split('：')
#         item.append(dict(zip(txt[0::2], txt[1::2])))
#     print(item)
#
# get_community_area('https://zhongliangxiangyun0531.fang.com/house/2410176649/housedetail.htm')
#
#
#
# def build_date_range():
#
#     star = '2019-8-23'
#     end = '2020-8-23'
#
#     data_time_range = []
#     day = star.split('-')[2]
#     mon = star.split('-')[1]
#     year = star.split('-')[0]
#     day = int(day)
#     mon = int(mon)
#     year = int(year)
#     while star != end:
#         data_time_range.append(star)
#         day += 1
#         big_mon = [1,3,5,7,8,10]
#         small_mon = [4,6,9,11]
#         spical = 2
#         if mon in big_mon and day == 32:
#                 day = 1
#                 mon += 1
#         elif mon in small_mon and day == 31:
#                 day = 1
#                 mon += 1
#         elif mon == spical and day == 30:
#                 day = 1
#                 mon += 1
#         elif mon == 12 and day == 32:
#             year = 2020
#             mon = 1
#             day = 1
#         star = '{}-{}-{}'.format(year,mon,day)
#     data_time_range.append(end)
#     return data_time_range
#
# print(build_date_range())
# headers = {
#     'accept': 'application/json, text/plain, */*',
#     'accept-encoding': 'gzip, deflate, br',
#     'accept-language': 'zh-CN,zh;q=0.9',
#     'cache-control': 'no-cache',
#     'pragma': 'no-cache',
#     'referer': 'https://trp.autonavi.com/migrate/index.do',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
#     'cookie': '_uab_collina=159797962670973574646665; UM_distinctid=1740f02100412c-0060d7142d7eea-6701b35-144000-1740f021005beb; __session:0.7035764361253245:state=111; user_unique_id=a184b07b741f1e0501741f8dd73906a9; SESSION=79dbebec-2361-40ea-8bc3-4676325b292b; CNZZDATA1256662931=1103843308-1597977235-https%253A%252F%252Ftrp.autonavi.com%252F%7C1598319841; user_unique_id=a187b9ae741f1d360174237a1d1070bf'
# }
# data = None
# willIdx = jsonpath.jsonpath(data, '$..willIdx')
# print(willIdx)


