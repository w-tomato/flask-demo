from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # 导入扩展类
from flask_login import LoginManager

# 在 Python 中，__init__.py 文件是特殊的。它是包的初始化文件。
# 当导入包时，Python 解释器会首先导入包中的 __init__.py 文件。__init__.py 文件可以用于执行以下操作：
# 1、导入包中的其他模块或文件
# 2、定义包的全局变量或常量
# 3、注册包中的钩子函数

# 这些没用的是sqlalchemy包的用法
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
import os
import sys
from sqlalchemy.orm import declarative_base, sessionmaker

app = Flask(__name__)
app.debug = True

# 配置数据库连接地址
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:whc123@39.105.13.3:3306/flask'
# 数据表的更改追踪，需要消耗额外的资源，不需要可以关闭
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 专门处理登录的包
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # 设置登录页面的端点，也就是登录页面的路由，这里的login是下边的login函数，也就是/login
login_manager.login_message = '登录失败'  # 设置登录时的提示消息

# 不设置的话会报错：RuntimeError: The session is unavailable because no secret key was set. Set the secret_key on the
# application to something unique and secret.
app.secret_key = "your_secret_key"


# 下边这个是sqlalchemy包的用法，本来用着也挺好，但是跟着教程写的时候发现没有get_or_404方法，所以就换回了教程里用的flask_sqlalchemy包
# engine = create_engine("mysql+pymysql://root:whc123@39.105.13.3:3306/flask", echo=True)
# Base = declarative_base(engine)  # 建立 sql rom基类
# metadata = MetaData(engine)  # 建立元数据
# session = sessionmaker(engine)()  # 构建session对象

from watchlist.models import User
@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


# 这个函数的作用是在所有模板中都能使用 user 变量，而不用每次在渲染模板时都传入这个变量。
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

# 这个函数的作用是在所有模板中都能使用 user 变量，而不用每次在渲染模板时都传入这个变量。
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


# 导入其他模块，为了避免循环导入依赖，放到最后导入
from watchlist import views, errors, commands

