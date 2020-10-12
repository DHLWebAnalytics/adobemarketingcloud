# flake8: noqa

import pytest
from unittest.mock import Mock
from experiencecloudapis import Target
from experiencecloudapis.exceptions import PayloadTooLargeError
from experiencecloudapis.target import requests


class TestProfileParameters:
    def test_profile_query_param_enhance(self):
        target_mock = Target(None, None)  # noqa
        profile_params_map = {
            'profile.key1': 'test1.!',
            'key2': 'test2~',
        }
        enhanced_map = target_mock.\
            _enchance_profile_map(profile_params_map)
        for key in enhanced_map.keys():
            assert key.startswith('profile.')


class TestError:
    def test_payload_too_large_error(self):
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

    @pytest.fixture()
    def mock_access_token(self):
        class Response:
            def json(self):
                return {
                    "accessToken": "dummy"
                }
        return Response()

    @pytest.fixture()
    def api_base(self):
        return 'https://mc.adobe.io/tenant'

    @pytest.mark.parametrize(
        'input, expected_url',
        [
            (('get_debug_authentication_token', 'get', ), '/target/authentication/token'),
            (('get_profile_authentication_token', 'get', ), '/target/authentication/token'),
            (('list_activities', 'get', ), '/target/activities/'),
            (('get_ab_activity', 'get', 'id'), '/target/activities/ab/id'),
            (('delete_ab_activity', 'delete', 'id'), '/target/activities/ab/id'),
            (('create_ab_activity', 'post', {}), '/target/activities/ab'),
            (('update_ab_activity', 'put', 'id', {}), '/target/activities/ab/id'),
            (('get_xt_activity', 'get', 'id'), '/target/activities/xt/id'),
            (('delete_xt_activity', 'delete', 'id'), '/target/activities/xt/id'),
            (('create_xt_activity', 'post', {}), '/target/activities/xt'),
            (('update_xt_activity', 'put', 'id', {}), '/target/activities/xt/id'),
            (('update_activity_name', 'put', 'id', {}), '/target/activities/id/name'),
            (('update_ab_activity_name', 'put', 'id', {}), '/target/activities/ab/id/name'),
            (('update_xt_activity_name', 'put', 'id', {}), '/target/activities/xt/id/name'),
            (('update_activity_state', 'put', 'id', {}), '/target/activities/id/state'),
            (('update_ab_activity_state', 'put', 'id', {}), '/target/activities/ab/id/state'),
            (('update_xt_activity_state', 'put', 'id', {}), '/target/activities/xt/id/state'),
            (('update_activity_priority', 'put', 'id', {}), '/target/activities/id/priority'),
            (('update_ab_activity_priority', 'put', 'id', {}), '/target/activities/ab/id/priority'),
            (('update_xt_activity_priority', 'put', 'id', {}), '/target/activities/xt/id/priority'),
            (('update_activity_schedule', 'put', 'id', {}), '/target/activities/id/schedule'),
            (('update_ab_activity_schedule', 'put', 'id', {}), '/target/activities/ab/id/schedule'),
            (('update_xt_activity_schedule', 'put', 'id', {}), '/target/activities/xt/id/schedule'),
            (('get_activity_changelog', 'get', 'id'), '/target/activities/id/changelog'),
            (('list_offers', 'get'), '/target/offers'),
            (('get_offer', 'get', 'id'), '/target/offers/content/id'),
            (('create_offer', 'post', {}), '/target/offers/content'),
            (('update_offer', 'put', 'id', {}), '/target/offers/content/id'),
            (('delete_offer', 'delete', 'id'), '/target/offers/content/id'),
            (('list_audiences', 'get'), '/target/audiences'),
            (('get_audience', 'get', 'id'), '/target/audiences/id'),
            (('create_audience', 'post', {}), '/target/audiences'),
            (('update_audience', 'put', 'id', {}), '/target/audiences/id'),
            (('delete_audience', 'delete', 'id'), '/target/audiences/id'),
            (('list_properties', 'get'), '/target/properties'),
            (('get_property', 'get', 'id'), '/target/properties/id'),
            (('get_ab_performance_report', 'get', 'id'), '/target/activities/ab/id/report/performance'),
            (('get_xt_performance_report', 'get', 'id'), '/target/activities/xt/id/report/performance'),
            (('get_ap_activity_performance_report', 'get', 'id'), '/target/activities/abt/id/report/performance'),
            (('get_ab_audit_report', 'get', 'id'), '/target/activities/ab/id/report/orders'),
            (('get_xt_audit_report', 'get', 'id'), '/target/activities/xt/id/report/orders'),
            (('get_ap_audit_report', 'get', 'id'), '/target/activities/abt/id/report/orders'),
            (('list_mboxes', 'get'), '/target/mboxes'),
            (('list_mbox_parameters', 'get', 'id'), '/target/mbox/id'),
            (('list_profile_parameters', 'get'), '/target/profileattributes/mbox'),
            (('list_environments', 'get'), '/target/environments'),
            (('batch', 'post', {}), '/target/batch'),
        ]
    )
    def test_correct_endpoint(self,
                              mock_response,
                              api_base,
                              input,
                              expected_url):
        method, http_method, *args = input
        m = Mock()
        attrs = dict()
        attrs[f'{http_method}.return_value'] = mock_response
        m.configure_mock(**attrs)
        target = Target(Mock(), 'tenant', m)
        getattr(target, method)(*args)
        getattr(target.session, http_method).assert_called()
        url = getattr(target.session, http_method).call_args[0][0]
        assert url == f'{api_base}{expected_url}'

    @pytest.mark.parametrize(
        'input, expected_url',
        [
            (('fetch_profile_tnt', 'id'), 'https://tenant.tt.omtrdc.net/rest/v1/profiles/id?client=tenant'),
            (('fetch_profile_trd_party', 'id'), 'https://tenant.tt.omtrdc.net/rest/v1/profiles/thirdPartyId/id?client=tenant'),
            (('single_profile_update_tnt', 'id', {}), 'https://tenant.tt.omtrdc.net/m2/client/profile/update'),
            (('single_profile_update_trd_party', 'id', {}), 'https://tenant.tt.omtrdc.net/m2/client/profile/update'),
        ]
    )
    def test_correct_format_profile(self,
                                    mock_response,
                                    mock_access_token,
                                    input,
                                    expected_url):
        method, *args = input
        m = Mock()
        m.get = Mock(return_value=mock_response)
        target = Target(Mock(), 'tenant', m)
        target.get_profile_authentication_token = \
            Mock(return_value=mock_access_token)
        getattr(target, method)(*args)
        target.session.get.assert_called()
        url = target.session.get.call_args[0][0]
        assert url == expected_url
