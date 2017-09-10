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
