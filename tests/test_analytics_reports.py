# flake8: noqa

import pytest
from unittest.mock import Mock
from requests import Session
from experiencecloudapis.authentication.auth import AuthenticationClient
from experiencecloudapis.analytics_reports import (
    Table,
    Reports,
    ColumnsMissmatchError
)


@pytest.fixture
def fake_authentication_client():
    class FakeAuthenticationClient(AuthenticationClient):
        @property
        def company_id(self) -> str:
            pass

        def authenticate(self, session: Session) -> Session:
            pass

    return FakeAuthenticationClient()


@pytest.mark.parametrize("filter,expected", [
    (
        [{"type": "segment","segmentId": "s1214_5e2f089d1c252a42bd21e816"},{"type": "dateRange","dateRange": "2020-01-01T00:00:00.000/2020-08-01T00:00:00.000"}],
        "[test]"
    ),
    (
        [{"type": "dateRange","dateRange": "2020-01-01T00:00:00.000/2020-08-01T00:00:00.000"}],
        ""
    ),
    (
        [{"type":"segment","segmentDefinition":{"container":{"func":"container","context":"hits","pred":{"func":"streq","str":"GoogleChrome84.0","val":{"func":"attr","name":"variables/browser"},"description":"Browser"}},"func":"segment","version":[1,0,0]}},{"type":"dateRange","dateRange":"2020-08-01T00:00:00.000/2020-09-01T00:00:00.000"}],
        "[Browser[GoogleChrome84.0]]"
    ),
    (
        [{"type": "segment","segmentId": "s1214_5e2f089d1c252a42bd21e816"},{"type":"segment","segmentDefinition":{"container":{"func":"container","context":"hits","pred":{"func":"streq","str":"GoogleChrome84.0","val":{"func":"attr","name":"variables/browser"},"description":"Browser"}},"func":"segment","version":[1,0,0]}},{"type":"dateRange","dateRange":"2020-08-01T00:00:00.000/2020-09-01T00:00:00.000"}],
        "[test][Browser[GoogleChrome84.0]]"
    )
])
def test_expand_segments(filter, expected):
    class FakeAnalytics:
        def get_segment(self, filter):
            class Response:
                def json(self):
                    return {"name": "test"}
            return Response()

    analytics_client = FakeAnalytics()
    table = Table(analytics_client)
    global_segments = table._expand_global_segment(filter)
    assert global_segments == expected


@pytest.mark.parametrize("filter,expected", [
    (
        [{"id":"0","type":"breakdown","dimension":"variables/evar200","itemId":"3530724823"},{"id":"1","type":"dateRange","dateRange":"2020-07-01T00:00:00.000/2020-08-01T00:00:00.000"},{"id":"2","type":"segment","segmentId":"s1214_5edf9083f6454c1edaf76fe9"},{"id":"3","type":"breakdown","dimension":"variables/mobiledevicetype","itemId":"0"},{"id":"4","type":"breakdown","dimension":"variables/mobiledevicetype","itemId":"0"}],
        {
            "0": "evar200[3530724823]",
            "1": "2020-07-01T00:00:00.000/2020-08-01T00:00:00.000",
            "2": "test",
            "3": "mobiledevicetype[0]",
            "4": "mobiledevicetype[0]"
        }
    ),
    (
        [{"id":"0","type":"segment","segmentId":"s1214_5edf9083f6454c1edaf76fe9"}],
        {
            "0": "test"
        }
    ),
    (
        [{"id":"0","type":"test","rubbish":"test"},{"id":"1","type":"test2","rubbish":"test"},{"id":"2","type":"segment","segmentId":"s1214_5edf9083f6454c1edaf76fe9"}],
        {
            "0": "unknown",
            "1": "unknown",
            "2": "test"
        }
    ),
    (
        [{"id":"0","type":"breakdown","dimension":"test"},{"id":"1","type":"segment","segmentId":"s1214_5edf9083f6454c1edaf76fe9"}],
        {
            "0": "test",
            "1": "test"
        }
    )
])
def test_create_metrics_filters_map(filter, expected):
    class FakeAnalytics:
        def get_segment(self, filter):
            class Response:
                def json(self):
                    return {"name": "test"}
            return Response()

    analytics_client = FakeAnalytics()
    table = Table(analytics_client)
    filter_map = table._create_metric_filters_dict(filter)
    assert filter_map == expected


