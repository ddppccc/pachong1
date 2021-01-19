import random
import re
import time

import pymongo
import requests
from jsonpath import jsonpath

info_base = pymongo.MongoClient(host='127.0.0.1', port=27017)['Booking']['info_fin']




def Headers():
    headers = {
        'Host': 'www.booking.com',
        'Connection': 'keep-alive',
        'X-Booking-Language-Code': 'zh-cn',
        'X-Booking-Client-Info': 'THHSOFRURURYNYHIYTLRQJRbWdWOGVO|1,THHSOFRURURYNYHIYTLRQJRbWdWOGVO|3,THHSOFRURURYNYHIYTLRQJRbWdWOGVO|5,eWHMBUHMfHMOPTOQKFUPKSCLNYUNZdeLEHT|1,adUAVYCIFBUYdXfMAPTLKGBfC|1,adUAVYCIFBUXLNYDIYScXQOVWe|1,eWHMAENYRCEHAQQJEceMdEPQPAURAfPVT|1,fdJcVSdMWZET|1,NReaHfUEYYPOCXDOET|1',
        'X-Booking-CSRF': '1dTFXwAAAAA=zmZeRu1k1ic_VN-WOWOb_Gk9AdK12Sw_zvFZ3gxrp69zc4G3AMBgeQ7rG4BWpUENQC9K7RPhvWPb54cfm2jn6eO9P-0jGQzMTDlPKUNMqzItg5XvRDRVILJ4VhcPh8T1OOCMhyrAQMV0W3U3KybVZmDL_Bb2UKIVK0yytBXCycU9smdSgvd2w8AxRVCDHmWLt4rBVcrgvMn5cHbz',
        'X-Booking-AID': '304142',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'X-Partner-Channel-Id': '3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Booking-Pageview-Id': '87171bf3704100d5',
        'Accept': '*/*',
        'X-Booking-Info': '1133410,1161170,1214730,1216210,1223840,1233530,1233800,1235840,1237350,1237430,1238510,1238740,1238790,1239730,1240510,1241480,1242370,1242530,1242800,1242990,1243360,1243610,1243960,1244560,1245410,1245980,MKMBNPUbYFTeNJPRJGNJHVCFfSWe|1,1243360|6,1235840|3,1243360|5,1243960|1,1243360|7,1242370|3,1243350|9,1243610|1,1242370|1,1243360|2,1242530|4,1223840|1,1242530|2,INLHIHMZMPZXYQRdFOGOdUTcO',
        'X-Booking-SiteType-Id': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Booking-Session-Id': '600d77276e7207c6e1ae6c35df00ed82',
        'Origin': 'https://www.booking.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.booking.com/hotel/cn/grand-hyatt-sanya-haitang-bay-resort-and-spa.zh-cn.html?aid=304142;label=gen173nr-1FCAEoggI46AdIM1gEaDGIAQGYASu4AQbIAQzYAQHoAQH4AQuIAgGoAgO4ApTa1_0FwAIB0gIkMzI0YTY0YmItYjBlOS00ZGI0LTkyNGItYjJjYWFhYjI4OWNh2AIG4AIB;sid=600d77276e7207c6e1ae6c35df00ed82;all_sr_blocks=180325803_262191985_2_2_0;checkin=2020-11-22;checkout=2020-11-23;dest_id=-1924026;dest_type=city;dist=0;from_beach_non_key_ufi_sr=1;group_adults=2;group_children=0;hapos=2;highlighted_blocks=180325803_262191985_2_2_0;hpos=2;no_rooms=1;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=180325803_262191985_2_2_0__150000;srepoch=1605770019;srpvid=8d5132d10ca0009e;type=total;ucfs=1&',
        'Cookie': '_pxhd=a627d098e18f735be974d4b54e57795fd76524c17ef6a80a0c22dafb782fb0cf%3Aabb9d110-2a1a-11eb-bb37-8fc25101e2ca; cors_js=1; _pxvid=abb9d110-2a1a-11eb-bb37-8fc25101e2ca; _ga=GA1.2.403134577.1605758105; _gcl_au=1.1.1546576241.1605758105; 11_srd=%7B%22features%22%3A%5B%7B%22id%22%3A16%7D%5D%2C%22score%22%3A3%2C%22detected%22%3Afalse%7D; bs=%7B%22sr_country_or_region_page%22%3A%22country%22%7D; BJS=-; has_preloaded=1; _gid=GA1.2.516267090.1606190191; _px3=b9e1d89d5077e252494b04297e58e9238d44b314b89687e38f5be80d862aea3a:8oy+F9ftnx0Gb4mScF9H/2C/dtwA1gW7iDXTc2DKL2L+fUNg3gcJXhw1LWNK4/og68dUCcQfrx0pKQ+wQX5pCg==:1000:/UAyHqOPdBg9fBrAbO1jKL/Pxwg+YLMbGGjNHo0uF3NKPeQplWsgUWHwpOeLKvnCFffEnUWJ/DNTnKSGO2I0KgwCCgH5llwiArmRHa50FbJjXyChXJ7TzM278ZMLrNCSYROw7icge15Na3DKUVMoySwSbKzNIS2kzguXkkkdTJo=; _uetsid=d0f6e4302d2e11eb81c6f7aa62b72e26; _uetvid=021a71102a1b11ebae63611d17654083; lastSeen=1606190370188; bkng=11UmFuZG9tSVYkc2RlIyh9Yaa29%2F3xUOLblgO%2Fz4BDP5tr1tqXKOhGi0zf7TKfsF47btwM5zjMrbzQ4yNp7ToeYeNC%2BkB7a6rOKsCbj35mIzyip7E9na1syB7snDyZB%2BkZkKq7uwW6lSo23TFsHDgG0sgFMVF0WZjEograqMSPp%2FppNzz8nQExe1Hvd7Nxk595S4UW9VevZtsgzhi5p3mJJw%3D%3D; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; _pxde=a1c7ef2b07ac391a9521fa52cda4cd3c79dc6d9f7f2c7bb23f5b6a9fa6b9f3d0:eyJ0aW1lc3RhbXAiOjE2MDYxOTAzMTY2NjYsImZfa2IiOjAsImlwY19pZCI6W119',

    }
    return headers


