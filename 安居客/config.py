import csv
import random
import time

import requests

city_map = ['深圳','北京','上海','广州','成都']



def statis_output(title, rowlist, database,city) -> object:
    csvfile = open('{}'.format(title), 'w+', newline='', encoding='utf-8')
    res_writer = csv.writer(csvfile, dialect='excel')
    res_writer.writerow(rowlist)
    for item in database.find({'city_name':city}):
        res_writer.writerow(list(item.values())[1:])

def get_ua():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
        'Opera/8.0 (Windows NT 5.1; U; en)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) '
    ]
    user_agent = random.choice(user_agents)  # random.choice(),从列表中随机抽取一个对象
    return user_agent


IpPool=[
        # "192.168.1.104:5010",
        # "192.168.1.130:5010",
        "118.24.52.95:5010",
        # "47.106.223.4:50002"
        ]
username = 'lum-customer-hl_dd804c17-zone-data_center-route_err-pass_dyn'
password = '1cysg9ek1vvk'
port = 22225
session_id = random.random()
super_proxy_url = ('http://%s-country-cn-session-%s:%s@zproxy.lum-superproxy.io:%d' %
    (username, session_id, password, port))



cc=[
"114.217.171.59:27908",
"115.209.79.98:27620",
"114.104.102.39:25493",
"121.230.209.130:41307",
"42.203.37.227:24059",
"61.191.84.66:27561",
"182.34.149.130:35820",
"180.108.200.125:37601",
"120.35.189.7:27088",
"110.187.227.179:20683",
]
# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"
# 代理隧道验证信息
proxyUser = "H6F2SWR51B5L56HD"
proxyPass = "0984F7A27D0598EB"
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}
def get_proxy():
    # return 'http://H041YJYT015P8T3D:0B6839D706F30F56@http-dyn.abuyun.com:9020'
    while True:
        try:
            response = requests.get('http://47.111.226.234:8000/getip2/')
            if response.status_code == 200:
                return response.text
            else:
                time.sleep(1)
        except:
            print('暂无ip')


if __name__ == '__main__':
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        'Connection': 'close',
        "referer": "https://www.anjuke.com/sy-city.html",
        "upgrade-insecure-requests": "1",
        # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        # "user-agent":UserAgent().chrome
        "user-agent": get_ua()
    }
    url='http://zunyi.anjuke.com/sale/huichuan-q-renmlo/p15/'
    r=requests.get(url,headers=headers)
    print(r.text)


def delete_proxy(proxy):
    html = requests.get('http://47.106.223.4:50002/delete/?proxy={}'.format(proxy))
    return html.text


