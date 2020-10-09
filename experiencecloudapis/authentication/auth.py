import abc
from requests.sessions import Session


class AuthenticationClient(abc.ABC):
    """
    Abstract Class for Authentication.
    This will be used for concrete authentication implementations
    """
    @property
    @abc.abstractmethod
    def company_id(self) -> str:
        raise NotImplementedError('company_id must be implemented')

    @abc.abstractmethod
    def authenticate(self, session: Session) -> Session:
        raise NotImplementedError('authenticate must be implemented')
