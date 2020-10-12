from experiencecloudapis.exceptions import ResponseError


def test_headers_from_reponse():
    class FakeResponse:
        text = 'text'
        headers = {
            'Content-Type': 'text/html',
            'Date': 'Sat, 10 Oct 2020 15:38:15 GMT',
            'ETag': '"5f48cb6f-93"',
            'Server': 'openresty',
            'X-Request-Id': 'xMi0oHLbkcnzqgm7r8iMz8zGVxOL3RYg',
            'Content-Length': '147',
            'Connection': 'keep-alive'
        }
        status_code = 404

    response_error = ResponseError(FakeResponse())
    assert response_error.headers.startswith('Content-Type')
