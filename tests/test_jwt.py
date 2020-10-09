# flake8: noqa

import pytest
import tempfile
from unittest.mock import Mock
from experiencecloudapis.authentication.jwt import requests
from experiencecloudapis.authentication import JWT
from experiencecloudapis.authentication.exceptions import (
    AuthenticationError,
    ConfigInsufficientInformationError
)


@pytest.fixture
def successful_token_response():
    class Response:
        status_code = 200

        def json(self):
            return {
                'token_type': 'bearer',
                'access_token': 'test_token',
                'expires_in': 86399994
            }

        def __call__(self, *args, **kwargs):
            return self

    return Response()


@pytest.fixture
def unsuccessful_token_response():
    class Response:
        status_code = 400

        def json(self):
            return {
                'error': 'error',
                'error_description': 'something went wrong'
            }

        def __call__(self, *args, **kwargs):
            return self

    return Response()


@pytest.fixture
def fake_private_file():
    tmp = tempfile.NamedTemporaryFile(mode="w", delete=False)
    tmp.write("-----BEGIN RSA PRIVATE KEY-----\n\
MIIEowIBAAKCAQEAhkXLalByIpQrkkIHdF1kNiAgqG1+k9Dx3O446HfBSWApzxfV\n\
XIVR5uCZ8kaa1UFmj+HFqasn3XKGbz52BduzsgMdQmUoidflM6YwBGP/s0QquJ2x\n\
5/gn6seY8JHU/n9UfD9SGfADkS+CwbA6xZEM4o1ZGrmyz2Ru+9OSZSjjwpHd5Jnl\n\
ppPHLuWD6jNlxMpu+h0gBoVOQ16VT6yCQE/HAvC5u+QmLTV2ebHWQwdUhOCbuyGh\n\
UEIqpoUBNWzcnIEdIop2WXOiabUAF8Uh6GOL2WEvKAV+nV7fk910Q1JX4tWQDE3P\n\
1F04qSSc7soHyI1Sv/U8C7iJeDuTMnoCBJllFwIDAQABAoIBAApExC25QUFLu5lP\n\
22oWylcpVdYLqaZ8UELpJQkCP5Hw/MGNvQ96Uq0peByDMcwlWEagqZE0ObRB0e4o\n\
BLal+rQecNpnChagoDK2/u0XCLMY/3tm8/gdjk/yO8wKGxPrgPaPkSPSqzMrQwC1\n\
DYmWcjnRPYNBuF8L+0DfCU8bNW/nwt0qxLAstIxuvveShS8ISaKU2EjoAenWCOhA\n\
pCITKhkicXTQTSVoskiiM7qTFxm3S4KAg7HoZePROzJoCDT70sy8mJnqT3JQx+5F\n\
1uLmXnm0498YMqDVF1pc5tSF4nskGvuQsLrV6onG6jbhDb79ehtYRqaqhmhw/hib\n\
I+tUR8ECgYEA5lhyrVuKDSB9xMkKEe5m3G2qDJKuXc5eq1jrXJTwoWX0vtf7XksQ\n\
NIpjVkpzIND6fL01EGlK9+jxt7B/7dYPs1hrpnhv4aoErajVYKOwtTflwwYdhj8+\n\
SguegZAv6N+UE11y8/QehlFH0ldyO0HBWCCrMf8IrsDTXfWpyj2jQGkCgYEAlTok\n\
Q8nX1pn8GyeflYu9o5Bots+PSXEe1DCzB7OUdoErp/p/dhJ5Ckts7Gt2FTgrUcXx\n\
JyaATOGUJ59SIwbMi+FxSOgES9oIeBMccIc9SkQlH4RhPfwSrnxiB0Mi5KSHQKIA\n\
Bza8r3+g7dhZz2J4J+/erLvsrwwFmeFsfOl6yX8CgYEAoABiL/785t9h3VZUU15J\n\
PuZCD5e33NsjsVwDqPygJUxf9Eysg7QaXpSeKetvCyV+STVYbbzl4UyC0ricNEXU\n\
BBzwMeNIu/TQaRx0kztA3LAmPhC6Y2z8xIxLnu3cCaN8BPONjN1Ocrh07ivl4jlr\n\
pt6SbBkeG90/NO4W8a9c/bkCgYAuYLOEneaGu7Sue9INGDEH9ImWx0sw+AcsyzXY\n\
3ub1LY/z1NZoS7VyjZ58m6lHTv2nnG0mTcDyI+l3pvxQBnzrvFUI45LyQAEB0G62\n\
SlGyExu2f9349a6Yq++LckIV7Uxbuf1oQIrDwFazlNnUqjXNs67w4Dbe8E2NVZHy\n\
AF444QKBgFTE5IAKpWBhQRtk0+YEB9Oj8Ny+PyMNwo9UCkYJSQgD/XZ5oRYaUzxz\n\
yaIWRbDf80xoeVjdNZU5/2n9lbLRXj0RWillUklgKhhuoX9su/mL8n1fXpTcGjZz\n\
pu/inMjiBCS/cVdTfDf6VZywQ2NLDBJqWzo9E1xxapBPDSBuB5nQ\n\
-----END RSA PRIVATE KEY-----\n")
    tmp.close()
    return tmp


