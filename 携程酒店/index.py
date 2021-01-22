import requests
import time
import datetime
import execjs
import os

from ws4py.client.threadedclient import WebSocketClient
from config import city_map_list, elevent_list

cookie = '' \
         '_RGUID=c1461406-eb54-4f73-9943-79aa0e6d7614; _RSG=pz4LhR0565CKONREeQU3b9; _RDG=28ae06a1d31f912556093f991d178ab833; magicid=DlIhPKz4FO8YiLX0K/aHU3Pq5G9moTc76Sbh1ixfm5zBaLSQv4yIN4/TI76Mhhde; _ga=GA1.2.1988880699.1590744994; MKT_CKID=1576636848313.u5oo4.4y1z; MKT_Pagesource=PC; _abtest_userid=814d20a9-879d-4568-b839-232a3da1c470; hoteluuid=A0zFC5pm95q5CHbd; _gid=GA1.2.1742368810.1590980138; ASP.NET_SessionId=zg30azsd5xmkmwudgupuxgxb; OID_ForOnlineHotel=159074499116512hxxp1590980160063102032; nfes_isSupportWebP=1; StartCity_Pkg=PkgStartCity=30; GUID=09031123210606373997; HotelDomesticVisitedHotels1=16197084=0,0,4.7,6172,/200l0q000000g9cyo7925.jpg,&48006023=0,0,0,1,/200l1800000141kcl2478.jpg,&50476254=0,0,0,0,/200c1a0000018o94t0997.jpg,&56187715=0,0,4.9,94,/200l1c000001di36z3715.jpg,&48565681=0,0,4.7,668,/2009180000014ymzeA807.jpg,; _RF1=119.137.54.170; MKT_CKID_LMT=1591078026313; HotelCityID=2split%E4%B8%8A%E6%B5%B7splitShanghaisplit2020-06-02split2020-06-03split0; Session=SmartLinkCode=U155952&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; Union=OUID=index&AllianceID=4897&SID=155952&SourceID=&createtime=1591090586&Expires=1591695386142; appFloatCnt=29; manualclose=1; hoteluuidkeys=zfZY3cekge1ZeHlrZYpY0DY1FEFYPYhNeafE3Zjm7WqYHYqajpqwQpr8MyGYfYnBjtgw1kxkMjqYdYGSIzXwnsv57IFY0YG8jzTYhkygAjTgvkUeGzYZGjksy1YQYbovlqvUqYXZwQTjTOe1FysHYZYzYqYQYazvQZelkYzTiP0YUY9YFYqYLDEQ7KkowsZi9zRBMjOr6bYGOJBcyBrAcYT8WHTv7lxpTeldYcDx4Hxf1YgOislwUqjG3E0XJN6WctjmrbaJNli4aw6TvsfRO4jzlY6OjNrsFyl7i5TwomRs6Ea1jZoxNaxPkEQOE4zE9sWaAe5OwMtE0ZjlQe1mil9YLSrbne3He6Gxc5iQPishxMAW3Ujg8e50wOcKcUwNcicmRUNjt9eMoEU9yQ7vXLinTE8MynQv6PKUTE1cKmqwcXis1RoFjzr7GYs6JnXycrU6jAXe5cj7oKQTjMdw4HxQGx5TxGMxzcEHQEpHEO7WUMe8mwHME1Zj8Get4iUFYQlrqDEBoyFLv0qibdESLyDSv73KpDW9AE7Njz9eNSxU8j6rDMEp5WbFeMmjsaYqnjQAxTDx4FxtmxTGEOLEtbEF7WtqeU4wqQET5j40ekoiFpYlBrUceSOe5sYt9EZNwksWb1i11KMsE7cEkdEp3Wfteb6wsHEnNjbNeLQiaQYqMrLteLZeL9EPhYsSE4nwNdWDnioYkYZzYpAi0pi16iTNjlYtYNTwpqEXlEoUJULjqpyLUj1mjtY8YDOR84JlZv8mRHZRA0wm3EkTYoLjnDjtHWPDYlqwoYfYNAYUqWAZrAOyZhEtfJocEkXRm1vTgJLNJo3JsqEHMvagJAmyfY9Y9DRLpJbFvH6WSnyhBEMdEaovdLvXDR5kRG3wHFJlY3YMHj08wh0vBH; _bfa=1.1590744991165.12hxxp.1.1591153225203.1591164288322.9.92.10650016817; _bfs=1.1; hotelhst=2012709687; _bfi=p1%3D102002%26p2%3D102002%26v1%3D92%26v2%3D91; _jzqco=%7C%7C%7C%7C1591078026563%7C1.1198146458.1590744994290.1591154173474.1591164291443.1591154173474.1591164291443.undefined.0.0.60.60; _gat=1; __zpspc=9.10.1591164291.1591164291.1%232%7Csp0.baidu.com%7C%7C%7C%25E6%2590%25BA%25E7%25A8%258B%7C%23'

class CG_Client(WebSocketClient):

    def opened(self):
        print("连接成功")
        self.send("Python" )

    def closed(self, code, reason=None):
        print("Closed down:", code, reason)

    def received_message(self, resp):
        # print('resp: ', resp, str(resp))
        elevent_list.append(str(resp))



def getTime():
    return str(time.time()).replace(".", "")[0:13]


def getCallbackParam():
    f = open("./callback.js")
    context = execjs.compile(f.read())
    return context.call("getCallback")


# 获取加密的url内容
def getContent(ws):
    t = getTime()
    callback = getCallbackParam()
    url = "https://hotels.ctrip.com/domestic/cas/oceanball?callback=%s&_=%s" % (callback, t)
    headers = {
        "user-agent": "Mozilla/5.0 (darwin) AppleWebKit/537.36 (KHTML, like Gecko) jsdom/16.2.2",
        "referer": "https://hotels.ctrip.com/hotel/shanghai2",
    }
    number = 3
    while number > 0:
        try:
            r = requests.get(url, headers=headers)
            break
        except Exception as e:
            print(e)
            number -= 1
            continue
    code = (
        """
        window["%s"] = function (e) {
        var f = e();
        console.log(f);
        ws.send(f);
    };;
    """ % callback + r.text
    )
    ws.send(code)

if __name__ == '__main__':

    ws = None
    try:
        ws = CG_Client("ws://127.0.0.1:8014/")
        ws.connect()
        for i in range(10):
            print(10)
            getContent()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()

