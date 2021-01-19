import re
import json

import csv
import requests


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Cookie": "x-zp-client-id=9422af0b-9a10-4f67-808c-0a549789dda0; sts_deviceid=16b64aba0cafd-0f5aec4c821e6f-492c7413-2073600-16b64aba0cbfd1; NTKF_T2D_CLIENTID=guestE59CD8BA-C249-CB37-6299-64AC2B6ECC18; adfbid2=0; select_city_code=2313; select_city_name=%E6%B1%9F%E5%8C%97%E5%8C%BA; sou_experiment=unexperiment; acw_tc=2760822a15681655109966628ed6cf3d714e455e192a6c3fc8464921e3ab8a; adfbid=0; sts_sg=1; sts_sid=16d1df357deaa0-06aaf7c05fae9d-34564b7f-2073600-16d1df357e0842; sts_chnlsid=121122523; zp_src_url=https%3A%2F%2Fwww.baidu.com%2Fbaidu.php%3Fsc.0s0000a7HcV7X_Q0LzYkLoFjLSeb5flgVJmVz9gnC5BYpDkLFOAtAVqA4HfQPeXFmz542ypUfyJ_HvhUZ1f4rJHyIXwK3kFtS2XnkBrBxv_nDVv7b28RyqPM4fxoPcaFAE2QDxhQcOj7UvRa_VpRXnCTaPvAIoZSxBPLrYS1ZIA8xf6bl1NjqN30hWBWL8Tkp2vqVYSnuvjB9HpjY6.7b_NR2Ar5Od669BCXgjRzeASFDZtwhUVHf632MRRt_Q_DNKnLeMX5DkgboozuPvHWdWxfik6zXrekLur5-veqhOWbtXrl1W3SHrHIblIdMubLeqO-WEl3FJQ7Na9WWOqmc2QnN1tL-sdn8kEBwKnMRSr6hUE6CpXyPvap7Q7erQKSU3X8a9G4I2UM3PQZsOhSZo6CpXy6hUikgY4PhOklX1o6CpXy7YNKnNKBAovIT7jHzs_lTUQqRHA5A_HAOuuguu_LtVvGmuCyrr1x__R.U1Yk0ZDqd_xKJ6Kspynqn0KY5TXsd_xKJVgfko60pyYqnW0Y0ATqUvNsT100Iybqmh7GuZN_UfKspyfqn1n0mv-b5Hf1PfKVIjYknjDLg1DsnH-xnH0YP-t1PW0k0AVG5H00TMfqnHc30ANGujYkPjczg1cknHcsg1c4PHczg1c4PHcsg1c4PHmLg1c4nWck0AFG5HDdPNtkPH9xnW0Y0AdW5HD3n1nknWfknjIxnH0snNtknjFxn0KkTA-b5H00TyPGujYs0ZFMIA7M5H00mycqn7ts0ANzu1Ys0ZKs5HckrHm4njcLrfK8IM0qna3snj0snj0sn0KVIZ0qn0KbuAqs5H00ThCqn0KbugmqTAn0uMfqn0KspjYs0Aq15H00mMTqn6K8IjYs0ZPl5fK9TdqGuAnqTZnVuLGCXZb0pywW5R9rffKYIgnqrjT4nj63PWnzPj6dPHnznj6vPsKzug7Y5HDdPW6kPWRdPjfYnWm0Tv-b5H6Lnyn4PhmLnj0zrjFBujR0mLPV5RPAPDn4rDfknHujP10YnDD0mynqnfKsUWYs0Z7VIjYs0Z7VT1Ys0ZGY5HD0UyPxuMFEUHYsg1Kxn7ts0Aw9UMNBuNqsUA78pyw15HKxn7tkPjmkPjbzg100TA7Ygvu_myTqn0Kbmv-b5H00ugwGujYVnfK9TLKWm1Ys0ZNspy4Wm1Ys0Z7VuWYs0AuWIgfqn0KlTAkdT1Ys0A7buhk9u1Yk0Akhm1Ys0AqW5HD0ULfqn0KETMKY5H0WnanWnansc10Wna3snj0snj0WnanWn0KWThnqPjTvPWm%26word%3D%25E6%2599%25BA%25E8%2581%2594%26ck%3D7403.1.73.247.456.247.454.71%26shh%3Dwww.baidu.com%26sht%3D98010089_dg%26us%3D1.0.1.0.1.428.0%26bc%3D110101; urlfrom=121114583; urlfrom2=121114583; adfcid=www.baidu.com; adfcid2=www.baidu.com; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22720402719%22%2C%22%24device_id%22%3A%2216b64ab9f351204-091aa4de9da7b38-492c7413-2073600-16b64ab9f37738%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_utm_source%22%3A%22baiduPC%22%2C%22%24latest_utm_medium%22%3A%22CPC%22%2C%22%24latest_utm_campaign%22%3A%22pp%22%2C%22%24latest_utm_content%22%3A%22chq%22%2C%22%24latest_utm_term%22%3A%2216289764%22%7D%2C%22first_id%22%3A%2216b64ab9f351204-091aa4de9da7b38-492c7413-2073600-16b64ab9f37738%22%7D; dywea=95841923.735183733695984800.1560762098.1566802085.1568165554.14; dywec=95841923; dywez=95841923.1568165554.14.5.dywecsr=baidu|dyweccn=(organic)|dywecmd=organic; dyweb=95841923.1.10.1568165554; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1568165554; __utma=269921210.1854267189.1560762098.1566802085.1568165554.14; __utmc=269921210; __utmz=269921210.1568165554.14.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; __utmb=269921210.1.10.1568165554; jobRiskWarning=true; ZP_OLD_FLAG=false; POSSPORTLOGIN=7; CANCELALL=0; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1568165793; LastCity=%E5%B9%BF%E4%B8%9C; LastCity%5Fid=548; sts_evtseq=9; ZL_REPORT_GLOBAL={%22sou%22:{%22actionid%22:%22380e2b2e-1d3f-42fd-b05e-cabcdb985311-sou%22%2C%22funczone%22:%22smart_matching%22}}"
}


