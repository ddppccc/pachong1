import requests
from selenium import webdriver

chromeOptions = webdriver.ChromeOptions()
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType


def get_proxy():
    return requests.get("http://47.106.223.4:50002/get/").json()
    # return requests.get("http://192.168.88.51:5010/get/").json()


proxy = get_proxy().get("proxy")

# proxy = Proxy(
#     {
#         'proxyType': ProxyType.MANUAL,
#         'httpProxy': proxy  # 代理ip和端口
#     }
# )
#
print(proxy)
# 设置代理
chromeOptions.add_argument("--proxy-server=http://{}".format(proxy))
# 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
browser = webdriver.Chrome(chrome_options=chromeOptions)

# 查看本机ip，查看代理是否起作用
browser.get("http://httpbin.org/ip")
print(browser.page_source)

# 退出，清除浏览器缓存
browser.quit()
