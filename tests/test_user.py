import pytest

from bucky.exceptions import BucketListAlreadyExistsError, \
    BucketListNotExistsError
from bucky.models import AppManager, BucketList


@pytest.fixture
def app_manager(request):
    """Fixture for App Manager initialized with a user"""
    app_manager = AppManager().instance
    app_manager.create_user(username="uname",
                            email="uname@gmail.cxom",
                            password="passy")

    # delete app manager after every single test
    def teardown():
        AppManager.instance = None
    request.addfinalizer(teardown)

    return app_manager


@pytest.fixture
def user_uname(app_manager):
    """Fixture for the unique user called 'uname' """
    user = app_manager.get_user(username="uname")
    yield user


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


def test__user_can_create_bucketlist__succeeds(user_uname):
    """Make sure a user can create a bucket-list"""
    bucketlist = user_uname.create_bucketlist(name="first one")
    assert isinstance(bucketlist, BucketList)
    assert isinstance(user_uname.buckets["first one"], BucketList)


def test__user_cannot_create_duplicate_bucketlist__raises(user_uname):
    """Make sure a user cannot create a duplicate bucket-list"""
    user_uname.create_bucketlist(name="first one")
    with pytest.raises(BucketListAlreadyExistsError):
        user_uname.create_bucketlist(name="first one")


def test__user_can_retrieve_bucketlist__succeeds(user_uname):
    """Make sure a user can retrieve a bucket-list"""
    user_uname.create_bucketlist(name="first one")
    bucketlist = user_uname.get_bucketlist(name="first one")
    assert isinstance(bucketlist, BucketList)
    bucketlist2 = user_uname.buckets["first one"]
    assert bucketlist2.name == "first one"


def test__user_cannot_retrieve_nonexistent_bucketlist__raises(user_uname):
    """Make sure a user cannot retrieve a non-existent bucket-list"""
    with pytest.raises(BucketListNotExistsError):
        user_uname.get_bucketlist(name="first one")


def test__user_can_delete_bucketlist__succeeds(user_uname):
    """Make sure a user can delete a bucket-list"""
    user_uname.create_bucketlist(name="first one")
    status = user_uname.delete_bucketlist(name="first one")
    assert status
    with pytest.raises(BucketListNotExistsError):
        user_uname.get_bucketlist(name="first one")


def test__user_cannot_delete_nonexistent_bucketlist__raises(user_uname):
    """Make sure a user cannot delete a non-existent bucket-list"""
    with pytest.raises(BucketListNotExistsError):
        user_uname.delete_bucketlist(name="first one")
