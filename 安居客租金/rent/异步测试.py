import asyncio

import aiohttp


# async with aiohttp.ClientSession() as session:
#     async with session.get("https://www.baidu.com") as resp:
#         # print(resp.text())
#         print(resp.status)
#         print(await resp.text())


# 异步等待
from lxml import etree


async def get_html(url, proxy):
    headers = {
        # :authority: wh.zu.anjuke.com
        # :method: GET
        # :path: /fangyuan/wuchanga/p50/
        # :scheme: https
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        # cookie: aQQ_ajkguid=A20A5957-B082-EC76-A06F-B136B3ED9E01; 58tj_uuid=90d79940-a0c8-4080-8ae9-4b63ccd755a4; _ga=GA1.2.1793385109.1562223154; als=0; isp=true; lps=https%3A%2F%2Faq.zu.anjuke.com%2Ffangyuan%2Fdaguan%2F%7C; wmda_uuid=6d17c4d9aead4ac57fa7408552c2bcc0; wmda_new_uuid=1; wmda_visited_projects=%3B6289197098934; twe=2; ajk_member_captcha=b4e74aacdfd64a62a6817930788a12f4; sessid=AA644069-B0AD-1804-3009-74AF2FEE630E; wmda_uuid=d4601febfb8e422f420417ddde35517d; wmda_new_uuid=1; wmda_visited_projects=%3B6289197098934; wmda_session_id_6289197098934=1565948518924-4d713465-52ef-beff; init_refer=; new_uv=5; _gid=GA1.2.1816315581.1565949588; new_session=0; Hm_lvt_c5899c8768ebee272710c9c5f365a6d8=1565951219; Hm_lpvt_c5899c8768ebee272710c9c5f365a6d8=1565951243; __xsptplus8=8.6.1565949588.1565951247.9%232%7Csp0.baidu.com%7C%7C%7C%25E5%25AE%2589%25E5%25B1%2585%25E5%25AE%25A2%7C%23%23flgnkbrYAzbPRjI-h11c58JY8_VjYigm%23; ctid=22; xzfzqtoken=7wYan3ArniGdLemKqHsAsDpYFNI2AoE6MxXxnoiXtOc1cmCI3GEb0vQ0q6EQFj3Min35brBb%2F%2FeSODvMgkQULA%3D%3D
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }
    timeout = aiohttp.ClientTimeout(total=5)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(  url=url,
                                   proxy =  "http://{}".format(proxy),
                                   headers=headers) as resp:
            html = await resp.text(encoding='utf-8')
            html = etree.HTML(html)

            if html.xpath("//div[@class='pop']/p[@class='title']"):
                print("出现滑动验证, 更改ip")


            # ip被封
            if "访问过于频繁" in "".join(html.xpath("//h2[@class='item']/text()")):
                print("访问过于频繁, ip被封, 更改ip")


            return html

loop = asyncio.get_event_loop()
html = loop.run_until_complete(get_html('https://ay.zu.anjuke.com/fangyuan/yindu/', '39.108.101.181:80'))

print(html)

# get_html("https://ww.baidu.com")