def get_script_data(url):
    proxy = requests.get("http://127.0.0.1:5010/get/").text
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    }
    s = requests.Session()
    r = s.get(url, headers=headers, timeout=10)
    # print(r.text)
    if 'arg1=' not in r.text:
        return r.text
    arg1 = re.search("arg1='([^']+)'", r.text).group(1)
    s.cookies['acw_sc__v2'] = zhilian_cookie_factory(arg1)
    cookie = '解密cookie: ' + zhilian_cookie_factory(arg1)
    # print(cookie)
    r = s.get(url, headers=headers, timeout=10)
    print(r.text[1:50])
    return r.text


def zhilian_cookie_factory(arg1):
    key_array = [15, 35, 29, 24, 33, 16, 1, 38, 10, 9, 19, 31, 40, 27, 22, 23, 25, 13, 6, 11, 39, 18, 20, 8, 14, 21, 32, 26, 2, 30, 7, 4, 17, 5, 3, 28, 34, 37, 12, 36]
    data = "3000176000856006061501533003690027800375"

    step1 = []
    for i in range(len(arg1)):
        for ii in range(len(key_array)):
            if key_array[ii] == i + 1:
                step1.append(ii)

    cache = ""
    for i in range(len(step1)):
        ii = step1.index(i)
        cache += arg1[ii]

    iii = 0
    cookie = ""
    while iii < len(cache) and iii < len(data):
        a = int(cache[iii:iii + 2], 16)
        b = int(data[iii:iii + 2], 16)
        c = hex(a ^ b)[2:]
        if len(c) == 1:
            c = '0' + c
        cookie += c
        iii += 2
    return cookie


def get_result(url):
    params = {
        "url": url
    }
    r = requests.get('http://121.40.96.182:4006/getResult', params=params)
    print("1231: ", r.text)
    print()
    return r.json()



r = get_result("https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId={1}&industry=400000000&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={0}&kt=3&=0&_v=0.94479675&x-zp-page-request-id=4d6d5b1d9a004d3a95566d2ffd301f12-1568165851934-256779&x-zp-client-id=9422af0b-9a10-4f67-808c-0a549789dda0".format('商务经理', 554))

