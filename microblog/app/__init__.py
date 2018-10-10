from flask  import Flask
#first one is flask package the second one is Class Flask

app=Flask(__name__)
#__name__：python预先设置的模块 表示当前调用它的模块的名字
#passing __name__ is almost always going to configure Flask in the correct way.

# from helloworld import routes
from app import routes

#The bottom import is a workaround to circular imports, a common problem with Flask applications.
#cause there are two app
#routes : 程序引用的不同app
