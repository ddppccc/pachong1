import json
import re
import urllib
import pandas as pd
import requests
from lxml import etree
import random
import pytesseract
from PIL import Image
from io import BytesIO
import os, codecs
import time
import pymongo
from urllib import parse

MONGODB_CONFIG = {
    "host": "8.135.119.198",
    "port": "27017",
    "user": "hladmin",
    "password": parse.quote("Hlxkd3,dk3*3@"),
    "db": "dianping",
    "collections": "dianping_collections",
}

info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['携程酒店']['酒店列表信息_202110']

url_data = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
    MONGODB_CONFIG['user'],
    MONGODB_CONFIG['password'],
    MONGODB_CONFIG['host'],
    MONGODB_CONFIG['port']),
    retryWrites="false")['携程酒店']['列表已爬取酒店id_202110']


class GET:
    def __init__(self):
        self.proxies = {}
        self.city_map_list = [{'display': '吐鲁番', 'data': 'turpan|吐鲁番|40', 'group': 'S', 'cityCode': '0995'},
                              {'display': '神农架', 'data': 'shennongjia|神农架|657', 'group': 'S', 'cityCode': '0719'},
                              {'display': '哈密', 'data': 'hami|哈密市|285', 'group': 'H', 'cityCode': '0902'},
                              {'display': '大理', 'data': 'dali|大理市|36', 'group': 'D', 'cityCode': '0872'},
                              {'display': '北京', 'data': 'Beijing|北京|1', 'group': 'B', 'cityCode': '010'},
                              {'display': '天津', 'data': 'Tianjin|天津|3', 'group': 'T', 'cityCode': '022'},
                              {'display': '上海', 'data': 'Shanghai|上海|2', 'group': 'S', 'cityCode': '021'},
                              {'display': '重庆', 'data': 'Chongqing|重庆|4', 'group': 'C', 'cityCode': '023'},
                              {'display': '石家庄', 'data': 'Shijiazhuang|石家庄|428', 'group': 'S', 'cityCode': 311},
                              {'display': '唐山', 'data': 'Tangshan|唐山|468', 'group': 'T', 'cityCode': 315},
                              {'display': '秦皇岛', 'data': 'Qinhuangdao|秦皇岛|147', 'group': 'Q', 'cityCode': 335},
                              {'display': '邯郸', 'data': 'Handan|邯郸|275', 'group': 'H', 'cityCode': 310},
                              {'display': '邢台', 'data': 'Xingtai|邢台|947', 'group': 'X', 'cityCode': 319},
                              {'display': '保定', 'data': 'baoding|保定|185', 'group': 'B', 'cityCode': '0312'},
                              {'display': '张家口', 'data': 'Zhangjiakou|张家口|550', 'group': 'Z', 'cityCode': 313},
                              {'display': '承德', 'data': 'Chengde|承德|562', 'group': 'C', 'cityCode': 314},
                              {'display': '沧州', 'data': 'Cangzhou|沧州|216', 'group': 'C', 'cityCode': 317},
                              {'display': '廊坊', 'data': 'Langfang|廊坊|340', 'group': 'L', 'cityCode': 316},
                              {'display': '衡水', 'data': 'Hengshui|衡水|290', 'group': 'H', 'cityCode': 318},
                              {'display': '太原', 'data': 'Taiyuan|太原|105', 'group': 'T', 'cityCode': 351},
                              {'display': '大同', 'data': 'Datong|大同|136', 'group': 'D', 'cityCode': 352},
                              {'display': '阳泉', 'data': 'Yangquan|阳泉|907', 'group': 'Y', 'cityCode': 353},
                              {'display': '长治', 'data': 'Changzhi|长治|137', 'group': 'C', 'cityCode': 355},
                              {'display': '晋城', 'data': 'Jincheng|晋城|1092', 'group': 'J', 'cityCode': 356},
                              {'display': '朔州', 'data': 'Shuozhou|朔州|1317', 'group': 'S', 'cityCode': 349},
                              {'display': '晋中', 'data': 'Jinzhong|晋中|1453', 'group': 'J', 'cityCode': 354},
                              {'display': '运城', 'data': 'Yuncheng|运城|140', 'group': 'Y', 'cityCode': 359},
                              {'display': '忻州', 'data': 'Xinzhou|忻州|513', 'group': 'X', 'cityCode': 350},
                              {'display': '临汾', 'data': 'Linfen|临汾|139', 'group': 'L', 'cityCode': 357},
                              {'display': '吕梁', 'data': 'Lvliang|吕梁|7631', 'group': 'L', 'cityCode': 358},
                              {'display': '呼和浩特', 'data': 'Hohhot|呼和浩特|103', 'group': 'H', 'cityCode': 471},
                              {'display': '包头', 'data': 'Baotou|包头|141', 'group': 'B', 'cityCode': 472},
                              {'display': '乌海', 'data': 'Wuhai|乌海|1133', 'group': 'W', 'cityCode': 473},
                              {'display': '赤峰', 'data': 'Chifeng|赤峰|202', 'group': 'C', 'cityCode': 476},
                              {'display': '通辽', 'data': 'Tongliao|通辽|458', 'group': 'T', 'cityCode': 475},
                              {'display': '鄂尔多斯', 'data': 'Ordos|鄂尔多斯|3976', 'group': 'E', 'cityCode': 477},
                              {'display': '呼伦贝尔', 'data': 'Hulunbuir|呼伦贝尔|4255', 'group': 'H', 'cityCode': 470},
                              {'display': '巴彦淖尔', 'data': 'Bayan Nur|巴彦淖尔|3887', 'group': 'B', 'cityCode': 478},
                              {'display': '乌兰察布', 'data': 'Ulanqab|乌兰察布|7518', 'group': 'W', 'cityCode': 474},
                              {'display': '兴安盟', 'data': 'Xinganmeng|兴安盟|21021', 'group': 'X', 'cityCode': 482},
                              {'display': '锡林郭勒盟', 'data': 'Xilinguole|锡林郭勒盟|7576', 'group': 'X', 'cityCode': 479},
                              {'display': '阿拉善', 'data': 'Alxa|阿拉善|7548', 'group': 'A', 'cityCode': 483},
                              {'display': '沈阳', 'data': 'Shenyang|沈阳|451', 'group': 'S', 'cityCode': '024'},
                              {'display': '大连', 'data': 'Dalian|大连|6', 'group': 'D', 'cityCode': 411},
                              {'display': '鞍山', 'data': 'Anshan|鞍山|178', 'group': 'A', 'cityCode': 412},
                              {'display': '抚顺', 'data': 'Fushun|抚顺|252', 'group': 'F', 'cityCode': 413},
                              {'display': '本溪', 'data': 'Benxi|本溪|1155', 'group': 'B', 'cityCode': 414},
                              {'display': '丹东', 'data': 'Dandong|丹东|221', 'group': 'D', 'cityCode': 415},
                              {'display': '锦州', 'data': 'Jinzhou|锦州|327', 'group': 'J', 'cityCode': 416},
                              {'display': '营口', 'data': 'Yingkou|营口|1300', 'group': 'Y', 'cityCode': 417},
                              {'display': '阜新', 'data': 'Fuxin|阜新|254', 'group': 'F', 'cityCode': 418},
                              {'display': '辽阳', 'data': 'Liaoyang|辽阳|351', 'group': 'L', 'cityCode': 419},
                              {'display': '盘锦', 'data': 'Panjin|盘锦|387', 'group': 'P', 'cityCode': 427},
                              {'display': '铁岭', 'data': 'Tieling|铁岭|1048', 'group': 'T', 'cityCode': 410},
                              {'display': '朝阳', 'data': 'Chaoyang|朝阳|211', 'group': 'C', 'cityCode': 421},
                              {'display': '葫芦岛', 'data': 'Huludao|葫芦岛|1050', 'group': 'H', 'cityCode': 429},
                              {'display': '长春', 'data': 'Changchun|长春|158', 'group': 'C', 'cityCode': 431},
                              {'display': '吉林市', 'data': 'Jilin|吉林市|159', 'group': 'J', 'cityCode': 432},
                              {'display': '四平', 'data': 'Siping|四平|440', 'group': 'S', 'cityCode': 434},
                              {'display': '辽源', 'data': 'Liaoyuan|辽源|352', 'group': 'L', 'cityCode': 437},
                              {'display': '通化', 'data': 'Tonghua|通化|456', 'group': 'T', 'cityCode': 435},
                              {'display': '白山', 'data': 'Baishan|白山|3886', 'group': 'B', 'cityCode': 439},
                              {'display': '松原', 'data': 'Songyuan|松原|1303', 'group': 'S', 'cityCode': 438},
                              {'display': '白城', 'data': 'Baicheng|白城|1116', 'group': 'B', 'cityCode': 436},
                              {'display': '延边', 'data': 'Yanbian|延边|867', 'group': 'Y', 'cityCode': 1433},
                              {'display': '哈尔滨', 'data': 'Harbin|哈尔滨|5', 'group': 'H', 'cityCode': 451},
                              {'display': '齐齐哈尔', 'data': 'Qiqihar|齐齐哈尔|149', 'group': 'Q', 'cityCode': 452},
                              {'display': '鸡西', 'data': 'Jixi|鸡西|157', 'group': 'J', 'cityCode': 467},
                              {'display': '鹤岗', 'data': 'Hegang|鹤岗|1611', 'group': 'H', 'cityCode': 468},
                              {'display': '双鸭山', 'data': 'Shuangyashan|双鸭山|1617', 'group': 'S', 'cityCode': 469},
                              {'display': '大庆', 'data': 'Daqing|大庆|231', 'group': 'D', 'cityCode': 459},
                              {'display': '伊春', 'data': 'Yichun|伊春|517', 'group': 'Y', 'cityCode': 458},
                              {'display': '佳木斯', 'data': 'Jiamusi|佳木斯|317', 'group': 'J', 'cityCode': 454},
                              {'display': '七台河', 'data': 'Qitaihe|七台河|1599', 'group': 'Q', 'cityCode': 464},
                              {'display': '牡丹江', 'data': 'Mudanjiang|牡丹江|150', 'group': 'M', 'cityCode': 453},
                              {'display': '黑河', 'data': 'Heihe|黑河|281', 'group': 'H', 'cityCode': 456},
                              {'display': '绥化', 'data': 'Suihua|绥化|1128', 'group': 'S', 'cityCode': 455},
                              {'display': '大兴安岭', 'data': "Daxing'anling|大兴安岭|7663", 'group': 'D', 'cityCode': 457},
                              {'display': '南京', 'data': 'Nanjing|南京|12', 'group': 'N', 'cityCode': '025'},
                              {'display': '无锡', 'data': 'Wuxi|无锡|13', 'group': 'W', 'cityCode': 510},
                              {'display': '徐州', 'data': 'Xuzhou|徐州|512', 'group': 'X', 'cityCode': 516},
                              {'display': '常州', 'data': 'Changzhou|常州|213', 'group': 'C', 'cityCode': 519},
                              {'display': '苏州', 'data': 'Suzhou|苏州|14', 'group': 'S', 'cityCode': 512},
                              {'display': '南通', 'data': 'Nantong|南通|82', 'group': 'N', 'cityCode': 513},
                              {'display': '连云港', 'data': 'Lianyungang|连云港|353', 'group': 'L', 'cityCode': 518},
                              {'display': '淮安', 'data': "Huai'an|淮安|577", 'group': 'H', 'cityCode': 517},
                              {'display': '盐城', 'data': 'Yancheng|盐城|1200', 'group': 'Y', 'cityCode': 515},
                              {'display': '扬州', 'data': 'Yangzhou|扬州|15', 'group': 'Y', 'cityCode': 514},
                              {'display': '镇江', 'data': 'Zhenjiang|镇江|16', 'group': 'Z', 'cityCode': 511},
                              {'display': '泰州', 'data': 'Taizhou|泰州|579', 'group': 'T', 'cityCode': 523},
                              {'display': '宿迁', 'data': 'Suqian|宿迁|1472', 'group': 'S', 'cityCode': 527},
                              {'display': '杭州', 'data': 'Hangzhou|杭州|17', 'group': 'H', 'cityCode': 571},
                              {'display': '宁波', 'data': 'Ningbo|宁波|375', 'group': 'N', 'cityCode': 574},
                              {'display': '温州', 'data': 'Wenzhou|温州|491', 'group': 'W', 'cityCode': 577},
                              {'display': '嘉兴', 'data': 'Jiaxing|嘉兴|571', 'group': 'J', 'cityCode': 573},
                              {'display': '湖州', 'data': 'Huzhou|湖州|86', 'group': 'H', 'cityCode': 572},
                              {'display': '绍兴', 'data': 'Shaoxing|绍兴|22', 'group': 'S', 'cityCode': 575},
                              {'display': '金华', 'data': 'Jinhua|金华|308', 'group': 'J', 'cityCode': 579},
                              {'display': '衢州', 'data': 'Quzhou|衢州|407', 'group': 'Q', 'cityCode': 570},
                              {'display': '舟山', 'data': 'Zhoushan|舟山|19', 'group': 'Z', 'cityCode': 580},
                              {'display': '台州', 'data': 'Taizhou|台州|578', 'group': 'T', 'cityCode': 576},
                              {'display': '丽水', 'data': 'Lishui|丽水|346', 'group': 'L', 'cityCode': 578},
                              {'display': '合肥', 'data': 'Hefei|合肥|278', 'group': 'H', 'cityCode': 551},
                              {'display': '芜湖', 'data': 'Wuhu|芜湖|478', 'group': 'W', 'cityCode': 553},
                              {'display': '蚌埠', 'data': 'Bengbu|蚌埠|182', 'group': 'B', 'cityCode': 552},
                              {'display': '淮南', 'data': 'Huainan|淮南|287', 'group': 'H', 'cityCode': 554},
                              {'display': '马鞍山', 'data': "Ma'anshan|马鞍山|1024", 'group': 'M', 'cityCode': 555},
                              {'display': '淮北', 'data': 'Huaibei|淮北|272', 'group': 'H', 'cityCode': 561},
                              {'display': '铜陵', 'data': 'Tongling|铜陵|459', 'group': 'T', 'cityCode': 562},
                              {'display': '安庆', 'data': 'Anqing|安庆|177', 'group': 'A', 'cityCode': 556},
                              {'display': '黄山', 'data': 'Huangshan|黄山|23', 'group': 'H', 'cityCode': 559},
                              {'display': '滁州', 'data': 'Chuzhou|滁州|214', 'group': 'C', 'cityCode': 550},
                              {'display': '阜阳', 'data': 'Fuyang|阜阳|257', 'group': 'F', 'cityCode': 1558},
                              {'display': '宿州', 'data': 'Suzhou|宿州|521', 'group': 'S', 'cityCode': 557},
                              {'display': '六安', 'data': 'Luan|六安|1705', 'group': 'L', 'cityCode': 564},
                              {'display': '亳州', 'data': 'Bozhou|亳州|1078', 'group': 'B', 'cityCode': 558},
                              {'display': '池州', 'data': 'Chizhou|池州|218', 'group': 'C', 'cityCode': 566},
                              {'display': '宣城', 'data': 'Xuancheng|宣城|1006', 'group': 'X', 'cityCode': 563},
                              {'display': '福州', 'data': 'Fuzhou|福州|258', 'group': 'F', 'cityCode': 591},
                              {'display': '厦门', 'data': 'Xiamen|厦门|25', 'group': 'X', 'cityCode': 592},
                              {'display': '莆田', 'data': 'Putian|莆田|667', 'group': 'P', 'cityCode': 594},
                              {'display': '三明', 'data': 'Sanming|三明|437', 'group': 'S', 'cityCode': 598},
                              {'display': '泉州', 'data': 'Quanzhou|泉州|406', 'group': 'Q', 'cityCode': 595},
                              {'display': '漳州', 'data': 'Zhangzhou|漳州|560', 'group': 'Z', 'cityCode': 596},
                              {'display': '南平', 'data': 'Nanping|南平|606', 'group': 'N', 'cityCode': 599},
                              {'display': '龙岩', 'data': 'Longyan|龙岩|348', 'group': 'L', 'cityCode': 597},
                              {'display': '宁德', 'data': 'Ningde|宁德|378', 'group': 'N', 'cityCode': 593},
                              {'display': '南昌', 'data': 'Nanchang|南昌|376', 'group': 'N', 'cityCode': 791},
                              {'display': '景德镇', 'data': 'Jingdezhen|景德镇|305', 'group': 'J', 'cityCode': 798},
                              {'display': '萍乡', 'data': 'Pingxiang|萍乡|1840', 'group': 'P', 'cityCode': 799},
                              {'display': '九江', 'data': 'Jiujiang|九江|24', 'group': 'J', 'cityCode': 792},
                              {'display': '新余', 'data': 'Xinyu|新余|603', 'group': 'X', 'cityCode': 790},
                              {'display': '鹰潭', 'data': 'Yingtan|鹰潭|534', 'group': 'Y', 'cityCode': 701},
                              {'display': '赣州', 'data': 'Ganzhou|赣州|268', 'group': 'G', 'cityCode': 797},
                              {'display': '吉安', 'data': "Ji'an|吉安|933", 'group': 'J', 'cityCode': 796},
                              {'display': '宜春', 'data': 'Yichun|宜春|518', 'group': 'Y', 'cityCode': 795},
                              {'display': '抚州', 'data': 'Fuzhou|抚州|3884', 'group': 'F', 'cityCode': 794},
                              {'display': '上饶', 'data': 'Shangrao|上饶|411', 'group': 'S', 'cityCode': 793},
                              {'display': '济南', 'data': 'Jinan|济南|144', 'group': 'J', 'cityCode': 531},
                              {'display': '青岛', 'data': 'Qingdao|青岛|7', 'group': 'Q', 'cityCode': 532},
                              {'display': '淄博', 'data': 'Zibo|淄博|542', 'group': 'Z', 'cityCode': 533},
                              {'display': '枣庄', 'data': 'Zaozhuang|枣庄|614', 'group': 'Z', 'cityCode': 632},
                              {'display': '东营', 'data': 'Dongying|东营|236', 'group': 'D', 'cityCode': 546},
                              {'display': '烟台', 'data': 'Yantai|烟台|533', 'group': 'Y', 'cityCode': 535},
                              {'display': '潍坊', 'data': 'Weifang|潍坊|475', 'group': 'W', 'cityCode': 536},
                              {'display': '济宁', 'data': 'Jining|济宁|318', 'group': 'J', 'cityCode': 537},
                              {'display': '泰安', 'data': 'Taian|泰安|454', 'group': 'T', 'cityCode': 538},
                              {'display': '威海', 'data': 'Weihai|威海|479', 'group': 'W', 'cityCode': 631},
                              {'display': '日照', 'data': 'Rizhao|日照|1106', 'group': 'R', 'cityCode': 633},
                              {'display': '临沂', 'data': 'Linyi|临沂|569', 'group': 'L', 'cityCode': 539},
                              {'display': '德州', 'data': 'Dezhou|德州|1370', 'group': 'D', 'cityCode': 534},
                              {'display': '聊城', 'data': 'Liaocheng|聊城|1071', 'group': 'L', 'cityCode': 635},
                              {'display': '滨州', 'data': 'Binzhou|滨州|1820', 'group': 'B', 'cityCode': 543},
                              {'display': '菏泽', 'data': 'Heze|菏泽|1074', 'group': 'H', 'cityCode': 530},
                              {'display': '郑州', 'data': 'Zhengzhou|郑州|559', 'group': 'Z', 'cityCode': 371},
                              {'display': '开封', 'data': 'Kaifeng|开封|331', 'group': 'K', 'cityCode': 378},
                              {'display': '洛阳', 'data': 'Luoyang|洛阳|350', 'group': 'L', 'cityCode': 379},
                              {'display': '平顶山', 'data': 'Pingdingshan|平顶山|3222', 'group': 'P', 'cityCode': 375},
                              {'display': '安阳', 'data': 'Anyang|安阳|181', 'group': 'A', 'cityCode': 372},
                              {'display': '鹤壁', 'data': 'Hebi|鹤壁|951', 'group': 'H', 'cityCode': 392},
                              {'display': '新乡', 'data': 'Xinxiang|新乡|507', 'group': 'X', 'cityCode': 373},
                              {'display': '焦作', 'data': 'Jiaozuo|焦作|1093', 'group': 'J', 'cityCode': 391},
                              {'display': '濮阳', 'data': 'Puyang|濮阳|1232', 'group': 'P', 'cityCode': 393},
                              {'display': '许昌', 'data': 'Xuchang|许昌|1094', 'group': 'X', 'cityCode': 374},
                              {'display': '漯河', 'data': 'Luohe|漯河|1088', 'group': 'L', 'cityCode': 395},
                              {'display': '三门峡', 'data': 'Sanmenxia|三门峡|436', 'group': 'S', 'cityCode': 398},
                              {'display': '南阳', 'data': 'Nanyang|南阳|385', 'group': 'N', 'cityCode': 377},
                              {'display': '商丘', 'data': 'Shangqiu|商丘|441', 'group': 'S', 'cityCode': 370},
                              {'display': '信阳', 'data': 'Xinyang|信阳|510', 'group': 'X', 'cityCode': 376},
                              {'display': '周口', 'data': 'Zhoukou|周口|3221', 'group': 'Z', 'cityCode': 394},
                              {'display': '驻马店', 'data': 'Zhumadian|驻马店|551', 'group': 'Z', 'cityCode': 396},
                              {'display': '济源', 'data': 'Jiyuan|济源|1454', 'group': 'J', 'cityCode': 1391},
                              {'display': '武汉', 'data': 'Wuhan|武汉|477', 'group': 'W', 'cityCode': '027'},
                              {'display': '黄石', 'data': 'Huangshi|黄石|292', 'group': 'H', 'cityCode': 714},
                              {'display': '十堰', 'data': 'Shiyan|十堰|452', 'group': 'S', 'cityCode': 719},
                              {'display': '宜昌', 'data': 'Yichang|宜昌|515', 'group': 'Y', 'cityCode': 717},
                              {'display': '襄阳', 'data': 'Xiangyang|襄阳|496', 'group': 'X', 'cityCode': 710},
                              {'display': '鄂州', 'data': 'Ezhou|鄂州|992', 'group': 'E', 'cityCode': 711},
                              {'display': '荆门', 'data': 'Jingmen|荆门|1121', 'group': 'J', 'cityCode': 724},
                              {'display': '孝感', 'data': 'Xiaogan|孝感|1490', 'group': 'X', 'cityCode': 712},
                              {'display': '荆州', 'data': 'Jingzhou|荆州|328', 'group': 'J', 'cityCode': 716},
                              {'display': '黄冈', 'data': 'Huanggang|黄冈|3885', 'group': 'H', 'cityCode': 713},
                              {'display': '咸宁', 'data': 'Xianning|咸宁|937', 'group': 'X', 'cityCode': 715},
                              {'display': '随州', 'data': 'Suizhou|随州|1117', 'group': 'S', 'cityCode': 722},
                              {'display': '恩施', 'data': 'Enshi|恩施|245', 'group': 'E', 'cityCode': 718},
                              {'display': '长沙', 'data': 'Changsha|长沙|206', 'group': 'C', 'cityCode': 731},
                              {'display': '株洲', 'data': 'Zhuzhou|株洲|601', 'group': 'Z', 'cityCode': 733},
                              {'display': '湘潭', 'data': 'Xiangtan|湘潭|598', 'group': 'X', 'cityCode': 732},
                              {'display': '衡阳', 'data': 'Hengyang|衡阳|297', 'group': 'H', 'cityCode': 734},
                              {'display': '邵阳', 'data': 'Shaoyang|邵阳|1111', 'group': 'S', 'cityCode': 739},
                              {'display': '岳阳', 'data': 'Yueyang|岳阳|539', 'group': 'Y', 'cityCode': 730},
                              {'display': '常德', 'data': 'Changde|常德|201', 'group': 'C', 'cityCode': 736},
                              {'display': '张家界', 'data': 'Zhangjiajie|张家界|27', 'group': 'Z', 'cityCode': 744},
                              {'display': '益阳', 'data': 'Yiyang|益阳|1125', 'group': 'Y', 'cityCode': 737},
                              {'display': '郴州', 'data': 'Chenzhou|郴州|612', 'group': 'C', 'cityCode': 735},
                              {'display': '永州', 'data': 'Yongzhou|永州|970', 'group': 'Y', 'cityCode': 746},
                              {'display': '怀化', 'data': 'Huaihua|怀化|282', 'group': 'H', 'cityCode': 745},
                              {'display': '娄底', 'data': 'Loudi|娄底|918', 'group': 'L', 'cityCode': 738},
                              {'display': '湘西', 'data': 'Xiangxi|湘西|3910', 'group': 'X', 'cityCode': 743},
                              {'display': '广州', 'data': 'Guangzhou|广州|32', 'group': 'G', 'cityCode': '020'},
                              {'display': '韶关', 'data': 'Shaoguan|韶关|422', 'group': 'S', 'cityCode': 751},
                              {'display': '深圳', 'data': 'Shenzhen|深圳|30', 'group': 'S', 'cityCode': 755},
                              {'display': '珠海', 'data': 'Zhuhai|珠海|31', 'group': 'Z', 'cityCode': 756},
                              {'display': '汕头', 'data': 'Shantou|汕头|447', 'group': 'S', 'cityCode': 754},
                              {'display': '佛山', 'data': 'Foshan|佛山|251', 'group': 'F', 'cityCode': 757},
                              {'display': '江门', 'data': 'Jiangmen|江门|316', 'group': 'J', 'cityCode': 750},
                              {'display': '湛江', 'data': 'Zhanjiang|湛江|547', 'group': 'Z', 'cityCode': 759},
                              {'display': '茂名', 'data': 'Maoming|茂名|1105', 'group': 'M', 'cityCode': 668},
                              {'display': '肇庆', 'data': 'Zhaoqing|肇庆|552', 'group': 'Z', 'cityCode': 758},
                              {'display': '惠州', 'data': 'Huizhou|惠州|299', 'group': 'H', 'cityCode': 752},
                              {'display': '梅州', 'data': 'Meizhou|梅州|3053', 'group': 'M', 'cityCode': 753},
                              {'display': '汕尾', 'data': 'Shanwei|汕尾|1436', 'group': 'S', 'cityCode': 660},
                              {'display': '河源', 'data': 'Heyuan|河源|693', 'group': 'H', 'cityCode': 762},
                              {'display': '阳江', 'data': 'Yangjiang|阳江|692', 'group': 'Y', 'cityCode': 662},
                              {'display': '清远', 'data': 'Qingyuan|清远|1422', 'group': 'Q', 'cityCode': 763},
                              {'display': '东莞', 'data': 'Dongguan|东莞|223', 'group': 'D', 'cityCode': 769},
                              {'display': '中山', 'data': 'Zhongshan|中山|553', 'group': 'Z', 'cityCode': 760},
                              {'display': '潮州', 'data': 'Chaozhou|潮州|215', 'group': 'C', 'cityCode': 768},
                              {'display': '揭阳', 'data': 'Jieyang|揭阳|956', 'group': 'J', 'cityCode': 663},
                              {'display': '云浮', 'data': 'Yunfu|云浮|3933', 'group': 'Y', 'cityCode': 766},
                              {'display': '南宁', 'data': 'Nanning|南宁|380', 'group': 'N', 'cityCode': 771},
                              {'display': '柳州', 'data': 'Liuzhou|柳州|354', 'group': 'L', 'cityCode': 772},
                              {'display': '桂林', 'data': 'Guilin|桂林|33', 'group': 'G', 'cityCode': 773},
                              {'display': '梧州', 'data': 'Wuzhou|梧州|492', 'group': 'W', 'cityCode': 774},
                              {'display': '北海', 'data': 'Beihai|北海|189', 'group': 'B', 'cityCode': 779},
                              {'display': '防城港', 'data': 'Fangchenggang|防城港|1677', 'group': 'F', 'cityCode': 770},
                              {'display': '钦州', 'data': 'Qinzhou|钦州|1899', 'group': 'Q', 'cityCode': 777},
                              {'display': '贵港', 'data': 'Guigang|贵港|1518', 'group': 'G', 'cityCode': 1755},
                              {'display': '玉林', 'data': 'Yulin|玉林|1113', 'group': 'Y', 'cityCode': 775},
                              {'display': '百色', 'data': 'Baise|百色|1140', 'group': 'B', 'cityCode': 776},
                              {'display': '贺州', 'data': 'Hezhou|贺州|4146', 'group': 'H', 'cityCode': 1774},
                              {'display': '河池', 'data': 'Hechi|河池|3969', 'group': 'H', 'cityCode': 778},
                              {'display': '来宾', 'data': 'Laibin|来宾|1892', 'group': 'L', 'cityCode': 1772},
                              {'display': '崇左', 'data': 'Chongzuo|崇左|1896', 'group': 'C', 'cityCode': 1771},
                              {'display': '海口', 'data': 'Haikou|海口|42', 'group': 'H', 'cityCode': 898},
                              {'display': '三亚', 'data': 'Sanya|三亚|43', 'group': 'S', 'cityCode': 899},
                              {'display': '五指山', 'data': 'Wuzhishan|五指山|46', 'group': 'W', 'cityCode': 1897},
                              {'display': '琼海', 'data': 'Qionghai|琼海|52', 'group': 'Q', 'cityCode': 1894},
                              {'display': '儋州', 'data': 'Danzhou|儋州|57', 'group': 'D', 'cityCode': 805},
                              {'display': '文昌', 'data': 'Wenchang|文昌|44', 'group': 'W', 'cityCode': 1893},
                              {'display': '万宁', 'data': 'Wanning|万宁|45', 'group': 'W', 'cityCode': 1898},
                              {'display': '东方', 'data': 'Dongfang|东方|48', 'group': 'D', 'cityCode': 807},
                              {'display': '定安', 'data': "Ding'an|定安|50", 'group': 'D', 'cityCode': 806},
                              {'display': '屯昌', 'data': 'Tunchang|屯昌|47', 'group': 'T', 'cityCode': 1892},
                              {'display': '澄迈', 'data': 'Chengmai|澄迈|20836', 'group': 'C', 'cityCode': 804},
                              {'display': '临高', 'data': 'Lingao|临高|20868', 'group': 'L', 'cityCode': 1896},
                              {'display': '白沙', 'data': 'Baisha|白沙|21025', 'group': 'B', 'cityCode': 802},
                              {'display': '昌江', 'data': 'Changjiang|昌江|56', 'group': 'C', 'cityCode': 803},
                              {'display': '乐东', 'data': 'Ledong|乐东|49', 'group': 'L', 'cityCode': 2802},
                              {'display': '陵水', 'data': 'Lingshui|陵水|55', 'group': 'L', 'cityCode': 809},
                              {'display': '保亭', 'data': 'Baoting|保亭|54', 'group': 'B', 'cityCode': 801},
                              {'display': '琼中', 'data': 'Qiongzhong|琼中|53', 'group': 'Q', 'cityCode': 1899},
                              {'display': '成都', 'data': 'Chengdu|成都|28', 'group': 'C', 'cityCode': '028'},
                              {'display': '自贡', 'data': 'Zigong|自贡|544', 'group': 'Z', 'cityCode': 813},
                              {'display': '攀枝花', 'data': 'Panzhihua|攀枝花|1097', 'group': 'P', 'cityCode': 812},
                              {'display': '泸州', 'data': 'Luzhou|泸州|355', 'group': 'L', 'cityCode': 830},
                              {'display': '德阳', 'data': 'Deyang|德阳|237', 'group': 'D', 'cityCode': 838},
                              {'display': '绵阳', 'data': 'Mianyang|绵阳|370', 'group': 'M', 'cityCode': 816},
                              {'display': '广元', 'data': 'Guangyuan|广元|267', 'group': 'G', 'cityCode': 839},
                              {'display': '遂宁', 'data': 'Suining|遂宁|1371', 'group': 'S', 'cityCode': 825},
                              {'display': '内江', 'data': 'Neijiang|内江|1597', 'group': 'N', 'cityCode': 1832},
                              {'display': '乐山', 'data': 'Leshan|乐山|345', 'group': 'L', 'cityCode': 833},
                              {'display': '南充', 'data': 'Nanchong|南充|377', 'group': 'N', 'cityCode': 817},
                              {'display': '眉山', 'data': 'Meishan|眉山|1148', 'group': 'M', 'cityCode': 1833},
                              {'display': '宜宾', 'data': 'Yibin|宜宾|514', 'group': 'Y', 'cityCode': 831},
                              {'display': '广安', 'data': "Guang'an|广安|1100", 'group': 'G', 'cityCode': 826},
                              {'display': '达州', 'data': 'Dazhou|达州|1233', 'group': 'D', 'cityCode': 818},
                              {'display': '雅安', 'data': "Ya'an|雅安|3277", 'group': 'Y', 'cityCode': 835},
                              {'display': '巴中', 'data': 'Bazhong|巴中|3966', 'group': 'B', 'cityCode': 827},
                              {'display': '资阳', 'data': 'Ziyang|资阳|1560', 'group': 'Z', 'cityCode': 832},
                              {'display': '阿坝', 'data': 'Abazhou|阿坝|1838', 'group': 'A', 'cityCode': 837},
                              {'display': '甘孜', 'data': 'Ganzizhou|甘孜|4124', 'group': 'G', 'cityCode': 836},
                              {'display': '凉山', 'data': 'Liangshanzhou|凉山|7537', 'group': 'L', 'cityCode': 834},
                              {'display': '贵阳', 'data': 'Guiyang|贵阳|38', 'group': 'G', 'cityCode': 851},
                              {'display': '六盘水', 'data': 'Liupanshui|六盘水|605', 'group': 'L', 'cityCode': 858},
                              {'display': '遵义', 'data': 'Zunyi|遵义|558', 'group': 'Z', 'cityCode': 852},
                              {'display': '安顺', 'data': 'Anshun|安顺|179', 'group': 'A', 'cityCode': 853},
                              {'display': '毕节', 'data': 'Bijie|毕节|22031', 'group': 'B', 'cityCode': 857},
                              {'display': '铜仁', 'data': 'Tongren|铜仁|22033', 'group': 'T', 'cityCode': 856},
                              {'display': '黔西南', 'data': 'Qianxinan|黔西南|21613', 'group': 'Q', 'cityCode': 859},
                              {'display': '黔东南', 'data': 'Qiandongnan|黔东南|21778', 'group': 'Q', 'cityCode': 855},
                              {'display': '黔南', 'data': 'Qiannan|黔南|21179', 'group': 'Q', 'cityCode': 854},
                              {'display': '昆明', 'data': 'Kunming|昆明|34', 'group': 'K', 'cityCode': 871},
                              {'display': '曲靖', 'data': 'Qujing|曲靖|985', 'group': 'Q', 'cityCode': 874},
                              {'display': '玉溪', 'data': 'Yuxi|玉溪|186', 'group': 'Y', 'cityCode': 877},
                              {'display': '保山', 'data': 'Baoshan|保山|197', 'group': 'B', 'cityCode': 875},
                              {'display': '昭通', 'data': 'Zhaotong|昭通|555', 'group': 'Z', 'cityCode': 870},
                              {'display': '丽江', 'data': 'Lijiang|丽江|37', 'group': 'L', 'cityCode': 888},
                              {'display': '普洱', 'data': "Pu'er|普洱|3996", 'group': 'P', 'cityCode': 879},
                              {'display': '临沧', 'data': 'Lincang|临沧|1236', 'group': 'L', 'cityCode': 883},
                              {'display': '楚雄', 'data': 'Chuxiong|楚雄|21658', 'group': 'C', 'cityCode': 878},
                              {'display': '红河', 'data': 'Honghe|红河|1341', 'group': 'H', 'cityCode': 873},
                              {'display': '文山', 'data': 'Wenshan|文山|20963', 'group': 'W', 'cityCode': 876},
                              {'display': '西双版纳', 'data': 'Xishuangbanna|西双版纳|35', 'group': 'X', 'cityCode': 691},
                              {'display': '德宏', 'data': 'Dehong|德宏|365', 'group': 'D', 'cityCode': 692},
                              {'display': '怒江', 'data': 'Nujiang|怒江|1806', 'group': 'N', 'cityCode': 886},
                              {'display': '迪庆', 'data': 'Diqing|迪庆|93', 'group': 'D', 'cityCode': 887},
                              {'display': '拉萨', 'data': 'Lhasa|拉萨|41', 'group': 'L', 'cityCode': 891},
                              {'display': '日喀则', 'data': 'Rikaze|日喀则|92', 'group': 'R', 'cityCode': 892},
                              {'display': '昌都', 'data': 'Qamdo|昌都|575', 'group': 'C', 'cityCode': 895},
                              {'display': '山南', 'data': 'Shannan|山南|439', 'group': 'S', 'cityCode': 893},
                              {'display': '那曲', 'data': 'Naqu|那曲|3839', 'group': 'N', 'cityCode': 896},
                              {'display': '阿里', 'data': 'Ali|阿里|97', 'group': 'A', 'cityCode': 897},
                              {'display': '林芝', 'data': 'Nyingchi|林芝|108', 'group': 'L', 'cityCode': 894},
                              {'display': '西安', 'data': "Xi'an|西安|10", 'group': 'X', 'cityCode': '029'},
                              {'display': '铜川', 'data': 'Tongchuan|铜川|118', 'group': 'T', 'cityCode': 919},
                              {'display': '宝鸡', 'data': 'Baoji|宝鸡|112', 'group': 'B', 'cityCode': 917},
                              {'display': '咸阳', 'data': 'Xianyang|咸阳|111', 'group': 'X', 'cityCode': 910},
                              {'display': '渭南', 'data': 'Weinan|渭南|1030', 'group': 'W', 'cityCode': 913},
                              {'display': '延安', 'data': "Yan'an|延安|110", 'group': 'Y', 'cityCode': 911},
                              {'display': '汉中', 'data': 'Hanzhong|汉中|129', 'group': 'H', 'cityCode': 916},
                              {'display': '榆林', 'data': 'Yulin|榆林|527', 'group': 'Y', 'cityCode': 912},
                              {'display': '安康', 'data': 'Ankang|安康|171', 'group': 'A', 'cityCode': 915},
                              {'display': '商洛', 'data': 'Shangluo|商洛|7551', 'group': 'S', 'cityCode': 914},
                              {'display': '兰州', 'data': 'Lanzhou|兰州|100', 'group': 'L', 'cityCode': 931},
                              {'display': '嘉峪关', 'data': 'Jiayuguan|嘉峪关|326', 'group': 'J', 'cityCode': 1937},
                              {'display': '金昌', 'data': 'Jinchang|金昌|1158', 'group': 'J', 'cityCode': 935},
                              {'display': '白银', 'data': 'Baiyin|白银|1541', 'group': 'B', 'cityCode': 943},
                              {'display': '天水', 'data': 'Tianshui|天水|464', 'group': 'T', 'cityCode': 938},
                              {'display': '武威', 'data': 'Wuwei|武威|664', 'group': 'W', 'cityCode': 1935},
                              {'display': '张掖', 'data': 'Zhangye|张掖|663', 'group': 'Z', 'cityCode': 936},
                              {'display': '平凉', 'data': 'Pingliang|平凉|388', 'group': 'P', 'cityCode': 933},
                              {'display': '酒泉', 'data': 'Jiuquan|酒泉|662', 'group': 'J', 'cityCode': 937},
                              {'display': '庆阳', 'data': 'Qingyang|庆阳|404', 'group': 'Q', 'cityCode': 934},
                              {'display': '定西', 'data': 'Dingxi|定西|1021', 'group': 'D', 'cityCode': 932},
                              {'display': '陇南', 'data': 'Longnan|陇南|7707', 'group': 'L', 'cityCode': 2935},
                              {'display': '临夏', 'data': 'Linxia|临夏|21892', 'group': 'L', 'cityCode': 930},
                              {'display': '甘南', 'data': 'Gannan|甘南|7844', 'group': 'G', 'cityCode': 941},
                              {'display': '西宁', 'data': 'Xining|西宁|124', 'group': 'X', 'cityCode': 971},
                              {'display': '海东', 'data': 'Haidong|海东|7752', 'group': 'H', 'cityCode': 972},
                              {'display': '海北', 'data': 'Haibei|海北|7807', 'group': 'H', 'cityCode': 970},
                              {'display': '黄南', 'data': 'Huangnan|黄南|7802', 'group': 'H', 'cityCode': 973},
                              {'display': '海南', 'data': 'Hainan|海南|7794', 'group': 'H', 'cityCode': 974},
                              {'display': '果洛', 'data': 'Golog|果洛|21862', 'group': 'G', 'cityCode': 975},
                              {'display': '玉树', 'data': 'Yushu|玉树|21114', 'group': 'Y', 'cityCode': 976},
                              {'display': '海西', 'data': 'Haixizhou|海西|7589', 'group': 'H', 'cityCode': 977},
                              {'display': '银川', 'data': 'Yinchuan|银川|99', 'group': 'Y', 'cityCode': 951},
                              {'display': '石嘴山', 'data': 'Shizuishan|石嘴山|4216', 'group': 'S', 'cityCode': 952},
                              {'display': '吴忠', 'data': 'Wuzhong|吴忠|7587', 'group': 'W', 'cityCode': 953},
                              {'display': '固原', 'data': 'Guyuan|固原|321', 'group': 'G', 'cityCode': 954},
                              {'display': '中卫', 'data': 'Zhongwei|中卫|556', 'group': 'Z', 'cityCode': 1953},
                              {'display': '乌鲁木齐', 'data': 'Urumqi|乌鲁木齐|39', 'group': 'W', 'cityCode': 991},
                              {'display': '克拉玛依', 'data': 'Karamay|克拉玛依|166', 'group': 'K', 'cityCode': 990},
                              {'display': '昌吉', 'data': 'Changji|昌吉|22032', 'group': 'C', 'cityCode': 994},
                              {'display': '博尔塔拉', 'data': 'Boertala|博尔塔拉|21468', 'group': 'B', 'cityCode': 909},
                              {'display': '巴音郭楞', 'data': 'Bayinguoleng|巴音郭楞|21130', 'group': 'B', 'cityCode': 996},
                              {'display': '阿克苏', 'data': 'Aksu|阿克苏|173', 'group': 'A', 'cityCode': 997},
                              {'display': '克孜勒苏', 'data': 'Kezilesu|克孜勒苏|21482', 'group': 'K', 'cityCode': 908},
                              {'display': '喀什', 'data': 'Kashi|喀什|21358', 'group': 'K', 'cityCode': 998},
                              {'display': '和田', 'data': 'Hetian|和田|20931', 'group': 'H', 'cityCode': 903},
                              {'display': '伊犁', 'data': 'Ili|伊犁|98', 'group': 'Y', 'cityCode': 999},
                              {'display': '塔城', 'data': 'Tacheng|塔城|455', 'group': 'T', 'cityCode': 901},
                              {'display': '阿勒泰', 'data': 'Aletai|阿勒泰|175', 'group': 'A', 'cityCode': 906},
                              {'display': '香港', 'data': 'Hong Kong|香港|58', 'group': 'X', 'cityCode': 1852},
                              {'display': '天门', 'data': 'tianmen|天门|3920', 'group': 'X', 'cityCode': '0728'},
                              {'display': '五家渠', 'data': 'wujiaqu|五家渠|7792', 'group': 'X', 'cityCode': '0994'},
                              {'display': '石河子', 'data': 'shihezi|石河子|426', 'group': 'X', 'cityCode': '0993'},
                              {'display': '北屯', 'data': 'beitun|北屯|77537', 'group': 'X', 'cityCode': ''},
                              {'display': '阿拉尔', 'data': 'alaer|阿拉尔|20943', 'group': 'X', 'cityCode': '0997'},
                              {'display': '仙桃', 'data': 'xiantao|仙桃|1882', 'group': 'X', 'cityCode': '0728'},
                              {'display': '潜江', 'data': 'qianjiang|潜江|4154', 'group': 'X', 'cityCode': '0728'},
                              {'display': '澳门', 'data': 'macau|澳门|59', 'group': 'X', 'cityCode': '1853'},
                              ]
        self.monny_list = []
        self.sj = []
        self.bj = []
        self.header = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'ibulanguage=CN; ibulocale=zh_cn; cookiePricesDisplayed=CNY; IBU_TRANCE_LOG_P=86189454181; Hm_lvt_4a51227696a44e11b0c61f6105dc4ee4=1633749870; _gcl_au=1.1.672454943.1633749872; _RSG=3HKojb14.n5B5dYjwcjKQB; _RDG=28333ea5cc990c2e6626e856d9b46dbf6c; _RGUID=5c7e1019-6dc9-4443-b694-b66ead8a714b; MKT_CKID=1633749873335.0irat.zzoe; _ga=GA1.2.1240620884.1633749874; _abtest_userid=f0ebb3a4-5dc2-47e5-9166-41eb9f39065b; MKT_Pagesource=PC; librauuid=3lSNuDDzobcaVG5a; _RF1=14.106.229.21; MKT_CKID_LMT=1635152482029; _gid=GA1.2.443495843.1635152482; Hm_lpvt_4a51227696a44e11b0c61f6105dc4ee4=1635226403; _bfa=1.1633749869935.448q8m.1.1635215946794.1635226346785.5.32; _bfs=1.5; _bfi=p1%3D102002%26p2%3D102002%26v1%3D32%26v2%3D31; _jzqco=%7C%7C%7C%7C1635152482329%7C1.1073515532.1633749873345.1635226384183.1635226405927.1635226384183.1635226405927.undefined.0.0.23.23; __zpspc=9.5.1635226350.1635226405.5%232%7Cwww.baidu.com%7C%7C%7C%7C%23; appFloatCnt=23',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }
        self.cookie_List = [
            'ibulanguage=CN; ibulocale=zh_cn; cookiePricesDisplayed=CNY; _gcl_au=1.1.672454943.1633749872; _RSG=3HKojb14.n5B5dYjwcjKQB; _RDG=28333ea5cc990c2e6626e856d9b46dbf6c; _RGUID=5c7e1019-6dc9-4443-b694-b66ead8a714b; MKT_CKID=1633749873335.0irat.zzoe; _ga=GA1.2.1240620884.1633749874; _abtest_userid=f0ebb3a4-5dc2-47e5-9166-41eb9f39065b; MKT_Pagesource=PC; _RF1=14.106.229.21; MKT_CKID_LMT=1635152482029; _gid=GA1.2.443495843.1635152482; librauuid=l4sg2F37HAsfuBpP; login_type=0; UUID=88F775BA0F5B4B739849B76CA42E43F1; appFloatCnt=44; Union=AllianceID=1315&SID=1535&OUID=; Session=smartlinkcode=U1535&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; login_uid=92E2FEA887C08D3F87A966619EFDDFA1; cticket=11B52C9DEFF0D18D854BC99CC71F51C0866021E658DDA036370CE9D4AF11867A; AHeadUserInfo=VipGrade=10&VipGradeName=%BB%C6%BD%F0%B9%F3%B1%F6&UserName=&NoReadMessageCount=4; DUID=u=92E2FEA887C08D3F87A966619EFDDFA1&v=0; IsNonUser=F; IsPersonalizedLogin=F; intl_ht1=h4=1_70400799,7_4719799,1_6719748; _uetsid=d681fa80362611ecafd9d9d0de5b586c; _uetvid=d6823c30362611ecb9c6151ac3f9b281; _bfi=p1%3D102003%26p2%3D102003%26v1%3D80%26v2%3D79; _jzqco=%7C%7C%7C%7C1635152482329%7C1.1073515532.1633749873345.1635230774030.1635230811694.1635230774030.1635230811694.undefined.0.0.50.50; __zpspc=9.6.1635230084.1635230811.18%232%7Cwww.baidu.com%7C%7C%7C%7C%23; _bfa=1.1633749869935.448q8m.1.1635226346785.1635230051335.6.81; _bfs=1.28',
            'ibulanguage=CN; ibulocale=zh_cn; cookiePricesDisplayed=CNY; librauuid=UMQp2Hqf5lOlCDXF; _RF1=14.106.229.21; _RDG=28d297ce19122b202e2d97c03cfc205a12; _RSG=BeaxcpyUNtBrGvnbl88htB; _RGUID=bdd77bcc-e6ee-4a0b-bdeb-208be5c79435; login_type=0; UUID=2290932E649D4BD8A86416605260AA34; _gcl_au=1.1.1782509575.1635302605; MKT_CKID=1635302607908.9hqvv.dox8; MKT_CKID_LMT=1635302607909; _ga=GA1.2.1728612954.1635302608; _gid=GA1.2.2104789030.1635302608; MKT_Pagesource=PC; appFloatCnt=1; login_uid=2AA012DF26821C0BAF96234742C7352C; cticket=3CD2373579DA1BB641FE453479C4D0C41000381D8E5D3D01F2FA33318811398D; AHeadUserInfo=VipGrade=0&VipGradeName=%C6%D5%CD%A8%BB%E1%D4%B1&UserName=&NoReadMessageCount=0; DUID=u=2AA012DF26821C0BAF96234742C7352C&v=0; IsNonUser=F; IsPersonalizedLogin=F; _gat=1; _jzqco=%7C%7C%7C%7C1635302608371%7C1.1300352383.1635302607933.1635302940049.1635303185055.1635302940049.1635303185055.0.0.0.3.3; __zpspc=9.1.1635302607.1635303185.3%234%7C%7C%7C%7C%7C%23; _bfi=p1%3D100101991%26p2%3D10320670296%26v1%3D11%26v2%3D10; intl_ht1=h4=2_80664565,1_72898766; _bfa=1.1635302467464.3ltfqx.1.1635302467464.1635302467464.1.13; _bfs=1.13',
            'ibulanguage=CN; ibulocale=zh_cn; cookiePricesDisplayed=CNY; intl_ht1=h4=1_72898766; librauuid=UMQp2Hqf5lOlCDXF; _RF1=14.106.229.21; _RSG=BeaxcpyUNtBrGvnbl88htB; _RDG=28d297ce19122b202e2d97c03cfc205a12; _RGUID=bdd77bcc-e6ee-4a0b-bdeb-208be5c79435; login_uid=F3E88DE93D03EB967917EF275B42FE7A; login_type=0; cticket=FD95326DA5E8404AA9C32CA52E6720EA58B142449B57C35AE164D690B88D2B24; AHeadUserInfo=VipGrade=0&VipGradeName=%C6%D5%CD%A8%BB%E1%D4%B1&UserName=&NoReadMessageCount=0; DUID=u=F3E88DE93D03EB967917EF275B42FE7A&v=0; IsNonUser=F; UUID=2290932E649D4BD8A86416605260AA34; IsPersonalizedLogin=T; _bfa=1.1635302467464.3ltfqx.1.1635302467464.1635302467464.1.3; _bfs=1.3; _gcl_au=1.1.1782509575.1635302605; _bfi=p1%3D102001%26p2%3D10320670296%26v1%3D3%26v2%3D2; MKT_CKID=1635302607908.9hqvv.dox8; MKT_CKID_LMT=1635302607909; __zpspc=9.1.1635302607.1635302607.1%234%7C%7C%7C%7C%7C%23; _ga=GA1.2.1728612954.1635302608; _gid=GA1.2.2104789030.1635302608; _gat=1; MKT_Pagesource=PC; appFloatCnt=1; _jzqco=%7C%7C%7C%7C1635302608371%7C1.1300352383.1635302607933.1635302607933.1635302607934.1635302607933.1635302607934.0.0.0.1.1',
            'ibulanguage=CN; ibulocale=zh_cn; cookiePricesDisplayed=CNY; librauuid=UMQp2Hqf5lOlCDXF; _RF1=14.106.229.21; _RSG=BeaxcpyUNtBrGvnbl88htB; _RDG=28d297ce19122b202e2d97c03cfc205a12; _RGUID=bdd77bcc-e6ee-4a0b-bdeb-208be5c79435; login_type=0; UUID=2290932E649D4BD8A86416605260AA34; _gcl_au=1.1.1782509575.1635302605; MKT_CKID=1635302607908.9hqvv.dox8; MKT_CKID_LMT=1635302607909; _ga=GA1.2.1728612954.1635302608; _gid=GA1.2.2104789030.1635302608; MKT_Pagesource=PC; intl_ht1=h4=2_80664565,1_72898766; appFloatCnt=2; _gat=1; _jzqco=%7C%7C%7C%7C1635302608371%7C1.1300352383.1635302607933.1635303200578.1635303455047.1635303200578.1635303455047.0.0.0.5.5; __zpspc=9.1.1635302607.1635303455.5%234%7C%7C%7C%7C%7C%23; _bfi=p1%3D10320670296%26p2%3D100101991%26v1%3D15%26v2%3D14; login_uid=3F4AEEEBF270964AE990F2675434EC60; cticket=88D96810E5BF3ECF87FD8363B8C5A755F879F762C2523883E88BAB0F7C3D31B5; AHeadUserInfo=VipGrade=0&VipGradeName=%C6%D5%CD%A8%BB%E1%D4%B1&UserName=&NoReadMessageCount=0; DUID=u=3F4AEEEBF270964AE990F2675434EC60&v=0; IsNonUser=F; IsPersonalizedLogin=T; _bfa=1.1635302467464.3ltfqx.1.1635302467464.1635302467464.1.16; _bfs=1.16'
        ]

    def get_proxy(self):
        while True:
            try:
                # return requests.get('http://1.116.204.248:5000/proxy').text
                return requests.get('http://47.106.223.4:50002/get/').json().get('proxy')
            except:
                print('暂无ip，等待20秒')
                time.sleep(20)

    def get_lb(self, city, cityId, pgsum):
        for pg in range(1, pgsum):
            print(pg)
            while True:
                try:
                    if self.proxies == {}:
                        proxy = self.get_proxy()
                        self.proxies = {"https": proxy}
                    html = requests.get('https://hotels.ctrip.com/hotel/' + city + cityId + '/p' + str(pg),
                                        headers=self.header,
                                        proxies=self.proxies, timeout=5).text
                    # html = requests.get('https://hotels.ctrip.com/hotel/Mile4243/p4', headers=self.header).text
                    tree = etree.HTML(html)
                    if tree.xpath('//div[@class="errorinfo"]/p/text()') == '人在旅途，难免迷路，好在你有携程。':
                        return
                    text = tree.xpath('//script/text()')
                    strs = text[2]
                    str1 = strs.split('\n')[1]
                    str2 = ''.join(re.findall('window.IBU_HOTEL=(.+)', str1))[:-1]
                    str3 = str2.split('{"member":')
                    for st in str3[1:]:
                        false = 'false'
                        true = 'true'
                        str4 = '{' + ''.join(re.findall('\{"list":\[\]\},(.+)"trace"', st)) + '}'
                        dicts = eval(str4)
                        item = {}
                        item["id"] = dicts['base']['hotelId']
                        try:
                            item["综合评分"] = dicts['score']['number']
                        except:
                            item["综合评分"] = ''
                        try:
                            item["评分详情"] = dicts['score']['subScore']
                        except:
                            item["评分详情"] = []
                        item["酒店名称"] = dicts['base']['hotelName']
                        try:
                            item["酒店星级"] = dicts['base']['star']
                        except:
                            item["酒店星级"] = '0'
                        try:
                            item["特点"] = dicts['base']['tags']
                        except:
                            item["特点"] = ''
                        item["lat"] = dicts['position']['lat']
                        item["lng"] = dicts['position']['lng']
                        item["地址"] = dicts['position']['address']
                        item["城市"] = dicts['position']['cityName']
                        try:
                            item["商圈"] = dicts['position']['area']
                        except:
                            item["商圈"] = ''
                        try:
                            item["评论数"] = dicts['comment']['content']
                        except:
                            item["评论数"] = ''
                        if {'酒店名称': item['酒店名称']} in self.bj:
                            continue
                        self.get_xq(item)
                        self.bj.append({'酒店名称': item['酒店名称']})
                    break
                except:
                    self.proxies = {}
                    continue

    def get_xq(self, item):
        data = {"masterHotelId": item['id'], "isBusiness": 'false', "feature": [], "cityCode": 1,
                "head": {"Locale": "zh-CN", "Currency": "CNY", "Device": "PC", "UserIP": "14.106.229.21", "Group": "",
                         "ReferenceID": "", "UserRegion": "CN", "AID": "1315", "SID": "1535", "Ticket": "", "UID": "",
                         "IsQuickBooking": "", "ClientID": "1633749869935.448q8m", "OUID": "", "TimeZone": "8",
                         "P": "86189454181", "PageID": "102003", "Version": "",
                         "HotelExtension": {"WebpSupport": 'true', "group": "CTRIP", "Qid": "26759643159",
                                            "hasAidInUrl": 'false'},
                         "Frontend": {"vid": "1633749869935.448q8m", "sessionID": 9, "pvid": 118}}, "ServerData": ""}
        while True:
            try:
                if self.proxies == {}:
                    proxy = self.get_proxy()
                    self.proxies = {"https": proxy}
                json1 = requests.post('https://m.ctrip.com/restapi/soa2/21881/json/hotelStaticInfo', json=data,
                                      headers=self.header, proxies=self.proxies, timeout=5).json()

                item["酒店简介"] = json1['Response']['hotelInfo']['basic']['description']
                text = '|' + '|'.join(json1['Response']['hotelInfo']['basic']['label']) + '|'
                item["开业时间"] = ''.join(re.findall('开业：(\d+)\|', text))
                item["房间数量"] = ''.join(re.findall('客房数：(\d+)\|', text))
                self.get_monny(item)
                self.get_fj(item)
                break
            except:
                self.proxies = {}
                continue

    def get_fj(self, item):
        data2 = {"masterHotelId": item['id'], "isBusiness": 'false', "feature": [], "cityCode": 1,
                 "head": {"Locale": "zh-CN", "Currency": "CNY", "Device": "PC", "UserIP": "14.106.229.21", "Group": "",
                          "ReferenceID": "", "UserRegion": "CN", "AID": "1315", "SID": "1535", "Ticket": "", "UID": "",
                          "IsQuickBooking": "", "ClientID": "1633749869935.448q8m", "OUID": "", "TimeZone": "8",
                          "P": "86189454181", "PageID": "102003", "Version": "",
                          "HotelExtension": {"WebpSupport": 'true', "group": "CTRIP", "Qid": "466763346518",
                                             "hasAidInUrl": 'false'},
                          "Frontend": {"vid": "1633749869935.448q8m", "sessionID": 7, "pvid": 88}}, "ServerData": ""}
        while True:
            try:
                if self.proxies == {}:
                    proxy = self.get_proxy()
                    self.proxies = {"https": proxy}
                json2 = requests.post('https://m.ctrip.com/restapi/soa2/21881/json/hotelPlaceInfo', json=data2,
                                      headers=self.header, proxies=self.proxies, timeout=5).json()['Response'][
                    'placeInfoList']
                lis = []
                for js in json2:
                    lis += js['list']
                item['附近'] = lis
                self.sj.append(item)
                break
            except:
                self.proxies = {}
                continue

    def get_monny(self, item):
        header2 = {'accept': 'application/json',
                   'accept-encoding': 'gzip, deflate, br',
                   'accept-language': 'zh-CN,zh;q=0.9',
                   'content-length': '551',
                   'content-type': 'application/json;charset=UTF-8',
                   'origin': 'https://hotels.ctrip.com',
                   'p': '86189454181',
                   'referer': 'https://hotels.ctrip.com/',
                   'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                   'sec-ch-ua-mobile': '?0',
                   'sec-ch-ua-platform': "Windows",
                   'sec-fetch-dest': 'empty',
                   'sec-fetch-mode': 'cors',
                   'sec-fetch-site': 'same-site',
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
        for i in range(5):
            json3 = {
                "searchCondition": {"adult": 1, "child": 0, "age": "", "cityName": "", "cityId": 1,
                                    "checkIn": "2021-10-27",
                                    "checkOut": "2021-10-28", "roomNum": 1, "masterHotelId": item['id'],
                                    "priceType": "",
                                    "url": "https://hotels.ctrip.com/hotels/detail/?hotelId=72898766&checkIn=2021-10-27&checkOut=2021-10-28&cityId=1&minprice=&mincurr=&adult=1&children=0&ages=&crn=1&curr=&fgt=&stand=&stdcode=&hpaopts=&mproom=&ouid=&shoppingid=&roomkey=&highprice=-1&lowprice=0&showtotalamt=&hotelUniqueKey="},
                "filterCondition": {"star": [], "rate": 0, "priceRange": {"highPrice": -1, "lowPrice": 0}},
                "masterHotelId": item['id'], "hotelStar": 4, "hotelName": item['酒店名称'],
                "coord": {"lng": "116.41674763863993", "lat": "40.054539606924386", "type": "bd"}, "isNewMap": "1",
                "head": {"Locale": "zh-CN", "Currency": "CNY", "Device": "PC", "UserIP": "14.106.229.21", "Group": "",
                         "ReferenceID": "", "UserRegion": "CN", "AID": "1315", "SID": "1535", "Ticket": "", "UID": "",
                         "IsQuickBooking": "", "ClientID": "1633749869935.448q8m", "OUID": "", "TimeZone": "8",
                         "P": "86189454181", "PageID": "102003", "Version": "",
                         "HotelExtension": {"WebpSupport": 'true', "group": "CTRIP", "Qid": "26759643159",
                                            "hasAidInUrl": 'false'},
                         "Frontend": {"vid": "1633749869935.448q8m", "sessionID": 9, "pvid": 118}}, "ServerData": ""}
            while True:
                try:
                    if self.proxies == {}:
                        proxy = self.get_proxy()
                        self.proxies = {"https": proxy}
                    fj = requests.post('https://m.ctrip.com/restapi/soa2/21881/json/hotelSearchNearby', headers=header2,
                                       json=json3, proxies=self.proxies, timeout=5).json()
                    break
                except:
                    continue
            bj = True
            for dic in fj['Response']['list']:
                dicts = {}
                try:
                    dicts['起步价'] = int(dic['money']['price'])
                except:
                    bj = False
                    header2['cookie'] = random.choice(self.cookie_List)
                    break
                # dicts['起步价'] = dic['money']['price']
                dicts['id'] = dic['base']['hotelId']
                if dicts in self.monny_list:
                    continue
                self.monny_list.append(dicts)
            if bj:
                return

    def run(self):
        for dic in self.city_map_list:
            start = time.time()
            city = dic['data'].split('|')[0]
            cityId = dic['data'].split('|')[-1]
            # if url_data.count_documents({city: '已爬取'}):
            #     print('当前城市已爬取:', dic['display'])
            #     continue
            # elif url_data.count_documents({city: '正在爬取'}):
            #     print('当前城市正在爬取:', dic['display'])
            #     continue
            # url_data.insert_one({city: '正在爬取'})

            html = requests.get('https://hotels.ctrip.com/hotel/' + city + cityId + '/p1',
                                headers=self.header,
                                proxies=self.proxies, timeout=5).text
            # html = requests.get('https://hotels.ctrip.com/hotel/Mile4243/p4', headers=self.header).text
            tree = etree.HTML(html)
            strs = ''.join(tree.xpath('//div[@class="filter-title clearfix"]/div/text()'))
            sums = ''.join(re.findall('(\d+?)', strs))
            sum2 = int(sums)
            if sum2 % 15 == 0:
                pgsum = sum2 // 15 + 1
            else:
                pgsum = sum2 // 15 + 2

            self.get_lb(city, cityId, pgsum)
            df = pd.DataFrame(self.monny_list)
            for ind in range(len(self.sj)):
                if url_data.count_documents({'id': self.sj[ind]['id']}):
                    continue
                df_ = df[df['id'] == self.sj[ind]['id']]
                try:
                    self.sj[ind]['起步价'] = df_['起步价'].values[0]
                except:
                    self.sj[ind]['起步价'] = ''
                info_base.find_one(self.sj[ind])
                url_data.insert_one({'id': self.sj[ind]['id']})
            url_data.insert_one({city: '已爬取'})
            print(time.time() - start)


if __name__ == '__main__':
    obj = GET()
    obj.run()
