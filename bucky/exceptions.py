class Error(Exception):
    """Base class for exceptions in this module"""
    pass


class UserNotExistsError(Error):
    """Exception raised when user cannot be found in App Manager

    Attributes:
        message -- explanation of error
    """

    def __init__(self, message):
        self.message = message


class UserAlreadyExistsError(Error):
    """Exception raised when creating user but already exists in App Manager

    Attributes:
        message -- explanation of error
    """

    def __init__(self, message):
        self.message = message


class BucketListNotExistsError(Error):
    """Exception raised when bucket-list cannot be found in user

        Attributes:
            message -- explanation of error
        """
    def __init__(self, message):
        self.message = message


class BucketListAlreadyExistsError(Error):
    """Exception raised when creating bucket-list but already exists in user

        Attributes:
            message -- explanation of error
        """
    def __init__(self, message):
        self.message = message


class TaskAlreadyExistsError(Error):
    """Exception raised when creating task but already exists in bucket-list

    Attributes:
        message -- explanation of error
    """

    def __init__(self, message):
        self.message = message

class TaskNotExistsError(Error):
    """Exception raised when task cannot be found in bucketlist

    Attributes:
        message -- explanation of error
    """

    def __init__(self, message):
        self.message = message
