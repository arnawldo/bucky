import pytest

from bucky.exceptions import UserAlreadyExistsError, UserNotExistsError
from bucky.models import AppManager


@pytest.fixture
def am():
    """Fixture for AppManager class
    """
    am = AppManager()
    return am


def test__app_manager_can_create_user__succeeds(am):
    """Make sure users can be created"""
    am.create_user(username="uname",
                   password="passy",
                   email="user@gmail.com")
    assert len(am.users) == 1


def test__app_manager_can_delete_user__succeeds(am):
    """Make sure users can be deleted"""
    am.create_user(username="uname",
                   password="passy",
                   email="user@gmail.com")
    assert len(am.users) == 1
    am.delete_user(username="uname")
    assert len(am.users) == 0


def test__app_manager_create_existing_user__raises(am):
    """Make sure app manager raises exception when creating user that
    already exists
    """
    am.create_user(username="uname",
                   password="passy",
                   email="user@gmail.com")
    with pytest.raises(UserAlreadyExistsError):
        am.create_user(username="uname",
                       password="passy",
                       email="user@gmail.com")


def test__app_manager_delete_non_existant_user__raises(am):
    """Make sure app manager raises exception when creating user that
     already exists
     """
    with pytest.raises(UserNotExistsError):
        am.delete_user(username="uname")
