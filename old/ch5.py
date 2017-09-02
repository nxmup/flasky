import os
from flask import Flask, session, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_script import Shell, Manager
from flask_bootstrap import Bootstrap
# 使用 Bootstrap 框架来组织用户界面
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# 使用 flask-wtf，每个 Web 表单都由一个继承自 Form 的类表示。
# 这个类定义表单中的一组字段，每个字段都用对象表示。字段可附属一个
# 或多个验证函数


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SECRET_KEY'] = "This is a CSRF key"
bootstrap = Bootstrap(app)
manager = Manager(app)
db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False))

if __name__ == '__main__':
    manager.add_command('shell', Shell(make_context=make_shell_context))
    # app.run(debug=True)
    manager.run()
