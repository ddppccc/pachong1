import requests
import re
from bs4 import BeautifulSoup

def SearchInfo():
    kv = {
        'dest_id' : '1',
        'dest_type' : 'country',
        'checkin_year':'2020',
        'checkin_month':'11',
        'checkin_monthday':'13',
        'checkout_year':'2020',
        'checkout_month':'11',
        'checkout_monthday':'14',
        'offset':'0',
    }
    return kv

def Headers():
    headers = {
        "Cookie":"_pxhd=381af356acfb8cbcc9a91318c4245a3fb8d0eadfba37ab03dc948d796e402982%3Afce926a1-24b9-11eb-b85f-95faa8e455bc; cors_js=1; _pxvid=fce926a1-24b9-11eb-b85f-95faa8e455bc; _ga=GA1.2.962562818.1605166729; zz_cook_tms_seg1=1; zz_cook_tms_ed=1; zz_cook_tms_seg3=8; BJS=-; bs=%7B%22sr_country_or_region_page%22%3A%22country%22%7D; _gid=GA1.2.1721812646.1605433941; zz_cook_tms_hlist=5664433; has_preloaded=1; utag_main=v_id:0175bb648a3500951b52f2b09ed00307200ff06a00bd0$_sn:3$_ss:0$_st:1605435766515$4split:1$4split2:3$ses_id:1605433941658%3Bexp-session$_pn:3%3Bexp-session; _uetsid=41a8e990272811eb9405c7d13f774bbe; _uetvid=1b6abf2024ba11ebb735bb3b1259d43c; _px3=d5506cb13b0d55582b8ee916a9d3da92adfa81b915a225ad6fce7e2769261c85:zlyTtWLR0meom4CnpUlXxY3/hYSIRdvQWiuRzFfG45rDy9gil/3FvNT9K23LVLywNCfFNlCCjp36ok8bIF81fQ==:1000:LMmLiITsBg1mAP1/rbTGqclau0inldzbnDp2XwOXcynOsQ3NcMbeExvIg1tCLFKyd5MY+7EN7/v0kGTp47AiuqHuhSDPoF9jdimlcJbHX7MquY67egEkrQQYMq5z0j223nsVN08IqPijfoET+AucIhWgAlR42K83ZAZgGYP9694=; _pxde=1f9ea372c7a2c50e106d05e1ab77081993391da924c4655590e81a1ec7dd27ab:eyJ0aW1lc3RhbXAiOjE2MDU0MzUxNDEzMjAsImZfa2IiOjAsImlwY19pZCI6W119; bkng=11UmFuZG9tSVYkc2RlIyh9YSvtNSM2ADX0BnR0tqAEmjtHvFvjAYHRJb2kb0evktMucTeFvmj4JeO1Sev%2BmSZg6Ts5nAAHgJRMFJNiSppI4QOZEcEj4PzUtQSHgiM1A3Fvhb9zobZowxiU4m7RKdCEsxi1kgGxHq0NfzblktVgKpZt6QOT32r8ap9Y4LMK05g5o%2BhQWiBCrgXBFVGIqiPuIA%3D%3D; lastSeen=0",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    }
    return headers

def getHTMLText(url, **kwargs):
    try:
        r = requests.get(url, **kwargs)
        r.raise_for_status()
        return r.text
    except:
        return None

def main():
    #input url
    url = 'https://www.booking.com/searchresults.zh-cn.html?'
    for i in range(10):
        kv = SearchInfo()
        headers = Headers()
        try:
            kv['offset']=i*50
            r = getHTMLText(url, params=kv, headers=headers)
            soup = BeautifulSoup(r, 'lxml')
            Hotels = soup.find_all(class_="sr-hotel__name")
            print("page %s" %(i+1))
            for name in Hotels:
                print(re.sub(r'\n', '', name.text))
        except:
            continue

main()