@pytest.mark.parametrize("payload,expected", [
    (
        {"rsid":"vrs_dhlcom1_countriesmxauuscopy","globalFilters":[{"type":"segment","segmentId":"s1214_5e2f089d1c252a42bd21e816"},{"type":"dateRange","dateRange":"2020-01-01T00:00:00.000/2020-08-01T00:00:00.000"}],"metricContainer":{"metrics":[{"columnId":"1","id":"metrics/visits","filters":["0"]},{"columnId":"2","id":"metrics/productinstances"},{"columnId":"7","id":"metrics/event190"},{"columnId":"9","id":"cm1214_5f05dbd75a90fb3af0913538","filters":["4"]}],"metricFilters":[{"id":"0","type":"breakdown","dimension":"variables/evar200","itemId":"3530724823"},{"id":"1","type":"dateRange","dateRange":"2020-07-01T00:00:00.000/2020-08-01T00:00:00.000"},{"id":"2","type":"segment","segmentId":"s1214_5edf9083f6454c1edaf76fe9"},{"id":"3","type":"breakdown","dimension":"variables/mobiledevicetype","itemId":"0"},{"id":"4","type":"breakdown","dimension":"variables/mobiledevicetype","itemId":"0"}]},"dimension":"variables/daterangemonth","settings":{"countRepeatInstances":True,"limit":400,"page":0,"dimensionSort":"asc","nonesBehavior":"return-nones"},"statistics":{"functions":["col-max","col-min"]}},
        ['visits[test][evar200[3530724823]]', 'productinstances[test]', 'event190[test]', 'test[test][mobiledevicetype[0]]']
    ),
    (
        {"rsid":"dhlglobalrolloutprod","globalFilters":[{"type":"dateRange","dateRange":"2020-08-01T00:00:00.000/2020-09-01T00:00:00.000"}],"metricContainer":{"metrics":[{"columnId":"1","id":"metrics/visits","filters":["0"]}],"metricFilters":[{"id":"0","type":"breakdown","dimension":"variables/evar36.1","itemId":"1249205158"}]},"dimension":"variables/daterangeday","settings":{"countRepeatInstances":True,"limit":400,"page":0,"dimensionSort":"asc","nonesBehavior":"return-nones"},"statistics":{"functions":["col-max","col-min"]}},
        ['visits[evar36.1[1249205158]]']
    ),
    (
        {"rsid":"dhlglobalrolloutprod","globalFilters":[{"type":"dateRange","dateRange":"2020-08-01T00:00:00.000/2020-09-01T00:00:00.000"}],"metricContainer":{"metrics":[{"columnId":"0","id":"metrics/visits"}]},"dimension":"variables/daterangeday","settings":{"countRepeatInstances":True,"limit":400,"page":0,"dimensionSort":"asc","nonesBehavior":"return-nones"},"statistics":{"functions":["col-max","col-min"]}},
        ['visits']
    ),
    (
        {"rsid":"dhlglobalrolloutprod","globalFilters":[{"type":"dateRange","dateRange":"2020-08-01T00:00:00.000/2020-09-01T00:00:00.000"}],"metricContainer":{"metrics":[{"columnId":"1","id":"metrics/visits","filters":["0"]}],"metricFilters":[{"id":"0","type":"dateRange","dateRange":"2020-07-01T00:00:00.000/2020-08-01T00:00:00.000"}]},"dimension":"variables/daterangeday","settings":{"countRepeatInstances":True,"limit":400,"page":0,"dimensionSort":"asc","nonesBehavior":"return-nones"},"statistics":{"functions":["col-max","col-min"]}},
        ['visits[2020-07-01T00:00:00.000/2020-08-01T00:00:00.000]']
    )
])
def test_expand_columns(payload, expected):
    class FakeAnalytics:
        def get_segment(self, filter):
            class Response:
                def json(self):
                    return {"name": "test"}
            return Response()

        def get_metric(self, id, rsid):
            class Response:
                def json(self):
                    return {"name": "test"}
            return Response()

        def get_calculatedmetric(self, id):
            class Response:
                def json(self):
                    return {"name": "test"}
            return Response()

    analytics_client = FakeAnalytics()
    table = Table(analytics_client)
    columns = table._expand_column_names(payload)
    assert columns == expected


