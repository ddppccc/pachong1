import time
import json
from selenium import webdriver


def selenium_bs():
    driver = webdriver.Chrome()
    driver.get('http://127.0.0.1:5000')
    return driver


def decrypt(bs, timestamp, data):
    ti = bs.find_element_by_id('time')
    ti.clear()
    ti.send_keys(timestamp)
    time.sleep(0.5)

    t = bs.find_element_by_id('code')
    t.clear()
    js = f"element = document.getElementById('code'); element.value = '{data}';"
    bs.execute_script(js)

    de = bs.find_element_by_id('de')
    de.click()
    time.sleep(0.5)

    de = bs.find_element_by_id('decode')
    code = de.text
    code_json = json.loads(code)
    return code_json


if __name__ == '__main__':
    # TODO 运行前首先运行 FlaskAPI.py 启动服务
    timestamp = '1610344798010'
    data = "U2FsdGVkX18zNTD9cIhULUipaCpe40o97mu0In22UXlgr4INusek+HUVhQ9PcGXrxEWoUWt/luIB/E3F9cLNd/Bs8WhuSkkdLSYT19llEZj6i7YPwyZBulsG0Xwek38bOiymirgZneYsGjzDOKvi3gAPvNro762/ZKIj2Ve6yUMZ3+yY/L+NUURNbQ7rpp/3MP+UUtfI4C1cHWflwgQt/m/6Xt7Uo51h3m/Vj+y4tefszKkEt7t6pNALC9fpQM1ck8CPxGW8LkQnC5I8I4XqcP1RniuL/t69zvFrhnvl8rUQKQ0rcmxbm3/oNp3VJ3h9rlLtMRvY98vsREL2VNznjYUVAhcC1OzdNNzFAkwBFkRLvouZxvR1D5h59dmsJFNqwRl5hVK1gb5fm+72PX53Z/xyjyLurJ+z2VUt6TqJzX72gN0wnZ8c2SaMJo6WMZ5s/ce1rEktmERyypDQ7rLF8zQr5SlZNo4wn9K/blDoW4AyRuf0JkdYFaRNjvG8oaou5UecPaBxJW/vYT3sKPI+rzuIGZhX4SlxtBwZQ7PjJAUEUXGP4rOZp7OzQoIMBbyk6pD+13vn+kzFzkhXstT0bdFQagVUCz/Cq7pXsvzPyAzAW24BUS3JRjUyfxeeOS3vrDfdaBBaxM1Enkkuz7TBY7JCbAqcJY/RQ4JotQ9j17gGWTdpFU3dN7I/WyNtXtN6bngt4258NMB4sTQ37KWohwo+Uho4spPtyTfZdrqp9YHHWsefJcEO6KNiPoju6TyKT8DorBw4xh51LP35zL4Kw/iMz8pI3lWaIMkVfkPns5vIyX2XjVSNHZnASf9mz/OliJ/h4cyF5UZp8sLAG9SnkhomEwcygx8GTFIruN42cy0YTrMv9rJJR8VEMVv5GMIfLVJdnjpwMPUtPKhDBB5wE/W4JDWWVIPpFZUFAcfBh8++tamQH1k+kT8YX+Yd14tKxxiNTUAkAxv4lSDzdYVDTCqnOmKj6X1YyyE1RZfrEFX2ydwLX20z9tBk28hm+Q7+mrpoeXsUO+wDD/DC3R/xLYtWcw9z4apz/AAYD06JIfg5gNcZbUJDtfrqHiFP3RFMpmLY+ZoFaq6DVcOwRyoVqX/KNyqRq4dX2qbYm3J/nMZQWakIpPZb1cNyETKyZkEvEplwNHBLzB4Wfz7ofkNnhaV1l5WQ/Tne4aLQEdNiUNcJXU1KpTtSSugVnGTvYLfZ4j5XQReZa/rPaCp1workwcNMlTvzqC1ism5eGAzRVDc5k7i9yNoS+8lcm7ms5jx4CpYC7iNP+/volivaQa+Vatn+FWrJTRIIGgva0+efd695oQsgnCNKQAIJfVehC4aTpyItw/NpFdL44HYzjx1sIwfjamQa2uYs2byyJ9cQUgHv0aEWINFaRcun40E2OIowtCxeJHOH7WFNGIjLKxvPPfToBBds+OxuQz4kXtvQiO1rkkbQeuRg2fGkudNefTKhTu75I2m47ZonRHY42kMMhWuUdx/9u4mf950BwgOqfb0="

    bs = selenium_bs()
    code_json = decrypt(bs, timestamp, data)
    print(code_json)