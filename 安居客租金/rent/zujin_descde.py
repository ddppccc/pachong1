# 定义一个替换文本操作
import base64
import io
import re

from fontTools.ttLib import TTFont


# 正则匹配获取加密文字代码
def get_font(html):
    font = re.findall(r"src:url\('data:application/font-ttf;charset=utf-8;base64,(.*?)'\) format", html)[0]
    return font


def multReplace(text, rpdict):
    rx = re.compile('|'.join(map(re.escape, rpdict)))
    return rx.sub(lambda match:rpdict[match.group(0)], text)


def decode_zujin(text,font):
    # text 含有加密字体的文本
    # font 加密的字体
    glyphdict = {
        'glyph00001': '0',
        'glyph00002': '1',
        'glyph00003': '2',
        'glyph00004': '3',
        'glyph00005': '4',
        'glyph00006': '5',
        'glyph00007': '6',
        'glyph00008': '7',
        'glyph00009': '8',
        'glyph00010': '9'
    }       # 字体对应效果
    data = base64.b64decode(font)  # base64解码
    fonts = TTFont(io.BytesIO(data))  # 生成二进制字节
    cmap = fonts.getBestCmap()      # 十进制ascii码到字形名的对应{38006:'glyph00002',...}
    chrMapNum = {}                  # 变为{‘龥’:'1',...}
    for asc in cmap:
        chrMapNum[chr(asc)] = glyphdict[cmap[asc]]
    return multReplace(text,chrMapNum)