from requests import Response


class ResponseError(Exception):
    """Raised for all non 200 response code from API methods"""
    def __init__(self, response: Response) -> None:
        self.response = response

    @property
    def headers(self):
        headers_str = ''
        if self.response.headers:
            for header, value in self.response.headers.items():
                headers_str += f'{header}: {value}\n'
        return headers_str

    def __str__(self):
        response_str = """
            Response Failed
            ==========================
            Status Code:
            {status_code}
            ==========================
            Headers:
            {headers}
            ==========================
            Response:
            {response_text}
            ==========================
        """
        response_str = response_str.replace(' ', '')
        response_str = response_str.replace('{status_code}',
                                            str(self.response.status_code))
        response_str = response_str.replace('{headers}', self.headers)
        response_str = response_str.replace('{response_text}',
                                            self.response.text)
        return response_str


class PayloadTooLargeError(Exception):
    """Raised if POST Payload is above 60KB"""
    def __init__(self, size):
        self.size = size

    def __str__(self):
        return f'Maximal size for payload is 60KB. Input was: {self.size} KB'
