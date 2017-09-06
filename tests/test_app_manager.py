import pytest
from bucky.models import AppManager, User

@pytest.fixture
def app_manager():
    """Fixture for AppManager class
    """
    am = AppManager()
    return am

@pytest.fixture
def user1():
    """Fixture for a unique User
    """
    user = User()
    return user

def test__app_manager_can_create_user__succeeds(am):
    """Make sure users can be created"""
    am.create_user(username="uname", password="passy", email="user@gmail.com")
    assert len(am.users) == 1
    assert am.username == "uname"

def test__app_manager_can_delete_user__succeeds(am):
    """Make sure users can be deleted"""
    am.create_user(username="uname", password="passy", email="user@gmail.com")
    assert len(am.users) == 1
    am.delete_user(username="uname")
    assert len(am.users) == 0
