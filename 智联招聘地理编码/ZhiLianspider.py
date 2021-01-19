# -*- coding: UTF-8 -*-
import datetime
import json

import requests
from lxml import etree
import re
import csv
import random
import threading
import time
from threading import Thread, Lock
from queue import Queue
import pandas
import os

# 这个修改后的
from check import read_file_path
from ip_pool import getHtml

os.chdir("D:\Project\智联招聘地理编码")
#
# headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
#          'Host':'jobs.zhaopin.com',
#          'Accept-Language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
#          'Cache-Control': 'max-age=0',
#          'Connection': 'keep-alive',
#          'Upgrade-Insecure-Requests': '1',
#          'Cookie':'acw_tc=2760822615638911885182574ed1c093d538baf413e32752b5199bff9adda8; __jsluid_s=ce454fbbfc31753cd0710cc956f961c7; x-zp-client-id=5b7ba0ca-b326-444b-9516-18a7cd6c8da1; sts_deviceid=16c1f2dc65749a-0b2264ab9ec70f-e353165-2073600-16c1f2dc65848c; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216c1f2dc6bb170-00f4fa9ec85df2-e353165-2073600-16c1f2dc6bc8d4%22%2C%22%24device_id%22%3A%2216c1f2dc6bb170-00f4fa9ec85df2-e353165-2073600-16c1f2dc6bc8d4%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; locationAuthorization=true; _uab_collina=156390293455501592099672; __jsluid_h=ad1ab0f3189e9980a85f5f365e84e386; acw_sc__=5d375d891eb0eaa84dfe9302c9cb4b3f2924646a; sts_sg=1; sts_sid=16c20580f4e860-01d455d68597bc-e353165-2073600-16c20580f4f9a8; sts_chnlsid=Unknown; jobRiskWarning=true; sts_evtseq=2; ZL_REPORT_GLOBAL={%22jobs%22:{%22recommandActionidShare%22:%22803754d6-1b53-4315-9ac2-0552e85465c2-job%22%2C%22funczoneShare%22:%22dtl_best_for_you%22}}'
#
#          }

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Host': 'jobs.zhaopin.com',
    'Accept-Language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    # 'cookie':'
    # acw_tc=2760822615638911885182574ed1c093d538baf413e32752b5199bff9adda8; __jsluid_s=ce454fbbfc31753cd0710cc956f961c7; x-zp-client-id=5b7ba0ca-b326-444b-9516-18a7cd6c8da1; sts_deviceid=16c1f2dc65749a-0b2264ab9ec70f-e353165-2073600-16c1f2dc65848c; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216c1f2dc6bb170-00f4fa9ec85df2-e353165-2073600-16c1f2dc6bc8d4%22%2C%22%24device_id%22%3A%2216c1f2dc6bb170-00f4fa9ec85df2-e353165-2073600-16c1f2dc6bc8d4%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; locationAuthorization=true; _uab_collina=156390293455501592099672; __jsluid_h=ad1ab0f3189e9980a85f5f365e84e386; acw_sc__=5d375d891eb0eaa84dfe9302c9cb4b3f2924646a; sts_sg=1; sts_sid=16c20580f4e860-01d455d68597bc-e353165-2073600-16c20580f4f9a8; sts_chnlsid=Unknown; jobRiskWarning=true; sts_evtseq=2; ZL_REPORT_GLOBAL={%22jobs%22:{%22recommandActionidShare%22:%22803754d6-1b53-4315-9ac2-0552e85465c2-job%22%2C%22funczoneShare%22:%22dtl_best_for_you%22}}'
    'cookie': 'bdshare_firstime=1581744761188; Hm_lvt_80e552e101e24fe607597e5f45c8d2a2=1581775812; acw_tc=2760820215845117636813470ef9ddb4c6988a1c7be14585879164902bd3dd; _qzja=1.111738821.1581744761234.1584511774564.1585646904758.1585646904758.1585647048806.0.0.0.8.6; sts_deviceid=17159400b3be4-00d7447265408d-6701b35-1327104-17159400b3c421; x-zp-client-id=bd2cb160-dc08-456f-8d98-4c8134b29c80; urlfrom2=121113803; adfbid2=0; LastCity%5Fid=531; LastCity=%E5%A4%A9%E6%B4%A5; ZP_OLD_FLAG=false; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1584511774,1585646905,1585734428,1586397813; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217159400be73f3-01a0f39c53812f-6701b35-1327104-17159400be880f%22%2C%22%24device_id%22%3A%2217159400be73f3-01a0f39c53812f-6701b35-1327104-17159400be880f%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22baidupcpz%22%2C%22%24latest_utm_medium%22%3A%22cpt%22%2C%22%24latest_utm_campaign%22%3A%22pc-biaoge2-1%22%2C%22%24latest_utm_content%22%3A%22pcpz%22%7D%7D; __utma=269921210.719407599.1586530374.1586530374.1586530374.1; __utmz=269921210.1586530374.1.1.utmcsr=jobs.zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct=/404.htm; dywea=95841923.283633627141548400.1586530375.1586530375.1586530375.1; dywez=95841923.1586530375.1.1.dywecsr=jobs.zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/404.htm; _uab_collina=158653043993032159777643; acw_sc__=5e92f30ce282b7741551a6f7a0715325026199c6; sts_sg=1; sts_sid=1716e056d7ae09-0b46757f709ad5-6701b35-1327104-1716e056d7bd63; sts_chnlsid=Unknown; zp_src_url=http%3A%2F%2Fjobs.zhaopin.com%2FCC120069275J00235315308.htm; jobRiskWarning=true; ZL_REPORT_GLOBAL={%22jobs%22:{%22recommandActionidShare%22:%229ea4e7bc-b2e3-41a6-9c9e-fb21a235f6ff-job%22}}; sts_evtseq=11',
    }


