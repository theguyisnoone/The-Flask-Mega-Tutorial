from flask import Flask
from flask_mail import Mail, Message
from threading import Thread
import os

app = Flask(__name__)
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.qq.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    # MAIL_USERNAME='953258481@qq.com',
    # MAIL_PASSWORD='wooajtqszqspbfcc'

))

mail = Mail(app)

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def SendMail():
    msg = Message('Test',sender='953258481@qq.com',\
                        recipients=["15821629082@163.com"])
    msg.body = 'From QQ'
    msg.html = '<b>Hola the world!</b>'
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return 'ok'

SendMail()