def postHTMLText(url, **kwargs):
    time.sleep(random.randint(10, 15) * 0.1 * 1)
    try:
        r = requests.post(url, **kwargs)
        r.encoding = 'utf-8'
        r.raise_for_status()
        return r.json()
    except:
        return None



def get_postdetail(form_data,item):
    label = re.search(r'label=(.*?)[&;]',item['深层url']).group(1)
    sid = re.search(r'sid=(.*?)[&;]',item['深层url']).group(1)
    srpvid = re.search(r'srpvid=(.*?)[&;]',item['深层url']).group(1)
    url = 'https://www.booking.com/fragment.zh-cn.json?label={};sid={};srpvid={}&'.format(label,sid,srpvid)
    # print(url)
    form_data['hotel_id'] = item['hotel_id']
    item['户型'] = []
    for i in item['room_id']:
        form_data['room_id'] = i
        headers = Headers()
        # print(form_data)
        # time.sleep(random.randint(10, 15) * 0.1 * 1)
        resp = postHTMLText(url=url, data=form_data, headers=headers)
        # print(resp)
        room_info = {}
        try:
            _ = jsonpath(resp,'$.data.rooms')[0][0]
            key = _['b_name_gen'].replace('(享免税店9.5折)','').replace('.','')
            url_list_node = _['b_room_data'][0]['b_photos']
            value = []
            for j in url_list_node:
                value.append("https://ac-q.static.booking.cn" + j['b_uri_max1024x768'])
            room_info[key] = value
            item['户型'].append(room_info)
        except:
            continue
    print(item)
    info_base.insert_one(item)
