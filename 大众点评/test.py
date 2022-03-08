import time

# print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


import requests
# d={"pageEnName":"shopList","moduleInfoList":[{"moduleName":"mapiSearch","query":{"search":{"start":20,"categoryId":"10","parentCategoryId":10,"locateCityid":0,"limit":20,"sortId":"0","cityId":9,"range":"-1","maptype":0,"keyword":""}}}],"_token":"eJylVVmu5CAMvBJ4heNAgPsfYcomPer+G2mkl84Dr1VeYmJqZGwFz7Bu/3de/6BfqOP9OT8m3lhT0sxYuHJh98HqhTdOyoybgt/Nkwp3uFOavml7p0KHzCs1FiJofOyVnC3tByyfjz00a2jRILfjE/oKvbThxos2VTN3JtwrH+34b7FrkUobN1U3tfBNHafNTZseFqBwSBZzRoMl/D3EPOFbqOvE47z10Ml4Dp3G58aTh0bEV7Lh7gXZC2I7LTt4ij0Oj8RUgi8ahhRt+mMG/FV7MtrgC8QEPmQiALFhuWxbJfgThPGFCMerkZpUGeCuSHgHFzavvTiIjHo063TgpRKwakTu3hBVX3/Tls+wJdMmYaE2bn3Ik98FT3k2vnyDTQE/xkCB18G7mIO9qPICH0BkUQ+4YLPNHUyhJ8C3Q662wQnwXf8+tQOdIZdHKrqJwcGQAQ5r9BIRJb+g2iHryHoJSzxdOWu4Enu1Lnw5ciQALwv+FZiqIBGJdhJ66BHoekFtKngBhRZ/AzbRn4p6H6AjUMimXvnIxIkdZq46GCwGx1Ig7lzQ2Cf6ErUXiTALGT9AGpgPTSAGn4BHgR/xYZv9EpYPOKi0fANI9L5EL6Hy9qk/ddpIvmS/IfcB2OjMiYiTsnvxbNxQaiz6yJmz4vi98vIjD40r95RjNlJOr3zF3KR8v3L5kW/gGykvr7z+yHM6vvLDRIIPjsbMucKEAXeLDoCnzA+34etAb8WMxEbAvcQERvdA2tiThXInPPMMaU5sxpeYUvjDRkmOauyEy3juoJLxeuaAjZL4HLEWdCm3R2yeRrmrIt6tAHqawxd58lL4Ey87mMMnvfVIzuD1xkPZYdkily+8gSc2WcSPmP0vXs5NNuExhrhd/Ik3+AlZBccXT/gIfwL/AzaW2/PmO1J2t1uB7cBd7MKof4HFeOMFHwVRGqQO++Ar+N14LGccWzHivRWIeE9uxPFOSeDv3L/8VZxb9lPJjRzxe27K228fvi3ziz6NXo6OQq9kfqEV9a1ZFeCm6J+S1ebskdjL9as+A97q341+sl4MueVXJ/gq777m7J3Ak/EpLMEAfKT+G/9+QY5GDfHFUMqzar0b/Z69/J7t64w4+PblPOQXgLZMfH3a238tuYuNOzLfqG/Xoy034tHp6w8+gcz5"}
# print(len(str(d)))
h = {

        'Host': 'm.dianping.com',
        'Connection': 'keep-alive',
        # 'Content-Length': '1929',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Mobile Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://m.dianping.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://m.dianping.com/shop/k6sCyr1j8sKjRPVu',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': '_lxsdk_cuid=179c01ab88cc8-0df2f0b9256ac1-2363163-1fa400-179c01ab88cc8; _hc.v=fb783b09-adc2-78df-f8a5-7b53f530416c.1622425648; s_ViewType=10; _dp.ac.v=19b24d59-781c-4e11-94fc-d848cfb75d8f; ctu=21fd3f032ee980c9b98bee37cc18e7671d5ddb8684865c57d85b840ce1fe7fff; aburl=1; cityid=9; Hm_lvt_233c7ef5b9b2d3d59090b5fc510a19ce=1622431578; ua=dpuser_1966568564; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1622711914; uuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; iuuid=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _lxsdk=61EFD7F9B5A8F9520AB0717DB4E451D6F4137EF2E367795739F0EC2028B713CD; _ga=GA1.2.1975686433.1622713531; fspop=test; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; cy=2; cye=beijing; logan_custom_report=; msource=default; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1623807276,1623807383,1623893307,1623915079; Hm_lvt_220e3bf81326a8b21addc0f9c967d48d=1623910751,1623913137,1623915440,1623916278; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1623916289; default_ab=shop%3AA%3A11%7CshopList%3AA%3A5%7Cmap%3AA%3A1; logan_session_token=ribyiqootr56pullb3h0; Hm_lpvt_220e3bf81326a8b21addc0f9c967d48d=1623916992; _lxsdk_s=17a1876fa2f-d0c-cf1-f00%7C%7C1992',
    }
