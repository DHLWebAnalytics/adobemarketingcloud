import typing
import json
import requests
from experiencecloudapis.authentication import AuthenticationClient
from requests import Response


class ResponseError(Exception):
    """Adobe Analytics failed API response error"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return json.dumps(self.message)


def authenticate(fun):
    def wrapper(*args, **kwargs):
        instance: Analytics = args[0]
        instance.auth_client.authenticate(instance.session)
        return fun(*args, **kwargs)
    return wrapper


class Analytics:
    """
    Adobe Analytics API implementation.
    """
    BASE_URL = 'https://analytics.adobe.io/api/{company_id}'

    def __init__(self,
                 auth_client: AuthenticationClient,
                 session: requests.Session = requests.Session()) -> None:
        self.session = session
        self.auth_client = auth_client
        self.base_url = self.BASE_URL.format(
            company_id=self.auth_client.company_id)

    # Endpoint Block
    # Calculated Metrics
    @authenticate
    def get_calculatedmetrics(self,
                              locale='en_US',
                              limit=10,
                              page=0,
                              sort_direction='ASC',
                              sort_property='id',
                              **kwargs) -> Response:
        endpoint = '/calculatedmetrics'
        params = {
            'locale': locale,
            'limit': limit,
            'page': page,
            'sortDirection': sort_direction,
            'sortProperty': sort_property,
            **kwargs
        }
        response = self.session.get(f'{self.base_url}{endpoint}',
                                    params=params)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    @authenticate
    def create_calculatedmetrics(self,
                                 payload: typing.Union[str, dict],
                                 locale: str = 'en_US') -> Response:
        endpoint = '/calculatedmetrics'
        params = {
            'locale': locale
        }
        if isinstance(payload, str):
            payload = json.loads(payload)
        response = self.session.post(f'{self.base_url}{endpoint}',
                                     params=params,
                                     json=payload)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    @authenticate
    def get_calculatedmetrics_functions(self,
                                        locale: str = 'en_US') -> Response:
        endpoint = '/calculatedmetrics/functions'
        params = {
            'locale': locale
        }
        response = self.session.get(f'{self.base_url}{endpoint}',
                                    params=params)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    @authenticate
    def get_calculatedmetrics_function(self, id: str,
                                       locale: str = 'en_US') -> Response:
        endpoint = f'/calculatedmetrics/functions/{id}'
        params = {
            'locale': locale
        }
        response = self.session.get(f'{self.base_url}{endpoint}',
                                    params=params)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    @authenticate
    def validate_calculatedmetrics(self,
                                   payload: typing.Union[str, dict],
                                   locale: str = 'en_US',
                                   migrating: bool = False) -> Response:
        endpoint = '/calculatedmetrics/validate'
        params = {
            'locale': locale,
            'migrating': migrating
        }
        if isinstance(payload, str):
            payload = json.loads(payload)
        response = self.session.post(f'{self.base_url}{endpoint}',
                                     params=params,
                                     json=payload)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    @authenticate
    def get_calculatedmetric(self, id: str, locale: str = 'en_US'):
        endpoint = f'/calculatedmetrics/{id}'
        params = {
            'locale': locale
        }
        response = self.session.get(f'{self.base_url}{endpoint}',
                                    params=params)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    @authenticate
    def update_calculatedmetric(self,
                                id: str,
                                payload: typing.Union[str, dict],
                                locale: str = 'en_US'):
        endpoint = f'/calculatedmetrics/{id}'
        params = {
            'locale': locale
        }
        if isinstance(payload, str):
            payload = json.loads(payload)
        response = self.session.put(f'{self.base_url}{endpoint}',
                                    params=params,
                                    json=payload)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    @authenticate
    def delete_calculatedmetric(self,
                                id: str,
                                locale: str = 'en_US'):
        endpoint = f'/calculatedmetrics/{id}'
        params = {
            'locale': locale
        }
        response = self.session.delete(f'{self.base_url}{endpoint}',
                                       params=params)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    # Endpoint Block
    # Collections
    @authenticate
    def get_collection_suites(self,
                              limit: int = 10,
                              page: int = 0,
                              **kwargs) -> Response:
        endpoint = '/collections/suites'
        params = {
            'limit': limit,
            'page': page,
            **kwargs
        }
        response = self.session.get(f'{self.base_url}{endpoint}',
                                    params=params)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    @authenticate
    def get_collection_suite(self, id: str) -> Response:
        endpoint = f'/collections/suites/{id}'
        response = self.session.get(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    # Endpoint Block
    # Dateranges
    @authenticate
    def get_dateranges(self,
                       locale: str = 'en_US',
                       limit: int = 10,
                       page: int = 0, **kwargs) -> Response:
        endpoint = '/dateranges'
        params = {
            'locale': locale,
            'limit': limit,
            'page': page,
            **kwargs
        }
        response = self.session.get(f'{self.base_url}{endpoint}',
                                    params=params)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    @authenticate
    def get_daterange(self, id: str,
                      locale: str = 'en_US',
                      **kwargs) -> Response:
        endpoint = f'/dateranges/{id}'
        params = {
            'locale': locale,
            **kwargs
        }
        response = self.session.get(f'{self.base_url}{endpoint}',
                                    params=params)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    # Endpoint Block
    # Dimensions
    @authenticate
    def get_dimensions(self,
                       rsid: str,
                       locale: str = 'en_US',
                       classficable: bool = False,
                       **kwargs) -> Response:
        endpoint = '/dimensions'
        params = {
            'rsid': rsid,
            'locale': locale,
            'classificable': classficable,
            **kwargs
        }
        response = self.session.get(f'{self.base_url}{endpoint}',
                                    params=params)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    @authenticate
    def get_dimension(self,
                      id: str,
                      rsid: str,
                      locale: str = 'en_US',
                      **kwargs) -> Response:
        endpoint = f'/dimensions/{id}'
        params = {
            'rsid': rsid,
            'locale': locale,
            **kwargs
        }
        response = self.session.get(f'{self.base_url}{endpoint}',
                                    params=params)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    # Endpoint Block
    # Metrics
    @authenticate
    def get_metrics(self,
                    rsid: str,
                    locale: str = 'en_US',
                    segmentable: bool = False,
                    **kwargs) -> Response:
        endpoint = '/metrics'
        params = {
            rsid: rsid,
            locale: locale,
            segmentable: segmentable,
            **kwargs
        }
        response = self.session.get(f'{self.base_url}{endpoint}',
                                    params=params)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    @authenticate
    def get_metric(self,
                   id: str,
                   rsid: str,
                   locale: str = 'en_US',
                   **kwargs):
        endpoint = f'/metrics/{id}'
        params = {
            'rsid': rsid,
            'locale': locale,
            **kwargs
        }
        response = self.session.get(f'{self.base_url}{endpoint}',
                                    params=params)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    # Endpoint Block
    # Reports
    @authenticate
    def reports(self, payload: typing.Union[str, dict]) -> Response:
        """Implementation of the /response endpoint
        Use the Adobe Analytics Reports creator of the workspace in order
        to get a valid payload for the request.
        TODO: link an explanation how to retrieve these inputs
        """
        endpoint = '/reports'
        if isinstance(payload, str):
            payload = json.loads(payload)
        response = self.session.post(f'{self.base_url}{endpoint}',
                                     json=payload)
        if not response:
            raise ResponseError(response.json())
        return response

    # Endpoint Block
    # Segments
    @authenticate
    def get_segments(self,
                     locale='en_US',
                     filterByPublishedSegments='all',
                     limit=10,
                     page=0,
                     sort_direction='ASC',
                     sort_property='id',
                     **kwargs):
        endpoint = '/segments'
        params = {
            'locale': locale,
            'filterByPublishedSegments': filterByPublishedSegments,
            'limit': limit,
            'page': page,
            'sortDirection': sort_direction,
            'sortProperty': sort_property,
            **kwargs
        }
        response = self.session.get(f'{self.base_url}{endpoint}',
                                    params=params)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    @authenticate
    def create_segments(self,
                        payload: typing.Union[str, dict],
                        locale: str = 'en_US',
                        **kwargs) -> Response:
        endpoint = '/segments'
        params = {
            'locale': locale,
            **kwargs
        }
        if isinstance(payload, str):
            payload = json.loads(payload)
        response = self.session.post(f'{self.base_url}{endpoint}',
                                     params=params,
                                     json=payload)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    @authenticate
    def validate_segment(self,
                         rsid: str,
                         payload: typing.Union[str, dict]) -> Response:
        endpoint = '/segments/validate'
        params = {
            'rsid': rsid
        }
        if isinstance(payload, str):
            payload = json.loads(payload)
        response = self.session.post(f'{self.base_url}{endpoint}',
                                     params=params,
                                     json=payload)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    @authenticate
    def get_segment(self,
                    id: str,
                    locale: str = 'en_US',
                    **kwargs):
        endpoint = f'/segments/{id}'
        params = {
            'locale': locale,
            **kwargs
        }
        response = self.session.get(f'{self.base_url}{endpoint}',
                                    params=params)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    @authenticate
    def update_segment(self,
                       id: str,
                       payload: typing.Union[str, dict],
                       locale: str = 'en_US',
                       **kwargs) -> Response:
        endpoint = f'/segments/{id}'
        params = {
            'locale': locale,
            **kwargs
        }
        if isinstance(payload, str):
            payload = json.loads(payload)
        response = self.session.put(f'{self.base_url}{endpoint}',
                                    params=params,
                                    json=payload)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    @authenticate
    def delete_segment(self,
                       id: str,
                       locale: str = 'en_US') -> Response:
        endpoint = f'/segments/{id}'
        params = {
            'locale': locale
        }
        response = self.session.delete(f'{self.base_url}{endpoint}',
                                       params=params)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    # Endpoint Block
    # Users

    @authenticate
    def users(self, limit: int = 0, page: int = 0) -> Response:
        endpoint = '/users'
        params = {
            'limit': limit,
            'page': page
        }
        response = self.session.get(f'{self.base_url}{endpoint}',
                                    params=params)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    @authenticate
    def user_me(self) -> Response:
        endpoint = '/users/me'
        response = self.session.get(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    # The below belongs to Adobe Analytics 1.4 API.
    # As classifications has not yet been ported to 2.0
    # we included it here for now.
    @authenticate
    def classifications_commit_import(self, job_id: int) -> Response:
        BASE_URL = 'https://api.omniture.com/admin/1.4/rest/'
        endpoint = 'Classifications.CommitImport'
        params = {
            'method': endpoint,
        }
        payload = {
            'job_id': job_id
        }
        response = self.session.post(f'{BASE_URL}',
                                     params=params,
                                     json=payload)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    @authenticate
    def classifications_create_import(self,
                                      element: str,
                                      description: str,
                                      email_address: str,
                                      header: typing.List[str],
                                      check_divisions: int = 1,
                                      export_results: int = 0,
                                      overwrite_conflicts: int = 0,
                                      **kwargs) -> Response:
        BASE_URL = 'https://api.omniture.com/admin/1.4/rest/'
        endpoint = 'Classifications.CreateImport'
        params = {
            'method': endpoint,
        }
        payload = {
            'element': element,
            'description': description,
            'email_address': email_address,
            'header': header,
            'check_divisions': check_divisions,
            'export_results': export_results,
            'overwrite_conflicts': overwrite_conflicts,
            **kwargs
        }
        response = self.session.post(f'{BASE_URL}',
                                     params=params,
                                     json=payload)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    @authenticate
    def classifications_get_status(self, job_id: int) -> Response:
        BASE_URL = 'https://api.omniture.com/admin/1.4/rest/'
        endpoint = 'Classifications.GetStatus'
        params = {
            'method': endpoint,
        }
        payload = {
            'job_id': job_id,
        }
        response = self.session.post(f'{BASE_URL}',
                                     params=params,
                                     json=payload)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    @authenticate
    def classifications_get_template(self,
                                     element: str,
                                     rsid_list: typing.List[str],
                                     encoding: str = "utf-8",
                                     **kwargs) -> Response:
        BASE_URL = 'https://api.omniture.com/admin/1.4/rest/'
        endpoint = 'Classifications.GetTemplate'
        params = {
            'method': endpoint,
        }
        payload = {
            'element': element,
            'encoding': encoding,
            'rsid_list': rsid_list,
            **kwargs,
        }
        response = self.session.post(f'{BASE_URL}',
                                     params=params,
                                     json=payload)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response

    @authenticate
    def classifications_populate_import(self,
                                        job_id: int,
                                        page: int,
                                        rows: typing.List[typing.List[str]]) \
            -> Response:
        BASE_URL = 'https://api.omniture.com/admin/1.4/rest/'
        endpoint = 'Classifications.PopulateImport'
        params = {
            'method': endpoint,
        }
        payload = {
            'job_id': job_id,
            'page': page,
            'rows': rows,
        }
        response = self.session.post(f'{BASE_URL}',
                                     params=params,
                                     json=payload)
        if response.status_code != 200:
            raise ResponseError(response.json())
        return response
