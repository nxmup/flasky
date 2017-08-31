# coding: utf-8
import datetime

from flask import Flask, render_template, session, redirect, url_for
# render_template 函数把 Jinja2 模板引擎集成到了程序中.
# 函数的第一个参数名是模板的文件名。随后的参数都是键值对，表示模板中变量对应的真实值。
# session 请求上下文。用户会话，用于存储请求之间需要记住的值的字典
# redirect 重定向到新链接
# url_for 获取动态路由的链接，第一个参数是 视图函数名，
# 可选参数 _external 如果被设置为 True，则会返回绝对链接
# 动态部分可作为关键字参数同时传入。

from flask_bootstrap import Bootstrap
# 使用 Bootstrap 框架来组织用户界面

from flask_moment import Moment
# 使用 moment 渲染日期和时间

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# 使用 flask-wtf，每个 Web 表单都由一个继承自 Form 的类表示。
# 这个类定义表单中的一组字段，每个字段都用对象表示。字段可附属一个
# 或多个验证函数

app = Flask(__name__)
app.config['SECRET_KEY'] = "hard to guess string"
# 实现跨站请求伪造（CSRF）保护。
bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(Form):
    name = StringField("What is your name?", validators=[DataRequired()])
    # StringField 类表示属性为 type="text" 的 <input> 元素
    # 可选参数 validators 指定一个验证函数组成的列表，在接受用户提交的数据之前验证数据
    submit = SubmitField("Submit")
    # SubmitField 类表示属性为 type="submit" 的 <input> 元素


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


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
