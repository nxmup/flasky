# coding: utf-8
import datetime
from flask import Flask, render_template
# render_template 函数把 Jinja2 模板引擎集成到了程序中.
# 函数的第一个参数名是模板的文件名。随后的参数都是键值对，
# 表示模板中变量对应的真实值。
from flask_bootstrap import Bootstrap
# 使用 Bootstrap 框架来组织用户界面
from flask_moment import Moment
# 使用 moment 渲染日期和时间

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/')
def index():
    # return render_template('index.html')
    return render_template('index.html',
                           current_time=datetime.datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
    # 左边的 name 表示参数名，就是模板中使用的占位符


@app.errorhandler(404)
def page_not_found(e):
    # 客户端请求未知页面或路由
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    # 有未处理异常
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
