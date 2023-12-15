# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask, url_for, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy  # 导入扩展类
from markupsafe import escape
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
import os
import sys

from sqlalchemy.orm import declarative_base, sessionmaker

app = Flask(__name__)
app.debug = True

# 配置数据库连接地址
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:whc123@localhost:3306/flask'
# 数据表的更改追踪，需要消耗额外的资源，不需要可以关闭
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
name = 'Grey Li'

# 不设置的话会报错：RuntimeError: The session is unavailable because no secret key was set. Set the secret_key on the application
# to something unique and secret.
app.secret_key = "your_secret_key"

# 下边这个是sqlalchemy包的用法，本来用着也挺好，但是跟着教程写的时候发现没有get_or_404方法，所以就换回了教程里用的flask_sqlalchemy包
# engine = create_engine("mysql+pymysql://root:whc123@39.105.13.3:3306/flask", echo=True)
# Base = declarative_base(engine)  # 建立 sql rom基类
# metadata = MetaData(engine)  # 建立元数据
# session = sessionmaker(engine)()  # 构建session对象


@app.route('/user/<name>')
def user_page(name):
    # 注意 用户输入的数据会包含恶意代码，所以不能直接作为响应返回，需要使用
    # MarkupSafe（Flask的依赖之一）提供的escape()函数对name变量进行转义处理，比如把 < 转换成 & lt;。这样在返回响应时浏览器就不会把它们当做代码执行。
    return f'User: {escape(name)}'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 获取表单数据
        title = request.form.get('title')
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('index'))  # 重定向回主页
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))  # 重定向回主页
    movies = Movie.query.all()
    return render_template('index.html', name=name, movies=movies)

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录

    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页

@app.route('/test')
def test_url_for():
    # print(url_for('hello'))  # 生成 hello 视图函数对应的 URL，将会输出：/
    # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
    print(url_for('user_page', name='peter'))  # 输出：/user/peter
    print(url_for('test_url_for'))  # 输出：/test
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'


# 这个函数的作用是在所有模板中都能使用 user 变量，而不用每次在渲染模板时都传入这个变量。
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    user = User.query.first()
    # 为了确保响应内容的状态码正确，我们需要在 render_template() 函数的返回值中指定状态码。
    # 因此，我们需要在 return render_template('404.html', user=user) 后面加上 , 404，以指定状态码为 404。
    # 如果我们不加 , 404，那么响应内容的状态码将是 200，这可能会导致错误。例如，如果用户访问一个不存在的 URL，Flask 将触发 page_not_found() 错误处理函数。
    # 然后 Flask 将返回 200 状态码，这可能会导致用户认为请求成功了。
    return render_template('404.html', user=user), 404  # 返回模板和状态码


class Movie(db.Model):  # 表名将会是 movie
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
