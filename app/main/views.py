from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app
from flask_login import login_required

from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_mail


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email="new_user_null_email@example.com").first()

        if user is not None:
            db.session.delete(user)
            db.session.commit()
            session['known'] = True
        else:
            session['known'] = False

        new_user = User()
        new_user.email='new_user_null_email@example.com'
        new_user.username=form.name.data
        new_user.password='default_password'

        db.session.add(new_user)
        db.session.commit()
        send_mail(current_app._get_current_object().config['FLASKY_ADMIN'],
                  'New User', 'mail/new_user', user=new_user)
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False),
                           current_time=datetime.utcnow())


@main.route('/secret')
@login_required
# login_required modifier -- only login user have access to the page
def secret():
    return "Only authenticated user are allowed!"
