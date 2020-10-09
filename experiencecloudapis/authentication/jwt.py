import typing
import json
import jwt
import requests
import datetime
from requests import Session
from .auth import AuthenticationClient
from .exceptions import (
    ConfigInsufficientInformationError,
    AuthenticationError
)
from experiencecloudapis.utils import (
    read_file_or_string,
    lower_keys,
    now_in_ms
)


class JWT(AuthenticationClient):
    """
    Implementation of the Service Account Integration (JWT authentication flow)

    A documentation of how to set up this flow can be found here:
    https://www.adobe.io/authentication/auth-methods.html#!AdobeDocs/adobeio-auth/master/AuthenticationOverview/ServiceAccountIntegration.md
    """

    EXCHANGE_ENDPOINT = "https://ims-na1.adobelogin.com/ims/exchange/jwt"
    AUD_ENDPOINT = "https://ims-na1.adobelogin.com/c/"
    REQUIRED_FIELDS = 'client_secret org_id api_key technical_account_id ' \
                      'technical_account_email'.split(' ')

    def __init__(self,
                 config: typing.Union[str, typing.TextIO],
                 key: typing.Union[str, typing.TextIO],
                 company_id: str) -> None:
        # create config object for token creation
        self.config = self.__class__.create_config(config)
        # check if config file has all required fields
        self.__class__.check_config(self.config)
        # read private key and assign to member
        # if key is a file, then it needs to be of type string and not bytes
        self.key = read_file_or_string(key)
        self.config["company_id"] = company_id
        # ToDo: Find a way to make the metascopes configurable
        self.metascopes = {
            "https://ims-na1.adobelogin.com/s/ent_analytics_bulk_ingest_sdk": True # noqa
        }
        self.expires_in: typing.Union[int, None] = None
        self.access_token: typing.Union[str, None] = None

    @property
    def company_id(self) -> str:
        return self.config["company_id"]

    @staticmethod
    def check_config(config: dict) -> bool:
        if not all([k.lower() in config for k in JWT.REQUIRED_FIELDS]):
            missing = ", ".join(filter(lambda f: f.lower() not in config,
                                       JWT.REQUIRED_FIELDS))
            raise ConfigInsufficientInformationError(
                'The following required fields are missing in the config '
                'file: "{missing}". Please make sure that '
                'you use the JSON export file from Adobe IO in the format it '
                'provides.'.format(missing=missing)
            )
        return True

    @staticmethod
    def create_config(data: typing.Union[str, dict, typing.TextIO]) -> dict:
        """
        This method either parses a string to dict or reads a file
        an does the same
        """
        if isinstance(data, dict):
            dict_data = data
        else:
            str_data = read_file_or_string(data)
            dict_data = json.loads(str_data)
        dict_data = lower_keys(dict_data)
        dict_data = \
            {k: v for k, v in dict_data.items() if k in JWT.REQUIRED_FIELDS}
        return dict_data

    @property
    def jwt(self) -> str:
        """
        Building a json web token from the data provided in config

        :return: encrypted jwt token
        """
        return jwt.encode({
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            "iss": self.config['org_id'],
            "sub": self.config['technical_account_id'],
            "aud": f"{self.AUD_ENDPOINT}{self.config['api_key']}",
            **self.metascopes
        }, self.key, algorithm='RS256')

    @property
    def token_response(self) -> dict:
        """
        If successful this method returns an access token for further requests
        with the API. This token needs to be embedded in the HTTP header of the
        API method calls.

        :return: access token, which has this format:

        {
            "expires_in": (int) time in ms
            "access_token": (str) the access token
            "token_type": (str) token type
        }
        """
        jwt_token = self.jwt
        payload = {
            "client_id": self.config['api_key'],
            "client_secret": self.config['client_secret'],
            "jwt_token": jwt_token
        }

        result = requests.post(JWT.EXCHANGE_ENDPOINT, data=payload)
        if result.status_code != 200:
            raise AuthenticationError(result.json())
        else:
            response = result.json()
        return response

    def refresh_token(self):
        token = self.token_response
        self.access_token = token['access_token']
        # set the expiration date in ms. this will be used for checks,
        # if the token needs to be refreshed
        self.expires_in = token['expires_in'] + now_in_ms()

    def authenticate(self, session: Session) -> Session:
        # refresh token if close to expiration or not yet set
        if not self.access_token or not \
                self.expires_in or self.expires_in >= (now_in_ms() + 5000):
            self.refresh_token()
        session.headers.update({
            "x-api-key": self.config['api_key'],
            "x-proxy-global-company-id": self.config["company_id"],
            "Authorization": f'Bearer {self.access_token}',
            "Content-Type": "application/json"
        })
        return session
