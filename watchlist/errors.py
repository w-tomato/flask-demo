from flask import render_template
from watchlist.models import User
from watchlist import app

@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    user = User.query.first()
    # 为了确保响应内容的状态码正确，我们需要在 render_template() 函数的返回值中指定状态码。
    # 因此，我们需要在 return render_template('404.html', user=user) 后面加上 , 404，以指定状态码为 404。
    # 如果我们不加 , 404，那么响应内容的状态码将是 200，这可能会导致错误。例如，如果用户访问一个不存在的 URL，Flask 将触发 page_not_found() 错误处理函数。
    # 然后 Flask 将返回 200 状态码，这可能会导致用户认为请求成功了。
    return render_template('404.html', user=user), 404  # 返回模板和状态码