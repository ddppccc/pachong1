import csv
import random
import datetime
import re
import time
import os
import pymongo
import requests
from lxml import etree
from logstic import get_postdetail

info_base = pymongo.MongoClient(host='127.0.0.1', port=27017)['Booking']['info_fin']

form_data = {
    'name': 'room.lightbox',
    'room_id': '',
    'hotel_id': '',
    'search_config': '{"b_adults_total":2,"b_nr_rooms_needed":1,"b_children_total":0,"b_children_ages_total":[],"b_is_group_search":0,"b_pets_total":0,"b_rooms":[{"b_adults":2,"b_room_order":1}]}',
    'other_available_room_ids': '[]',
    'is_soldout': '0',
    'hide_existing_bed_rules': '1',
    'checkin': (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
    'checkout': (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y-%m-%d'),
}


def statis_output(title, rowlist, database) -> object:
    csvfile = open('{}'.format(title), 'w+', newline='', encoding='utf-8')
    res_writer = csv.writer(csvfile, dialect='excel')
    res_writer.writerow(rowlist)
    for item in database.find():
        res_writer.writerow(list(item.values())[1:])


def get_proxy():
    return requests.get("http://192.168.88.51:5010/get/").json()


def Headers():
    headers = {
        "Cookie": "_pxhd=a627d098e18f735be974d4b54e57795fd76524c17ef6a80a0c22dafb782fb0cf%3Aabb9d110-2a1a-11eb-bb37-8fc25101e2ca; cors_js=1; _pxvid=abb9d110-2a1a-11eb-bb37-8fc25101e2ca; _ga=GA1.2.403134577.1605758105; _gcl_au=1.1.1546576241.1605758105; 11_srd=%7B%22features%22%3A%5B%7B%22id%22%3A16%7D%5D%2C%22score%22%3A3%2C%22detected%22%3Afalse%7D; bs=%7B%22sr_country_or_region_page%22%3A%22country%22%7D; BJS=-; has_preloaded=1; _gid=GA1.2.516267090.1606190191; _uetsid=d0f6e4302d2e11eb81c6f7aa62b72e26; _uetvid=021a71102a1b11ebae63611d17654083; _px3=337f63e869e403ab1b94692dda29ad7cc0d9af047fdc7892df849b1cb56c6c0f:j5kdweXuUQTBqdujRiHhPh7cr50YoU5Un2vVWjout3VujFFvIhv+g+JDEApeDV0fs0TMu81c2zHibRRfbFNpaw==:1000:pwQw9eg2ligzw/D0/EidYVMlU/p8ilYThSbQnPFK2XtaJySZqp2snxmKzwP2NNopv2h7Dtkp+/qqvBwyp/aSxTXFgD4adaYol+rXfHIKgLED19J0+WV0LbP8k+v+3h22L70AmlRr16yGRSjtE9vTJb60d3ktz+6ZfXB5KEjq0EM=; _pxde=1e37b66e145c79699aa93ae81a727091c85f9e58618af59a56687fc15b0dd309:eyJ0aW1lc3RhbXAiOjE2MDYyMDU4MjMwMTAsImZfa2IiOjAsImlwY19pZCI6W119; _gat=1; lastSeen=1606206090479; bkng=11UmFuZG9tSVYkc2RlIyh9Yaa29%2F3xUOLbwcLxQQ4VaCrbPGZpiETcqSsEzZs%2FocqroWFGkdevjn1asYZ1W0%2F%2BvUhJ%2B6PbqQilwUMyhNeQEBaG%2Flls3UPla1KAxOFoS5foIBdy8sIJm0AIAG3oTeb4%2F79dGLBVEftzgeIvFHoP8DjFDQQIb8ls3lLLuKEjKTAoKpZbcoYa83W7D3eUHO%2FvGw%3D%3D",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    }
    return headers


def getHTMLText(url, **kwargs):
    time.sleep(random.randint(10, 15) * 0.1 * 0.5)
    try:
        r = requests.get(url, **kwargs)
        r.raise_for_status()
        return r.text
    except:
        return None


def SearchInfo():
    kv = {
        'dest_id': '',
        'dest_type': 'country',
        'checkin_year': '2020',
        'checkin_month': '12',
        'checkin_monthday': '15',
        'checkout_year': '2020',
        'checkout_month': '12',
        'checkout_monthday': '16',
        'offset': '',
    }
    return kv


def request_download(img_url, path):
    import requests
    r = requests.get(img_url)
    with open(path, 'wb') as f:
        f.write(r.content)


def get_MapList(dest_id, page):
    kv['dest_id'] = str(dest_id)
    kv['offset'] = page * 25
    url = 'https://www.booking.com/searchresults.zh-cn.html?'
    try:
        resp = getHTMLText(url=url, params=kv, headers=headers)
        tree = etree.HTML(resp)
    except:
        print('wating....')
        time.sleep(30)
        resp = getHTMLText(url=url, params=kv, headers=headers)
        tree = etree.HTML(resp)
    div = tree.xpath('//div[@id="hotellist_inner"]/div')
    for info in div:
        item = {}
        try:
            item['hotel_id'] = info.xpath('string(@data-hotelid)')
        except:
            break
        try:
            item['??????'] = info.xpath('string(@data-score)')
        except:
            item['??????'] = ''
        item['??????'] = info.xpath(
            'string(./div[@class="sr_item_content sr_item_content_slider_wrapper "]/div/div/div/h3/a/span)').replace(
            '\n', '')
        print('???????????????', item['??????'])
        if item['??????'] == '':
            continue
        item['??????url'] = "https://www.booking.com" + info.xpath(
            'string(./div[@class="sr_item_content sr_item_content_slider_wrapper "]/div/div/div/h3/a/@href)').replace(
            '\r\n', '').replace('\n', '')
        item['??????'] = info.xpath('string(//div[@class="sr_header "]/h1)').replace('\n', '').split('???')[0].replace('??????',
                                                                                                                 '').replace(
            '??????????????????', '')
        try:
            item['??????'] = info.xpath(
                'string(./div[@class="sr_item_content sr_item_content_slider_wrapper "]/div/div/div[@class="sr_card_address_line"]/a)').replace(
                '\r\n', '').replace('??????????????????', '').strip()
        except:
            item['??????'] = ''
        try:
            item['latitude'] = info.xpath(
                'string(./div[@class="sr_item_content sr_item_content_slider_wrapper "]/div/div/div[@class="sr_card_address_line"]/a/@data-coords)').split(
                ',')[0]
        except:
            item['latitude'] = ''
        try:
            item['longitude'] = info.xpath(
                'string(./div[@class="sr_item_content sr_item_content_slider_wrapper "]/div/div/div[@class="sr_card_address_line"]/a/@data-coords)').split(
                ',')[1]
        except:
            item['longitude'] = ''
        try:
            item['??????'] = info.xpath(
                'string(./div[@class="sr_item_content sr_item_content_slider_wrapper "]/div[@class="sr_rooms_table_block clearfix sr_card_rooms_container"]/div/div/div/div/div[@class="roomPrice roomPrice_flex  with-payment-method  sr_discount "]/div/div[2]/div/div)').replace(
                '\n', '')
        except:
            item['??????'] = ''
        get_deepUrlInfo(item['??????url'], item)
    try:
        s = re.findall(r'\d+', tree.xpath('string(//div[@class="sr_header "]/h1)').replace('\n', '').split('???')[1])
        total_count = ''
        for i in s:
            total_count += i
        total_count = int(total_count)
        print(total_count)
    except:
        try:
            s = re.findall(r'\d+', tree.xpath('string(//div[@class="sr_header "]/h1)').replace('\n', ''))
            total_count = ''
            for i in s:
                total_count += i
            total_count = int(total_count)
            print(total_count)
        except:
            total_count = 0
            print('?????????????????????')

    if page == 1:
        print('???????????????????????????')
        if total_count < 25:
            return
        if total_count > 1000:
            total_count = 1000
        all_page = total_count // 25
        for page in range(2, all_page - 1):
            print('???????????????', page)
            get_MapList(dest_id, page)
    else:
        print('???????????????????????????????????????{}'.format(page))


def get_deepUrlInfo(url, item):
    try:
        resp = getHTMLText(url=url, params=kv, headers=headers)
        tree = etree.HTML(resp)
    except:
        print('wating....')
        time.sleep(30)
        resp = getHTMLText(url=url, params=kv, headers=headers)
        tree = etree.HTML(resp)
    try:
        item['??????'] = tree.xpath('string(//div[@class="hp_desc_main_content "])').replace('\n', '')
    except:
        item['??????'] = ''
    try:
        item['????????????'] = tree.xpath('string(//p[@id="showMap2"])').replace('\n', '').replace('??????????????? - ??????????????????', '')
    except:
        item['????????????'] = ''
    try:
        item['????????????'] = tree.xpath('string(//div[@id="hotelPoliciesInc"])').replace('\n', '')
    except:
        item['????????????'] = ''
    try:
        roomlist = tree.xpath('//tbody/tr[@data-et-view="\n"]')
        item['room_id'] = []
        for i in roomlist:
            room_id = int(i.xpath('string(@data-block-id)').split('_')[0])
            if room_id in item['room_id']:
                continue
            else:
                item['room_id'].append(room_id)
    except:
        item['room_id'] = []
    get_postdetail(form_data=form_data, item=item)


# 36
if __name__ == '__main__':
    headers = Headers()
    kv = SearchInfo()
    for dest_id in range(1, 255):
        print('??????????????????', dest_id)
        get_MapList(dest_id, 1)
    # statis_output('Booking_????????????_{}_????????????.csv'.format(time.strftime("%Y-%m-%d", time.localtime())),
    #               ['hotelID', '??????', '??????', '??????url', '??????', '??????', 'latitude', 'longitude', '??????', '??????', '????????????',
    #                '????????????', 'room_ID', '??????'], info_base)

    for item in info_base.find():
        if item['??????'] in ['??????','????????????','???????????????','????????????','?????????????????????','??????','?????????',
                          '????????????','??????','??????','???????????????','????????????','?????????','?????????','?????????',
                          '?????????','???????????????','????????????','??????','??????','????????????','????????????','??????',
                          '??????','?????????','???????????????','?????????????????????','?????????','????????????','??????',
                          '????????????','???????????????','???????????????','????????????','????????????','???????????????',
                          '???????????????(??????)','????????????','??????']:
            continue
        try:
            for a in item['??????']:
                for buildtype in a.keys():
                    path = r'{}/{}/{}/'.format(item['??????'], item['??????'], buildtype)
                    os.makedirs(path)
                    count = 1
                    for _ in a.values():
                        for img_url in _:
                            request_download(img_url, path + '//' + buildtype + str(count) + '.png')
                            count += 1
        except:
            pass
