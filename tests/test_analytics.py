# flake8: noqa

from unittest.mock import Mock
from experiencecloudapis import Analytics


def test_authentication():
    class FakeResponse:
        status_code = 200

        def json(self):
            return {"test": "test"}

    mock_auth_client = Mock()
    mock_session = Mock()
    mock_session.get = Mock(return_value=FakeResponse())
    analytics_client = Analytics(mock_auth_client, mock_session)
    response = analytics_client.get_calculatedmetrics()
    mock_auth_client.authenticate.assert_called_once()
    assert isinstance(response, FakeResponse)
