# flake8: noqa

import pytest
from unittest.mock import Mock
from experiencecloudapis import Target
from experiencecloudapis.exceptions import PayloadTooLargeError
from experiencecloudapis.target import requests


def test_profile_query_param_enhance():
    target_mock = Target(None, None)  # noqa
    profile_params_map = {
        'profile.key1': 'test1.!',
        'key2': 'test2~',
    }
    enhanced_map = target_mock.\
        _enchance_profile_map(profile_params_map)
    for key in enhanced_map.keys():
        assert key.startswith('profile.')


def test_payload_too_large_error():
    target_mock = Target(Mock(), requests.Session())  # noqa

    class MockResponse:
        def json(self):
            return {
                'accessToken': 'test',
            }

    target_mock.get_profile_authentication_token = \
        Mock(return_value=MockResponse())
    profile_params = {"a": "a" * 10000}
    with pytest.raises(PayloadTooLargeError):
        target_mock.single_profile_update_tnt('test', profile_params)


class TestAPIMethodEndpoints:
    @pytest.fixture()
    def mock_response(self):
        class Response:
            status_code = 200
        return Response()

    @pytest.mark.parametrize(
        'method,expected_url',
        [
            ('get_debug_authentication_token', 'https://mc.adobe.io/tenant/target/authentication/token'),
            ('get_profile_authentication_token', 'https://mc.adobe.io/tenant/target/authentication/token'),
            ('list_activities', 'https://mc.adobe.io/tenant/target/activities/'),
        ]
    )
    def test_endpoint(self, mock_response, method, expected_url):
        m = Mock()
        m.get = Mock(return_value=mock_response)
        target = Target(Mock(), 'tenant', m)
        getattr(target, method)()
        target.session.get.assert_called()
        url = target.session.get.call_args[0][0]
        assert url == expected_url
