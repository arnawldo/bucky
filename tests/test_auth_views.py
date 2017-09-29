def test__user_login_invalid_credentials__fails(client):
    """Make sure a user with invalid credentials cannot login"""
    response = client.post('/auth/login', data=dict(
        user_name="arny",
        password="test"
    ), follow_redirects=True)
    assert b'Login' in response.data
    assert response.status_code == 200


def test__user_can_register_login_logout__succeeds(client):
    """Make sure user can register, login, and logout successfully"""
    response = client.post('/auth/register', data=dict(
        username="arny",
        email="arny@gm.com",
        password="test",
        password2="test"
    ), follow_redirects=True)
    assert b"Login" in response.data
    assert response.status_code == 200

    response = client.post('/auth/login', data=dict(
        username="arny",
        password="test"
    ), follow_redirects=True)
    assert b'Looks like you dont have any buckets' in response.data
    assert response.status_code == 200

    response = client.get('/auth/logout', follow_redirects=True)
    assert b'You have been logged out.' in response.data
    assert response.status_code == 200
