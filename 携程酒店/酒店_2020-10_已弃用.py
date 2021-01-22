import datetime
import os
import re
import math
import time

import requests
import pandas as pd
from scrapy import Selector
from urllib.parse import quote
from config import city_map_list, elevent_list
from index import CG_Client, getContent


cookie = '' \
         '_RGUID=c1461406-eb54-4f73-9943-79aa0e6d7614; _RDG=28ae06a1d31f912556093f991d178ab833; _RSG=pz4LhR0565CKONREeQU3b9; magicid=cfaGiyUU2j1u4Mdk3ScHNtYu+E9Nj7kGZB8SB3eI/1LBaLSQv4yIN4/TI76Mhhde; _ga=GA1.2.1005284998.1591869359; MKT_CKID=1576636848313.u5oo4.4y1z; _abtest_userid=c30f87c7-e48b-4db0-8179-f94dab411936; hoteluuid=A0zFC5pm95q5CHbd; AHeadUserInfo=VipGrade=0&VipGradeName=%C6%D5%CD%A8%BB%E1%D4%B1&UserName=&NoReadMessageCount=0; IsPersonalizedLogin=F; UUID=D0849EC573624A8E8E95D3F7016AD3D1; nfes_isSupportWebP=1; GUID=09031071210792750836; clientid=51482101210832301737; __utma=13090024.1005284998.1591869359.1597304246.1597304246.1; __utmz=13090024.1597304246.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); FlightIntl=Search=[%22BJS|%E5%8C%97%E4%BA%AC(BJS)|1|BJS|480%22%2C%22US|%E7%BE%8E%E5%9B%BD|country%22%2C%222020-08-19%22%2C%222020-08-23%22]; MKT_Pagesource=PC; Session=SmartLinkCode=U155952&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; _gid=GA1.2.982426286.1600051090; MKT_CKID_LMT=1600051090153; _RF1=119.137.55.207; FD_SearchHistorty={"type":"S","data":"S%24%u6DF1%u5733%28SZX%29%24SZX%242020-09-15%24%u4E0A%u6D77%28SHA%29%24SHA%24%24%24"}; ASP.NET_SessionId=1qqv3zwelnaessosw4onq5sx; OID_ForOnlineHotel=15918693555821fns3c1600070740225102032; Union=OUID=table&AllianceID=4897&SID=155952&SourceID=&createtime=1600070742&Expires=1600675542288; MKT_OrderClick=ASID=4897155952&AID=4897&CSID=155952&OUID=table&CT=1600070742297&CURL=https%3A%2F%2Fhotels.ctrip.com%2Fhotel%2Fshanghai2%3Fsid%3D155952%26allianceid%3D4897%26ouid%3Dtable&VAL={"pc_vid":"1591869355582.1fns3c"}; HotelDomesticVisitedHotels1=429531=0,0,4.5,1917,/20031900000166atc8EC9.jpg,&35970539=0,0,4.9,85,/02074120002striu75E67.jpg,&40865717=0,0,4.8,62,/200l15000000yfgek381D.jpg,&11090264=0,0,0,77,/200q1a0000018zplp979D.jpg,&12090109=0,0,4.9,266,/200j0u000000ixxcu22A5.jpg,&48315854=0,0,5,37,/200d1h000001hk9cj16D5.jpg,; librauuid=P5O14kqFUsUh0kT6o9; MjAxNS8wNi8yOSAgSE9URUwgIERFQlVH=OceanBall; login_uid=E6990F62CCB2B96BF88D24990AE6B674; login_type=6; cticket=2A83DEC40ECC50E8AC3BC06B2A8150FC3420207D59CED67638FE29EEC7F09603; ticket_ctrip=bJ9RlCHVwlu1ZjyusRi+ypZ7X2r4+yoj4wvWr3vD9yAonOkv1Df735vv0Lo4R+XwRR+vOfAnp2rwLJXIkyxR+qvzGtbEwWm3zXRRGBDwZo7QtFkClDrIhQ0GmGdp6F/uY+p2LdD9nyOF4k6DCasuRd0k6zMwluL7pSMvw6ZlSPtL4LBxc3W5fWf25jLNJlSqY3aqCsatjKJVUHRjzEkuAQvZG/UyKC0+aCSm3Dwgm2glf2JvYrlCWwAAoMCyTa3BRs3p675lWXz1J37Lpy9eJ2chTdoggMk5er2p9cnizTU=; DUID=u=2783388A416905203FFA5C75A1B7A523&v=0; IsNonUser=F; _bfi=p1%3D102002%26p2%3D10320670296%26v1%3D417%26v2%3D416; _gat=1; _jzqco=%7C%7C%7C%7C1600051090467%7C1.262374949.1591869358657.1600071309956.1600071413006.1600071309956.1600071413006.undefined.0.0.287.287; __zpspc=9.64.1600070742.1600071413.13%232%7Cwww.baidu.com%7C%7C%7C%25E6%2590%25BA%25E7%25A8%258B%7C%23; appFloatCnt=271; hotelhst=6907176; _bfa=1.1591869355582.1fns3c.1.1600051082282.1600070740053.61.418.10650016818; _bfs=1.18'