#
# s = requests.Session()
#
# for u in ['云南', '贵州', '湖北', '河南', '西藏', '四川', '重庆', '山西', '陕西', '海口', '广东']:
#     if u == '云南':
#         code = 554
#     if u == '贵州':
#         code = 553
#     if u == '湖北':
#         code = 546
#     if u == '河南':
#         code = 545
#     if u == '西藏':
#         code = 555
#     if u == '四川':
#         code = 552
#     if u == '新疆':
#         code = 560
#     if u == '重庆':
#         code = 551
#     if u == '山西':
#         code = 533
#     if u == '陕西':
#         code = 556
#     if u == '海口':
#         code = 550
#     if u == '广东':
#         code = 548
#     for p in ['商务经理', '总工', '给排水工程师', '暖通工程师', '电气工程师', '一级结构师', '岩土工程师', '消防工程师', '市政工程师', '监理员', '建筑师', '建筑设计师', '工程部经理', '工程部副经理', '生产经理', '造价师', '造价工程师', '建造师']:
#         try:
#             count = 0
#             title1 = 0
#             for q in range(3):
#                 if q == 0:
#                     print(p, code)
#                     try:
#                         r = get_result("https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId={1}&industry=400000000&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={0}&kt=3&=0&_v=0.94479675&x-zp-page-request-id=4d6d5b1d9a004d3a95566d2ffd301f12-1568165851934-256779&x-zp-client-id=9422af0b-9a10-4f67-808c-0a549789dda0".format(p, code))
#                         print(r)
#                     except:
#                         r = get_result("https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId={1}&industry=400000000&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={0}&kt=3&=0&_v=0.94479675&x-zp-page-request-id=4d6d5b1d9a004d3a95566d2ffd301f12-1568165851934-256779&x-zp-client-id=9422af0b-9a10-4f67-808c-0a549789dda0".format(p, code))
#                         print(r)
#                 elif q == 1:
#                     try:
#                         r = get_result("https://fe-api.zhaopin.com/c/i/sou?pageSize=180&cityId={1}&industry=400000000&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={0}&kt=3&=0&_v=0.94479675&x-zp-page-request-id=4d6d5b1d9a004d3a95566d2ffd301f12-1568165851934-256779&x-zp-client-id=9422af0b-9a10-4f67-808c-0a549789dda0".format(p, code))
#                     except:
#                         r = get_result("https://fe-api.zhaopin.com/c/i/sou?pageSize=180&cityId={1}&industry=400000000&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={0}&kt=3&=0&_v=0.94479675&x-zp-page-request-id=4d6d5b1d9a004d3a95566d2ffd301f12-1568165851934-256779&x-zp-client-id=9422af0b-9a10-4f67-808c-0a549789dda0".format(p, code))
#                 else:
#                     try:
#                         r = get_result("https://fe-api.zhaopin.com/c/i/sou?pageSize=270&cityId={1}&industry=400000000&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={0}&kt=3&=0&_v=0.94479675&x-zp-page-request-id=4d6d5b1d9a004d3a95566d2ffd301f12-1568165851934-256779&x-zp-client-id=9422af0b-9a10-4f67-808c-0a549789dda0".format(p, code))
#                     except:
#                         r = get_result("https://fe-api.zhaopin.com/c/i/sou?pageSize=270&cityId={1}&industry=400000000&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={0}&kt=3&=0&_v=0.94479675&x-zp-page-request-id=4d6d5b1d9a004d3a95566d2ffd301f12-1568165851934-256779&x-zp-client-id=9422af0b-9a10-4f67-808c-0a549789dda0".format(p, code))
#                 print(type(r))
#                 data = r
#                 print("data: ",data)
#                 print(type(data))
#                 lists = data.get("data")
#                 print(lists)
#                 urls = []
#                 for i in lists:
#                     print(i.get("positionURL"))
#                     urls.append(i.get("positionURL"))
#
#
#                 for y in urls:
#                     print(y)
#                     try:
#                         try:
#                             html = get_script_data(y)
#                         except:
#                             pass
#                         print("html[1:10]: ", html[1:10])
#                         data = re.findall("_INITIAL_STATE__=(.*?)</script>", html)[0]
#                         print(data)
#                         data1 = json.loads(data).get("jobInfo").get("jobDetail")
#                         with open('./zhilian/智联_{1}__{0}.csv'.format(p, u), 'a', encoding='utf-8-sig', newline='') as csvfile:
#                             spamwriter = csv.writer(csvfile, dialect=('excel'))
#                             # 设置标题
#                             if title1 == 0:
#                                 spamwriter.writerow(
#                                     ["公司名称", "岗位名称", "岗位职责", "任职资格", "公司性质", "公司人数", "工作地点", "工资待遇", "公司简介"])
#                                 title1 = 1
#                             companyName = data1.get("detailedCompany").get("companyName")
#                             jobName = data1.get("detailedPosition").get("name")
#                             jobDuty = data1.get("detailedPosition").get("jobDesc")
#                             jobQualify = "工作经验：" + data1.get("detailedPosition").get("workingExp") + "|" + "学历：" + data1.get("detailedPosition").get("education") + "|" + "招{0}人".format(str(data1.get("detailedPosition").get("jobStatus")))
#                             companyQuality = data1.get("detailedCompany").get("industry")
#                             companySize = data1.get("detailedCompany").get("companySize")
#                             companyAddress = data1.get("detailedPosition").get("workAddress")
#                             salary = data1.get("detailedPosition").get("salary60")
#                             conmpanyDescription = data1.get("detailedCompany").get("companyDescription")
#                             spamwriter.writerow(
#                                 [companyName, jobName, jobDuty, jobQualify, companyQuality, companySize, companyAddress, salary, conmpanyDescription])
#                             count += 1
#                         if count >= 200:
#                             break
#                     except:
#                         continue
#                 if count >= 200:
#                     break
#         except:
#             continue
