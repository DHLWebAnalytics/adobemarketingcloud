class ConfigInsufficientInformationError(Exception):
    """
    Config file has insufficient information and an authentication
    would fail
    """

    def __init__(self, *args, **kwargs):
        pass


class AuthenticationError(Exception):
    """Error when jwt authentication request fails"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'{self.message["error"]}\n{self.message["error_description"]}'


class InvalidMethodInvocation(Exception):
    """Raised if invalid requests method is tried to be invoked"""
    pass
