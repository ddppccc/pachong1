# coding:utf8

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MyEmail:
    def __init__(self):
        self.user = '1260252261@qq.com'
        self.passwd = 'ysodlyleavshfhhg'
        self.to_list = ["", "1260252261@qq.com"]
        self.cc_list = []
        self.tag = None
        self.doc = None         # 正文内容

    def send(self):
        """
        发送邮件
        """
        try:
            server = smtplib.SMTP_SSL("smtp.qq.com", port=465)
            server.login(self.user, self.passwd)
            server.sendmail("<%s>" % self.user, self.to_list, self.get_attach())
            server.close()
            print("send email successful")
        except Exception as e:
            print("send email failed %s" % e)

    def get_attach(self):
        """
        构造邮件内容
        """
        attach = MIMEMultipart()
        if self.tag is not None:
            # 主题,最上面的一行
            attach["Subject"] = self.tag
        if self.user is not None:
            # 显示在发件人
            attach["From"] = "发件人姓名，<%s>" % self.user
        if self.to_list:
            # 收件人列表
            attach["To"] = ";".join(self.to_list)
        if self.doc:
            attach.attach(MIMEText(self.doc))

        # if self.cc_list:
        #     # 抄送列表
        #     attach["Cc"] = ";".join(self.cc_list)
        # if self.doc:
        #     # 估计任何文件都可以用base64，比如rar等
        #     # 文件名汉字用gbk编码代替
        #     name = os.path.basename(self.doc).encode("gbk")
        #     f = open(self.doc, "rb")
        #     doc = MIMEText(f.read(), "base64", "gb2312")
        #     doc["Content-Type"] = 'application/octet-stream'
        #     doc["Content-Disposition"] = 'attachment; filename="' + name + '"'
        #     attach.attach(doc)
        #     f.close()
        return attach.as_string()


if __name__ == "__main__":
    my = MyEmail()
    my.tag = "猫眼爬虫"
    my.doc = 'ip被封'
    my.send()