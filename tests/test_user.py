import pytest
from bucky.models import AppManager


@pytest.fixture
def app_manager():
    """Fixture for App Manager initialized with a user"""
    app_manager = AppManager()
    app_manager.create_user(username="uname",
                            email="uname@gmail.cxom",
                            password="passy")
    return app_manager


@pytest.fixture
def user_uname(app_manager):
    """Fixture for the unique user called 'uname' """
    user = app_manager.get_user(username="uname")
    return user


def test__password_is_hashed__succeeds(user_uname):
    """Make sure user password is stored hashed"""
    assert user_uname.password_hashed != "passy"


def test__two_users_same_password_different_hash__succeeds(app_manager):
    """Make sure two users with similar passwords have different
     hashed passwords"""
    harry = app_manager.create_user(username="harry",
                                    email="harry@gmail.com",
                                    password="passy")
    uname = app_manager.get_user(username="uname")
    assert uname.password_hashed != harry.password_hashed
