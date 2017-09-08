from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from bucky import login_manager
from bucky.exceptions import UserNotExistsError, UserAlreadyExistsError, BucketListAlreadyExistsError, \
    BucketListNotExistsError, TaskAlreadyExistsError, TaskNotExistsError


class AppManager(object):
    """Creates AppManager (User store) of the web app.

    This class implements the singleton pattern to keep only a single AppManager
    object wherever it is instantiated.
    AppManager is a shell class that always returns __AppManager (the Singleton)

    All data on app is lost if the AppManager object is deleted

    Attributes:
        instance -- Class attribute that stores the singleton
    """
    class __AppManager(object):
        """Class that stores and manages User instances.
        Only one of this can be created

        """
        def __init__(self):
            """Initialize app manager with zero users"""
            self.users = {}

        def create_user(self, username, email, password):
            """
            Add user instance to storage

            :param username: username of user
            :type username: str
            :param email: email of user
            :type email: str
            :param password: hashed password
            :type password: str
            :return: created user instance
            :rtype: User
            """
            try:
                user = self.users[username]
                raise UserAlreadyExistsError("User <{}> already exists".format(user.username))
            except KeyError:
                self.users[username] = User(username, email, password)
                return self.users[username]

        def delete_user(self, username):
            """
            Delete user instance from storage

            :param username: username of user
            :return: Operation success
            :rtype: bool
            """

            try:
                del self.users[username]
                return True
            except KeyError:
                raise UserNotExistsError("User <{}> cannot be found".format(username))

        def get_user(self, username):
            """
            Retrieve user instance of given name

            :param username: username of user
            :return: User object
            """
            try:
                return self.users[username]
            except KeyError:
                raise UserNotExistsError("User <{}> cannot be found".format(username))

        def __repr__(self):
            return "AppManager <n_users={}>".format(len(self.users))

    instance = None # Singleton store

    def __init__(self):
        if not AppManager.instance:
            AppManager.instance = AppManager.__AppManager()

    def __repr__(self):
        return "AppManager Store\nStoring:{}".format(AppManager.instance)


class User(UserMixin, object):
    """Class for users of app

    Attributes:
        username -- username of user
        email -- email address of user
        password -- hashed password
        buckets -- bucket-lists created by user
    """

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hashed = None
        self.set_password(password)
        self.buckets = {}

    def set_password(self, password):
        """Hash password plus a salt --algorithm by Werkzeug

        :param password: unhashed password
        :type password: str
        :return: None
        """
        self.password_hashed = generate_password_hash(password)

    def verify_password(self, password):
        """Verify password

        :param password: unhashed password
        :type password: str
        :return: verification status
        :rtype: bool
        """
        return check_password_hash(self.password_hashed, password)

    def create_bucketlist(self, name):
        """Create bucket-list with given name

        :param name: name of bucketlist
        :type name: str
        :return: created bucket-list
        :rtype: BucketList
        """
        try:
            bucketlist = self.buckets[name]
            raise BucketListAlreadyExistsError("BucketList <{}> already exists".format(bucketlist.name))
        except KeyError:
            self.buckets[name] = BucketList(name=name)
            return self.buckets[name]

    def get_bucketlist(self, name):
        """Retrieve bucket-list of given name

        :param name: name of bucket-list
        :type name: str
        :return: bucket-list
        :rtype: BucketList
        """
        try:
            return self.buckets[name]
        except KeyError:
            raise BucketListNotExistsError("BucketList <{}> cannot be found".format(name))

    def delete_bucketlist(self, name):
        """Delete bucket-list of given name

        :param name: name of bucket-list
        :type name: str
        :return: operation success
        :rtype: bool
        """
        try:
            del self.buckets[name]
            return True
        except KeyError:
            raise BucketListNotExistsError("BucketList <{}> cannot be found".format(name))

    def get_id(self):
        """Get unique identifier of user. Requirement for flask-login ext

        :return: username of user
        """
        return self.username

    def __repr__(self):
        return "User <{}>".format(self.username)

@login_manager.user_loader
def load_user(user_id):
    am = AppManager().instance
    try:
        return am.get_user(username=user_id)
    except UserNotExistsError:
        return None

class BucketList(object):
    """Class for bucket-lists created by users of app

    Attributes:
        name -- name of bucket-list
        tasks -- tasks created by bucket-list
    """

    def __init__(self, name):
        self.name = name
        self.tasks = {}

    def create_task(self, description):
        """Create task with given description

        :param description: description of task
        :type name: str
        :return: created task
        :rtype: Task
        """
        try:
            task = self.tasks[description]
            raise TaskAlreadyExistsError("Task <{}> already exists".format(task.description))
        except KeyError:
            self.tasks[description] = Task(description=description)
            return self.tasks[description]

    def get_task(self, description):
        """Retrieve task of given description

        :param description: description of task
        :type name: str
        :return: task
        :rtype: Task
        """
        try:
            return self.tasks[description]
        except KeyError:
            raise TaskNotExistsError("Task <{}> cannot be found".format(description))

    def delete_task(self, description):
        """Delete task of given description

        :param description: description of task
        :type name: str
        :return: operation success
        :rtype: bool
        """
        try:
            del self.tasks[description]
            return True
        except KeyError:
            raise TaskNotExistsError("Task <{}> cannot be found".format(description))

    def __repr__(self):
        return "BucketList <{}>".format(self.name)


class Task(object):
    """Class for tasks created by bucket-list of user

        Attributes:
            description -- description of task
        """

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return "Task <{}>".format(self.description)