@pytest.mark.parametrize("payload,expected", [
    (
        {"rsid":"vrs_dhlcom1_countriesmxauuscopy","globalFilters":[{"type":"segment","segmentId":"s1214_5e2f089d1c252a42bd21e816"},{"type":"dateRange","dateRange":"2020-01-01T00:00:00.000/2020-08-01T00:00:00.000"}],"metricContainer":{"metrics":[{"columnId":"1","id":"metrics/visits","filters":["0"]},{"columnId":"2","id":"metrics/productinstances"},{"columnId":"7","id":"metrics/event190"},{"columnId":"9","id":"cm1214_5f05dbd75a90fb3af0913538","filters":["4"]}],"metricFilters":[{"id":"0","type":"breakdown","dimension":"variables/evar200","itemId":"3530724823"},{"id":"1","type":"dateRange","dateRange":"2020-07-01T00:00:00.000/2020-08-01T00:00:00.000"},{"id":"2","type":"segment","segmentId":"s1214_5edf9083f6454c1edaf76fe9"},{"id":"3","type":"breakdown","dimension":"variables/mobiledevicetype","itemId":"0"},{"id":"4","type":"breakdown","dimension":"variables/mobiledevicetype","itemId":"0"}]},"dimension":"variables/daterangemonth","settings":{"countRepeatInstances":True,"limit":400,"page":0,"dimensionSort":"asc","nonesBehavior":"return-nones"},"statistics":{"functions":["col-max","col-min"]}},
        ['visits[test][evar200[3530724823]]', 'productinstances[test]', 'event190[test]', 'test[test][mobiledevicetype[0]]']
    ),
    (
        {"rsid":"dhlglobalrolloutprod","globalFilters":[{"type":"dateRange","dateRange":"2020-08-01T00:00:00.000/2020-09-01T00:00:00.000"}],"metricContainer":{"metrics":[{"columnId":"1","id":"metrics/visits","filters":["0"]}],"metricFilters":[{"id":"0","type":"breakdown","dimension":"variables/evar36.1","itemId":"1249205158"}]},"dimension":"variables/daterangeday","settings":{"countRepeatInstances":True,"limit":400,"page":0,"dimensionSort":"asc","nonesBehavior":"return-nones"},"statistics":{"functions":["col-max","col-min"]}},
        ['visits[evar36.1[1249205158]]']
    ),
    (
        """{"rsid":"dhlglobalrolloutprod","globalFilters":[{"type":"dateRange","dateRange":"2020-08-01T00:00:00.000/2020-09-01T00:00:00.000"}],"metricContainer":{"metrics":[{"columnId":"0","id":"metrics/visits"}]},"dimension":"variables/daterangeday","settings":{"countRepeatInstances":true,"limit":400,"page":0,"dimensionSort":"asc","nonesBehavior":"return-nones"},"statistics":{"functions":["col-max","col-min"]}}""",
        ['visits']
    ),
    (
        """{"rsid":"dhlglobalrolloutprod","globalFilters":[{"type":"dateRange","dateRange":"2020-08-01T00:00:00.000/2020-09-01T00:00:00.000"}],"metricContainer":{"metrics":[{"columnId":"1","id":"metrics/visits","filters":["0"]}],"metricFilters":[{"id":"0","type":"dateRange","dateRange":"2020-07-01T00:00:00.000/2020-08-01T00:00:00.000"}]},"dimension":"variables/daterangeday","settings":{"countRepeatInstances":true,"limit":400,"page":0,"dimensionSort":"asc","nonesBehavior":"return-nones"},"statistics":{"functions":["col-max","col-min"]}}""",
        ['visits[2020-07-01T00:00:00.000/2020-08-01T00:00:00.000]']
    )
])
def test_process_payload(payload, expected):
    class FakeAnalytics:
        def get_segment(self, filter):
            class Response:
                def json(self):
                    return {"name": "test"}
            return Response()

        def get_metric(self, id, rsid):
            class Response:
                def json(self):
                    return {"name": "test"}
            return Response()

        def get_calculatedmetric(self, id):
            class Response:
                def json(self):
                    return {"name": "test"}
            return Response()

    analytics_client = FakeAnalytics()
    table = Table(analytics_client)
    table.process_payload(payload)
    columns = table.columns
    assert columns == expected