def get_html(city, city_pinyin, cityId, cityCode, ws, page=1):
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "if-modified-since": "Thu, 01 Jan 1970 00:00:00 GMT",
        'cookie': cookie,
        "origin": "https://hotels.ctrip.com",
        "referer": "https://hotels.ctrip.com/hotel/shanghai2",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    }
    today = datetime.datetime.now()  # 今天，如 "2020-06-11"
    last_time = today + datetime.timedelta(hours=24)
    tomorrow = last_time.strftime("%Y-%m-%d")  # 明天，如 '2020-06-12'
    while True:
        getContent(ws)
        time.sleep(0.5)
        print("elevent_list: ", elevent_list)
        try:
            eleven = elevent_list.pop()
            if not eleven: continue
            break
        except:
            continue

    params = {
        "__VIEWSTATEGENERATOR": "DB1FBB6D",
        "cityName": quote(city),
        "StartTime": today.strftime("%Y-%m-%d"),
        "DepTime": tomorrow,
        "RoomGuestCount": "1,1,0",
        "txtkeyword": "",
        "Resource": "",
        "Room": "",
        "Paymentterm": "",
        "BRev": "",
        "Minstate": "",
        "PromoteType": "",
        "PromoteDate": "",
        "operationtype": "NEWHOTELORDER",
        "PromoteStartDate": "",
        "PromoteEndDate": "",
        "OrderID": "",
        "RoomNum": "",
        "IsOnlyAirHotel": "F",
        "cityId": cityId,
        "cityPY": city_pinyin,
        "cityCode": cityCode,
        "cityLat": "38.8801531302",
        "cityLng": "115.4712668627",
        "positionArea": "",
        "positionId": "",
        "hotelposition": "",
        "keyword": "",
        "hotelId": "",
        "htlPageView": "0",
        "hotelType": "F",
        "hasPKGHotel": "F",
        "requestTravelMoney": "F",
        "isusergiftcard": "F",
        "useFG": "F",
        "HotelEquipment": "",
        "priceRange": "-2",
        "hotelBrandId": "",
        "promotion": "F",
        "prepay": "F",
        "IsCanReserve": "F",
        "OrderBy": "99",
        "OrderType": "",
        "k1": "",
        "k2": "",
        "CorpPayType": "",
        "viewType": "",
        "checkIn": today.strftime("%Y-%m-%d"),
        "checkOut": tomorrow,
        "DealSale": "",
        "ulogin": "",
        "hidTestLat": "0%7C0",
        "AllHotelIds": "",
        "psid": "",
        "isfromlist": "T",
        "ubt_price_key": "htl_search_noresult_promotion",
        "showwindow": "",
        "defaultcoupon": "",
        "isHuaZhu": "False",
        "hotelPriceLow": "",
        "unBookHotelTraceCode": "",
        "showTipFlg": "",
        "traceAdContextId": "",
        "allianceid": "0",
        "sid": "0",
        "pyramidHotels": "",
        "hotelIds": "",
        "markType": "0",
        "zone": "",
        "location": "",
        "type": "",
        "brand": "",
        "group": "",
        "feature": "",
        "equip": "",
        "bed": "",
        "breakfast": "",
        "other": "",
        "star": "",
        "sl": "",
        "s": "",
        "l": "",
        "price": "",
        "a": "0",
        "keywordLat": "",
        "keywordLon": "",
        "contrast": "0",
        "PaymentType": "",
        "CtripService": "",
        "promotionf": "",
        "allpoint": "",
        "page_id_forlog": "102002",
        "contyped": "0",
        "productcode": "",
        "eleven": eleven,
        "page": page,
    }
    url = 'https://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx'
    while True:
        try:
            # print(params)
            res = requests.post(url, headers=headers, data=params).json()
            if int(res['hotelAmount']) == 0:
                print(res)
                print(city, '酒店数量为0 : ', 'https://hotels.ctrip.com/hotel/shanghai2')

                number = input('number 不为1-5 跳出: ')
                if number in ['1', '2', '3', '4', '5']:
                    continue
                else:
                    break
            break
        except Exception as e:
            print('需要验证', e)
            continue
    return res


