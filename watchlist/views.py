from watchlist import app, db
from watchlist.models import User, Movie
from flask import render_template, request, redirect, url_for, flash
from markupsafe import escape
from flask_login import login_required, current_user, login_user, logout_user

# 这里的@app.route @代表装饰器，@后边的内容是装饰器函数，这里的app就是上边的app = Flask(__name__)里的app，所以如果上边改成abc = Flask(__name__)
# 那么这里就要改成@abc.route，也可以自定义一个函数，比如定义一个def abc():   然后在方法上边写@abc，就可以用abc函数将被装饰的函数包裹起来执行额外的逻辑
@app.route('/user/<name>')
def user_page(name):
    # 注意 用户输入的数据会包含恶意代码，所以不能直接作为响应返回，需要使用
    # MarkupSafe（Flask的依赖之一）提供的escape()函数对name变量进行转义处理，比如把 < 转换成 & lt;。这样在返回响应时浏览器就不会把它们当做代码执行。
    return f'User: {escape(name)}'


# 首页，因为新增按钮也在首页，所以这里也处理新增的逻辑
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
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
    User.query.filter(User.username == 'greyli').first()
    return render_template('index.html', name='', movies=movies)


# 修改电影信息
@login_required
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


# 删除电影信息
@login_required
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.filter(User.username == username).first()
        # 验证用户名和密码是否一致
        if user and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('index'))  # 重定向到主页

        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')


@app.route('/logout')
@login_required  # 用于视图保护,加了这个装饰器，就必须登录才能访问这个页面
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')