def test_custom_column_labels(fake_authentication_client):
    payload = {
        "metricContainer": {
            "metrics": [
                {
                    "columnId": "1",
                    "id": "metrics/visits",
                    "filters": [
                        "0"
                    ]
                },
                {
                    "columnId": "2",
                    "id": "metrics/productinstances"
                }
            ]
        }
    }
    custom_columns = ["test_1", "test_2"]
    reports_client = Reports(fake_authentication_client, Session())
    reports_client._create_table = Mock()
    reports_client.request_report(payload, column_names=custom_columns)
    reports_client._create_table.assert_called_with(payload, True, custom_columns)


def test_columns_missmatch_error(fake_authentication_client):
    payload = {
        "metricContainer": {
            "metrics": [
                {
                    "columnId": "1",
                    "id": "metrics/visits",
                    "filters": [
                        "0"
                    ]
                },
                {
                    "columnId": "2",
                    "id": "metrics/productinstances"
                }
            ]
        }
    }
    custom_columns = ["test_1", "test_2", "test_3"]
    reports_client = Reports(fake_authentication_client, Session())
    reports_client._create_table = Mock()
    with pytest.raises(ColumnsMissmatchError):
        reports_client.request_report(payload, column_names=custom_columns)


@pytest.mark.parametrize("response,expected", [
    (
        {"totalPages":1,"firstPage":True,"lastPage":True,"numberOfElements":31,"number":0,"totalElements":31,"columns":{"dimension":{"id":"variables/daterangeday","type":"time"},"columnIds":["1"]},"rows":[{"itemId":"1200601","value":"Jul1,2020","data":[623411]},{"itemId":"1200602","value":"Jul2,2020","data":[615693]},{"itemId":"1200603","value":"Jul3,2020","data":[554453]},{"itemId":"1200604","value":"Jul4,2020","data":[319997]},{"itemId":"1200605","value":"Jul5,2020","data":[243997]},{"itemId":"1200606","value":"Jul6,2020","data":[614759]},{"itemId":"1200607","value":"Jul7,2020","data":[651221]},{"itemId":"1200608","value":"Jul8,2020","data":[648018]},{"itemId":"1200609","value":"Jul9,2020","data":[717985]},{"itemId":"1200610","value":"Jul10,2020","data":[711176]},{"itemId":"1200611","value":"Jul11,2020","data":[430227]},{"itemId":"1200612","value":"Jul12,2020","data":[327528]},{"itemId":"1200613","value":"Jul13,2020","data":[797155]},{"itemId":"1200614","value":"Jul14,2020","data":[827032]},{"itemId":"1200615","value":"Jul15,2020","data":[813953]},{"itemId":"1200616","value":"Jul16,2020","data":[792625]},{"itemId":"1200617","value":"Jul17,2020","data":[688593]},{"itemId":"1200618","value":"Jul18,2020","data":[400140]},{"itemId":"1200619","value":"Jul19,2020","data":[307529]},{"itemId":"1200620","value":"Jul20,2020","data":[734327]},{"itemId":"1200621","value":"Jul21,2020","data":[791913]},{"itemId":"1200622","value":"Jul22,2020","data":[785724]},{"itemId":"1200623","value":"Jul23,2020","data":[761433]},{"itemId":"1200624","value":"Jul24,2020","data":[705225]},{"itemId":"1200625","value":"Jul25,2020","data":[428831]},{"itemId":"1200626","value":"Jul26,2020","data":[330641]},{"itemId":"1200627","value":"Jul27,2020","data":[767689]},{"itemId":"1200628","value":"Jul28,2020","data":[830582]},{"itemId":"1200629","value":"Jul29,2020","data":[820369]},{"itemId":"1200630","value":"Jul30,2020","data":[787743]},{"itemId":"1200631","value":"Jul31,2020","data":[683612]}],"summaryData":{"filteredTotals":[19486184],"totals":[19486184],"col-max":[830582],"col-min":[243997]}},
        ([('Jul1,2020', [623411]),('Jul2,2020', [615693]),('Jul3,2020', [554453]),('Jul4,2020', [319997]),('Jul5,2020', [243997]),('Jul6,2020', [614759]),('Jul7,2020', [651221]),('Jul8,2020', [648018]),('Jul9,2020', [717985]),('Jul10,2020', [711176]),('Jul11,2020', [430227]),('Jul12,2020', [327528]),('Jul13,2020', [797155]),('Jul14,2020', [827032]),('Jul15,2020', [813953]),('Jul16,2020', [792625]),('Jul17,2020', [688593]),('Jul18,2020', [400140]),('Jul19,2020', [307529]),('Jul20,2020', [734327]),('Jul21,2020', [791913]),('Jul22,2020', [785724]),('Jul23,2020', [761433]),('Jul24,2020', [705225]),('Jul25,2020', [428831]),('Jul26,2020', [330641]),('Jul27,2020', [767689]),('Jul28,2020', [830582]),('Jul29,2020', [820369]),('Jul30,2020', [787743]),('Jul31,2020', [683612])], "variables/daterangeday")
    ),
    (
        {"totalPages":0,"firstPage":True,"lastPage":True,"numberOfElements":0,"number":0,"totalElements":0,"columns":{"columnIds":["metrics/visits:::0"]},"summaryData":{"filteredTotals":[19486184],"totals":[19486184]}},
        ([('Total', [19486184])], 'Summary')
    ),
    (
        {"totalPages":0,"firstPage":True,"lastPage":True,"numberOfElements":0,"number":0,"totalElements":0,"columns":{"columnIds":["metrics/visits:::0","metrics/visits:::2"]},"summaryData":{"filteredTotals":[32,16],"totals":[32,16]}},
        ([('Total', [32, 16])], 'Summary')
    )
])
def test_process_response(response, expected):
    class FakeAnalytics:
        def get_segment(self, filter):
            class Response:
                def json(self):
                    return {"name": "test"}
            return Response()

        def get_metric(self, id, rsid):
            class Response:
                def json(self):
                    return {"name": "test"}
            return Response()

        def get_calculatedmetric(self, id):
            class Response:
                def json(self):
                    return {"name": "test"}
            return Response()

    analytics_client = FakeAnalytics()
    table = Table(analytics_client)
    table.process_response(response)
    assert table.rows == expected[0]
    assert table.dimension == expected[1]


def test_increment_settings_page():
    payload = {"rsid":"dhlglobalrolloutprod","globalFilters":[{"type":"dateRange","dateRange":"2020-08-01T00:00:00.000/2020-09-01T00:00:00.000"}],"metricContainer":{"metrics":[{"columnId":"0","id":"metrics/visits","sort":"desc"}]},"dimension":"variables/evar36.1","search":{"clause":"(CONTAINS'cn')"},"settings":{"countRepeatInstances":True,"limit":400,"page":0,"nonesBehavior":"return-nones"},"statistics":{"functions":["col-max","col-min"]}}
    updated_payload_one = Reports._update_page_settings(payload)
    updated_payload_two = Reports._update_page_settings(updated_payload_one)
    assert payload['settings']['page'] == 0
    assert updated_payload_one['settings']['page'] == 1
    assert updated_payload_two['settings']['page'] == 2
