from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, abort, flash
from flask_login import login_required, current_user

from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm
from .. import db
from ..models import User, Permission, Role
from ..email import send_mail
from ..decorators import admin_required, permission_required


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

        new_user = User(email='new_user_null_email@example.com', username=form.name.data, password='default_password')
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


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/secret')
@login_required
# login_required modifier -- only login user have access to the page
def secret():
    return "Only authenticated user are allowed!"


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For Administrators!"


@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return "For comment mederators!"


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)
