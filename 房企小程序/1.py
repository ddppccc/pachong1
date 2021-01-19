import requests
import re
headers = {
    'Host': 'dm-api.elab-plus.cn',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'elabEnvironment': '4',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
    'Origin': 'https://dm-mng.elab-plus.cn',
    'Content-Type': 'application/json;charset=UTF-8',
    'Referer': 'https://dm-mng.elab-plus.cn/touFangBao/index.html',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-us,en',
    'Cookie': '707c9f9616063819019415652e75412157d13677959872ccbf0ae71225367d',
}
resp_post = requests.post(url='https://dm-api.elab-plus.cn/elab-marketing-tfb/template/content/detailById',headers=headers,json={'id':'645'})

url = re.findall(r'\\"https://.*?\\"',resp_post.text)
print(url)