url='https://m.dianping.com/shop/H6NR1LTJ37z9ocXT?from=shoplist&shoplistqueryid=0df0ccda-548f-4120-9f6a-aef8433c7d83'

# r=requests.get(url,headers=h)
# r.encoding='utf8'
# print(r.text)

import sys
import time

if __name__ == "__main__":
    url='http://api.wandoudl.com/api/ip?app_key=d6383c46ea061db3f35a5d8e1a451d67&pack=222801&num=1&xy=1&type=2&lb=\t&mr=2&area_id=undefined'
    # r=requests.get(url)
    # print('%s:%s'%(r.json()['data'][0]['ip'],r.json()['data'][0]['port']))
    import redis
    # pool = redis.StrictRedis(host='192.168.1.130', port=6379, db=0,password='0',decode_responses=True)
    # x=pool.hkeys('use_proxy')
    # for i in x:
    #     print(i)
    # from lxml import etree
    # import re
    #
    # head = {
    #     'Connection': 'keep-alive',
    #     'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Mobile Safari/537.36'
    # }
    # url='https://www.zdaye.com/dayProxy.html'
    # r=requests.get(url,headers=head)
    # r.encoding='utf8'
    # html=etree.HTML(r.text)
    # nurl='https://www.zdaye.com/' +(html.xpath('//*[@id="J_posts_list"]/div[2]/div/h3/a/@href')[0])
    # uid=re.findall('(\d+)',nurl.split('/')[-1])[0]
    # print(uid)
    # rr=requests.get(nurl,headers=head)
    # r.encoding = 'utf-8'
    # text=rr.content.decode('utf-8').replace('\n','').replace(' ','')
    # data=re.findall("本次发布共<fontcolor='orange'><b>(\d+)</b></font>个代理IP，每页(\d+)个",text)[0]
    # d0=int(data[1])
    # d1=int(data[0])
    # if d1%d0 == 0:
    #     page=int(d1/d0)
    # else:
    #     page = int(d1 / d0) + 1
    # print(page)
    # for i in range(1,page+1):
    #     url=f'https://www.zdaye.com/dayProxy/ip/{uid}/{i}.html'
    #     res=requests.get(url,headers=head)
    #
    #     text = rr.content.decode('utf-8').replace('\n', '').replace(' ', '').replace('\r\t\t','').replace('\r\t','')
    #     data=re.findall("<tbody>(.*?)</tbody>",text)[0]
    #     trs=data.split('<tr>')[1:]
    #     for tr in trs:
    #         host=re.findall('<td>(\d+\.\d+\.\d+\.\d+)</td>',tr)[0]
    #         port=re.findall('<td>(\d+)</td>',tr)[0]
    #         # print(f'{host}:{port}')
    #         # yield f'{host}:{port}'

        # html=etree.HTML(res.content.decode('utf-8'))
        # tr=html.xpath('//*[@id="ipc"]/tbody/tr')[0]
        # for td in tr:
        #     host=td.xpath('./td[1]/text()')[0]
        #     port=td.xpath('./td[2]/text()')[0]
        #     print(host,port)





    # @staticmethod
    def freeProxycjy1():
        """
        站大爷代理 https://www.zdaye.com/
        :return:
        """
        from lxml import etree
        import re

        head = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Mobile Safari/537.36'
        }
        url = 'https://www.zdaye.com/dayProxy.html'
        r = requests.get(url, headers=head)
        r.encoding = 'utf8'
        html = etree.HTML(r.text)
        nurl = 'https://www.zdaye.com/' + (html.xpath('//*[@id="J_posts_list"]/div[2]/div/h3/a/@href')[0])
        uid = re.findall('(\d+)', nurl.split('/')[-1])[0]
        rr = requests.get(nurl, headers=head)
        r.encoding = 'utf-8'
        text = rr.content.decode('utf-8').replace('\n', '').replace(' ', '')
        data = re.findall("本次发布共<fontcolor='orange'><b>(\d+)</b></font>个代理IP，每页(\d+)个", text)[0]
        d0 = int(data[1])
        d1 = int(data[0])
        if d1 % d0 == 0:
            page = int(d1 / d0)
        else:
            page = int(d1 / d0) + 1
        for i in range(1, page + 1):
            url = f'https://www.zdaye.com/dayProxy/ip/{uid}/{i}.html'
            res = requests.get(url, headers=head)
            text = res.content.decode('utf-8').replace('\n', '').replace(' ', '').replace('\r\t\t', '').replace('\r\t',
                                                                                                               '')
            data = re.findall("<tbody>(.*?)</tbody>", text)[0]
            trs = data.split('<tr>')[1:]
            for tr in trs:
                host = re.findall('<td>(\d+\.\d+\.\d+\.\d+)</td>', tr)[0]
                port = re.findall('<td>(\d+)</td>', tr)[0]
                print(f'{host}:{port}')
                # yield f'{host}:{port}'


    freeProxycjy1()


