from flask import Flask
from flask_mail import Mail, Message
from threading import Thread
#使用线程编程实现异步发送，否则服务就会卡主，如果是web的话在发送完成之前网页是loading状态

app = Flask(__name__)
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.qq.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = '953258481@qq.com',
    MAIL_PASSWORD = 'wooajtqszqspbfcc',#看下面第一张图

))

mail = Mail(app)

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def SendMail():
    msg = Message('This is a mail from QQ SMTP HOST',sender='953258481@qq.com',\
                        recipients=["15821629082@163.com"])
    msg.body = 'From QQ'
    msg.html = '<b>Halo the world!</b>'
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return 'ok'

SendMail()
