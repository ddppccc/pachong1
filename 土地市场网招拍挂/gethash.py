import time
from selenium import webdriver
url='http://192.168.1.197/zpg/'
def gethash(keys):                                 #删除一些元素
    # print(keys)
    # option = webdriver.ChromeOptions()
    # option.headless = True
    driver = webdriver.Chrome('E:\谷歌驱动\chromedriver.exe', )    # options=option   #驱动存在的文件目录
    driver.get(url)
    driver.execute_script('document.close()')
    driver.execute_script("document.write(strenc('%s'))" % keys)
    time.sleep(0.2)
    js = driver.find_elements_by_xpath('/html/body')[0].text
    driver.close()
    # print(js)
    return js
    
    
def getdriver():
    driver = webdriver.Chrome()
    driver.get(url)
    return driver
if __name__ == '__main__':
    gethash('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.3610list')