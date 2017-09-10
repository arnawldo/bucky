from flask import render_template, flash, redirect, url_for, jsonify
from flask_login import current_user, login_required

from bucky.exceptions import BucketListAlreadyExistsError, BucketListNotExistsError, TaskAlreadyExistsError
from bucky.main import main
from bucky.main.forms import BucketListForm, TaskForm


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/create_bucketlist', methods=['GET', 'POST'])
@login_required
def create_bucketlist():
    form = BucketListForm()
    if form.validate_on_submit():
        try:
            _ = current_user.create_bucketlist(name=form.name.data)
            return redirect(url_for('main.index'))
        except BucketListAlreadyExistsError:
            flash('This bucket-list already exists! Try another.')
    return render_template('create_bucketlist.html', form=form)


@main.route('/bucketlist/<string:name>', methods=['GET', 'POST'])
@login_required
def bucketlist(name):
    form = TaskForm()
    if form.validate_on_submit():
        try:
            bucketlist = current_user.get_bucketlist(name)
        except BucketListNotExistsError:
            flash('This bucket-list does not exist!')
            return redirect(url_for('main.index'))
        try:
            bucketlist.create_task(description=form.description.data)
        except TaskAlreadyExistsError:
            flash('This task already exists')
        tasks = [task for task_description, task in bucketlist.tasks.items()]
        return render_template('bucketlist.html', bucketlistname=name, tasks=tasks, form=form)

    try:
        tasks = [task for task_description, task in current_user.get_bucketlist(name).tasks.items()]
    except BucketListNotExistsError:
        flash('This bucket-list does not exist!')
        return redirect(url_for('main.index'))
    return render_template('bucketlist.html', bucketlistname=name, tasks=tasks, form=form)
