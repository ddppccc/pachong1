import time
from selenium import webdriver
url='http://1.116.204.248:1234/zpg/'
def gethash(keys):
    print(keys)
    driver = webdriver.Chrome('E:/chromedriver.exe')         #
    driver.get(url)
    driver.execute_script('document.close()')
    driver.execute_script("document.write(strenc('%s'))" % keys)
    time.sleep(0.2)
    js = driver.find_elements_by_xpath('/html/body')[0].text
    # print(js)
    return js
    
    
def getdriver():
    driver = webdriver.Chrome()
    driver.get(url)
    return driver
if __name__ == '__main__':
    gethash('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.3610list')