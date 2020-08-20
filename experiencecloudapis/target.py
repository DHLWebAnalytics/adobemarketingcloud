import typing
import json
from requests import Response


class ResponseError(Exception):
    """Adobe Target failed API response error"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return json.dumps(self.message)


class Target:
    """
    Adobe Target API implementation.
    """
    BASE_URL = 'https://mc.adobe.io/{tenant}'

    def __init__(self,
                 config: typing.Union[str, typing.TextIO],
                 tenant: str) -> None:
        self.session = jwt.JWTAuth(config)
        self.BASE_URL = self.BASE_URL.format(tenant=tenant)

    def list_activities(self,
                        limit: int = 10,
                        offset: int = 0,
                        sort_by: str = 'id') -> Response:
        endpoint = '/target/activities'
        params = {
            "limit": limit,
            "offset": offset,
            "sortBy": sort_by
        }
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v2+json"
        }
        response = self.session.request('get',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers,
                                        params=params)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def get_ab_activity(self,
                        id: typing.Union[int, str]) -> Response:
        endpoint = f'/target/activities/{id}'
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v2+json"
        }
        response = self.session.request('get',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def delete_ab_activity(self,
                           id: typing.Union[int, str]) -> Response:
        endpoint = f'/target/activities/{id}'
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v2+json"
        }
        response = self.session.request('delete',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def create_ab_activity(self,
                           payload: typing.Union[str, dict]) -> Response:
        endpoint = '/target/activities/ab'
        if isinstance(payload, str):
            payload = json.loads(payload)
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v2+json"
        }
        response = self.session.request('post',
                                        f'{self.BASE_URL}{endpoint}',
                                        json=payload,
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def update_ab_activity(self,
                           id: typing.Union[int, str],
                           payload: typing.Union[str, dict]) -> Response:
        endpoint = f'/target/activities/ab/{id}'
        if isinstance(payload, str):
            payload = json.loads(payload)
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v2+json"
        }
        response = self.session.request('put',
                                        f'{self.BASE_URL}{endpoint}',
                                        json=payload,
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def get_xt_activity(self,
                        id: typing.Union[int, str]) -> Response:
        endpoint = f'/target/activities/xt/{id}'
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v2+json"
        }
        response = self.session.request('get',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def delete_xt_activity(self,
                           id: typing.Union[int, str]) -> Response:
        endpoint = f'/target/activities/xt/{id}'
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v2+json"
        }
        response = self.session.request('delete',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def create_xt_activity(self,
                           payload: typing.Union[str, dict]) -> Response:
        endpoint = '/target/activities/xt'
        if isinstance(payload, str):
            payload = json.loads(payload)
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v2+json"
        }
        response = self.session.request('post',
                                        f'{self.BASE_URL}{endpoint}',
                                        json=payload,
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def update_xt_activity(self,
                           id: typing.Union[int, str],
                           payload: typing.Union[str, dict]) -> Response:
        endpoint = f'/target/activities/xt/{id}'
        if isinstance(payload, str):
            payload = json.loads(payload)
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v2+json"
        }
        response = self.session.request('put',
                                        f'{self.BASE_URL}{endpoint}',
                                        json=payload,
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def update_activity_name(self,
                             id: typing.Union[str, int],
                             payload: typing.Union[str, dict]):
        endpoint = f'/target/activities/{id}/name'
        if isinstance(payload, str):
            payload = json.loads(payload)
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v1+json"
        }
        response = self.session.request('put',
                                        f'{self.BASE_URL}{endpoint}',
                                        json=payload,
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def update_activity_state(self,
                              id: typing.Union[str, int],
                              payload: typing.Union[str, dict]):
        endpoint = f'/target/activities/{id}/state'
        if isinstance(payload, str):
            payload = json.loads(payload)
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v1+json"
        }
        response = self.session.request('put',
                                        f'{self.BASE_URL}{endpoint}',
                                        json=payload,
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def update_activity_priority(self,
                                 id: typing.Union[str, int],
                                 payload: typing.Union[str, dict]):
        endpoint = f'/target/activities/{id}/priority'
        if isinstance(payload, str):
            payload = json.loads(payload)
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v1+json"
        }
        response = self.session.request('put',
                                        f'{self.BASE_URL}{endpoint}',
                                        json=payload,
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def update_activity_schedule(self,
                                 id: typing.Union[str, int],
                                 payload: typing.Union[str, dict]):
        endpoint = f'/target/activities/{id}/schedule'
        if isinstance(payload, str):
            payload = json.loads(payload)
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v1+json"
        }
        response = self.session.request('put',
                                        f'{self.BASE_URL}{endpoint}',
                                        json=payload,
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def get_activity_changelog(self,
                               id: typing.Union[str, int]):
        endpoint = f'/target/activities/{id}/changelog'
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v1+json"
        }
        response = self.session.request('get',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def list_offers(self,
                    limit: int = 10,
                    offset: int = 0,
                    sort_by: str = 'id') -> Response:
        endpoint = '/target/offers'
        params = {
            "limit": limit,
            "offset": offset,
            "sortBy": sort_by
        }
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v2+json"
        }
        response = self.session.request('get',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers,
                                        params=params)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def get_offer(self,
                  id: typing.Union[int, str]) -> Response:
        endpoint = f'/target/offers/content/{id}'
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v2+json"
        }
        response = self.session.request('get',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def create_offer(self,
                     payload: typing.Union[str, dict]) -> Response:
        endpoint = '/target/offers/content'
        if isinstance(payload, str):
            payload = json.loads(payload)
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v2+json"
        }
        response = self.session.request('post',
                                        f'{self.BASE_URL}{endpoint}',
                                        json=payload,
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def update_offer(self,
                     id: typing.Union[int, str],
                     payload: typing.Union[str, dict]) -> Response:
        endpoint = f'/target/offers/content/{id}'
        if isinstance(payload, str):
            payload = json.loads(payload)
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v2+json"
        }
        response = self.session.request('put',
                                        f'{self.BASE_URL}{endpoint}',
                                        json=payload,
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def delete_offer(self,
                     id: typing.Union[int, str]) -> Response:
        endpoint = f'/target/offers/content/{id}'
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v2+json"
        }
        response = self.session.request('delete',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def list_audiences(self,
                       limit: int = 10,
                       offset: int = 0,
                       sort_by: str = 'id') -> Response:
        endpoint = '/target/audiences'
        params = {
            "limit": limit,
            "offset": offset,
            "sortBy": sort_by
        }
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v2+json"
        }
        response = self.session.request('get',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers,
                                        params=params)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def get_audience(self,
                     id: typing.Union[int, str]) -> Response:
        endpoint = f'/target/audiences/{id}'
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v2+json"
        }
        response = self.session.request('get',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def create_audience(self,
                        payload: typing.Union[str, dict]) -> Response:
        endpoint = '/target/audiences'
        if isinstance(payload, str):
            payload = json.loads(payload)
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v2+json"
        }
        response = self.session.request('post',
                                        f'{self.BASE_URL}{endpoint}',
                                        json=payload,
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def update_audience(self,
                        id: typing.Union[int, str],
                        payload: typing.Union[str, dict]) -> Response:
        endpoint = f'/target/audiences/{id}'
        if isinstance(payload, str):
            payload = json.loads(payload)
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v2+json"
        }
        response = self.session.request('put',
                                        f'{self.BASE_URL}{endpoint}',
                                        json=payload,
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def delete_audience(self,
                        id: typing.Union[int, str]) -> Response:
        endpoint = f'/target/audiences/{id}'
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v2+json"
        }
        response = self.session.request('delete',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def list_properties(self) -> Response:
        endpoint = '/target/properties'
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v1+json"
        }
        response = self.session.request('get',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def get_property(self,
                     id: typing.Union[int, str]) -> Response:
        endpoint = f'/target/properties/{id}'
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v1+json"
        }
        response = self.session.request('get',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def get_ab_performance_report(self,
                                  id: typing.Union[int, str]) -> Response:
        endpoint = f'/target/activities/ab/{id}/report/performance'
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v1+json"
        }
        response = self.session.request('get',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def get_xt_performance_report(self,
                                  id: typing.Union[int, str]) -> Response:
        endpoint = f'/target/activities/xt/{id}/report/performance'
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v1+json"
        }
        response = self.session.request('get',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def get_ap_activity_performance_report(self,
                                           id: typing.Union[int, str]) -> Response:
        endpoint = f'/target/activities/abt/{id}/report/performance'
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v1+json"
        }
        response = self.session.request('get',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def get_audit_performance_report(self,
                                     id: typing.Union[int, str]) -> Response:
        endpoint = f'/target/activities/ab/{id}/report/orders'
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v1+json"
        }
        response = self.session.request('get',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def list_mboxes(self) -> Response:
        endpoint = '/target/mboxes'
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v1+json"
        }
        response = self.session.request('get',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def get_mbox_parameters(self,
                            mbox_name: str) -> Response:
        endpoint = f'/target/mbox/{mbox_name}'
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v1+json"
        }
        response = self.session.request('get',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def list_profile_parameters(self) -> Response:
        endpoint = '/target/profileattributes/mbox'
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v1+json"
        }
        response = self.session.request('get',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def list_environments(self) -> Response:
        endpoint = '/target/environments'
        method_headers = {
            "cache-control": "no-cache",
            "accept": "application/vnd.adobe.target.v1+json"
        }
        response = self.session.request('get',
                                        f'{self.BASE_URL}{endpoint}',
                                        method_headers=method_headers)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response

    def execute_batch(self,
                        payload: typing.Union[str, dict]) -> Response:
        endpoint = '/target/batch'
        if isinstance(payload, str):
            payload = json.loads(payload)
        response = self.session.request('post',
                                        f'{self.BASE_URL}{endpoint}',
                                        json=payload)
        if response.status_code != 200:
            try:
                r = response.json()
                raise ResponseError(r)
            except json.decoder.JSONDecodeError:
                return response
        return response