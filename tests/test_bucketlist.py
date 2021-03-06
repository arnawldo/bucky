import pytest

from bucky.exceptions import TaskNotExistsError, TaskAlreadyExistsError
from bucky.models import AppManager, Task


@pytest.fixture
def bucket1(request):
    """Fixture for a unique bucket-list
    """
    am = AppManager().instance
    user = am.create_user(username="uname",
                          email="uname@gmail.com",
                          password="passy")
    bucket1 = user.create_bucketlist(name="bucket1")

    # delete app manager after every single test
    def teardown():
        AppManager.instance = None
    request.addfinalizer(teardown)

    return bucket1


def test__bucketlist_has_custom_repr__succeeds(bucket1):
    """Make sure bucketlist has custom __repr__ method"""
    assert 'BucketList <bucket1>' in bucket1.__repr__()


def test__bucketlist_can_create_task__succeeds(bucket1):
    """Make sure bucket-list can create a task"""
    assert len(bucket1.tasks) == 0
    bucket1.create_task(description="first task")
    assert len(bucket1.tasks) == 1
    task1 = bucket1.get_task(description="first task")
    assert task1.description == "first task"


def test__task_has_custom_repr__succeeds(bucket1):
    """Make sure task has custom __repr__ method"""
    task = bucket1.create_task(description="first task")
    assert 'Task <first task>' in task.__repr__()


def test__bucketlist_cannot_create_existing_task__raises(bucket1):
    """Make sure bucket-list cannot create an already existing task"""
    bucket1.create_task(description="first task")
    assert len(bucket1.tasks) == 1
    with pytest.raises(TaskAlreadyExistsError):
        bucket1.create_task(description="first task")


def test__bucketlist_can_retrieve_task__succeeds(bucket1):
    """Make sure a bucket-list can retrieve a task"""
    task = bucket1.create_task(description="first task")
    task1 = bucket1.get_task(description="first task")
    assert isinstance(task, Task)
    assert task1.description == "first task"


def test__bucketlist_cannot_retrieve_nonexistent_task__raises(bucket1):
    """Make sure a bucketlist cannot retrieve a non-existent task"""
    with pytest.raises(TaskNotExistsError):
        bucket1.get_task(description="first task")


def test__bucketlist_can_delete_task__succeeds(bucket1):
    """Make sure a bucket-list can delete a task"""
    bucket1.create_task(description="first task")
    status = bucket1.delete_task(description="first task")
    assert status
    with pytest.raises(TaskNotExistsError):
        bucket1.get_task(description="first task")


def test__bucketlist_cannot_delete_nonexistent_task__raises(bucket1):
    """Make sure a bucketlist cannot delete a non-existent task"""
    with pytest.raises(TaskNotExistsError):
        bucket1.delete_task(description="first task")
