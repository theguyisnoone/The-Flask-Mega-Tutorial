from flask  import Flask
#first one is flask package the second one is Class Flask
from config import Config
#sql
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#登录模块
from flask_login import LoginManager

app=Flask(__name__)
#__name__：python预先设置的模块 表示当前调用它的模块的名字
#passing __name__ is almost always going to configure Flask in the correct way.

# app.config['SECRET_KEY']='you-will-never-guess'
#better write in a individe .py
app.config.from_object(Config)
db=SQLAlchemy(app)
migrate=Migrate(app,db)
login=LoginManager(app)#登录
login.login_view='login'
# from helloworld import routes
from app import routes,models

#The bottom import is a workaround to circular imports, a common problem with Flask applications.
#cause there are two app
#routes : 程序引用的不同app
