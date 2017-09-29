from flask import render_template, flash, redirect, request, url_for
from flask_login import login_user, login_required, logout_user

from bucky.auth import auth
from bucky.auth.forms import LoginForm, RegistrationForm
from bucky.exceptions import UserNotExistsError, UserAlreadyExistsError
from bucky.models import AppManager


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            am = AppManager().instance
            user = am.get_user(username=form.username.data)
            if user.verify_password(password=form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(request.args.get('next') or url_for('main.index'))
        except UserNotExistsError:
            flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            am = AppManager().instance
            am.create_user(username=form.username.data,
                           email=form.email.data,
                           password=form.password.data)
            flash("You can login now.")
            return redirect(url_for('auth.login'))
            # return {"data": "user was created"}
        except UserAlreadyExistsError:
            flash('User already exists')
    # else:
        # return {"data": "form did not validate"}
    return render_template('auth/register.html', form=form)
    # return {"data": "user already exists"}

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
