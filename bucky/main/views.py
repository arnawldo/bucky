from flask import render_template, flash, redirect, url_for, jsonify
from flask_login import current_user, login_required

from bucky.exceptions import BucketListAlreadyExistsError
from bucky.main import main
from bucky.main.forms import BucketListForm


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/create_bucketlist', methods=['GET', 'POST'])
@login_required
def create_bucketlist():
    form = BucketListForm()
    if form.validate_on_submit():
        try:
            print(current_user)
            current_user.create_bucketlist(name=form.name.data)
            return redirect(url_for('main.index'))
        except BucketListAlreadyExistsError:
            flash('This bucket-list already exists! Try another.')
    return render_template('create_bucketlist.html', form=form)
