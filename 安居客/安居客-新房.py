import requests
import random
from lxml import etree
import re
import time
from concurrent.futures import ThreadPoolExecutor
from urllib import parse
import pymongo
import redis


class GET:
    def __init__(self):
        self.headers = {'accept': 'application/json, text/plain, */*',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'zh-CN,zh;q=0.9',
                        # 'cookie': 'aQQ_ajkguid=05056b58-1f3d-4a38-8396-078c4268af1d; sessid=bd18fa8b-96e6-4d3a-ac07-2cfbbe168625; id58=CpQMQ2FMFdWhfdcfEx5GAg==; __xsptplus8=8.6.1632623029.1632623040.2%233%7Ccallback.58.com%7C%7C%7C%7C%23%23lhKE6lJwoWe7Tr2mIYvVINHHBoLR7ipR%23; 58tj_uuid=3746ea03-747a-4b58-ac03-7e7cc8fa0a1a; als=0; _ga=GA1.2.1804108362.1632733536; isp=true; ctid=229; cmctid=10106; twe=2; init_refer=https%253A%252F%252Fwww.baidu.com%252Fother.php%253Fsc.K000000p3EapSheHFJZV-Igl6nBOjvzlmDSrddpC7mqtGykehXdRs5VKSZa-4Z--tfC-PHX_ZPKMnQvg6a4m1i8o6AW2jc0yV1cvJN4LxDaWYRB3HKskPtjVz_mELkC-rzo3YucTeGpaKJHKbGmk0v4_IpnabwXaerCs_qwkbh027l-o5yvEPYb2NO9b2p95toAnnmVK-mc5G8UBfawVTmO84fHC.DY_NR2Ar5Od663rj6thm_8jViBjEWXkSUSwMEukmnSrZr1wC4eL_8C5RojPak3S5Zm0.TLFWgv-b5HDkrfK1ThPGujYknHb0THY0IAYq_Q2SYeOP0ZN1ugFxIZ-suHYs0A7bgLw4TARqnsKLULFb5UazEVrO1fKzmLmqnfKdThkxpyfqnHRzrH63rj6kPsKVINqGujYkPjfYP1TdP6KVgv-b5HDknHczn10Y0AdYTAkxpyfqnHczP1n0TZuxpyfqn0KGuAnqiD4a0ZKGujY1nsKWpyfqPjn10APzm1YdP1f4P0%2526ck%253D3350.1.119.376.151.342.152.711%2526dt%253D1635733398%2526wd%253D%2525E5%2525AE%252589%2525E5%2525B1%252585%2525E5%2525AE%2525A2%2526tpl%253Dtpl_12273_25897_22126%2526l%253D1529888817%2526us%253DlinkName%25253D%252525E6%252525A0%25252587%252525E9%252525A2%25252598-%252525E4%252525B8%252525BB%252525E6%252525A0%25252587%252525E9%252525A2%25252598%252526linkText%25253D%252525E5%252525AE%25252589%252525E5%252525B1%25252585%252525E5%252525AE%252525A2-%252525E5%25252585%252525A8%252525E6%25252588%252525BF%252525E6%252525BA%25252590%252525E7%252525BD%25252591%252525EF%252525BC%2525258C%252525E6%25252596%252525B0%252525E6%25252588%252525BF%25252520%252525E4%252525BA%2525258C%252525E6%25252589%2525258B%252525E6%25252588%252525BF%25252520%252525E6%2525258C%25252591%252525E5%252525A5%252525BD%252525E6%25252588%252525BF%252525E4%252525B8%2525258A%252525E5%252525AE%25252589%252525E5%252525B1%25252585%252525E5%252525AE%252525A2%252525EF%252525BC%25252581%252526linkType%25253D; new_uv=9; _gid=GA1.2.632837752.1635733404; xxzl_cid=378a0b5c98514100a98b1d0f6be6ba66; xzuid=726dbb66-823a-4d29-8ae2-9b9312b945f1; obtain_by=2; new_session=0; lp_lt_ut=25cf080af144e4a0a8de8116bd78fd3c',
                        'origin': 'https://www.anjuke.com',
                        'referer': 'https://www.anjuke.com/',
                        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': "Windows",
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-site',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
        # self.citys = {}
        self.citys = {'鞍山': 'https://as.fang.anjuke.com/', '安阳': 'https://ay.fang.anjuke.com/',
                      '安庆': 'https://aq.fang.anjuke.com/', '安康': 'https://ank.fang.anjuke.com/',
                      '安顺': 'https://ans.fang.anjuke.com/', '阿坝': 'https://ab.fang.anjuke.com/',
                      '阿克苏': 'https://aks.fang.anjuke.com/', '阿拉尔': 'https://ale.fang.anjuke.com/',
                      '阿拉善盟': 'https://alsm.fang.anjuke.com/', '安丘': 'https://anq.fang.anjuke.com/loupan/',
                      '安宁': 'https://ann.fang.anjuke.com/loupan/', '安吉县': 'https://anji.fang.anjuke.com/',
                      '安溪': 'https://ax.fang.anjuke.com/', '林州': 'https://aylz.fang.anjuke.com/',
                      '安岳': 'https://anyuexian.fang.anjuke.com/', '北京': 'https://bj.fang.anjuke.com/',
                      '保定': 'https://bd.fang.anjuke.com/', '包头': 'https://bt.fang.anjuke.com/',
                      '滨州': 'https://bz.fang.anjuke.com/', '宝鸡': 'https://bao.fang.anjuke.com/',
                      '蚌埠': 'https://bb.fang.anjuke.com/', '本溪': 'https://bx.fang.anjuke.com/',
                      '北海': 'https://bh.fang.anjuke.com/', '巴音郭楞': 'https://bygl.fang.anjuke.com/',
                      '巴中': 'https://ba.fang.anjuke.com/', '巴彦淖尔市': 'https://bycem.fang.anjuke.com/',
                      '亳州': 'https://boz.fang.anjuke.com/', '白银': 'https://by.fang.anjuke.com/',
                      '白城': 'https://bc.fang.anjuke.com/', '百色': 'https://bais.fang.anjuke.com/',
                      '白山': 'https://baish.fang.anjuke.com/', '博尔塔拉': 'https://betl.fang.anjuke.com/',
                      '毕节': 'https://bij.fang.anjuke.com/', '保山': 'https://bs.fang.anjuke.com/',
                      '霸州': 'https://baz.fang.anjuke.com/loupan/', '北票': 'https://bp.fang.anjuke.com/loupan/',
                      '北流': 'https://beil.fang.anjuke.com/loupan/', '博白': 'https://bob.fang.anjuke.com/',
                      '博罗': 'https://boluo.fang.anjuke.com/', '宝应县': 'https://baoyingx.fang.anjuke.com/',
                      '博兴': 'https://box.fang.anjuke.com/', '成都': 'https://cd.fang.anjuke.com/',
                      '重庆': 'https://cq.fang.anjuke.com/', '长沙': 'https://cs.fang.anjuke.com/',
                      '常州': 'https://cz.fang.anjuke.com/', '长春': 'https://cc.fang.anjuke.com/',
                      '沧州': 'https://cang.fang.anjuke.com/', '昌吉': 'https://cj.fang.anjuke.com/',
                      '赤峰': 'https://cf.fang.anjuke.com/', '常德': 'https://chd.fang.anjuke.com/',
                      '郴州': 'https://chen.fang.anjuke.com/', '承德': 'https://cheng.fang.anjuke.com/',
                      '长治': 'https://chang.fang.anjuke.com/', '池州': 'https://chi.fang.anjuke.com/',
                      '滁州': 'https://chu.fang.anjuke.com/', '朝阳': 'https://cy.fang.anjuke.com/',
                      '潮州': 'https://chao.fang.anjuke.com/', '楚雄': 'https://cx.fang.anjuke.com/',
                      '巢湖': 'https://hf.fang.anjuke.com/', '昌都': 'https://changd.fang.anjuke.com/',
                      '长葛': 'https://cg.fang.anjuke.com/', '崇左': 'https://chongz.fang.anjuke.com/',
                      '赤壁': 'https://chb.fang.anjuke.com/loupan/', '岑溪': 'https://cengx.fang.anjuke.com/loupan/',
                      '慈溪': 'https://cix.fang.anjuke.com/loupan/', '慈利': 'https://clzjj.fang.anjuke.com/',
                      '长岭': 'https://changl.fang.anjuke.com/', '长兴': 'https://changxing.fang.anjuke.com/',
                      '苍南县': 'https://cangnanxian.fang.anjuke.com/', '曹县': 'https://caoxian.fang.anjuke.com/',
                      '长垣县': 'https://changyuan.fang.anjuke.com/', '昌乐': 'https://cl.fang.anjuke.com/',
                      '沧县': 'https://cxcz.fang.anjuke.com/', '长宁': 'https://cn.fang.anjuke.com/',
                      '磁县': 'https://cixian.fang.anjuke.com/', '大连': 'https://dl.fang.anjuke.com/',
                      '东莞': 'https://dg.fang.anjuke.com/', '德阳': 'https://de.fang.anjuke.com/',
                      '大理': 'https://da.fang.anjuke.com/', '德州': 'https://dz.fang.anjuke.com/',
                      '东营': 'https://dy.fang.anjuke.com/', '大庆': 'https://dq.fang.anjuke.com/',
                      '丹东': 'https://dd.fang.anjuke.com/', '大同': 'https://dt.fang.anjuke.com/',
                      '达州': 'https://dzh.fang.anjuke.com/', '大丰': 'https://df.fang.anjuke.com/',
                      '德宏': 'https://dh.fang.anjuke.com/', '定州': 'https://ding.fang.anjuke.com/',
                      '迪庆': 'https://diq.fang.anjuke.com/', '定西': 'https://dx.fang.anjuke.com/',
                      '大兴安岭': 'https://dxal.fang.anjuke.com/', '东台': 'https://dongt.fang.anjuke.com/loupan/',
                      '邓州': 'https://dengz.fang.anjuke.com/loupan/', '东方': 'https://dfx.fang.anjuke.com/',
                      '儋州': 'https://danz.fang.anjuke.com/', '丹阳': 'https://danyangshi.fang.anjuke.com/loupan/',
                      '灯塔': 'https://dengt.fang.anjuke.com/loupan/', '敦煌': 'https://dunh.fang.anjuke.com/loupan/',
                      '东阳': 'https://dongyang.fang.anjuke.com/loupan/', '东至': 'https://dongz.fang.anjuke.com/',
                      '德清': 'https://deqing.fang.anjuke.com/', '东海': 'https://donghai.fang.anjuke.com/',
                      '单县': 'https://shanxian.fang.anjuke.com/', '凤城': 'https://ddfc.fang.anjuke.com/',
                      '禹城': 'https://dzyc.fang.anjuke.com/', '大竹': 'https://dzsc.fang.anjuke.com/',
                      '定边': 'https://db.fang.anjuke.com/', '东明': 'https://dm.fang.anjuke.com/',
                      '东平': 'https://dp.fang.anjuke.com/', '大悟': 'https://dw.fang.anjuke.com/',
                      '鄂尔多斯': 'https://eeds.fang.anjuke.com/', '恩施': 'https://es.fang.anjuke.com/',
                      '鄂州': 'https://ez.fang.anjuke.com/', '佛山': 'https://fs.fang.anjuke.com/',
                      '福州': 'https://fz.fang.anjuke.com/', '阜阳': 'https://fy.fang.anjuke.com/',
                      '抚顺': 'https://fsh.fang.anjuke.com/', '阜新': 'https://fx.fang.anjuke.com/',
                      '抚州': 'https://fuz.fang.anjuke.com/', '防城港': 'https://fcg.fang.anjuke.com/',
                      '肥城市': 'https://fcs.fang.anjuke.com/loupan/', '丰城': 'https://fengc.fang.anjuke.com/loupan/',
                      '福安': 'https://fa.fang.anjuke.com/loupan/', '福鼎': 'https://fding.fang.anjuke.com/loupan/',
                      '范县': 'https://fanx.fang.anjuke.com/', '分宜': 'https://fyxy.fang.anjuke.com/',
                      '扶余': 'https://fuy.fang.anjuke.com/', '阜宁': 'https://fn.fang.anjuke.com/',
                      '浮梁': 'https://fl.fang.anjuke.com/', '府谷': 'https://gf.fang.anjuke.com/',
                      '广州': 'https://gz.fang.anjuke.com/', '贵阳': 'https://gy.fang.anjuke.com/',
                      '桂林': 'https://gl.fang.anjuke.com/', '赣州': 'https://gan.fang.anjuke.com/',
                      '广安': 'https://ga.fang.anjuke.com/', '贵港': 'https://gg.fang.anjuke.com/',
                      '广元': 'https://guang.fang.anjuke.com/', '甘孜': 'https://gaz.fang.anjuke.com/',
                      '甘南': 'https://gn.fang.anjuke.com/', '固原': 'https://gu.fang.anjuke.com/',
                      '公主岭市': 'https://gzls.fang.anjuke.com/loupan/', '高密市': 'https://gms.fang.anjuke.com/loupan/',
                      '格尔木': 'https://gem.fang.anjuke.com/loupan/', '广汉': 'https://gh.fang.anjuke.com/',
                      '桂平': 'https://gp.fang.anjuke.com/loupan/', '高安': 'https://gaoanshi.fang.anjuke.com/loupan/',
                      '固始': 'https://gs.fang.anjuke.com/', '桂阳': 'https://guiy.fang.anjuke.com/',
                      '高平': 'https://gaop.fang.anjuke.com/', '广饶县': 'https://guangrao.fang.anjuke.com/',
                      '灌云县': 'https://guanyun.fang.anjuke.com/', '灌南县': 'https://guannan.fang.anjuke.com/',
                      '固安': 'https://gua.fang.anjuke.com/', '谷城': 'https://gc.fang.anjuke.com/',
                      '高唐': 'https://gaot.fang.anjuke.com/', '冠县': 'https://gx.fang.anjuke.com/',
                      '杭州': 'https://hz.fang.anjuke.com/', '合肥': 'https://hf.fang.anjuke.com/',
                      '哈尔滨': 'https://heb.fang.anjuke.com/', '海口': 'https://hai.fang.anjuke.com/',
                      '惠州': 'https://hui.fang.anjuke.com/', '邯郸': 'https://hd.fang.anjuke.com/',
                      '呼和浩特': 'https://hhht.fang.anjuke.com/', '黄冈': 'https://hg.fang.anjuke.com/',
                      '淮南': 'https://hn.fang.anjuke.com/', '黄山': 'https://hsh.fang.anjuke.com/',
                      '鹤壁': 'https://hb.fang.anjuke.com/', '衡阳': 'https://hy.fang.anjuke.com/',
                      '湖州': 'https://hu.fang.anjuke.com/', '衡水': 'https://hs.fang.anjuke.com/',
                      '汉中': 'https://han.fang.anjuke.com/', '淮安': 'https://ha.fang.anjuke.com/',
                      '黄石': 'https://huang.fang.anjuke.com/', '菏泽': 'https://hez.fang.anjuke.com/',
                      '怀化': 'https://hh.fang.anjuke.com/', '淮北': 'https://huai.fang.anjuke.com/',
                      '葫芦岛': 'https://hld.fang.anjuke.com/', '河源': 'https://he.fang.anjuke.com/',
                      '红河': 'https://hong.fang.anjuke.com/', '哈密': 'https://hami.fang.anjuke.com/',
                      '鹤岗': 'https://heg.fang.anjuke.com/', '呼伦贝尔': 'https://hlbe.fang.anjuke.com/',
                      '海东': 'https://haid.fang.anjuke.com/', '海南': 'https://hain.fang.anjuke.com/',
                      '河池': 'https://hc.fang.anjuke.com/', '黑河': 'https://heih.fang.anjuke.com/',
                      '贺州': 'https://hezh.fang.anjuke.com/', '霍邱': 'https://hq.fang.anjuke.com/',
                      '和田': 'https://ht.fang.anjuke.com/', '海西': 'https://hx.fang.anjuke.com/',
                      '黄骅': 'https://huangh.fang.anjuke.com/loupan/', '河间': 'https://hj.fang.anjuke.com/loupan/',
                      '韩城': 'https://hanch.fang.anjuke.com/loupan/',
                      '汉川市': 'https://hanchuansh.fang.anjuke.com/loupan/', '海门': 'https://hm.fang.anjuke.com/loupan/',
                      '海宁': 'https://haining.fang.anjuke.com/loupan/', '淮滨': 'https://huaib.fang.anjuke.com/',
                      '海安': 'https://haian.fang.anjuke.com/', '惠东': 'https://huidong.fang.anjuke.com/',
                      '海丰县': 'https://haifengxian.fang.anjuke.com/', '桓台县': 'https://huantaixian.fang.anjuke.com/',
                      '常宁': 'https://hycn.fang.anjuke.com/', '海盐': 'https://haiyan.fang.anjuke.com/',
                      '永城': 'https://hnyc.fang.anjuke.com/', '滑县': 'https://huax.fang.anjuke.com/',
                      '衡东': 'https://hengd.fang.anjuke.com/', '华容': 'https://hr.fang.anjuke.com/',
                      '济南': 'https://jn.fang.anjuke.com/', '嘉兴': 'https://jx.fang.anjuke.com/',
                      '吉林': 'https://jl.fang.anjuke.com/', '江门': 'https://jm.fang.anjuke.com/',
                      '荆门': 'https://jing.fang.anjuke.com/', '锦州': 'https://jz.fang.anjuke.com/',
                      '景德镇': 'https://jdz.fang.anjuke.com/', '吉安': 'https://ja.fang.anjuke.com/',
                      '济宁': 'https://ji.fang.anjuke.com/', '金华': 'https://jh.fang.anjuke.com/',
                      '揭阳': 'https://jy.fang.anjuke.com/', '晋中': 'https://jin.fang.anjuke.com/',
                      '九江': 'https://jj.fang.anjuke.com/', '焦作': 'https://jiao.fang.anjuke.com/',
                      '晋城': 'https://jc.fang.anjuke.com/', '荆州': 'https://jzh.fang.anjuke.com/',
                      '佳木斯': 'https://jms.fang.anjuke.com/', '酒泉': 'https://jq.fang.anjuke.com/',
                      '鸡西': 'https://jixi.fang.anjuke.com/', '济源': 'https://jiy.fang.anjuke.com/',
                      '金昌': 'https://jinc.fang.anjuke.com/', '嘉峪关': 'https://jyg.fang.anjuke.com/',
                      '江阴': 'https://jiangy.fang.anjuke.com/loupan/', '靖江': 'https://jingj.fang.anjuke.com/loupan/',
                      '简阳市': 'https://jys.fang.anjuke.com/loupan/', '金坛': 'https://jint.fang.anjuke.com/loupan/',
                      '晋江': 'https://jinjiangs.fang.anjuke.com/loupan/', '句容': 'https://jr.fang.anjuke.com/loupan/',
                      '嘉鱼': 'https://jiay.fang.anjuke.com/', '建湖': 'https://jianhu.fang.anjuke.com/',
                      '嘉善': 'https://jiashanx.fang.anjuke.com/', '莒县': 'https://juxian.fang.anjuke.com/',
                      '昌邑': 'https://jlcy.fang.anjuke.com/', '桦甸': 'https://jlhd.fang.anjuke.com/',
                      '京山': 'https://jmjs.fang.anjuke.com/', '进贤': 'https://jinx.fang.anjuke.com/',
                      '金湖': 'https://jinh.fang.anjuke.com/', '钟祥': 'https://jmzx.fang.anjuke.com/',
                      '孟州': 'https://jzmz.fang.anjuke.com/', '靖边': 'https://jb.fang.anjuke.com/',
                      '巨野': 'https://jyhz.fang.anjuke.com/', '鄄城': 'https://juanc.fang.anjuke.com/',
                      '昆明': 'https://km.fang.anjuke.com/', '昆山': 'https://ks.fang.anjuke.com/',
                      '开封': 'https://kf.fang.anjuke.com/', '喀什': 'https://ka.fang.anjuke.com/',
                      '克拉玛依': 'https://klmy.fang.anjuke.com/', '克孜勒苏': 'https://kzls.fang.anjuke.com/',
                      '开平': 'https://kp.fang.anjuke.com/loupan/', '兰考': 'https://kflk.fang.anjuke.com/',
                      '兰州': 'https://lz.fang.anjuke.com/', '廊坊': 'https://lf.fang.anjuke.com/',
                      '洛阳': 'https://ly.fang.anjuke.com/', '柳州': 'https://lzh.fang.anjuke.com/',
                      '莱芜': 'https://lw.fang.anjuke.com/', '六安': 'https://la.fang.anjuke.com/',
                      '泸州': 'https://lu.fang.anjuke.com/', '丽江': 'https://lj.fang.anjuke.com/',
                      '临沂': 'https://liny.fang.anjuke.com/', '聊城': 'https://lc.fang.anjuke.com/',
                      '连云港': 'https://lyg.fang.anjuke.com/', '丽水': 'https://li.fang.anjuke.com/',
                      '娄底': 'https://ld.fang.anjuke.com/', '乐山': 'https://le.fang.anjuke.com/',
                      '辽阳': 'https://liao.fang.anjuke.com/', '拉萨': 'https://ls.fang.anjuke.com/',
                      '临汾': 'https://lin.fang.anjuke.com/', '龙岩': 'https://long.fang.anjuke.com/',
                      '漯河': 'https://lh.fang.anjuke.com/', '凉山': 'https://liang.fang.anjuke.com/',
                      '六盘水': 'https://lps.fang.anjuke.com/', '辽源': 'https://liaoy.fang.anjuke.com/',
                      '来宾': 'https://lb.fang.anjuke.com/', '临沧': 'https://linc.fang.anjuke.com/',
                      '临夏': 'https://lx.fang.anjuke.com/', '临猗': 'https://linyis.fang.anjuke.com/',
                      '林芝': 'https://lizh.fang.anjuke.com/', '陇南': 'https://ln.fang.anjuke.com/',
                      '吕梁': 'https://lvl.fang.anjuke.com/', '临海市': 'https://lihs.fang.anjuke.com/loupan/',
                      '龙海市': 'https://lhs.fang.anjuke.com/loupan/', '醴陵市': 'https://lls.fang.anjuke.com/loupan/',
                      '临清': 'https://linq.fang.anjuke.com/loupan/', '龙口': 'https://lk.fang.anjuke.com/loupan/',
                      '莱阳': 'https://lay.fang.anjuke.com/loupan/', '溧阳': 'https://liy.fang.anjuke.com/loupan/',
                      '灵宝市': 'https://lingb.fang.anjuke.com/loupan/', '冷水江': 'https://lshj.fang.anjuke.com/loupan/',
                      '涟源': 'https://liany.fang.anjuke.com/loupan/', '陆丰': 'https://lufengshi.fang.anjuke.com/loupan/',
                      '乐平市': 'https://lp.fang.anjuke.com/loupan/', '莱州市': 'https://lzs.fang.anjuke.com/loupan/',
                      '梨树': 'https://lis.fang.anjuke.com/', '利津': 'https://lij.fang.anjuke.com/',
                      '柳林': 'https://liul.fang.anjuke.com/', '滦南': 'https://luann.fang.anjuke.com/',
                      '临朐': 'https://linj.fang.anjuke.com/', '宜阳': 'https://lyyiy.fang.anjuke.com/',
                      '乐陵': 'https://ll.fang.anjuke.com/', '澧县': 'https://lxcd.fang.anjuke.com/',
                      '梁山': 'https://liangs.fang.anjuke.com/', '临邑': 'https://lydz.fang.anjuke.com/',
                      '鹿邑': 'https://luy.fang.anjuke.com/', '绵阳': 'https://my.fang.anjuke.com/',
                      '茂名': 'https://mm.fang.anjuke.com/', '马鞍山': 'https://mas.fang.anjuke.com/',
                      '牡丹江': 'https://mdj.fang.anjuke.com/', '眉山': 'https://ms.fang.anjuke.com/',
                      '梅州': 'https://mz.fang.anjuke.com/', '梅河口': 'https://mhk.fang.anjuke.com/loupan/',
                      '弥勒': 'https://ml.fang.anjuke.com/', '渑池': 'https://mc.fang.anjuke.com/',
                      '孟津': 'https://mj.fang.anjuke.com/', '南京': 'https://nj.fang.anjuke.com/',
                      '宁波': 'https://nb.fang.anjuke.com/', '南昌': 'https://nc.fang.anjuke.com/',
                      '南宁': 'https://nn.fang.anjuke.com/', '南通': 'https://nt.fang.anjuke.com/',
                      '南充': 'https://nan.fang.anjuke.com/', '南阳': 'https://ny.fang.anjuke.com/',
                      '宁德': 'https://nd.fang.anjuke.com/', '内江': 'https://nei.fang.anjuke.com/',
                      '南平': 'https://np.fang.anjuke.com/', '那曲': 'https://nq.fang.anjuke.com/',
                      '怒江': 'https://nu.fang.anjuke.com/', '南安': 'https://na.fang.anjuke.com/loupan/',
                      '宁国': 'https://ningg.fang.anjuke.com/loupan/', '南城': 'https://nanc.fang.anjuke.com/',
                      '南县': 'https://nx.fang.anjuke.com/', '南漳': 'https://nz.fang.anjuke.com/',
                      '宁津': 'https://ningj.fang.anjuke.com/', '宁阳': 'https://ningy.fang.anjuke.com/',
                      '攀枝花': 'https://pzh.fang.anjuke.com/', '平顶山': 'https://pds.fang.anjuke.com/',
                      '盘锦': 'https://pj.fang.anjuke.com/', '萍乡': 'https://px.fang.anjuke.com/',
                      '濮阳': 'https://py.fang.anjuke.com/', '莆田': 'https://pt.fang.anjuke.com/',
                      '普洱': 'https://pe.fang.anjuke.com/', '平凉': 'https://pl.fang.anjuke.com/',
                      '邳州': 'https://piz.fang.anjuke.com/loupan/', '蓬莱市': 'https://pls.fang.anjuke.com/loupan/',
                      '平湖': 'https://ph.fang.anjuke.com/loupan/', '平阳': 'https://pingyangxian.fang.anjuke.com/',
                      '平邑': 'https://pingy.fang.anjuke.com/', '磐石': 'https://ps.fang.anjuke.com/',
                      '青岛': 'https://qd.fang.anjuke.com/', '秦皇岛': 'https://qhd.fang.anjuke.com/',
                      '泉州': 'https://qz.fang.anjuke.com/', '曲靖': 'https://qj.fang.anjuke.com/',
                      '齐齐哈尔': 'https://qqhe.fang.anjuke.com/', '衢州': 'https://qu.fang.anjuke.com/',
                      '清远': 'https://qy.fang.anjuke.com/', '钦州': 'https://qin.fang.anjuke.com/',
                      '庆阳': 'https://qing.fang.anjuke.com/', '黔东南': 'https://qdn.fang.anjuke.com/',
                      '潜江': 'https://qian.fang.anjuke.com/', '清徐': 'https://qx.fang.anjuke.com/',
                      '黔南': 'https://qn.fang.anjuke.com/', '七台河': 'https://qth.fang.anjuke.com/',
                      '黔西南': 'https://qxn.fang.anjuke.com/', '迁安市': 'https://qns.fang.anjuke.com/loupan/',
                      '青州市': 'https://qzs.fang.anjuke.com/loupan/', '清镇': 'https://qzh.fang.anjuke.com/loupan/',
                      '琼海': 'https://qh.fang.anjuke.com/', '沁阳': 'https://qinyangshi.fang.anjuke.com/loupan/',
                      '启东': 'https://qid.fang.anjuke.com/loupan/', '淇县': 'https://qxhb.fang.anjuke.com/',
                      '祁阳': 'https://qiy.fang.anjuke.com/', '渠县': 'https://qux.fang.anjuke.com/',
                      '杞县': 'https://qixianqu.fang.anjuke.com/', '迁西': 'https://qianx.fang.anjuke.com/',
                      '栖霞': 'https://qix.fang.anjuke.com/', '江山': 'https://qzjs.fang.anjuke.com/',
                      '齐河': 'https://qih.fang.anjuke.com/', '祁东': 'https://qidongxian.fang.anjuke.com/',
                      '日照': 'https://rz.fang.anjuke.com/', '日喀则': 'https://rkz.fang.anjuke.com/',
                      '瑞安': 'https://ra.fang.anjuke.com/', '汝州市': 'https://rzs.fang.anjuke.com/loupan/',
                      '任丘市': 'https://rqs.fang.anjuke.com/loupan/', '乳山市': 'https://rsh.fang.anjuke.com/loupan/',
                      '仁怀': 'https://rh.fang.anjuke.com/', '如皋': 'https://rg.fang.anjuke.com/loupan/',
                      '荣成市': 'https://rcheng.fang.anjuke.com/loupan/', '如东': 'https://rudong.fang.anjuke.com/',
                      '仁寿': 'https://renshouxian.fang.anjuke.com/', '上海': 'https://sh.fang.anjuke.com/',
                      '深圳': 'https://sz.fang.anjuke.com/', '苏州': 'https://su.fang.anjuke.com/',
                      '石家庄': 'https://sjz.fang.anjuke.com/', '沈阳': 'https://shen.fang.anjuke.com/',
                      '三亚': 'https://sy.fang.anjuke.com/', '绍兴': 'https://sx.fang.anjuke.com/',
                      '汕头': 'https://st.fang.anjuke.com/', '十堰': 'https://shi.fang.anjuke.com/',
                      '三门峡': 'https://smx.fang.anjuke.com/', '三明': 'https://sm.fang.anjuke.com/',
                      '韶关': 'https://sg.fang.anjuke.com/', '商丘': 'https://sq.fang.anjuke.com/',
                      '宿迁': 'https://suq.fang.anjuke.com/', '绥化': 'https://sui.fang.anjuke.com/',
                      '邵阳': 'https://shao.fang.anjuke.com/', '遂宁': 'https://sn.fang.anjuke.com/',
                      '上饶': 'https://sr.fang.anjuke.com/', '四平': 'https://sip.fang.anjuke.com/',
                      '石河子': 'https://shz.fang.anjuke.com/', '顺德': 'https://sd.fang.anjuke.com/',
                      '宿州': 'https://suz.fang.anjuke.com/', '松原': 'https://song.fang.anjuke.com/',
                      '沭阳': 'https://shuy.fang.anjuke.com/', '石嘴山': 'https://szs.fang.anjuke.com/',
                      '随州': 'https://suiz.fang.anjuke.com/', '朔州': 'https://shuo.fang.anjuke.com/',
                      '汕尾': 'https://sw.fang.anjuke.com/', '商洛': 'https://sl.fang.anjuke.com/',
                      '神农架': 'https://snj.fang.anjuke.com/', '双鸭山': 'https://sys.fang.anjuke.com/',
                      '石狮': 'https://shis.fang.anjuke.com/loupan/', '三河市': 'https://shs.fang.anjuke.com/loupan/',
                      '寿光': 'https://shg.fang.anjuke.com/loupan/', '嵊州': 'https://shzhou.fang.anjuke.com/loupan/',
                      '松滋': 'https://songz.fang.anjuke.com/loupan/', '上杭': 'https://shly.fang.anjuke.com/',
                      '睢县': 'https://sxsq.fang.anjuke.com/', '沙洋': 'https://shay.fang.anjuke.com/',
                      '邵东': 'https://shaod.fang.anjuke.com/', '射洪': 'https://sheh.fang.anjuke.com/',
                      '双峰': 'https://sf.fang.anjuke.com/', '随县': 'https://szsx.fang.anjuke.com/',
                      '邵阳县': 'https://syx.fang.anjuke.com/', '泗阳县': 'https://siyang.fang.anjuke.com/',
                      '泗洪县': 'https://sihong.fang.anjuke.com/', '安达': 'https://shad.fang.anjuke.com/',
                      '肇东': 'https://shzd.fang.anjuke.com/', '广水': 'https://szgs.fang.anjuke.com/',
                      '孝义': 'https://sxxy.fang.anjuke.com/', '商水': 'https://ss.fang.anjuke.com/',
                      '射阳': 'https://syyc.fang.anjuke.com/', '涉县': 'https://sxhd.fang.anjuke.com/',
                      '沈丘': 'https://shenq.fang.anjuke.com/', '神木': 'https://shenmu.fang.anjuke.com/',
                      '天津': 'https://tj.fang.anjuke.com/', '太原': 'https://ty.fang.anjuke.com/',
                      '泰州': 'https://tz.fang.anjuke.com/', '唐山': 'https://ts.fang.anjuke.com/',
                      '泰安': 'https://ta.fang.anjuke.com/', '台州': 'https://tai.fang.anjuke.com/',
                      '铁岭': 'https://tl.fang.anjuke.com/', '通辽': 'https://tongl.fang.anjuke.com/',
                      '铜陵': 'https://tong.fang.anjuke.com/', '天水': 'https://tian.fang.anjuke.com/',
                      '通化': 'https://th.fang.anjuke.com/', '台山': 'https://taish.fang.anjuke.com/',
                      '铜川': 'https://tc.fang.anjuke.com/', '吐鲁番': 'https://tlf.fang.anjuke.com/',
                      '天门': 'https://tm.fang.anjuke.com/', '桐城': 'https://tongc.fang.anjuke.com/',
                      '铜仁': 'https://tr.fang.anjuke.com/', '泰兴': 'https://taix.fang.anjuke.com/loupan/',
                      '滕州市': 'https://tzs.fang.anjuke.com/loupan/', '桐乡': 'https://tx.fang.anjuke.com/loupan/',
                      '天长': 'https://tch.fang.anjuke.com/loupan/', '通许': 'https://tongxu.fang.anjuke.com/',
                      '开原': 'https://tlky.fang.anjuke.com/', '太康': 'https://tk.fang.anjuke.com/',
                      '郯城': 'https://tancheng.fang.anjuke.com/', '武汉': 'https://wh.fang.anjuke.com/',
                      '无锡': 'https://wx.fang.anjuke.com/', '威海': 'https://wei.fang.anjuke.com/',
                      '潍坊': 'https://wf.fang.anjuke.com/', '乌鲁木齐': 'https://wlmq.fang.anjuke.com/',
                      '温州': 'https://wz.fang.anjuke.com/', '芜湖': 'https://wuh.fang.anjuke.com/',
                      '梧州': 'https://wu.fang.anjuke.com/', '渭南': 'https://wn.fang.anjuke.com/',
                      '乌海': 'https://wuhai.fang.anjuke.com/', '文山': 'https://ws.fang.anjuke.com/',
                      '武威': 'https://wuwei.fang.anjuke.com/', '乌兰察布': 'https://wlcb.fang.anjuke.com/',
                      '瓦房店': 'https://wfd.fang.anjuke.com/', '五家渠': 'https://wjq.fang.anjuke.com/',
                      '武夷山': 'https://wys.fang.anjuke.com/', '吴忠': 'https://wuz.fang.anjuke.com/',
                      '五指山': 'https://wzs.fang.anjuke.com/', '温岭': 'https://wls.fang.anjuke.com/loupan/',
                      '武安市': 'https://was.fang.anjuke.com/loupan/', '文昌': 'https://wenchangshi.fang.anjuke.com/',
                      '武穴': 'https://wux.fang.anjuke.com/loupan/', '万宁': 'https://wann.fang.anjuke.com/',
                      '尉氏': 'https://weishixian.fang.anjuke.com/', '无为': 'https://ww.fang.anjuke.com/',
                      '温县': 'https://wenxian.fang.anjuke.com/', '无棣': 'https://wd.fang.anjuke.com/',
                      '微山': 'https://wsjn.fang.anjuke.com/', '汶上': 'https://wsj.fang.anjuke.com/',
                      '武义': 'https://wy.fang.anjuke.com/', '西安': 'https://xa.fang.anjuke.com/',
                      '厦门': 'https://xm.fang.anjuke.com/', '徐州': 'https://xz.fang.anjuke.com/',
                      '湘潭': 'https://xiang.fang.anjuke.com/', '襄阳': 'https://xy.fang.anjuke.com/',
                      '新乡': 'https://xx.fang.anjuke.com/', '信阳': 'https://xiny.fang.anjuke.com/',
                      '咸阳': 'https://xiany.fang.anjuke.com/', '邢台': 'https://xt.fang.anjuke.com/',
                      '孝感': 'https://xg.fang.anjuke.com/', '西宁': 'https://xn.fang.anjuke.com/',
                      '许昌': 'https://xc.fang.anjuke.com/', '忻州': 'https://xin.fang.anjuke.com/',
                      '宣城': 'https://xuan.fang.anjuke.com/', '咸宁': 'https://xiann.fang.anjuke.com/',
                      '兴安盟': 'https://xam.fang.anjuke.com/', '新余': 'https://xinyu.fang.anjuke.com/',
                      '西双版纳': 'https://bn.fang.anjuke.com/', '湘西': 'https://xiangx.fang.anjuke.com/',
                      '仙桃': 'https://xiant.fang.anjuke.com/', '锡林郭勒盟': 'https://xl.fang.anjuke.com/',
                      '新泰市': 'https://xts.fang.anjuke.com/loupan/', '兴化': 'https://xh.fang.anjuke.com/loupan/',
                      '宣威': 'https://xuanw.fang.anjuke.com/loupan/', '项城市': 'https://xiangch.fang.anjuke.com/loupan/',
                      '新沂': 'https://xinyi.fang.anjuke.com/loupan/', '浚县': 'https://juanxian.fang.anjuke.com/',
                      '襄垣': 'https://xiangyuanxian.fang.anjuke.com/', '孝昌': 'https://xiaochang.fang.anjuke.com/',
                      '宣汉': 'https://xuanhan.fang.anjuke.com/', '象山': 'https://xiangshanxian.fang.anjuke.com/',
                      '沛县': 'https://xzpeixian.fang.anjuke.com/', '老河口': 'https://xylhk.fang.anjuke.com/',
                      '新安': 'https://xina.fang.anjuke.com/', '香河': 'https://xiangh.fang.anjuke.com/',
                      '宜城': 'https://xyyc.fang.anjuke.com/', '沙河': 'https://xtsh.fang.anjuke.com/',
                      '安陆': 'https://xgal.fang.anjuke.com/', '湘阴': 'https://xyyy.fang.anjuke.com/',
                      '新昌': 'https://xcsx.fang.anjuke.com/', '盱眙': 'https://xyha.fang.anjuke.com/',
                      '莘县': 'https://xxlc.fang.anjuke.com/', '响水': 'https://xs.fang.anjuke.com/',
                      '新野': 'https://xyny.fang.anjuke.com/', '烟台': 'https://yt.fang.anjuke.com/',
                      '扬州': 'https://yz.fang.anjuke.com/', '宜昌': 'https://yi.fang.anjuke.com/',
                      '银川': 'https://yin.fang.anjuke.com/', '阳江': 'https://yj.fang.anjuke.com/',
                      '永州': 'https://yong.fang.anjuke.com/', '玉林': 'https://yu.fang.anjuke.com/',
                      '盐城': 'https://yan.fang.anjuke.com/', '岳阳': 'https://yy.fang.anjuke.com/',
                      '运城': 'https://yun.fang.anjuke.com/', '宜春': 'https://ych.fang.anjuke.com/',
                      '营口': 'https://yk.fang.anjuke.com/', '榆林': 'https://yl.fang.anjuke.com/',
                      '宜宾': 'https://yb.fang.anjuke.com/', '益阳': 'https://yiy.fang.anjuke.com/',
                      '义乌': 'https://yw.fang.anjuke.com/', '玉溪': 'https://yx.fang.anjuke.com/',
                      '伊犁': 'https://yili.fang.anjuke.com/', '阳泉': 'https://yq.fang.anjuke.com/',
                      '延安': 'https://yanan.fang.anjuke.com/', '鹰潭': 'https://ying.fang.anjuke.com/',
                      '延边': 'https://yanb.fang.anjuke.com/', '云浮': 'https://yf.fang.anjuke.com/',
                      '雅安': 'https://ya.fang.anjuke.com/', '阳春': 'https://yang.fang.anjuke.com/',
                      '鄢陵': 'https://yanl.fang.anjuke.com/', '伊春': 'https://yichuns.fang.anjuke.com/',
                      '乐清': 'https://yue.fang.anjuke.com/', '禹州': 'https://yuzh.fang.anjuke.com/',
                      '永康市': 'https://yks.fang.anjuke.com/loupan/', '宜都': 'https://yd.fang.anjuke.com/loupan/',
                      '扬中': 'https://yzh.fang.anjuke.com/loupan/', '余姚': 'https://yuy.fang.anjuke.com/loupan/',
                      '偃师市': 'https://yss.fang.anjuke.com/loupan/', '永兴': 'https://yongxing.fang.anjuke.com/',
                      '云梦': 'https://ym.fang.anjuke.com/', '玉环县': 'https://yuhuan.fang.anjuke.com/',
                      '当阳': 'https://ycdy.fang.anjuke.com/', '攸县': 'https://youx.fang.anjuke.com/',
                      '玉田': 'https://yut.fang.anjuke.com/', '永春': 'https://yongc.fang.anjuke.com/',
                      '伊川': 'https://yichuan.fang.anjuke.com/', '沅江': 'https://yyrj.fang.anjuke.com/',
                      '阳谷': 'https://yg.fang.anjuke.com/', '沂南': 'https://yn.fang.anjuke.com/',
                      '沂源': 'https://yiyuan.fang.anjuke.com/', '郓城': 'https://yc.fang.anjuke.com/',
                      '燕郊': 'https://lfyanjiao.fang.anjuke.com/', '郑州': 'https://zz.fang.anjuke.com/',
                      '珠海': 'https://zh.fang.anjuke.com/', '中山': 'https://zs.fang.anjuke.com/',
                      '镇江': 'https://zj.fang.anjuke.com/', '淄博': 'https://zb.fang.anjuke.com/',
                      '张家口': 'https://zjk.fang.anjuke.com/', '株洲': 'https://zhu.fang.anjuke.com/',
                      '漳州': 'https://zhang.fang.anjuke.com/', '湛江': 'https://zhan.fang.anjuke.com/',
                      '肇庆': 'https://zq.fang.anjuke.com/', '枣庄': 'https://zao.fang.anjuke.com/',
                      '舟山': 'https://zhou.fang.anjuke.com/', '遵义': 'https://zy.fang.anjuke.com/',
                      '驻马店': 'https://zmd.fang.anjuke.com/', '自贡': 'https://zg.fang.anjuke.com/',
                      '资阳': 'https://zi.fang.anjuke.com/', '周口': 'https://zk.fang.anjuke.com/',
                      '章丘': 'https://zhq.fang.anjuke.com/', '张家界': 'https://zjj.fang.anjuke.com/',
                      '诸城': 'https://zc.fang.anjuke.com/', '庄河': 'https://pld.fang.anjuke.com/',
                      '张掖': 'https://zhangy.fang.anjuke.com/', '昭通': 'https://zt.fang.anjuke.com/',
                      '中卫': 'https://zw.fang.anjuke.com/', '赵县': 'https://zx.fang.anjuke.com/',
                      '邹城市': 'https://zcs.fang.anjuke.com/loupan/', '遵化': 'https://zunh.fang.anjuke.com/loupan/',
                      '枝江': 'https://zhij.fang.anjuke.com/loupan/', '招远市': 'https://zhys.fang.anjuke.com/loupan/',
                      '资兴': 'https://zixing.fang.anjuke.com/loupan/', '樟树': 'https://zhsh.fang.anjuke.com/loupan/',
                      '诸暨': 'https://zhj.fang.anjuke.com/loupan/', '涿州市': 'https://zzs.fang.anjuke.com/loupan/',
                      '枣阳市': 'https://zys.fang.anjuke.com/loupan/', '泽州': 'https://zezhou.fang.anjuke.com/',
                      '邹平县': 'https://zouping.fang.anjuke.com/', '肇州': 'https://zhaoz.fang.anjuke.com/',
                      '漳浦': 'https://zp.fang.anjuke.com/', '阿坝州': 'https://cd.fang.anjuke.com/',
                      '大邑': 'https://cd.fang.anjuke.com/', '金堂': 'https://cd.fang.anjuke.com/',
                      '淳安': 'https://hz.fang.anjuke.com/', '富阳': 'https://hz.fang.anjuke.com/',
                      '临安': 'https://hz.fang.anjuke.com/', '桐庐': 'https://hz.fang.anjuke.com/',
                      '铜梁': 'https://cq.fang.anjuke.com/', '丰都': 'https://cq.fang.anjuke.com/',
                      '长寿': 'https://cq.fang.anjuke.com/', '涪陵': 'https://cq.fang.anjuke.com/',
                      '南川': 'https://cq.fang.anjuke.com/', '永川': 'https://cq.fang.anjuke.com/',
                      '綦江': 'https://cq.fang.anjuke.com/', '黔江': 'https://cq.fang.anjuke.com/',
                      '万州': 'https://cq.fang.anjuke.com/', '江津': 'https://cq.fang.anjuke.com/',
                      '合川': 'https://cq.fang.anjuke.com/', '普兰店': 'https://dl.fang.anjuke.com/',
                      '平阴': 'https://jn.fang.anjuke.com/', '济阳': 'https://jn.fang.anjuke.com/',
                      '商河': 'https://jn.fang.anjuke.com/', '中牟': 'https://zz.fang.anjuke.com/',
                      '巩义': 'https://zz.fang.anjuke.com/', '宁乡': 'https://cs.fang.anjuke.com/',
                      '无极': 'https://sjz.fang.anjuke.com/', '辛集': 'https://sjz.fang.anjuke.com/',
                      '元氏': 'https://sjz.fang.anjuke.com/', '即墨': 'https://qd.fang.anjuke.com/',
                      '胶南': 'https://qd.fang.anjuke.com/', '周至': 'https://xa.fang.anjuke.com/',
                      '户县': 'https://xa.fang.anjuke.com/', '蓝田': 'https://xa.fang.anjuke.com/',
                      '宁海': 'https://nb.fang.anjuke.com/', '肥东': 'https://hf.fang.anjuke.com/',
                      '肥西': 'https://hf.fang.anjuke.com/', '庐江': 'https://hf.fang.anjuke.com/',
                      '长丰': 'https://hf.fang.anjuke.com/', '长乐': 'https://fz.fang.anjuke.com/',
                      '连江': 'https://fz.fang.anjuke.com/', '平潭': 'https://fz.fang.anjuke.com/',
                      '宜良': 'https://km.fang.anjuke.com/', '辽中': 'https://shen.fang.anjuke.com/',
                      '新民': 'https://shen.fang.anjuke.com/', '新建': 'https://nc.fang.anjuke.com/',
                      '白沙县': 'https://hai.fang.anjuke.com/', '儋州市': 'https://hai.fang.anjuke.com/',
                      '澄迈县': 'https://hai.fang.anjuke.com/', '定安': 'https://hai.fang.anjuke.com/',
                      '琼中': 'https://hai.fang.anjuke.com/', '屯昌': 'https://hai.fang.anjuke.com/',
                      '文昌市': 'https://hai.fang.anjuke.com/', '农安': 'https://cc.fang.anjuke.com/',
                      '陵水': 'https://sy.fang.anjuke.com/', '保亭': 'https://sy.fang.anjuke.com/',
                      '东方市': 'https://sy.fang.anjuke.com/', '龙门': 'https://hui.fang.anjuke.com/',
                      '永登': 'https://lz.fang.anjuke.com/', '榆中': 'https://lz.fang.anjuke.com/',
                      '文安': 'https://lf.fang.anjuke.com/', '汝阳': 'https://ly.fang.anjuke.com/',
                      '宾阳': 'https://nn.fang.anjuke.com/', '横县': 'https://nn.fang.anjuke.com/',
                      '晋安': 'https://qz.fang.anjuke.com/', '上虞': 'https://sx.fang.anjuke.com/',
                      '乐亭': 'https://ts.fang.anjuke.com/', '滦县': 'https://ts.fang.anjuke.com/',
                      '丰县': 'https://xz.fang.anjuke.com/', '睢宁': 'https://xz.fang.anjuke.com/',
                      '江都': 'https://yz.fang.anjuke.com/', '肇源': 'https://dq.fang.anjuke.com/',
                      '当涂': 'https://mas.fang.anjuke.com/', '巴州': 'https://ba.fang.anjuke.com/'}
        self.proxies = {}
        MONGODB_CONFIG = {
            "host": "8.135.119.198",
            "port": "27017",
            "user": "hladmin",
            "password": parse.quote("Hlxkd3,dk3*3@"),
            "db": "dianping",
            "collections": "dianping_collections",
        }
        self.hash_table = redis.Redis(host="192.168.1.230", port=6379, db=7)
        self.hash_table_w = redis.Redis(host="r-wz95zxx6pxgosfs91lpd.redis.rds.aliyuncs.com", port=61379,
                                        password='202^1125DKCd', db=7, decode_responses=True)
        self.bkxf_make = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['小区坐标信息']['data']

        # 建立连接
        self.info_base = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['安居客']['新房_数据_202111']
        self.has_spider = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(
            MONGODB_CONFIG['user'],
            MONGODB_CONFIG['password'],
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port']),
            retryWrites="false")['安居客']['新房_去重_202111']

    def get_proxy(self):
        while True:
            try:
                return requests.get('http://1.116.204.248:5000/proxy').text
                # return requests.get('http://47.106.223.4:50002/get/').json().get('proxy')
            except:
                print('暂无ip，等待20秒')
                time.sleep(20)

    def get_tree(self, url):
        s = 0
        while True:
            try:
                # if self.proxies == {}:
                proxy = self.get_proxy()
                self.proxies = {"https": proxy}
                response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=(5, 10))
                encod = response.apparent_encoding
                if encod.upper() in ['GB2312', 'WINDOWS-1254']:
                    encod = 'gbk'
                response.encoding = encod
                if '人机认证' in response.text:
                    continue
                tree = etree.HTML(response.text)
                if '登录' in ''.join(tree.xpath('//head/title/text()')):
                    continue
                if '访问验证-安居客' in ''.join(tree.xpath('//head/title/text()')):
                    continue
                if "访问过于频繁" in "".join(tree.xpath("//h2[@class='item']/text()")):
                    continue
                if '点击去完成' in "".join(tree.xpath('//div[@class="verify-button"]//text()')):
                    continue

                if response.status_code in [403]:
                    continue

                if '房产网，二手房/新房/租房/写字楼/商铺/房价 -房地产租售服务平台 -安居客' == ''.join(
                        tree.xpath('//head/title/text()')) or '新房一手房' in ''.join(
                    tree.xpath('//head/title/text()')) or '房产信息网' in ''.join(
                    tree.xpath('//head/title/text()')) or '产权年限' in ''.join(
                    tree.xpath('//head/title/text()')) or '周边配套' in ''.join(tree.xpath('//head/title/text()')):
                    return tree
            except Exception as e:
                s += 1
                self.proxies = {}
                # print('get_html错误', e)
                continue

    def get_zb(self, starturl):
        tree = self.get_tree(starturl)
        houseId = ''.join(tree.xpath('//a[@id="similarloupansubs"]/@data-loupan_id'))
        url = 'https://m.anjuke.com/xinfang/api/loupan/map_info?loupan_id=' + houseId + '&source=vr_page'
        js = requests.get(url, headers=self.headers).json()
        lat = js['result']['mark']['baidu_lat']
        lng = js['result']['mark']['baidu_lng']
        return lat, lng

    def get_zb_gaode(self, city, qx, xq, url):
        keys = city + qx + xq
        try:
            data = self.hash_table.hget(name='xiaoqu', key=keys)
            location = str(data, encoding='utf8').split(',')
            return location[0], location[1]
        except:
            for timeout in range(5):
                try:
                    # api请求函数
                    #     print(keywords)
                    gaode_key = [
                        "ac2d0d6951b7662e1b98aabb51b4aeb6",
                        "705d303822d6685c2b05915464483a9c",
                        "9411ece7ba7c9ff934a093219215b47d",
                        "de3514f87e2d145179e4adbd0cb01b1d",
                        "f7e4985b165ebcb8d9976d0af95de9ff"
                    ]
                    url = 'https://restapi.amap.com/v3/place/text?keywords=' + keys + '&offset=20&page=1&key=' + random.choice(
                        gaode_key)
                    zb = requests.get(url).json()['pois']
                    text = zb[0]['location']
                    self.bkxf_make.insert_one(
                        {"城市": city, "区县": qx, "小区": xq, "longitude": text.split(',')[0],
                         "latitude": text.split(',')[1]})
                    self.hash_table.hset(name='xiaoqu', key=keys, value=str(text))
                    self.hash_table_w.hset(name='xiaoqu', key=keys, value=str(text))
                    return text.split(',')[0], text.split(',')[1]
                except Exception as e:
                    print('高德接口访问失败了', e)
            return self.get_zb(url)

    def get_url(self):
        url = 'https://www.anjuke.com/sy-city.html'
        tree = self.get_tree(url)
        for a in tree.xpath('//div[@class="city_list"]/a'):
            city = ''.join(a.xpath('./text()'))
            ur = ''.join(a.xpath('./@href'))
            if city in self.citys.keys():
                continue
            print(city, ur)
            tre = self.get_tree(ur)
            for i in tre.xpath('//li[@class="li_single li_itemsnew li_unselected"]/a[@class="a_navnew"]'):
                if ''.join(i.xpath('./text()')) == '新 房':
                    self.citys[city] = ''.join(i.xpath('./@href'))

    def get_item(self, city, url):
        start = time.time()
        if self.has_spider.count_documents({city: url}):
            print(url, '已爬取')
            return
        tree = self.get_tree(url)
        for li in tree.xpath('//div[@rel="nofollow"]'):
            item = {}
            item['标题'] = ''.join(li.xpath('./div/a[@class="lp-name"]/span/text()'))
            item['城市'] = city
            text = ''.join(li.xpath('./div/a[@class="address"]/span/text()'))
            item['区县'] = re.findall('([\u4E00-\u9FA5]+)', text)[0]
            jm = ''.join(li.xpath('./div/a[@class="huxing"]/span[@class="building-area"]/text()'))
            item['建面'] = ''.join(re.findall('建筑面积：(.+)㎡', jm))
            item['最大建面'] = item['建面'].split('-')[-1]
            item['最小建面'] = item['建面'].split('-')[0]
            item['标题url'] = ''.join(li.xpath('./a[@class="pic"]/@href'))
            houseId = ''.join(re.findall('loupan/(\d+)', item['标题url']))
            item['地址'] = ''.join(re.findall('\](.+)', text)).replace(' ', '').replace('\xa0', '')
            item['分类'] = ''.join(li.xpath('./div/a[@class="tags-wrap"]/div/i[@class="status-icon wuyetp"]/text()'))
            item['标签'] = li.xpath('./div/a[@class="tags-wrap"]/div/span/text()')
            item['户型'] = li.xpath('./div/a[@class="huxing"]/span/text()')[:-1]
            item['销售情况'] = li.xpath('./div/a[@class="tags-wrap"]/div/i/text()')[0]
            if item['销售情况'] == '':
                print(city, url, item['标题'])
            item['lat'], item['lng'] = self.get_zb_gaode(item['城市'], item['区县'], item['标题'], item['标题url'])
            item = self.get_xq(item, houseId)
            print(item)
            self.info_base.insert_one(item)
        self.has_spider.insert_one({city: url})

    def get_xq(self, item, houseId):
        url = 'https://bao.fang.anjuke.com/loupan/canshu-' + houseId + '.html'
        tree = self.get_tree(url)
        items = {}
        for li in tree.xpath('//div[@class="can-left"]//ul[@class="list"]/li'):
            bj = ''.join(li.xpath('./div[@class="name"]/text()')).replace('\n', '').replace(' ', '')
            items[bj] = ''.join(li.xpath('./div[@class="des"]//text()')).replace('\n', '').replace('[查看详情]',
                                                                                                   '').replace(
                '[价格走势]', '').replace(' ', '')
        try:
            item['均价'] = items['参考单价']
        except:
            item['均价'] = ''
        try:
            item['总价'] = items['楼盘总价']
        except:
            item['总价'] = ''
        try:
            item['开盘时间'] = items['最新开盘']
        except:
            item['开盘时间'] = ''
        try:
            item['容积率'] = ''.join(re.findall('(\d\.\d+?)', items['容积率']))
        except:
            item['容积率'] = ''
        try:
            item['绿化率'] = items['绿化率']
        except:
            item['绿化率'] = ''
        try:
            item['总户数'] = items['规划户数']
        except:
            item['总户数'] = ''
        try:
            item['物业费'] = ''.join(re.findall('(\d+?\.?\d+?)', items['物业管理费']))
        except:
            item['物业费'] = ''
        item['抓取年份'] = time.localtime(time.time()).tm_year
        item['抓取月份'] = time.localtime(time.time()).tm_mon
        item['抓取时间'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return item

    def get_pg(self, url):
        tree = self.get_tree(url)
        sum1 = ''.join(tree.xpath('//span[@class="result"]/em/text()'))
        sum2 = int(''.join(re.findall('(\d+?)', sum1)))
        if sum2 % 60 == 0:
            return sum2 // 60
        else:
            return sum2 // 60 + 1

    def run(self):
        # self.info_base.delete_many({})
        # self.has_spider.delete_many({})
        pool = ThreadPoolExecutor()
        # self.get_url()
        print(self.citys)
        for city in self.citys:
            if self.has_spider.count_documents({city: '已爬取'}):
                print('当前城市已爬取', city)
                continue
            elif self.has_spider.count_documents({city: '正在爬取'}):
                print('当前城市正在爬取', city)
                continue
            self.has_spider.insert_one({city: '正在爬取'})
            url = self.citys[city]
            l = []
            start = time.time()
            for pg in range(1, self.get_pg(url) + 1):
                newurl = url + 'loupan/all/p' + str(pg) + '/'
                l.append(pool.submit(self.get_item, city, newurl))
            [ob.result() for ob in l]
            self.has_spider.insert_one({city: '已爬取'})


if __name__ == '__main__':
    obj = GET()

    obj.run()
