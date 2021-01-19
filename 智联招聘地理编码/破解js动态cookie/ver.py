import requests


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Host': 'jobs.zhaopin.com',

        'Accept-Language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cookie': 'acw_tc=2760823b15866900164434294e5cfe118b1b122702a5643342c66c5963e821; x-zp-client-id=7dfbc5df-46fa-4fac-f5c1-56138d274728; sts_deviceid=1716e19daf5168-05abca6ba421f8-6701b35-1327104-1716e19daf692b; sts_sg=1; sts_chnlsid=Unknown; zp_src_url=https%3A%2F%2Fjobs.zhaopin.com%2FCC183970727J00236754910.htm; jobRiskWarning=true; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221716e19dad9d2-0bcdcbb98cbd7a-6701b35-1327104-1716e19dada121%22%2C%22%24device_id%22%3A%221716e19dad9d2-0bcdcbb98cbd7a-6701b35-1327104-1716e19dada121%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%7D; acw_sc__v2=5e93c8e8ea8f4d363a8bb42d0ef66c74526466c0; sts_sid=1717148cde93af-0c4036d132e7e5-6701b35-1327104-1717148cdea7b1; acw_sc__=5e93cbe212ae879323183038e01768581405a7ec; ZL_REPORT_GLOBAL={%22jobs%22:{%22recommandActionidShare%22:%22ea954cfb-0540-484e-83f1-4a5c0fa6a211-job%22}}; sts_evtseq=9'
        }


proxy = "114.237.91.15:36194"
url = "https://jobs.zhaopin.com/CC183970727J00236754910.htm"


html = requests.get(url=url, headers=headers, timeout=(2.5, 5), proxies={"https": "https://{}".format(proxy)})
# html = requests.get(url=url, headers=headers, timeout=(2.5, 5))
html.encoding='utf-8'
print(html.text[:200])

