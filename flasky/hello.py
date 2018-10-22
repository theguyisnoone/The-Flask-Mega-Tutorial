# #启动
# from flask import Flask
# app=Flask(__name__)
#
# #路由
# @app.route('/')
# def index():
#     return '<h1>hello world</h1>'
from flask   import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, LLEE!'

if __name__ == '__main__':
    app.run()
