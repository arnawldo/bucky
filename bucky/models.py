from werkzeug.security import generate_password_hash, check_password_hash
from bucky.exceptions import UserNotExistsError, UserAlreadyExistsError


class AppManager(object):
    """Creates and manages User instances of the web app.
    All data on app is lost if the AppManager object is deleted

    Attributes:
        users -- Collection of User instances
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


class User(object):
    """Class for users of app

    Attributes:
        username -- username of user
        email -- email address of user
        password -- hashed password
    """

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hashed = None
        self.set_password(password)

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


class BucketList(object):
    """Class for bucket-lists created by users of app

    Attributes:
        name -- name of bucket-list
    """
    pass
