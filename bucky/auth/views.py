from flask import render_template, flash, redirect, request, url_for
from flask_login import login_user, login_required, logout_user

from bucky.auth import auth
from bucky.auth.forms import LoginForm
from bucky.exceptions import UserNotExistsError
from bucky_app import am


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = am.get_user(username=form.username.data)
            if user.verify_password(password=form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(request.args.get('next') or url_for('main.index'))
        except UserNotExistsError:
            flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))