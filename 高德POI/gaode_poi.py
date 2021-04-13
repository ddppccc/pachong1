import config
import requests
from requests.adapters import HTTPAdapter

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))#设置重试次数为3次
s.mount('https://', HTTPAdapter(max_retries=3))