# 创建UA池
def get_ua():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
        'Opera/8.0 (Windows NT 5.1; U; en)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) '
    ]
    user_agent = random.choice(user_agents)  # random.choice(),从列表中随机抽取一个对象
    return user_agent


def openPage(save_path, numlist, citylist):
    """
    :param list:
    :param save_path: 19-07-25_肇庆.csv   保存的路径
    :param numlist:   ['sdf','']        唯一标识
    :param citylist:    ['','']         城市列表
    :return:
    """
    while True:
        if queue.empty() == True:
            break
        url = queue.get()  # 链接  https://jobs.zhaopin.com/176383228250289.htm
        numA = queue2.get()  # 当前中序号   0

        flag = 1
        numb = 0
        while True:
            try:
                if 'xiaoyuan' in url or 'http' not in url:
                    flag = 0
                    break
                headers['User-Agent'] = get_ua()
                response, proxy = getHtml(url=url, headers=headers)  # 使用免费代理获取网页信息

                tree = etree.HTML(response.text, parser=etree.HTMLParser(encoding='utf-8'))

                if 'arg1=' in response.text:
                    print("在判断中,", url, proxy)
                    flag = 0
                    break

                # print(tree.xpath("//title/text()")[0], response.status_code)
                if "404" in tree.xpath("//title/text()")[0]:
                    print('没有找到页面, 404')
                    flag = 0
                    break

                elif response.status_code == 200:  # 如果找不到就会出错
                    a = tree.xpath('//a[@class="navigation__channel-item-name"]/span/span')[0].text
                    if a == '首页':
                        print('首页, 有数据, ', url, "当前ip: ", proxy)
                        break
                    else:  # 出现第一次验证的情况,重新请求
                        numb += 1
                        if numb > 3:
                            break
                        continue
                elif tree.xpath("//div[@class='content']/div[@class='right']/p/text()"):
                    print("出现验证码, 重新请求")
                    continue

                # 返回状态码不为200,或者404的时候,更换ip 跳出
                else:
                    print('状态码ip ==> : ', response.status_code, response.url, response.text)
                    break

            except:  # 当网页链接超时的时候,或者出错, 丢掉 url
                pass

        # 404 页面 网页链接失效
        if flag == 0:
            num = '招0人'  # 招聘人数
            latitude = ''  # 纬度
            longitude = ''  # 经度
            location = ''  # 地址
            companyAddress = ''
            jobQualify = ''
            jobDuty = ''
            skillLabel = ''
            welfareLabel = ''
            companyQuality = ''
            industryLevel = ''

        else:
            """
            # 有数据的时候进行 解析网页
            descriptionTemp = []
            description = tree.xpath('//div[@class="describtion__detail-content"]//text()')
            for i in range(len(description)):
                description[i] = ''.join(description[i].split())
                descriptionTemp.append(description[i])


            # 招聘人数
            try:
                num = tree.xpath('//ul[@class="summary-plane__info"]/li[4]')[0].text
                if not num:
                    num = tree.xpath()
                #
            except:
                num = ''


            # 找不到locat在找地点
            try:
                latitude = re.search('latitude":"(\S+)","longitude', response.text).group(1)
                longitude = re.search('longitude":"(\S+)","publishTime', response.text).group(1)
                if not latitude or not longitude:
                    latitude = re.search("JobAddress = \['(\d+\.?\d+)', '(\d+\.?\d+)'", response.text).group(1)
                    longitude = re.search("JobAddress = \['(\d+\.?\d+)', '(\d+\.?\d+)'", response.text).group(2)
            except:
                latitude = ''
                longitude = ''
            # 地址
            try:

                location = tree.xpath('//span[@class="job-address__content-text"]//text()')[0]
                if not longitude:
                    longitude  = re.search('workAddress":"(\S+)","latitude', response.text).group(1) or  tree.xpath("*//p[@class='add-txt']/text()")[0]

            except:
                location = ''
            """
            data = re.findall("_INITIAL_STATE__=(.*?)</script>", response.text)[0]

            data1 = json.loads(data).get("jobInfo").get("jobDetail")
            # 工作描述
            jobDuty = data1.get("detailedPosition").get("jobDesc")
            # 招聘人数
            jobQualify = "招{0}人".format(
                str(data1.get("detailedPosition").get("recruitNumber", '0')))
            # 企业分类
            companyQuality = data1.get("detailedCompany").get("industry")
            # 企业分类 层级
            industryLevel = data1.get("detailedCompany").get("industry")
            # 企业规模
            companySize = data1.get("detailedCompany").get("companySize")
            # 工作地址
            companyAddress = data1.get("detailedPosition").get("workAddress")
            # 经纬度
            longitude = data1.get("detailedPosition").get("longitude")
            latitude = data1.get("detailedPosition").get("latitude")
            # 职位两点
            welfareLabel = [i['value'] for i in data1.get("detailedPosition").get("welfareLabel")]
            # 职位技能
            skillLabel = [i['value'] for i in data1.get("detailedPosition").get("skillLabel")]

            conmpanyDescription = data1.get("detailedCompany").get("companyDescription")

        # 保存数据
        savePath = os.path.join('data', save_path)
        # 判断是否存在当前文件夹
        if not os.path.exists(savePath):  # 不存在
            with open(savePath, 'a', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                lock = Lock()
                lock.acquire()
                writer.writerow(
                    ['城市', 'number', '地址', '招聘人数', 'longitude', 'latitude', 'url', '岗位描述', '职位技能', '职位亮点', '企业分类',
                     '分类层级'])
                city = citylist[numA]
                number = numlist[numA]
                writer.writerow(
                    [city, number, companyAddress, jobQualify, longitude, latitude, url, jobDuty, skillLabel,
                     welfareLabel, companyQuality, industryLevel])
                lock.release()
        else:
            print("保存数据, 招聘人数: ", jobQualify, )
            with open(savePath, 'a', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                lock = Lock()
                lock.acquire()
                writer.writerow(
                    [citylist[numA], numlist[numA], companyAddress, jobQualify, longitude, latitude, url, jobDuty,
                     skillLabel, welfareLabel, companyQuality, industryLevel])
                lock.release()
        print()
        queue.task_done()  # 不能走出第一个循环


def run():
    with open("geocity.txt", 'r', encoding='utf-8') as fp:
        exists_city = [ci.split("\\")[1].replace(".csv", "_智联.xlsx").rstrip() for ci in fp.readlines()]

    yuan_path = "JobData"
    city_list = [i for i in os.listdir(yuan_path) if 'xlsx' in os.path.splitext(i)[1]]
    for cityFileName in city_list:
        print(cityFileName)
        if cityFileName in exists_city:
            print("已经抓取过: ", cityFileName)
            continue

        # if cityFileName.split('_')[1] not  in  ['东莞', '深圳', '汕头','汕尾', '惠州']:
        #     continue

        if "成都" in cityFileName:
            print('跳过成都')
            continue
        save_path = "_".join(cityFileName.split('_')[0:2]) + ".csv"
        savePath = os.path.join('data', save_path)
        yuanPath = os.path.join(yuan_path, cityFileName)
        # print("当前城市: ",save_path, yuanPath,savePath)
        df = read_file_path(yuanPath, savePath)
        df.index = [i for i in range(df.shape[0])]

        print(df.shape, df.head(3))
        urllist = []
        numlist = []
        citylist = []
        url_list = df[['positionURL']]
        num_list = df[['number']]
        city_list = df[['city']]
        print(url_list['positionURL'], url_list.shape)
        for i in range(len(url_list)):
            urllist.append(url_list['positionURL'][i])  # url列表
            numlist.append(num_list['number'][i])  # 唯一标识列表
            citylist.append(city_list['city'][i])  # 城市列表

        for i in range(len(citylist)):
            queue2.put(int(i))  # 将城市列表的序号添加到队列中
        for url in urllist:
            queue.put(url)  # 将url 添加到 队列中
        # max = queue.qsize()       # 最大长度
        # tasklist|findstr "12528"
        # 开启多线程
        for i in range(2):
            time.sleep(0.5)
            t = Thread(target=openPage, args=(save_path, numlist, citylist,))
            t.daemon = True  # 设置线程daemon  主线程退出，daemon线程也会推出，即时正在运行
            t.start()
        time.sleep(3)
        queue.join()
        print("当前城市 编码完毕")
        with open('geocity.txt', 'a', encoding='utf-8') as fp:
            fp.write(savePath)
            fp.write('\n')


if __name__ == '__main__':
    queue = Queue()
    queue2 = Queue()

    run()