def get_parse_html(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': cookie,
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }
    while True:
        try:
            res = requests.get(url, headers=headers, timeout=(2, 5))
            break
        except Exception as e:
            print('出错: ', e)
            continue

    return res


def parse_info(value, data_all):
    res = get_parse_html(value['url'])
    response = Selector(text=res.text)
    info_str = response.xpath('string(//*[@id="htlDes"]/p/text())').get()
    # 开业时间
    value['区县'] = response.xpath("//span[@id='ctl00_MainContentPlaceHolder_commonHead_lnkLocation']/text()").get() \
                  or response.xpath("//span[@id='ctl00_MainContentPlaceHolder_commonHead_lnkCity']/text()").get()
    value['开业时间'] = "".join(re.findall('(\d+)年开业', info_str))
    value['装修时间'] = "".join(re.findall('(\d+)年装修', info_str))
    value['房间总数'] = "".join(re.findall('(\d+)间', info_str))
    data_all.append(value)
    # return value


def parse(city_map, page, pageTotal, ws, data_all):
    city_pinyin, city, cityId = city_map['data'].split('|')
    cityCode = city_map['cityCode']
    html = get_html(city, city_pinyin, cityId, cityCode, page=page, ws=ws)
    response = Selector(text=html['hotelList'])

    print('城市: %s, 总页数: %s, 页数: %s' % (city, pageTotal, page))

    p = []
    for value in html['hotelPositionJSON']:
        value['url'] = 'https://hotels.ctrip.com' + value['url']

        value['起步价'] = response.xpath(
            "//div[contains(@data-id, '{}')]//span[@class='J_price_lowList']/text()".format(value['id'])).get()
        # item = parse_info(value['url'])
        # value.update(item)
        data_all.append(value)
    #     d = pool.submit(parse_info, value, data_all)
    #     p.append(d)
    # [obj.result() for obj in p]

    if not pageTotal:
        # 酒店数量
        hotelAmount = int(html['hotelAmount'])
        pageNumber = int(hotelAmount // 25)
        if hotelAmount == 0:
            print('没有酒店: ', city)
        pageTotal = pageNumber

    if page <= pageTotal:
        page += 1
        parse(city_map, page=page, ws=ws, pageTotal=pageTotal, data_all=data_all)


def run(ws):
    currentDate = datetime.datetime.now().strftime("%Y-%m")
    for city_map in city_map_list:
        # if city_map['display'] in ['长沙']:continue
        # if city_map['display'] not in ["北京","天津","石家庄","呼和浩特","太原","沈阳","大连","长春","哈尔滨","上海","南京","杭州","宁波","合肥","福州","厦门","南昌","济南","青岛","郑州","武汉","长沙","广州","深圳","南宁","海口","重庆","成都","贵阳","昆明","西安","兰州","西宁","银川","乌鲁木齐","唐山","秦皇岛","包头","丹东","锦州",
# "吉林","牡丹江","无锡","扬州","徐州","温州","金华","蚌埠","安庆","泉州","九江","赣州","烟台","济宁","洛阳","平顶山","宜昌","襄阳","岳阳","常德","惠州","湛江","韶关","桂林","北海","三亚","泸州","南充","遵义","大理"]:continue
        print(city_map)
#
        if city_map['display'] in [i.split('_')[1] for i in os.listdir('酒店数据')]:
            print('已经存在', '\n')
            continue
        data_all = []
        parse(city_map, page=1, pageTotal=None, ws=ws, data_all=data_all)

        df = pd.DataFrame(data_all)
        df.rename(columns={'address': '地址',
                           'dpcount': '评论数',
                           'dpscore': '评论推荐率',
                           'score': '客户点评(5.0满分)',
                           'star': '酒店星级（星级和数据已存在钻石级)'}, inplace=True)

        save_dir = '酒店数据'
        os.path.exists(save_dir) or os.makedirs(save_dir)
        file_name = "{}_{}_{}条携程酒店数据.xlsx".format(currentDate, city_map['display'], len(data_all))
        df.to_excel(os.path.join(save_dir, file_name), index=False)


if __name__ == '__main__':
    # TODO 首先启动nodejs服务, 启动油候脚本, 刷新后执行程序
    ws = None
    try:
        ws = CG_Client("ws://127.0.0.1:8014/")  # 启动js服务
        ws.connect()

        # pool = ThreadPoolExecutor(10)
        run(ws)
        print('程序结束')
        # pool.shutdown()
        ws.run_forever()

    except KeyboardInterrupt:
        ws.close()
