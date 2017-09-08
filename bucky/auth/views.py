from flask import render_template
from bucky.auth import auth


@auth.route('/login')
def login():
    return render_template('auth/login.html')