@pytest.fixture
def correct_config():
    return {
        "CLIENT_SECRET": "testtesttest",
        "ORG_ID": "testtesttest",
        "API_KEY": "testtesttest",
        "PUBLIC_KEYS_WITH_EXPIRY": {
            "testtesttest": "07/21/2030"
        },
        "TECHNICAL_ACCOUNT_ID": "testtesttest@techacct.adobe.com",
        "TECHNICAL_ACCOUNT_EMAIL": "testtesttest@techacct.adobe.com"
    }


def test_config_check(correct_config):
    wrong_config = {
        "CLIENT_SECRET": "testtesttest",
        "ORG_ID": "testtesttest",
        "PUBLIC_KEYS_WITH_EXPIRY": {
            "testtesttest": "07/21/2030"
        },
        "TECHNICAL_ACCOUNT_EMAIL": "testtesttest@techacct.adobe.com"
    }
    config_1 = JWT.create_config(correct_config)
    assert JWT.check_config(config_1) is True
    config_2 = JWT.create_config(wrong_config)
    with pytest.raises(ConfigInsufficientInformationError):
        JWT.check_config(config_2)


def test_jwt_client_init(correct_config, fake_private_file):
    jwt_client = JWT(correct_config, fake_private_file, 'test_company')
    assert list(jwt_client.config.keys()) == \
           'client_secret org_id api_key technical_account_id ' \
           'technical_account_email company_id'.split(' ')
    with open(fake_private_file.name, "r") as fd:
        data = fd.read()
    assert jwt_client.key == data


def test_jwt_client_init_from_path(correct_config, fake_private_file):
    jwt_client = JWT(correct_config, fake_private_file.name, 'test_company')
    assert list(jwt_client.config.keys()) == \
           'client_secret org_id api_key technical_account_id ' \
           'technical_account_email company_id'.split(' ')
    with open(fake_private_file.name, "r") as fd:
        data = fd.read()
    assert jwt_client.key == data


def test_jwt_client_init_file_not_found(correct_config):
    with pytest.raises(FileNotFoundError):
        jwt_client = JWT(correct_config, "testtesttest", 'test_company')


def test_get_jwt(correct_config, fake_private_file):
    jwt_client = JWT(correct_config, fake_private_file.name, 'test_company')
    jwt = jwt_client.jwt
    assert jwt is not None
    assert isinstance(jwt, bytes)


def test_access_token(correct_config,
                      fake_private_file,
                      monkeypatch,
                      successful_token_response):
    jwt_client = JWT(correct_config, fake_private_file.name, 'test_company')
    monkeypatch.setattr(requests, "post", successful_token_response)
    access_token = jwt_client.token_response
    assert access_token == {'access_token': 'test_token',
                            'expires_in': 86399994,
                            'token_type': 'bearer'}


def test_access_token_fail(correct_config,
                           fake_private_file,
                           monkeypatch,
                           unsuccessful_token_response):
    jwt_client = JWT(correct_config, fake_private_file.name, 'test_company')
    monkeypatch.setattr(requests, "post", unsuccessful_token_response)
    with pytest.raises(AuthenticationError):
        access_token = jwt_client.token_response


def test_access_token_update(correct_config,
                             fake_private_file,
                             monkeypatch,
                             successful_token_response):
    jwt_client = JWT(correct_config, fake_private_file.name, 'test_company')
    mock_session = Mock()
    jwt_client.refresh_token = Mock()
    jwt_client.authenticate(mock_session)
    mock_session.headers.update.assert_called_once()
    jwt_client.refresh_token.assert_called_once()


def test_access_token_no_update(correct_config,
                                fake_private_file,
                                monkeypatch,
                                successful_token_response):
    jwt_client = JWT(correct_config, fake_private_file.name, 'test_company')
    jwt_client.access_token = "123"
    jwt_client.expires_in = 123
    mock_session = Mock()
    jwt_client.refresh_token = Mock()
    jwt_client.authenticate(mock_session)
    mock_session.headers.update.assert_called_once()
    jwt_client.refresh_token.assert_not_called()