city_url = {

    '鞍山':'https://anshan.anjuke.com',
    '安阳':'https://anyang.anjuke.com',
    '安庆':'https://anqing.anjuke.com',
    '安康':'https://ankang.anjuke.com',
    '安顺':'https://anshun.anjuke.com',
    '阿坝':'https://aba.anjuke.com',
    '阿克苏':'https://akesu.anjuke.com',
    '阿里':'https://ali.anjuke.com',
    '阿拉尔':'https://alaer.anjuke.com',
    '阿拉善盟':'https://alashanmeng.anjuke.com',
    '安丘':'https://anqiu.anjuke.com',
    '安宁':'https://anning.anjuke.com',
    '安吉县':'https://anjixian.anjuke.com',
    '安溪':'https://anxi.anjuke.com',
    '林州':'https://aylinzhou.anjuke.com',
    '安岳':'https://anyuexian.anjuke.com',
    '阿勒泰':'https://aletai.anjuke.com',
    '北京':'https://beijing.anjuke.com',
    '保定':'https://baoding.anjuke.com',
    '包头':'https://baotou.anjuke.com',
    '滨州':'https://binzhou.anjuke.com',
    '宝鸡':'https://baoji.anjuke.com',
    '蚌埠':'https://bengbu.anjuke.com',
    '本溪':'https://benxi.anjuke.com',
    '北海':'https://beihai.anjuke.com',
    '巴音郭楞':'https://bayinguoleng.anjuke.com',
    '巴中':'https://bazhong.anjuke.com',
    '巴彦淖尔市':'https://bayannaoer.anjuke.com',
    '亳州':'https://bozhou.anjuke.com',
    '白银':'https://baiyin.anjuke.com',
    '白城':'https://baicheng.anjuke.com',
    '百色':'https://baise.anjuke.com',
    '白山':'https://baishan.anjuke.com',
    '博尔塔拉':'https://boertala.anjuke.com',
    '毕节':'https://bijie.anjuke.com',
    '保山':'https://baoshan.anjuke.com',
    '霸州':'https://bazh.anjuke.com',
    '北票':'https://beipiao.anjuke.com',
    '北流':'https://beiliu.anjuke.com',
    '博白':'https://bobaixian.anjuke.com',
    '博罗':'https://boluoxian.anjuke.com',
    '宝应县':'https://baoyingxian.anjuke.com',
    '博兴':'https://boxingxian.anjuke.com',
    '成都':'https://chengdu.anjuke.com',
    '重庆':'https://chongqing.anjuke.com',
    '长沙':'https://cs.anjuke.com',
    '常州':'https://cz.anjuke.com',
    '长春':'https://cc.anjuke.com',
    '沧州':'https://cangzhou.anjuke.com',
    '昌吉':'https://changji.anjuke.com',
    '赤峰':'https://chifeng.anjuke.com',
    '常德':'https://changde.anjuke.com',
    '郴州':'https://chenzhou.anjuke.com',
    '承德':'https://chengde.anjuke.com',
    '长治':'https://changzhi.anjuke.com',
    '池州':'https://chizhou.anjuke.com',
    '滁州':'https://chuzhou.anjuke.com',
    '朝阳':'https://chaoyang.anjuke.com',
    '潮州':'https://chaozhou.anjuke.com',
    '楚雄':'https://chuxiong.anjuke.com',
    '巢湖':'https://chaohu.anjuke.com',
    '昌都':'https://changdu.anjuke.com',
    '长葛':'https://changge.anjuke.com',
    '崇左':'https://chongzuo.anjuke.com',
    '常熟':'https://changshushi.anjuke.com',
    '赤壁':'https://chibi.anjuke.com',
    '岑溪':'https://cengxi.anjuke.com',
    '慈溪':'https://cixi.anjuke.com',
    '崇州':'https://chongzhou.anjuke.com',
    '慈利':'https://cilixian.anjuke.com',
    '长岭':'https://changlingxian.anjuke.com',
    '长兴':'https://changxingxian.anjuke.com',
    '苍南县':'https://cangnanxian.anjuke.com',
    '曹县':'https://caoxian.anjuke.com',
    '长垣县':'https://changyuanxian.anjuke.com',
    '昌乐':'https://changle.anjuke.com',
    '沧县':'https://cangxian.anjuke.com',
    '长宁':'https://changning.anjuke.com',
    '磁县':'https://cixian.anjuke.com',
    '茌平':'https://chiping.anjuke.com',
    '大连':'https://dalian.anjuke.com',
    '东莞':'https://dg.anjuke.com',
    '德阳':'https://deyang.anjuke.com',
    '大理':'https://dali.anjuke.com',
    '德州':'https://dezhou.anjuke.com',
    '东营':'https://dongying.anjuke.com',
    '大庆':'https://daqing.anjuke.com',
    '丹东':'https://dandong.anjuke.com',
    '大同':'https://datong.anjuke.com',
    '达州':'https://dazhou.anjuke.com',
    '大丰':'https://dafeng.anjuke.com',
    '德宏':'https://dehong.anjuke.com',
    '定州':'https://dingzhou.anjuke.com',
    '迪庆':'https://diqing.anjuke.com',
    '定西':'https://dingxi.anjuke.com',
    '大兴安岭':'https://dxanling.anjuke.com',
    '东台':'https://dongtai.anjuke.com',
    '邓州':'https://dengzhou.anjuke.com',
    '东方':'https://dongfang.anjuke.com',
    '儋州':'https://danzhou.anjuke.com',
    '丹阳':'https://danyang.anjuke.com',
    '灯塔':'https://dengta.anjuke.com',
    '敦煌':'https://dunhuang.anjuke.com',
    '大冶':'https://daye.anjuke.com',
    '都匀':'https://duyun.anjuke.com',
    '东阳':'https://dongyang.anjuke.com',
    '都江堰':'https://dujiangyan.anjuke.com',
    '东至':'https://dongzhixian.anjuke.com',
    '德清':'https://deqingxian.anjuke.com',
    '东海':'https://donghaixian.anjuke.com',
    '单县':'https://danxian.anjuke.com',
    '凤城':'https://ddfengcheng.anjuke.com',
    '禹城':'https://dzyucheng.anjuke.com',
    '大竹':'https://dazhu.anjuke.com',
    '定边':'https://dingbianxian.anjuke.com',
    '东明':'https://dongmingxian.anjuke.com',
    '东平':'https://dongpingxian.anjuke.com',
    '大悟':'https://dawuxian.anjuke.com',
    '鄂尔多斯':'https://eerduosi.anjuke.com',
    '恩施':'https://enshi.anjuke.com',
    '鄂州':'https://ezhou.anjuke.com',
    '恩平':'https://enping.anjuke.com',
    '峨眉山':'https://emeishan.anjuke.com',
    '佛山':'https://foshan.anjuke.com',
    '福州':'https://fz.anjuke.com',
    '阜阳':'https://fuyang.anjuke.com',
    '抚顺':'https://fushun.anjuke.com',
    '阜新':'https://fuxin.anjuke.com',
    '抚州':'https://fuzhoushi.anjuke.com',
    '防城港':'https://fangchenggang.anjuke.com',
    '肥城市':'https://feichengshi.anjuke.com',
    '丰城':'https://fengchengshi.anjuke.com',
    '福清':'https://fuqing.anjuke.com',
    '福安':'https://fuan.anjuke.com',
    '福鼎':'https://fuding.anjuke.com',
    '范县':'https://fanxian.anjuke.com',
    '分宜':'https://fenyixian.anjuke.com',
    '扶余':'https://fuyushi.anjuke.com',
    '阜宁':'https://funing.anjuke.com',
    '浮梁':'https://fuliang.anjuke.com',
    '府谷':'https://fuguxian.anjuke.com',
    '广州':'https://guangzhou.anjuke.com',
    '贵阳':'https://gy.anjuke.com',
    '桂林':'https://guilin.anjuke.com',
    '赣州':'https://ganzhou.anjuke.com',
    '广安':'https://guangan.anjuke.com',
    '贵港':'https://guigang.anjuke.com',
    '广元':'https://guangyuan.anjuke.com',
    '甘孜':'https://ganzi.anjuke.com',
    '甘南':'https://gannan.anjuke.com',
    '馆陶':'https://guantao.anjuke.com',
    '果洛':'https://guoluo.anjuke.com',
    '固原':'https://guyuan.anjuke.com',
    '公主岭市':'https://gongzhulingshi.anjuke.com',
    '高邮':'https://gaoyou.anjuke.com',
    '高密市':'https://gaomishi.anjuke.com',
    '格尔木':'https://geermu.anjuke.com',
    '广汉':'https://guanghan.anjuke.com',
    '桂平':'https://guiping.anjuke.com',
    '高安':'https://gaoanshi.anjuke.com',
    '高碑店':'https://gaobeidian.anjuke.com',
    '固始':'https://gushixian.anjuke.com',
    '桂阳':'https://guiyangxian.anjuke.com',
    '高平':'https://gaopingshi.anjuke.com',
    '广饶县':'https://guangraoxian.anjuke.com',
    '灌云县':'https://guanyunxian.anjuke.com',
    '灌南县':'https://guannanxian.anjuke.com',
    '固安':'https://guan.anjuke.com',
    '谷城':'https://gucheng.anjuke.com',
    '高唐':'https://gaotangxian.anjuke.com',
    '冠县':'https://guanxian.anjuke.com',
    '改则':'https://gaizexian.anjuke.com',
    '杭州':'https://hangzhou.anjuke.com',
    '合肥':'https://hf.anjuke.com',
    '哈尔滨':'https://heb.anjuke.com',
    '海口':'https://haikou.anjuke.com',
    '惠州':'https://huizhou.anjuke.com',
    '邯郸':'https://handan.anjuke.com',
    '呼和浩特':'https://huhehaote.anjuke.com',
    '黄冈':'https://huanggang.anjuke.com',
    '淮南':'https://huainan.anjuke.com',
    '黄山':'https://huangshan.anjuke.com',
    '鹤壁':'https://hebi.anjuke.com',
    '衡阳':'https://hengyang.anjuke.com',
    '湖州':'https://huzhou.anjuke.com',
    '衡水':'https://hengshui.anjuke.com',
    '汉中':'https://hanzhong.anjuke.com',
    '淮安':'https://huaian.anjuke.com',
    '黄石':'https://huangshi.anjuke.com',
    '菏泽':'https://heze.anjuke.com',
    '怀化':'https://huaihua.anjuke.com',
    '淮北':'https://huaibei.anjuke.com',
    '葫芦岛':'https://huludao.anjuke.com',
    '河源':'https://heyuan.anjuke.com',
    '红河':'https://honghe.anjuke.com',
    '哈密':'https://hami.anjuke.com',
    '鹤岗':'https://hegang.anjuke.com',
    '呼伦贝尔':'https://hulunbeier.anjuke.com',
    '海北':'https://haibei.anjuke.com',
    '海东':'https://haidong.anjuke.com',
    '海南':'https://hainan.anjuke.com',
    '河池':'https://hechi.anjuke.com',
    '黑河':'https://heihe.anjuke.com',
    '和县':'https://hexian.anjuke.com',
    '贺州':'https://hezhou.anjuke.com',
    '海拉尔':'https://hailaer.anjuke.com',
    '霍邱':'https://huoqiu.anjuke.com',
    '和田':'https://hetian.anjuke.com',
    '黄南':'https://huangnan.anjuke.com',
    '海西':'https://hexi.anjuke.com',
    '鹤山':'https://heshan.anjuke.com',
    '海城':'https://haicheng.anjuke.com',
    '黄骅':'https://huanghua.anjuke.com',
    '河间':'https://hejian.anjuke.com',
    '韩城':'https://hancheng.anjuke.com',
    '汉川市':'https://hanchuanshi.anjuke.com',
    '海门':'https://haimen.anjuke.com',
    '海宁':'https://haining.anjuke.com',
    '海阳':'https://haiyang.anjuke.com',
    '淮滨':'https://huaibinxian.anjuke.com',
    '海安':'https://haianxian.anjuke.com',
    '惠东':'https://huidongxian.anjuke.com',
    '海丰县':'https://haifengxian.anjuke.com',
    '桓台县':'https://huantaixian.anjuke.com',
    '常宁':'https://hychangning.anjuke.com',
    '海盐':'https://haiyan.anjuke.com',
    '永城':'https://hnyongcheng.anjuke.com',
    '滑县':'https://huaxian.anjuke.com',
    '衡东':'https://hengdongxian.anjuke.com',
    '华容':'https://huarongxian.anjuke.com',
    '济南':'https://jinan.anjuke.com',
    '嘉兴':'https://jx.anjuke.com',
    '吉林':'https://jilin.anjuke.com',
    '江门':'https://jiangmen.anjuke.com',
    '荆门':'https://jingmen.anjuke.com',
    '锦州':'https://jinzhou.anjuke.com',
    '景德镇':'https://jingdezhen.anjuke.com',
    '吉安':'https://jian.anjuke.com',
    '济宁':'https://jining.anjuke.com',
    '金华':'https://jinhua.anjuke.com',
    '揭阳':'https://jieyang.anjuke.com',
    '晋中':'https://jinzhong.anjuke.com',
    '九江':'https://jiujiang.anjuke.com',
    '焦作':'https://jiaozuo.anjuke.com',
    '晋城':'https://jincheng.anjuke.com',
    '荆州':'https://jingzhou.anjuke.com',
    '佳木斯':'https://jiamusi.anjuke.com',
    '酒泉':'https://jiuquan.anjuke.com',
    '鸡西':'https://jixi.anjuke.com',
    '济源':'https://jiyuan.anjuke.com',
    '金昌':'https://jinchang.anjuke.com',
    '嘉峪关':'https://jiayuguan.anjuke.com',
    '江阴':'https://jiangyin.anjuke.com',
    '靖江':'https://jingjiang.anjuke.com',
    '简阳市':'https://jianyangshi.anjuke.com',
    '金坛':'https://jintan.anjuke.com',
    '吉首':'https://jishou.anjuke.com',
    '景洪':'https://jinghong.anjuke.com',
    '晋江':'https://jinjiangshi.anjuke.com',
    '建瓯':'https://jianou.anjuke.com',
    '胶州':'https://jiaozhoux.anjuke.com',
    '句容':'https://jurong.anjuke.com',
    '江油市':'https://jiangyoushi.anjuke.com',
    '嘉鱼':'https://jiayuxian.anjuke.com',
    '建湖':'https://jianhuxian.anjuke.com',
    '嘉善':'https://jiashanxian.anjuke.com',
    '莒县':'https://juxian.anjuke.com',
    '昌邑':'https://jlchangyi.anjuke.com',
    '桦甸':'https://jlhuadian.anjuke.com',
    '京山':'https://jmjingshan.anjuke.com',
    '进贤':'https://jinxian.anjuke.com',
    '金湖':'https://jinhu.anjuke.com',
    '钟祥':'https://jmzhongxiang.anjuke.com',
    '孟州':'https://jzmengzhou.anjuke.com',
    '靖边':'https://jingbianxian.anjuke.com',
    '巨野':'https://juyexian.anjuke.com',
    '鄄城':'https://juanchengxian.anjuke.com',
    '姜堰':'https://jiangyan.anjuke.com',
    '昆明':'https://km.anjuke.com',
    '昆山':'https://ks.anjuke.com',
    '开封':'https://kaifeng.anjuke.com',
    '喀什':'https://kashi.anjuke.com',
    '克拉玛依':'https://kelamayi.anjuke.com',
    '垦利':'https://kenli.anjuke.com',
    '克孜勒苏':'https://lezilesu.anjuke.com',
    '库尔勒':'https://kuerle.anjuke.com',
    '凯里':'https://kaili.anjuke.com',
    '开平':'https://kaiping.anjuke.com',
    '兰考':'https://kflankao.anjuke.com',
    '兰州':'https://lanzhou.anjuke.com',
    '廊坊':'https://langfang.anjuke.com',
    '洛阳':'https://luoyang.anjuke.com',
    '柳州':'https://liuzhou.anjuke.com',
    '莱芜':'https://laiwu.anjuke.com',
    '六安':'https://luan.anjuke.com',
    '泸州':'https://luzhou.anjuke.com',
    '丽江':'https://lijiang.anjuke.com',
    '临沂':'https://linyi.anjuke.com',
    '聊城':'https://liaocheng.anjuke.com',
    '连云港':'https://lianyungang.anjuke.com',
    '丽水':'https://lishui.anjuke.com',
    '娄底':'https://loudi.anjuke.com',
    '乐山':'https://leshan.anjuke.com',
    '辽阳':'https://liaoyang.anjuke.com',
    '拉萨':'https://lasa.anjuke.com',
    '临汾':'https://linfen.anjuke.com',
    '龙岩':'https://longyan.anjuke.com',
    '漯河':'https://luohe.anjuke.com',
    '凉山':'https://liangshan.anjuke.com',
    '六盘水':'https://liupanshui.anjuke.com',
    '辽源':'https://liaoyuan.anjuke.com',
    '来宾':'https://laibin.anjuke.com',
    '临沧':'https://lingcang.anjuke.com',
    '临夏':'https://linxia.anjuke.com',
    '临猗':'https://linyishi.anjuke.com',
    '林芝':'https://linzhi.anjuke.com',
    '陇南':'https://longnan.anjuke.com',
    '吕梁':'https://lvliang.anjuke.com',
    '临海市':'https://linhaishi.anjuke.com',
    '龙海市':'https://longhaishi.anjuke.com',
    '醴陵市':'https://lilingshi.anjuke.com',
    '临清':'https://linqing.anjuke.com',
    '龙口':'https://longkou.anjuke.com',
    '莱阳':'https://laiyang.anjuke.com',
    '耒阳':'https://leiyang.anjuke.com',
    '溧阳':'https://liyang.anjuke.com',
    '凌源':'https://lingyuan.anjuke.com',
    '灵宝市':'https://lingbaoshi.anjuke.com',
    '冷水江':'https://lengshuijiang.anjuke.com',
    '涟源':'https://lianyuan.anjuke.com',
    '陆丰':'https://lufengshi.anjuke.com',
    '罗定':'https://luoding.anjuke.com',
    '乐平市':'https://lepingshi.anjuke.com',
    '莱州市':'https://laizhoushi.anjuke.com',
    '莱西':'https://laixi.anjuke.com',
    '梨树':'https://lishuxian.anjuke.com',
    '利津':'https://lijingxian.anjuke.com',
    '柳林':'https://liulinxian.anjuke.com',
    '滦南':'https://luannan.anjuke.com',
    '临朐':'https://linju.anjuke.com',
    '宜阳':'https://lyyiyang.anjuke.com',
    '乐陵':'https://leling.anjuke.com',
    '澧县':'https://lixian.anjuke.com',
    '梁山':'https://liangshanxian.anjuke.com',
    '临邑':'https://linyixian.anjuke.com',
    '鹿邑':'https://luyixian.anjuke.com',
    '绵阳':'https://mianyang.anjuke.com',
    '茂名':'https://maoming.anjuke.com',
    '马鞍山':'https://maanshan.anjuke.com',
    '牡丹江':'https://mudanjiang.anjuke.com',
    '眉山':'https://meishan.anjuke.com',
    '梅州':'https://meizhou.anjuke.com',
    '明港':'https://minggang.anjuke.com',
    '梅河口':'https://meihekou.anjuke.com',
    '弥勒':'https://mileshi.anjuke.com',
    '渑池':'https://mianchixian.anjuke.com',
    '孟津':'https://mengjin.anjuke.com',
    '南京':'https://nanjing.anjuke.com',
    '宁波':'https://nb.anjuke.com',
    '南昌':'https://nc.anjuke.com',
    '南宁':'https://nanning.anjuke.com',
    '南通':'https://nantong.anjuke.com',
    '南充':'https://nanchong.anjuke.com',
    '南阳':'https://nanyang.anjuke.com',
    '宁德':'https://ningde.anjuke.com',
    '内江':'https://neijiang.anjuke.com',
    '南平':'https://nanping.anjuke.com',
    '那曲':'https://naqu.anjuke.com',
    '怒江':'https://nujiang.anjuke.com',
    '南安':'https://nananshi.anjuke.com',
    '宁国':'https://ningguo.anjuke.com',
    '南城':'https://nanchengxian.anjuke.com',
    '南县':'https://nanxian.anjuke.com',
    '南漳':'https://nanzhangxian.anjuke.com',
    '宁津':'https://ningjinxian.anjuke.com',
    '宁阳':'https://ningyangxian.anjuke.com',
    '攀枝花':'https://panzhihua.anjuke.com',
    '平顶山':'https://pingdingsha.anjuke.com',
    '盘锦':'https://panjin.anjuke.com',
    '萍乡':'https://pingxiang.anjuke.com',
    '濮阳':'https://puyang.anjuke.com',
    '莆田':'https://putian.anjuke.com',
    '普洱':'https://puer.anjuke.com',
    '平凉':'https://pingliang.anjuke.com',
    '普宁':'https://puning.anjuke.com',
    '邳州':'https://pizhou.anjuke.com',
    '蓬莱市':'https://penglaishi.anjuke.com',
    '平湖':'https://pinghu.anjuke.com',
    '平度':'https://pingdu.anjuke.com',
    '彭州':'https://pengzhou.anjuke.com',
    '舞钢':'https://pdswugang.anjuke.com',
    '平阳':'https://pingyang.anjuke.com',
    '平邑':'https://pingyi.anjuke.com',
    '磐石':'https://panshishi.anjuke.com',
    '青岛':'https://qd.anjuke.com',
    '秦皇岛':'https://qinhuangdao.anjuke.com',
    '泉州':'https://quanzhou.anjuke.com',
    '曲靖':'https://qujing.anjuke.com',
    '齐齐哈尔':'https://qiqihaer.anjuke.com',
    '衢州':'https://quzhou.anjuke.com',
    '清远':'https://qingyuan.anjuke.com',
    '钦州':'https://qinzhou.anjuke.com',
    '庆阳':'https://qingyang.anjuke.com',
    '黔东南':'https://qiandongnan.anjuke.com',
    '潜江':'https://qianjiang.anjuke.com',
    '清徐':'https://qingxu.anjuke.com',
    '黔南':'https://qiannan.anjuke.com',
    '七台河':'https://qitaihe.anjuke.com',
    '黔西南':'https://qianxinan.anjuke.com',
    '迁安市':'https://qiananshi.anjuke.com',
    '青州市':'https://qingzhoushi.anjuke.com',
    '清镇':'https://qingzhen.anjuke.com',
    '琼海':'https://qionghai.anjuke.com',
    '沁阳':'https://qinyangshi.anjuke.com',
    '曲阜':'https://qufu.anjuke.com',
    '启东':'https://qidong.anjuke.com',
    '淇县':'https://qixian.anjuke.com',
    '祁阳':'https://qiyangxian.anjuke.com',
    '渠县':'https://quxian.anjuke.com',
    '杞县':'https://qixianqu.anjuke.com',
    '迁西':'https://qianxi.anjuke.com',
    '栖霞':'https://qixia.anjuke.com',
    '江山':'https://qzjiangshan.anjuke.com',
    '齐河':'https://qihexian.anjuke.com',
    '祁东':'https://qidongxian.anjuke.com',
    '日照':'https://rizhao.anjuke.com',
    '日喀则':'https://rikeze.anjuke.com',
    '瑞安':'https://ruian.anjuke.com',
    '汝州市':'https://ruzhoushi.anjuke.com',
    '任丘市':'https://renqiushi.anjuke.com',
    '瑞金':'https://ruijin.anjuke.com',
    '乳山市':'https://rushanshi.anjuke.com',
    '仁怀':'https://renhuai.anjuke.com',
    '瑞丽':'https://ruili.anjuke.com',
    '如皋':'https://rugao.anjuke.com',
    '荣成市':'https://rongchengshi.anjuke.com',
    '如东':'https://rudongxian.anjuke.com',
    '仁寿':'https://renshouxian.anjuke.com',
    '日土':'https://rituxian.anjuke.com',
    '上海':'https://shanghai.anjuke.com',
    '深圳':'https://shenzhen.anjuke.com',
    '苏州':'https://suzhou.anjuke.com',
    '石家庄':'https://sjz.anjuke.com',
    '沈阳':'https://sy.anjuke.com',
    '三亚':'https://sanya.anjuke.com',
    '绍兴':'https://shaoxing.anjuke.com',
    '汕头':'https://shantou.anjuke.com',
    '十堰':'https://shiyan.anjuke.com',
    '三门峡':'https://sanmenxia.anjuke.com',
    '三明':'https://sanming.anjuke.com',
    '韶关':'https://shaoguan.anjuke.com',
    '商丘':'https://shangqiu.anjuke.com',
    '宿迁':'https://suqian.anjuke.com',
    '绥化':'https://suihua.anjuke.com',
    '邵阳':'https://shaoyang.anjuke.com',
    '遂宁':'https://suining.anjuke.com',
    '上饶':'https://shangrao.anjuke.com',
    '四平':'https://siping.anjuke.com',
    '石河子':'https://shihezi.anjuke.com',
    '顺德':'https://shunde.anjuke.com',
    '宿州':'https://suzhoushi.anjuke.com',
    '松原':'https://songyuan.anjuke.com',
    '沭阳':'https://shuyang.anjuke.com',
    '石嘴山':'https://shizuishan.anjuke.com',
    '随州':'https://suizhou.anjuke.com',
    '朔州':'https://shuozhou.anjuke.com',
    '汕尾':'https://shanwei.anjuke.com',
    '三沙':'https://sansha.anjuke.com',
    '商洛':'https://shangluo.anjuke.com',
    '山南':'https://shannan.anjuke.com',
    '神农架':'https://shennongjia.anjuke.com',
    '双鸭山':'https://shuangyashan.anjuke.com',
    '石狮':'https://shishi.anjuke.com',
    '三河市':'https://sanheshi.anjuke.com',
    '寿光':'https://shouguang.anjuke.com',
    '嵊州':'https://shengzhou.anjuke.com',
    '四会':'https://sihui.anjuke.com',
    '邵武':'https://shaowu.anjuke.com',
    '松滋':'https://songzi.anjuke.com',
    '上杭':'https://shagnhangxian.anjuke.com',
    '睢县':'https://suixian.anjuke.com',
    '沙洋':'https://shayangxian.anjuke.com',
    '邵东':'https://shaodongxian.anjuke.com',
    '射洪':'https://shehongxian.anjuke.com',
    '双峰':'https://shuangfengxian.anjuke.com',
    '随县':'https://suixia.anjuke.com',
    '邵阳县':'https://shaoyangxian.anjuke.com',
    '泗阳县':'https://siyangxian.anjuke.com',
    '泗洪县':'https://sihongxian.anjuke.com',
    '安达':'https://shanda.anjuke.com',
    '永安':'https://smyongan.anjuke.com',
    '肇东':'https://shzhaodong.anjuke.com',
    '广水':'https://szguangshui.anjuke.com',
    '孝义':'https://sxxiaoyi.anjuke.com',
    '商水':'https://shangshui.anjuke.com',
    '射阳':'https://sheyangxian.anjuke.com',
    '涉县':'https://shexian.anjuke.com',
    '沈丘':'https://shenqiuxian.anjuke.com',
    '神木':'https://shenmuxian.anjuke.com',
    '天津':'https://tianjin.anjuke.com',
    '太原':'https://ty.anjuke.com',
    '泰州':'https://taizhou.anjuke.com',
    '唐山':'https://tangshan.anjuke.com',
    '泰安':'https://taian.anjuke.com',
    '台州':'https://taiz.anjuke.com',
    '铁岭':'https://tieling.anjuke.com',
    '通辽':'https://tongliao.anjuke.com',
    '铜陵':'https://tongling.anjuke.com',
    '天水':'https://tianshui.anjuke.com',
    '通化':'https://tonghua.anjuke.com',
    '台山':'https://taishan.anjuke.com',
    '铜川':'https://tongchuan.anjuke.com',
    '吐鲁番':'https://tulufan.anjuke.com',
    '天门':'https://tianmen.anjuke.com',
    '图木舒克':'https://tumushuke.anjuke.com',
    '桐城':'https://tongcheng.anjuke.com',
    '铜仁':'https://tongren.anjuke.com',
    '太仓':'https://taicang.anjuke.com',
    '泰兴':'https://taixing.anjuke.com',
    '滕州市':'https://tengzhoushi.anjuke.com',
    '桐乡':'https://tongxiang.anjuke.com',
    '天长':'https://tianchang.anjuke.com',
    '通许':'https://tongxuxian.anjuke.com',
    '开原':'https://tlkaiyuan.anjuke.com',
    '太康':'https://taikangxian.anjuke.com',
    '郯城':'https://tanchengxian.anjuke.com',
    '塔城':'https://tuscaloosa.anjuke.com',
    '武汉':'https://wuhan.anjuke.com',
    '无锡':'https://wuxi.anjuke.com',
    '威海':'https://weihai.anjuke.com',
    '潍坊':'https://weifang.anjuke.com',
    '乌鲁木齐':'https://wulumuqi.anjuke.com',
    '温州':'https://wenzhou.anjuke.com',
    '芜湖':'https://wuhu.anjuke.com',
    '梧州':'https://wuzhou.anjuke.com',
    '渭南':'https://weinan.anjuke.com',
    '乌海':'https://wuhai.anjuke.com',
    '文山':'https://wenshan.anjuke.com',
    '武威':'https://wuwei.anjuke.com',
    '乌兰察布':'https://wulanchabu.anjuke.com',
    '瓦房店':'https://wafangdian.anjuke.com',
    '五家渠':'https://wujiaqu.anjuke.com',
    '武夷山':'https://wuyishan.anjuke.com',
    '吴忠':'https://wuzhong.anjuke.com',
    '五指山':'https://wuzhishan.anjuke.com',
    '温岭':'https://wnelingshi.anjuke.com',
    '武安市':'https://wuanshi.anjuke.com',
    '文昌':'https://wenchang.anjuke.com',
    '乌兰浩特':'https://wulanhaote.anjuke.com',
    '武穴':'https://wuxue.anjuke.com',
    '万宁':'https://wanning.anjuke.com',
    '尉氏':'https://weishixian.anjuke.com',
    '无为':'https://wuweixian.anjuke.com',
    '温县':'https://wenxian.anjuke.com',
    '无棣':'https://wudi.anjuke.com',
    '微山':'https://weishanxian.anjuke.com',
    '汶上':'https://wenshangxian.anjuke.com',
    '武义':'https://wuyi.anjuke.com',
    '西安':'https://xa.anjuke.com',
    '厦门':'https://xm.anjuke.com',
    '徐州':'https://xuzhou.anjuke.com',
    '湘潭':'https://xiangtan.anjuke.com',
    '襄阳':'https://xiangyang.anjuke.com',
    '新乡':'https://xinxiang.anjuke.com',
    '信阳':'https://xinyang.anjuke.com',
    '咸阳':'https://xianyang.anjuke.com',
    '邢台':'https://xingtai.anjuke.com',
    '孝感':'https://xiaogan.anjuke.com',
    '西宁':'https://xining.anjuke.com',
    '许昌':'https://xuchang.anjuke.com',
    '忻州':'https://xinzhou.anjuke.com',
    '宣城':'https://xuancheng.anjuke.com',
    '咸宁':'https://xianning.anjuke.com',
    '兴安盟':'https://xinganmeng.anjuke.com',
    '新余':'https://xinyu.anjuke.com',
    '西双版纳':'https://bannan.anjuke.com',
    '湘西':'https://xiangxi.anjuke.com',
    '仙桃':'https://xiantao.anjuke.com',
    '锡林郭勒盟':'https://xilinguole.anjuke.com',
    '新泰市':'https://xintaishi.anjuke.com',
    '湘乡':'https://xiangxiang.anjuke.com',
    '兴化':'https://xinghuashi.anjuke.com',
    '兴义':'https://xingyi.anjuke.com',
    '宣威':'https://xuanwei.anjuke.com',
    '项城市':'https://xiangchengshi.anjuke.com',
    '兴城':'https://xingcheng.anjuke.com',
    '新沂':'https://xinyishi.anjuke.com',
    '荥阳':'https://xingyang.anjuke.com',
    '新密':'https://xinmi.anjuke.com',
    '浚县':'https://xunxian.anjuke.com',
    '襄垣':'https://xiangyuanxian.anjuke.com',
    '孝昌':'https://xiaochangxian.anjuke.com',
    '宣汉':'https://xuanhanxian.anjuke.com',
    '象山':'https://xiangshanxian.anjuke.com',
    '沛县':'https://xzpeixian.anjuke.com',
    '老河口':'https://xylaohekou.anjuke.com',
    '新安':'https://xinan.anjuke.com',
    '香河':'https://xianghe.anjuke.com',
    '宜城':'https://xyyicheng.anjuke.com',
    '沙河':'https://xtshahe.anjuke.com',
    '安陆':'https://xganlu.anjuke.com',
    '湘阴':'https://xiangyin.anjuke.com',
    '新昌':'https://xinchang.anjuke.com',
    '盱眙':'https://xuyuxian.anjuke.com',
    '莘县':'https://xinxian.anjuke.com',
    '响水':'https://xiangshuixian.anjuke.com',
    '新野':'https://xinyexian.anjuke.com',
    '烟台':'https://yt.anjuke.com',
    '扬州':'https://yangzhou.anjuke.com',
    '宜昌':'https://yichang.anjuke.com',
    '银川':'https://yinchuan.anjuke.com',
    '阳江':'https://yangjiang.anjuke.com',
    '永州':'https://yongzhou.anjuke.com',
    '玉林':'https://yulinshi.anjuke.com',
    '盐城':'https://yancheng.anjuke.com',
    '岳阳':'https://yueyang.anjuke.com',
    '运城':'https://yuncheng.anjuke.com',
    '宜春':'https://yichun.anjuke.com',
    '营口':'https://yingkou.anjuke.com',
    '榆林':'https://yulin.anjuke.com',
    '宜宾':'https://yibin.anjuke.com',
    '益阳':'https://yiyang.anjuke.com',
    '义乌':'https://yiwu.anjuke.com',
    '玉溪':'https://yuxi.anjuke.com',
    '伊犁':'https://yili.anjuke.com',
    '阳泉':'https://yangquan.anjuke.com',
    '延安':'https://yanan.anjuke.com',
    '鹰潭':'https://yingtan.anjuke.com',
    '延边':'https://yanbian.anjuke.com',
    '云浮':'https://yufu.anjuke.com',
    '雅安':'https://yaan.anjuke.com',
    '阳春':'https://yangchun.anjuke.com',
    '鄢陵':'https://yanling.anjuke.com',
    '伊春':'https://yichunshi.anjuke.com',
    '玉树':'https://yushu.anjuke.com',
    '乐清':'https://yueqing.anjuke.com',
    '禹州':'https://yuzhou.anjuke.com',
    '永新':'https://yongxin.anjuke.com',
    '永康市':'https://yongkangshi.anjuke.com',
    '宜都':'https://yidou.anjuke.com',
    '仪征':'https://yizheng.anjuke.com',
    '延吉':'https://yanji.anjuke.com',
    '扬中':'https://yangzhong.anjuke.com',
    '伊宁':'https://yining.anjuke.com',
    '英德':'https://yingde.anjuke.com',
    '余姚':'https://yuyao.anjuke.com',
    '偃师市':'https://yanshishi.anjuke.com',
    '宜兴':'https://yixing.anjuke.com',
    '永兴':'https://yongxingxian.anjuke.com',
    '云梦':'https://yunmengxian.anjuke.com',
    '玉环县':'https://yuhuanxian.anjuke.com',
    '当阳':'https://ycdangyang.anjuke.com',
    '攸县':'https://youxian.anjuke.com',
    '玉田':'https://yutian.anjuke.com',
    '永春':'https://yongchun.anjuke.com',
    '伊川':'https://yichuan.anjuke.com',
    '沅江':'https://yyruanjiang.anjuke.com',
    '阳谷':'https://yangguxian.anjuke.com',
    '沂南':'https://yinanxian.anjuke.com',
    '沂源':'https://yiyuanxian.anjuke.com',
    '郓城':'https://yunchengxian.anjuke.com',
    '余江':'https://yujiangc.anjuke.com',
    '燕郊':'https://yanjiao.anjuke.com',
    '郑州':'https://zhengzhou.anjuke.com',
    '珠海':'https://zh.anjuke.com',
    '中山':'https://zs.anjuke.com',
    '镇江':'https://zhenjiang.anjuke.com',
    '淄博':'https://zibo.anjuke.com',
    '张家口':'https://zhangjiakou.anjuke.com',
    '株洲':'https://zhuzhou.anjuke.com',
    '漳州':'https://zhangzhou.anjuke.com',
    '湛江':'https://zhanjiang.anjuke.com',
    '肇庆':'https://zhaoqing.anjuke.com',
    '枣庄':'https://zaozhuang.anjuke.com',
    '舟山':'https://zhoushan.anjuke.com',
    '遵义':'https://zunyi.anjuke.com',
    '驻马店':'https://zhumadian.anjuke.com',
    '自贡':'https://zigong.anjuke.com',
    '资阳':'https://ziyang.anjuke.com',
    '周口':'https://zhoukou.anjuke.com',
    '章丘':'https://zhangqiu.anjuke.com',
    '张家界':'https://zhangjiajie.anjuke.com',
    '诸城':'https://zhucheng.anjuke.com',
    '庄河':'https://zhuanghe.anjuke.com',
    '正定':'https://zhengding.anjuke.com',
    '张北':'https://zhangbei.anjuke.com',
    '张掖':'https://zhangye.anjuke.com',
    '昭通':'https://zhaotong.anjuke.com',
    '中卫':'https://weizhong.anjuke.com',
    '赵县':'https://zhaoxian.anjuke.com',
    '邹城市':'https://zouchengshi.anjuke.com',
    '遵化':'https://zunhua.anjuke.com',
    '张家港':'https://zhangjiagang.anjuke.com',
    '枝江':'https://zhijiang.anjuke.com',
    '招远市':'https://zhaoyuanshi.anjuke.com',
    '资兴':'https://zixing.anjuke.com',
    '樟树':'https://zhangshu.anjuke.com',
    '诸暨':'https://zhuji.anjuke.com',
    '涿州市':'https://zhuozhoushi.anjuke.com',
    '枣阳市':'https://zaoyangshi.anjuke.com',
    '泽州':'https://zezhouxian.anjuke.com',
    '邹平县':'https://zoupingxian.anjuke.com',
    '肇州':'https://zhaozhou.anjuke.com',
    '漳浦':'https://zhangpu.anjuke.com',
    '阿坝州':'https://chengdu.anjuke.com',
    '大邑':'https://chengdu.anjuke.com',
    '金堂':'https://chengdu.anjuke.com',
    '淳安':'https://hangzhou.anjuke.com',
    '富阳':'https://hangzhou.anjuke.com',
    '临安':'https://hangzhou.anjuke.com',
    '桐庐':'https://hangzhou.anjuke.com',
    '铜梁':'https://chongqing.anjuke.com',
    '丰都':'https://chongqing.anjuke.com',
    '长寿':'https://chongqing.anjuke.com',
    '涪陵':'https://chongqing.anjuke.com',
    '南川':'https://chongqing.anjuke.com',
    '永川':'https://chongqing.anjuke.com',
    '綦江':'https://chongqing.anjuke.com',
    '黔江':'https://chongqing.anjuke.com',
    '万州':'https://chongqing.anjuke.com',
    '江津':'https://chongqing.anjuke.com',
    '合川':'https://chongqing.anjuke.com',
    '普兰店':'https://dalian.anjuke.com',
    '平阴':'https://jinan.anjuke.com',
    '济阳':'https://jinan.anjuke.com',
    '商河':'https://jinan.anjuke.com',
    '中牟':'https://zhengzhou.anjuke.com',
    '巩义':'https://zhengzhou.anjuke.com',
    '宁乡':'https://cs.anjuke.com',
    '无极':'https://sjz.anjuke.com',
    '辛集':'https://sjz.anjuke.com',
    '元氏':'https://sjz.anjuke.com',
    '即墨':'https://qd.anjuke.com',
    '胶南':'https://qd.anjuke.com',
    '周至':'https://xa.anjuke.com',
    '户县':'https://xa.anjuke.com',
    '蓝田':'https://xa.anjuke.com',
    '宁海':'https://nb.anjuke.com',
    '肥东':'https://hf.anjuke.com',
    '肥西':'https://hf.anjuke.com',
    '庐江':'https://hf.anjuke.com',
    '长丰':'https://hf.anjuke.com',
    '长乐':'https://fz.anjuke.com',
    '连江':'https://fz.anjuke.com',
    '平潭':'https://fz.anjuke.com',
    '宜良':'https://km.anjuke.com',
    '辽中':'https://sy.anjuke.com',
    '新民':'https://sy.anjuke.com',
    '新建':'https://nc.anjuke.com',
    '白沙县':'https://haikou.anjuke.com',
    '儋州市':'https://haikou.anjuke.com',
    '澄迈县':'https://haikou.anjuke.com',
    '定安':'https://haikou.anjuke.com',
    '琼中':'https://haikou.anjuke.com',
    '屯昌':'https://haikou.anjuke.com',
    '文昌市':'https://haikou.anjuke.com',
    '农安':'https://cc.anjuke.com',
    '陵水':'https://sanya.anjuke.com',
    '保亭':'https://sanya.anjuke.com',
    '东方市':'https://sanya.anjuke.com',
    '龙门':'https://huizhou.anjuke.com',
    '永登':'https://lanzhou.anjuke.com',
    '榆中':'https://lanzhou.anjuke.com',
    '文安':'https://langfang.anjuke.com',
    '汝阳':'https://luoyang.anjuke.com',
    '宾阳':'https://nanning.anjuke.com',
    '横县':'https://nanning.anjuke.com',
    '晋安':'https://quanzhou.anjuke.com',
    '上虞':'https://shaoxing.anjuke.com',
    '乐亭':'https://tangshan.anjuke.com',
    '滦县':'https://tangshan.anjuke.com',
    '丰县':'https://xuzhou.anjuke.com',
    '睢宁':'https://xuzhou.anjuke.com',
    '江都':'https://yangzhou.anjuke.com',
    '肇源':'https://daqing.anjuke.com',
    '当涂':'https://maanshan.anjuke.com',
    '巴州':'https://bazhong.anjuke.com',

}



t=''''''
u=''''''

if __name__ == '__main__':
    print('dasdas')