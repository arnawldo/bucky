import pytest

from bucky.models import AppManager


@pytest.fixture
def client(request, app):

    client = app.test_client()

    def teardown():
        AppManager.instance = None
    request.addfinalizer(teardown)

    return client


def register_and_login(client, username, password, email=None):
    """Helper function to register and log in user"""
    if email is None:
        email = username + '@gm.com'
    response = client.post('/auth/register', data=dict(
        username=username,
        password=password,
        password2=password,
        email=email
    ), follow_redirects=True)

    assert b"Login" in response.data
    assert response.status_code == 200

    response = client.post('/auth/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

    return response


def test__new_user_is_not_shown_bucketlists__succeeds(client):
    """Make sure newly registered user is not shown any bucket-lists"""
    response = register_and_login(client, "arny", "passy")
    assert b'Looks like you dont have any buckets' in response.data


def test__user_can_create_bucketlist__succeeds(client):
    """Make sure user can create bucket-list and can see it"""
    register_and_login(client, "arny", "passy")
    response = client.post('/create_bucketlist',
                           data=dict(name="bucket 1"),
                           follow_redirects=True)
    assert b'bucket 1' in response.data


def test__create_duplicate_bucketlist_and_task__fails(client):
    """Make sure user can create bucket-list and can see it"""
    register_and_login(client, "arny", "passy")
    response = client.post('/create_bucketlist',
                           data=dict(name="bucket 1"),
                           follow_redirects=True)
    assert b'bucket 1' in response.data
    # cannot create duplicate bucket-list
    response = client.post('/create_bucketlist',
                           data=dict(name="bucket 1"),
                           follow_redirects=True)
    assert b'This bucket-list already exists!' in response.data
    # create task
    response = client.post('/bucketlist/bucket 1',
                           data=dict(description="task 1"),
                           follow_redirects=True)
    assert b'task 1' in response.data
    # cannot add duplicate task
    response = client.post('/bucketlist/bucket 1',
                           data=dict(description="task 1"),
                           follow_redirects=True)
    assert b'This task already exists' in response.data
    # cannot add task to non-existent bucket-list
    response = client.post('/bucketlist/bucket 2',
                           data=dict(description="task 2"),
                           follow_redirects=True)
    assert b'This bucket-list does not exist' in response.data


def test__user_can_get_tasks__succeeds(client):
    """Make sure user can see created tasks and can see it"""
    register_and_login(client, "arny", "passy")
    response = client.post('/create_bucketlist',
                           data=dict(name="bucket 1"),
                           follow_redirects=True)
    assert b'bucket 1' in response.data
    # create task
    response = client.post('/bucketlist/bucket 1',
                           data=dict(description="task 1"),
                           follow_redirects=True)
    assert b'task 1' in response.data
    # get tasks
    response = client.get('/bucketlist/bucket 1',
                          follow_redirects=True)
    assert b'task 1' in response.data


def test__user_cannot_get_tasks_from_nonexistent_bucketlist__fails(client):
    """Make sure user cannot see tasks from non-existent bucket-list"""
    register_and_login(client, "arny", "passy")
    response = client.post('/create_bucketlist',
                           data=dict(name="bucket 1"),
                           follow_redirects=True)
    assert b'bucket 1' in response.data
    # create task
    response = client.post('/bucketlist/bucket 1',
                           data=dict(description="task 1"),
                           follow_redirects=True)
    assert b'task 1' in response.data
    # cannot see tasks from non existent bucket-list
    response = client.get('/bucketlist/bucket 2',
                          follow_redirects=True)
    assert b'This bucket-list does not exist' in response.data


def test__user_can_create_bucketlist_ajax__succeeds(client):
    """Make sure user can create bucket-list when on ajax-dependent page"""
    register_and_login(client, "arny", "passy")
    response = client.get('/_create_bucketlist',
                          query_string=dict(bucketName='bucket 1'))
    assert b'bucket 1' in response.data
    assert response.status_code == 200
    # check bucket-list already exists
    response = client.get('/_create_bucketlist',
                          query_string=dict(bucketName='bucket 1'))
    assert b'This bucket-list already exists' in response.data
    assert response.status_code == 200
    # nothing is done with empty request
    response = client.get('/_create_bucketlist',
                          query_string=dict())
    assert b'false' in response.data
    assert response.status_code == 200


def test__user_can_delete_bucketlist_ajax__succeeds(client):
    """Make sure user can delete bucket-list when on ajax-dependent page"""
    register_and_login(client, "arny", "passy")
    response = client.get('/_create_bucketlist',
                          query_string=dict(bucketName='bucket 1'))
    assert b'bucket 1' in response.data
    assert response.status_code == 200
    # try deleting bucket-list
    response = client.get('/_delete_bucketlist',
                          query_string=dict(bucketName='bucket 1'))
    assert b'true' in response.data
    # cannot delete non existent bucket-list
    response = client.get('/_delete_bucketlist',
                          query_string=dict(bucketName='bucket 1'))
    assert b'This bucket-list does not exist!' in response.data
    assert response.status_code == 200
    # nothing is done with empty request
    response = client.get('/_delete_bucketlist',
                          query_string=dict())
    assert b'false' in response.data
    assert response.status_code == 200


def test__user_can_create_task_ajax__succeeds(client):
    """Make sure user can create task when on ajax-dependent page"""
    register_and_login(client, "arny", "passy")
    response = client.get('/_create_bucketlist',
                          query_string=dict(bucketName='bucket 1'))
    assert b'bucket 1' in response.data
    assert response.status_code == 200
    # create task
    response = client.get('/_create_task',
                          query_string=dict(bucketName='bucket 1',
                                            taskDescription='task 1'))
    assert b'task 1' in response.data
    assert response.status_code == 200
    # cannot create duplicate task
    response = client.get('/_create_task',
                          query_string=dict(bucketName='bucket 1',
                                            taskDescription='task 1'))
    assert b'This task already exists' in response.data
    assert response.status_code == 200
    # cannot create task for non-existent bucket-list
    response = client.get('/_create_task',
                          query_string=dict(bucketName='bucket 2',
                                            taskDescription='task 1'))
    assert b'This bucket-list does not exist' in response.data
    assert response.status_code == 200
    # nothing is done with empty request
    response = client.get('/_create_task',
                          query_string=dict())
    assert b'false' in response.data
    assert response.status_code == 200


def test__user_can_delete_task_ajax__succeeds(client):
    """Make sure user can delete task when on ajax-dependent page"""
    register_and_login(client, "arny", "passy")
    response = client.get('/_create_bucketlist',
                          query_string=dict(bucketName='bucket 1'))
    assert b'bucket 1' in response.data
    assert response.status_code == 200
    # create task
    response = client.get('/_create_task',
                          query_string=dict(bucketName='bucket 1',
                                            taskDescription='task 1'))
    assert b'task 1' in response.data
    assert response.status_code == 200
    # delete task
    response = client.get('/_delete_task',
                          query_string=dict(bucketName='bucket 1',
                                            taskDescription='task 1'))
    assert b'true' in response.data
    assert response.status_code == 200
    # cannot delete non-existent task
    response = client.get('/_delete_task',
                          query_string=dict(bucketName='bucket 1',
                                            taskDescription='task 1'))
    assert b'This task does not exist' in response.data
    assert response.status_code == 200
    # cannot delete task from non-existent bucket-list
    response = client.get('/_delete_task',
                          query_string=dict(bucketName='bucket 2',
                                            taskDescription='task 1'))
    assert b'This bucket-list does not exist' in response.data
    assert response.status_code == 200
    # nothing is done with empty request
    response = client.get('/_delete_task',
                          query_string=dict())
    assert b'false' in response.data
    assert response.status_code == 200
