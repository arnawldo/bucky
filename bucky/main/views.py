from flask import render_template, flash, redirect, url_for, jsonify, request
from flask_login import current_user, login_required

from bucky.exceptions import BucketListAlreadyExistsError, BucketListNotExistsError, TaskAlreadyExistsError, \
    TaskNotExistsError
from bucky.main import main
from bucky.main.forms import BucketListForm, TaskForm


@main.route('/')
def index():
    bucket_form = BucketListForm()
    return render_template('index.html', bucket_form=bucket_form)


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


@main.route('/_create_bucketlist')
@login_required
def create_bucketlist_ajax():
    bucket_name = request.args.get('bucketName', None, type=str)
    if bucket_name:
        try:
            created_bucket = current_user.create_bucketlist(name=bucket_name)
            return jsonify(statusCode=True,
                           bucketName=created_bucket.name,
                           bucketLink=url_for('main.bucketlist', name=created_bucket.name, _external=True))
        except BucketListAlreadyExistsError:
            return jsonify(statusCode=False, errorMessage='This bucket-list already exists!')
    return jsonify(statusCode=False)


@main.route('/_delete_bucketlist')
@login_required
def delete_bucketlist_ajax():
    bucket_name = request.args.get('bucketName', None, type=str)
    if bucket_name:
        try:
            current_user.delete_bucketlist(bucket_name)
            return jsonify(statusCode=True)
        except BucketListNotExistsError:
            return jsonify(statusCode=False, errorMessage='This bucket-list does not exist!')
    return jsonify(statusCode=False)


@main.route('/_create_task')
@login_required
def create_task_ajax():
    task_description = request.args.get('taskDescription', None, type=str)
    bucket_name = request.args.get('bucketName', None, type=str)

    if task_description and bucket_name:
        try:
            bucketlist = current_user.get_bucketlist(bucket_name)
            try:
                bucketlist.create_task(description=task_description)
                return jsonify(statusCode=True,
                               taskDescription=task_description)
            except TaskAlreadyExistsError:
                return jsonify(statusCode=False,
                               errorMessage='This task already exists!')
        except BucketListNotExistsError:
            return jsonify(statusCode=False,
                           errorMessage='This bucket-list does not exist!')
    return jsonify(statusCode=False)


@main.route('/_delete_task')
@login_required
def delete_task_ajax():
    task_description = request.args.get('taskDescription', None, type=str)
    bucket_name = request.args.get('bucketName', None, type=str)

    if task_description and bucket_name:
        try:
            bucketlist = current_user.get_bucketlist(bucket_name)
            try:
                bucketlist.delete_task(description=task_description)
                return jsonify(statusCode=True)
            except TaskNotExistsError:
                return jsonify(statusCode=False,
                               errorMessage='This task does not exist!')
        except BucketListNotExistsError:
            return jsonify(statusCode=False,
                           errorMessage='This bucket-list does not exist!')
    return jsonify(statusCode=False)


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
