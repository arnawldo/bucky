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