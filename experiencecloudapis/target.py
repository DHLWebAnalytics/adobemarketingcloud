"""
Adobe Target API
~~~~~~~~~~~~~~~~

This module implements the Adobe Target API
Visit the below website for more information about the available methods:
https://developers.adobetarget.com/api/

You can use Adobe Target’s Admin and Profile REST APIs that use the Adobe.IO
integration to manage activities, audiences, offers, properties, reports,
mboxes, environments, and profiles.
"""

import typing
import json
import requests
import urllib.parse
import functools
from experiencecloudapis.authentication import AuthenticationClient
from experiencecloudapis.exceptions import ResponseError, PayloadTooLargeError
from experiencecloudapis.utils import size_in_kbs
from requests import Response


def authenticate(fun):
    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        instance: Target = args[0]
        instance.auth_client.authenticate(instance.session)
        return fun(*args, **kwargs)
    return wrapper


class Target:
    """Adobe Target API class"""
    BASE_URL = 'https://mc.adobe.io/{tenant_name}'

    def __init__(self,
                 auth_client: AuthenticationClient,
                 tenant_name: str,
                 session: requests.Session = requests.Session()) -> None:
        self.session = session
        self.auth_client = auth_client
        self.tenant_name = tenant_name
        self.base_url = self.BASE_URL.format(
            tenant_name=self.tenant_name)

    # Authentication Tokens
    # Debug Authentication Token
    @authenticate
    def get_debug_authentication_token(self) -> Response:
        """
        Generate a Debug Authentication Token for use with mboxTrace.

        :returns: requests.Response with debug authentication token
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/authentication/token'
        params = {
            'scope': 'debug_tools',
        }
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}',
                                    params=params)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Profile Authentication Token
    @authenticate
    def get_profile_authentication_token(self) -> Response:
        """
        Generate a Profile Authentication Token for use with Profile APIs.

        :returns: requests.Response with profile authentication token
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/authentication/token'
        params = {
            'scope': 'profile_api',
        }
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}',
                                    params=params)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Activities
    # List Activities
    @authenticate
    def list_activities(self,
                        limit: int = 2147483647,
                        offset: int = 0,
                        sortBy: str = 'id') -> Response:
        """
        Get a list of activities created in your Target account, with the
        ability to filter and sort by attributes.

        :param limit: (optional) set the limit of activities per request,
        defaults to 2147483647
        :param offset: (optional) set the page offset per request,
        defaults to 0
        :param sortBy: (optional) set the sort key, defaults to 'id'
        :returns: requests.Response with activities
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/'
        params = {
            'limit': limit,
            'offset': offset,
            'sortBy': sortBy,
        }
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v3+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}',
                                    params=params)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Get AB Activity
    @authenticate
    def get_ab_activity(self, id: str) -> Response:
        """
        Fetch the current definition of an AB activity if it is found as
        referenced by the id.

        :param id: AB activity Id
        :returns: requests.Response with AB test activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/ab/{id}'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v3+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Delete AB Activity
    @authenticate
    def delete_ab_activity(self, id: str) -> Response:
        """
        Deletes the AB activity that is referenced by the id, if it is found.

        :param id: AB activity Id
        :returns: requests.Response with AB test activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/ab/{id}'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v3+json',
        })
        response = self.session.delete(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Create AB Activity
    @authenticate
    def create_ab_activity(self,
                           payload: typing.Union[str, dict]) -> Response:
        """
        Creates a new AB activity with the specified contents and returns the
        created activity.

        Activities created using the API can only be edited using the API.
        You can’t edit it in the UI.

        :param payload: Payload for activity creation
        :returns: requests.Response with created AB Activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/ab'
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v3+json',
        })
        if type(payload) == str:
            payload = json.loads(payload)
        response = self.session.post(f'{self.base_url}{endpoint}', payload)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Update AB Activity
    @authenticate
    def update_ab_activity(self,
                           id: str,
                           payload: typing.Union[str, dict]) -> Response:
        """
        Updates the AB activity definition with the contents as provided in
        the request. This can change the state and behaviour of an
        existing activity.

        Refer “Create AB Activity” for the available inputs, limitations and
        the description. The input for “Update AB Activity” method is very
        similar to the “Create AB Activity” method.

        :param id: AB activity Id
        :param payload: Payload for Activity update
        :returns: requests.Response with updated AB Activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/ab/{id}'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v3+json',
        })
        if type(payload) == str:
            payload = json.loads(payload)
        response = self.session.put(f'{self.base_url}{endpoint}', payload)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Get XT Activity
    @authenticate
    def get_xt_activity(self, id: str) -> Response:
        """
        Gets a Experience Targeted activity that is referenced by the id.

        :param id: XT activity Id
        :returns: requests.Response with XT test activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/xt/{id}'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v3+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Delete XT Activity
    @authenticate
    def delete_xt_activity(self, id: str) -> Response:
        """
        Deletes the XT activity that is referenced by the id, if it is found.

        :param id: XT activity Id
        :returns: requests.Response with XT test activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/xt/{id}'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v3+json',
        })
        response = self.session.delete(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Create XT Activity
    @authenticate
    def create_xt_activity(self,
                           payload: typing.Union[str, dict]) -> Response:
        """
        Creates a new XT activity with the specified contents and returns the
        created activity.

        Refer “Create AB Activity” for the available inputs, limitations and
        the description. The input for “Create XT Activity” method is very
        similar to the “Create AB Activity” method.

        Activities created using the API can only be edited using the API.
        You can’t edit it in the UI.

        :param payload: Payload for activity creation
        :returns: requests.Response with created XT Activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/xt'
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v3+json',
        })
        if type(payload) == str:
            payload = json.loads(payload)
        response = self.session.post(f'{self.base_url}{endpoint}', payload)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Update XT Activity
    @authenticate
    def update_xt_activity(self,
                           id: str,
                           payload: typing.Union[str, dict]) -> Response:
        """
        Updates the Experience Targeted activity definition with the contents
        as provided in the request. This can change the state and behaviour
        of an existing activity.

        To Update an XT Activity use the same input as described in
        “Create XT Activity”. You have to make a PUT request instead of a
        POST request to update an already existing activity.

        :param id: AB activity Id
        :param payload: Payload for Activity update
        :returns: requests.Response with updated AB Activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/xt/{id}'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v3+json',
        })
        if type(payload) == str:
            payload = json.loads(payload)
        response = self.session.put(f'{self.base_url}{endpoint}', payload)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Update Activity Name
    @authenticate
    def update_activity_name(self,
                             id: str,
                             payload: typing.Union[str, dict]) -> Response:
        """
        Updates the name of the AB activity that is referenced by the
        supplied id.

        You can also use the specific endpoints /activities/ab/{id}/name and
        /activities/xt/{id}/name for updating the name of an AB or XT
        activity respectively. Best practice is to use the generic
        /activities/{id}/name so that you don’t have to know or specify
        the type in the request.

        Payload Example:
        {
            "name": "New Name for Activity"
        }

        :param id: Activity Id
        :param payload: Payload for Activity update
        :returns: requests.Response with updated Activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/{id}/name'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        if type(payload) == str:
            payload = json.loads(payload)
        response = self.session.put(f'{self.base_url}{endpoint}', payload)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Update AB Activity Name
    @authenticate
    def update_ab_activity_name(self,
                                id: str,
                                payload: typing.Union[str, dict]) -> Response:
        """
        Updates the name of the AB activity that is referenced by the
        supplied id.

        Payload Example:
        {
            "name": "New Name for Activity"
        }

        :param id: AB Activity Id
        :param payload: Payload for Activity update
        :returns: requests.Response with updated Activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/ab/{id}/name'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        if type(payload) == str:
            payload = json.loads(payload)
        response = self.session.put(f'{self.base_url}{endpoint}', payload)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Update XT Activity Name
    @authenticate
    def update_xt_activity_name(self,
                                id: str,
                                payload: typing.Union[str, dict]) -> Response:
        """
        Updates the name of the XT activity that is referenced by the
        supplied id.

        Payload Example:
        {
            "name": "New Name for Activity"
        }

        :param id: XT Activity Id
        :param payload: Payload for Activity update
        :returns: requests.Response with updated Activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/xt/{id}/name'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        if type(payload) == str:
            payload = json.loads(payload)
        response = self.session.put(f'{self.base_url}{endpoint}', payload)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Update Activity State
    @authenticate
    def update_activity_state(self,
                              id: str,
                              payload: typing.Union[str, dict]) -> Response:
        """
        Update state for an activity that is referenced by the provided id.
        Valid values are:
        - approved : corresponds to Live in Target UI.
        - deactivated : corresponds to Inactive in Target UI.
        - saved : corresponds to Inactive in Target UI.

        You can also use the specific endpoints /activities/ab/{id}/state and
        /activities/xt/{id}/state for updating the state of an AB or XT
        activity respectively. Best practice is to use the generic
        /activities/{id}/state so that you don’t have to know or specify the
        type in the request.

        Payload Example:
        {
            "state": "deactivated"
        }

        :param id: Activity Id
        :param payload: Payload for Activity update
        :returns: requests.Response with updated Activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/{id}/state'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        if type(payload) == str:
            payload = json.loads(payload)
        response = self.session.put(f'{self.base_url}{endpoint}', payload)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Update AB Activity State
    @authenticate
    def update_ab_activity_state(self,
                                 id: str,
                                 payload: typing.Union[str, dict]) -> Response:
        """
        Update state for an activity that is referenced by the provided id.
        Valid values are:
        - approved : corresponds to Live in Target UI.
        - deactivated : corresponds to Inactive in Target UI.
        - saved : corresponds to Inactive in Target UI.

        Payload Example:
        {
            "state": "deactivated"
        }

        :param id: AB Activity Id
        :param payload: Payload for Activity update
        :returns: requests.Response with updated Activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/ab/{id}/state'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        if type(payload) == str:
            payload = json.loads(payload)
        response = self.session.put(f'{self.base_url}{endpoint}', payload)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Update XT Activity State
    @authenticate
    def update_xt_activity_state(self,
                                 id: str,
                                 payload: typing.Union[str, dict]) -> Response:
        """
        Update state for an activity that is referenced by the provided id.
        Valid values are:
        - approved : corresponds to Live in Target UI.
        - deactivated : corresponds to Inactive in Target UI.
        - saved : corresponds to Inactive in Target UI.

        Payload Example:
        {
            "state": "deactivated"
        }

        :param id: XT Activity Id
        :param payload: Payload for Activity update
        :returns: requests.Response with updated Activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/xt/{id}/state'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        if type(payload) == str:
            payload = json.loads(payload)
        response = self.session.put(f'{self.base_url}{endpoint}', payload)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Update Activity Priority
    @authenticate
    def update_activity_priority(self,
                                 id: str,
                                 payload: typing.Union[str, dict]) -> Response:
        """
        Change priority for the AB activity that is referenced by the supplied
        id. Allowed values for priority are 0-999. If you are using low,
        medium and high in the Target UI, those correspond to 0,5 and 10
        respectively. You need to turn granular priority on in the settings
        page inorder to use the 0-999 scale.

        You can also use the specific endpoints /activities/ab/{id}/priority
        and /activities/xt/{id}/priority for updating the priority of an AB
        or XT activity respectively. Best practice is to use the generic
        /activities/{id}/priority so that you don’t have to know or specify
        the type in the request.

        Payload Example:
        {
            "priority": "100"
        }

        :param id: Activity Id
        :param payload: Payload for Activity update
        :returns: requests.Response with updated Activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/{id}/priority'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        if type(payload) == str:
            payload = json.loads(payload)
        response = self.session.put(f'{self.base_url}{endpoint}', payload)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Update AB Activity Priority
    @authenticate
    def update_ab_activity_priority(self,
                                    id: str,
                                    payload: typing.Union[str, dict])\
            -> Response:
        """
        Change priority for the AB activity that is referenced by the supplied
        id. Allowed values for priority are 0-999. If you are using low,
        medium and high in the Target UI, those correspond to 0,5 and 10
        respectively. You need to turn granular priority on in the settings
        page inorder to use the 0-999 scale.

        Payload Example:
        {
            "priority": "100"
        }

        :param id: AB Activity Id
        :param payload: Payload for Activity update
        :returns: requests.Response with updated Activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/ab/{id}/priority'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        if type(payload) == str:
            payload = json.loads(payload)
        response = self.session.put(f'{self.base_url}{endpoint}', payload)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Update XT Activity Priority
    @authenticate
    def update_xt_activity_priority(self,
                                    id: str,
                                    payload: typing.Union[str, dict])\
            -> Response:
        """
        Change priority for the XT activity that is referenced by the supplied
        id. Allowed values for priority are 0-999. If you are using low,
        medium and high in the Target UI, those correspond to 0,5 and 10
        respectively. You need to turn granular priority on in the settings
        page inorder to use the 0-999 scale.

        Payload Example:
        {
            "priority": "100"
        }

        :param id: XT Activity Id
        :param payload: Payload for Activity update
        :returns: requests.Response with updated Activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/xt/{id}/priority'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        if type(payload) == str:
            payload = json.loads(payload)
        response = self.session.put(f'{self.base_url}{endpoint}', payload)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Update Activity Schedule
    @authenticate
    def update_activity_schedule(self,
                                 id: str,
                                 payload: typing.Union[str, dict]) -> Response:
        """
        Update the startsAt and endsAt fields of the AB activity referenced
        by the provided id. The schedule defines the start and end date and
        time for the activity. You need to pass the startsAt and endsAt
        values. If successful, it returns a status code 200. startsAt and
        endsAt support ISO 8601 style date-hour formats.

        yyyy-MM-dd’T'HH:mm:ssXXX
        yyyy-MM-dd’T'HH:mm:ss
        yyyy-MM-dd’T'HH
        yyyy-MM-dd
        yyyy-MM-dd’T'HH:mm:ss.SSS
        yyyy-MM-dd’T'HH:mm:ss.SSSXXX

        You can also use the specific endpoints /activities/ab/{id}/schedule
        and /activities/xt/{id}/schedule for updating the schedule of an
        AB or XT activity respectively. Best practice is to use the generic
        /activities/{id}/schedule so that you don’t have to know or specify
        the type in the request.

        Payload Example:
        {
            "startsAt": "2017-05-01T08:00Z",
            "endsAt": "2017-09-01T07:59:59Z"
        }

        :param id: Activity Id
        :param payload: Payload for Activity update
        :returns: requests.Response with updated Activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/{id}/schedule'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        if type(payload) == str:
            payload = json.loads(payload)
        response = self.session.put(f'{self.base_url}{endpoint}', payload)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Update AB Activity Schedule
    @authenticate
    def update_ab_activity_schedule(self,
                                    id: str,
                                    payload: typing.Union[str, dict]) \
            -> Response:
        """
        Update the startsAt and endsAt fields of the AB activity referenced
        by the provided id. The schedule defines the start and end date and
        time for the activity. You need to pass the startsAt and endsAt
        values. If successful, it returns a status code 200. startsAt and
        endsAt support ISO 8601 style date-hour formats.

        yyyy-MM-dd’T'HH:mm:ssXXX
        yyyy-MM-dd’T'HH:mm:ss
        yyyy-MM-dd’T'HH
        yyyy-MM-dd
        yyyy-MM-dd’T'HH:mm:ss.SSS
        yyyy-MM-dd’T'HH:mm:ss.SSSXXX

        Payload Example:
        {
            "startsAt": "2017-05-01T08:00Z",
            "endsAt": "2017-09-01T07:59:59Z"
        }

        :param id: Activity Id
        :param payload: Payload for Activity update
        :returns: requests.Response with updated Activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/ab/{id}/schedule'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        if type(payload) == str:
            payload = json.loads(payload)
        response = self.session.put(f'{self.base_url}{endpoint}', payload)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Update XT Activity Schedule
    @authenticate
    def update_xt_activity_schedule(self,
                                    id: str,
                                    payload: typing.Union[str, dict]) \
            -> Response:
        """
        Update the startsAt and endsAt fields of the XT activity referenced
        by the provided id. The schedule defines the start and end date and
        time for the activity. You need to pass the startsAt and endsAt
        values. If successful, it returns a status code 200. startsAt and
        endsAt support ISO 8601 style date-hour formats.

        yyyy-MM-dd’T'HH:mm:ssXXX
        yyyy-MM-dd’T'HH:mm:ss
        yyyy-MM-dd’T'HH
        yyyy-MM-dd
        yyyy-MM-dd’T'HH:mm:ss.SSS
        yyyy-MM-dd’T'HH:mm:ss.SSSXXX

        Payload Example:
        {
            "startsAt": "2017-05-01T08:00Z",
            "endsAt": "2017-09-01T07:59:59Z"
        }

        :param id: Activity Id
        :param payload: Payload for Activity update
        :returns: requests.Response with updated Activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/xt/{id}/schedule'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        if type(payload) == str:
            payload = json.loads(payload)
        response = self.session.put(f'{self.base_url}{endpoint}', payload)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Get Activity Changelog
    @authenticate
    def get_activity_changelog(self,
                               id: str) -> Response:
        """
        Returns the changelog for a given activity id.

        :param id: Activity Id
        :returns: requests.Response with changelog of Activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/{id}/changelog'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Offers
    # List Offers
    @authenticate
    def list_offers(self,
                    limit: int = 2147483647,
                    offset: int = 0,
                    sortBy: str = 'id') -> Response:
        """
        Retrieve the list of previously-created content offers. The parameters
        passed through the query string are optional and are used to indicate
        the sorting and filtering options.

        :param limit: (optional) set the limit of activities per request,
        defaults to 2147483647
        :param offset: (optional) set the page offset per request,
        defaults to 0
        :param sortBy: (optional) set the sort key, defaults to 'id'
        :returns: requests.Response with offers
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/offers'
        params = {
            'limit': limit,
            'offset': offset,
            'sortBy': sortBy,
        }
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v2+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}',
                                    params=params)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Get Offer
    @authenticate
    def get_offer(self, id: str) -> Response:
        """
        Retrieves the contents of an offer given an offer id.

        :param id: Offer Id
        :returns: requests.Response with Offer
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/offers/content/{id}'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v2+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Create Offer
    @authenticate
    def create_offer(self,
                     payload: typing.Union[str, dict]) -> Response:
        """
        Creates a new content offer as defined by the request data.

        :param offer: new Offer
        :returns: requests.Response with created XT Activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/offers/content'
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v2+json',
        })
        if type(payload) == str:
            payload = json.loads(payload)
        response = self.session.post(f'{self.base_url}{endpoint}',
                                     json=payload)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Update Offer
    @authenticate
    def update_offer(self,
                     id: str,
                     payload: typing.Union[str, dict]) -> Response:
        """
        Updates the content offer referenced by the id specified in the URL.

        :param offer: Offer
        :param id: Offer Id
        :returns: requests.Response with Offer
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/offers/content/{id}'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v2+json',
        })
        if type(payload) == str:
            payload = json.loads(payload)
        response = self.session.put(f'{self.base_url}{endpoint}',
                                    json=payload)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Delete Offer
    @authenticate
    def delete_offer(self, id: str) -> Response:
        """
        Deletes the content offer referenced by the provided id.

        :param id: Offer Id
        :returns: requests.Response with Offer
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/offers/content/{id}'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v2+json',
        })
        response = self.session.delete(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Audiences
    # List Audiences
    @authenticate
    def list_audiences(self,
                       limit: int = 2147483647,
                       offset: int = 0,
                       sortBy: str = 'id') -> Response:
        """
        List all available audiences with options to filter and sort by each
        available field.

        You can use the URL parameters to define pagination properties and
        sorting order of the list of audiences returned by this method.

        :param limit: (optional) set the limit of activities per request,
        defaults to 2147483647
        :param offset: (optional) set the page offset per request,
        defaults to 0
        :param sortBy: (optional) set the sort key, defaults to 'id'
        :returns: requests.Response with offers
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/audiences'
        params = {
            'limit': limit,
            'offset': offset,
            'sortBy': sortBy,
        }
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v3+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}',
                                    params=params)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Get Audience
    @authenticate
    def get_audience(self, id: str) -> Response:
        """
        Get the audience definition specified by the provided id.

        :param id: Audience Id
        :returns: requests.Response with Audience
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/audiences/{id}'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v3+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Create Audience
    @authenticate
    def create_audience(self,
                        audience: typing.Union[str, dict]) -> Response:
        """
        Create a new audience as specified by the contents of the request and
        return the newly-created audience definition.

        Each audience definition is made up of either target or audience rules.
        Target rules allow the API caller to define conjunctions (OR) or
        disjunctions (AND) between various targeting conditions.
        Audience rules allow the API caller to build conjunctions (OR) or
        disjunctions over pre-built audiences (referred by ids) to create
        even more powerful definitions

        Audiences created using the API can only be edited using the API.
        You can’t edit it in the UI. You can use it in your activities though.


        :param audience: new Audience
        :returns: requests.Response with created XT Activity
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/audiences'
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v3+json',
        })
        if type(audience) == 'str':
            audience = json.loads(audience)
        response = self.session.post(f'{self.base_url}{endpoint}',
                                     json=audience)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Update Audience
    @authenticate
    def update_audience(self,
                        id: str,
                        audience: typing.Union[str, dict]) -> Response:
        """
        Update an audience with the new rules specified by the request data.

        :param audience: Audience
        :param id: Audience Id
        :returns: requests.Response with Audience
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/audiences/{id}'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v3+json',
        })
        if type(audience) == 'str':
            audience = json.loads(audience)
        response = self.session.put(f'{self.base_url}{endpoint}',
                                    json=audience)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Delete Audience
    @authenticate
    def delete_audience(self, id: str) -> Response:
        """
        Delete the audience referenced by the specified id.

        :param id: Audience Id
        :returns: requests.Response with Audience
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/audiences/{id}'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v3+json',
        })
        response = self.session.delete(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Properties
    # List Properties
    @authenticate
    def list_properties(self) -> Response:
        """
        API methods for Properties. Applicable for Enterprise
        Permissions (Target Premium).

        :returns: requests.Response with Properties
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/properties'
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Get Property
    @authenticate
    def get_property(self, id: str) -> Response:
        """
        Retrieve property by property Id.

        :param id: Property Id
        :returns: requests.Response with Property
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/properties/{id}'.format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Reports
    # Get AB Performance Report
    @authenticate
    def get_ab_performance_report(self, id: str) -> Response:
        """
        Retrieve the performance report data for the AB activity referenced
        by the provided id.

        :param id: AB Activity Id
        :returns: requests.Response with Report
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/ab/{id}/report/performance'\
            .format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Get XT Performance Report
    @authenticate
    def get_xt_performance_report(self, id: str) -> Response:
        """
        Retrieve the performance report data for the Experience activity
        referenced by the provided id.

        :param id: XT Activity Id
        :returns: requests.Response with Report
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/xt/{id}/report/performance' \
            .format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Get AP Activity Performance Report
    @authenticate
    def get_ap_activity_performance_report(self, id: str) -> Response:
        """
        Retrieve the performance report data for the Automated Personalization
        activity referenced by the provided id.

        The request format is similar to AB and XT performance report.
        Change /ab or /xt to /abt in the request url. abt is the request
        paramater for Automated Personalization activities.

        :param id: AP Activity Id
        :returns: requests.Response with Report
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/abt/{id}/report/performance' \
            .format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Get AB Audit Report
    @authenticate
    def get_ab_audit_report(self, id: str) -> Response:
        """
        Retrieve the orders/audit report data for an AB

        Change /ab to /xt or /abt in the request url for XT and AP activities.
        abt is the request paramater for Automated Personalization activities.

        :param id: AB Activity Id
        :returns: requests.Response with Report
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/ab/{id}/report/orders' \
            .format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Get XT Audit Report
    @authenticate
    def get_xt_audit_report(self, id: str) -> Response:
        """
        Retrieve the orders/audit report data for an XT

        Change /ab to /xt or /abt in the request url for XT and AP activities.
        abt is the request paramater for Automated Personalization activities.

        :param id: XT Activity Id
        :returns: requests.Response with Report
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/xt/{id}/report/orders' \
            .format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Get ABT Audit Report
    @authenticate
    def get_ap_audit_report(self, id: str) -> Response:
        """
        Retrieve the orders/audit report data for an ABT

        Change /ab to /xt or /abt in the request url for XT and AP activities.
        abt is the request paramater for Automated Personalization activities.

        :param id: XT Activity Id
        :returns: requests.Response with Report
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/activities/abt/{id}/report/orders' \
            .format(id=id)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Mboxes
    # List Mboxes
    @authenticate
    def list_mboxes(self,
                    limit: int = 2147483647,
                    offset: int = 0,
                    sortBy: str = 'id') -> Response:
        """
        List all Mboxes

        :param limit: (optional) set the limit of activities per request,
        defaults to 2147483647
        :param offset: (optional) set the page offset per request,
        defaults to 0
        :param sortBy: (optional) set the sort key, defaults to 'id'
        :returns: requests.Response with offers
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/mboxes'
        params = {
            'limit': limit,
            'offset': offset,
            'sortBy': sortBy,
        }
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}',
                                    params=params)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # List Mbox Parameters
    @authenticate
    def list_mbox_parameters(self, mboxName: str) -> Response:
        """
        Get the list of mbox parameters.

        :param mboxName: Mbox Name
        :returns: requests.Response with Mbox Parameters
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/mbox/{mboxName}'.format(mboxName=mboxName)
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # List Profile Parameters
    @authenticate
    def list_profile_parameters(self) -> Response:
        """
        Retrieve the list of available profile attributes and mbox parameters
        of type profile

        Profile attributes and Profile Parameters mean the same thing.
        Both versions are used in the UI and the documentation.


        :returns: requests.Response with Profile Parameters
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/profileattributes/mbox'
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # List Environments
    @authenticate
    def list_environments(self) -> Response:
        """
        List all available environments with the options to filter and sort.
        Use the Environments API to retrieve the environment IDs corresponding
        to the various host groups set for the client.

        If you are looking to retrieve “Host Groups”, use this API.

        :returns: requests.Response with Environments
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/environments'
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        response = self.session.get(f'{self.base_url}{endpoint}')
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Batch
    @authenticate
    def batch(self, payload: typing.Union[str, dict]) -> Response:
        """
        Stack multiple API calls together and execute them in a single batch.

        Batching allows you to pass instructions for several operations in a
        single HTTP request. You can also specify dependencies between related
        operations (described in a section below). TNT will process each of
        your independent operations (possibly in parallel) and will process
        your dependent operations sequentially. Once all operations have been
        completed, a consolidated response will be passed back and the HTTP
        connection will be closed.

        :param payload: Batch operations
        :returns: requests.Response with Environments
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = '/target/batch'
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/vnd.adobe.target.v1+json',
        })
        if type(payload) == str:
            payload = json.loads(payload)
        response = self.session.post(f'{self.base_url}{endpoint}',
                                     json=payload)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Profile
    """
    Adobe Target creates and maintains a profile for every individual user.
    This profile is stored on the Target edge cluster and is updated in real
    time after every visit.

    https://developers.adobetarget.com/api/#profiles

    A Target Profile can be fetched in two ways
    1. Using a tnt id
    Target automatically assigns a tntid for every request.

    2. Using a thirdPartyId
    Target profiles can be augmented with your own identifier
    (eg: CRM id, uuid, membership number etc)

    The Profile API can be secured by turning authentication on from the
    Target UI as described here
    (https://marketing.adobe.com/resources/help/en_US/target/ov2/c_profile-api-settings.html).
    Once authentication is switched ON, all profile API requests must have the
    profile authentication token set in the request headers. The token itself
    can be generated using the Target UI or using the steps explained above in
    the Profile Authentication Token section.
    (https://developers.adobetarget.com/api/#authentication-tokens)
    """
    # Fetch profile TNT Id
    @authenticate
    def fetch_profile_tnt(self, tnt_id: str) -> Response:
        """
        Fetch profile via TNT Id

        :param tnt_id: TNT Id
        :returns: requests.Response with Profile data
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = 'https://{client_code}.tt.omtrdc.net/rest/v1/profiles/' \
                   '{tnt_id}?client={client_code}'.format(
                    client_code=self.tenant_name, tnt_id=tnt_id)
        # Profile Access Token is required in HTTP Header for retrieving
        # Profile data
        profile_response = self.get_profile_authentication_token()
        profile_authentication_token = \
            profile_response.json()['accessToken']
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'access_token': profile_authentication_token,
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
        })
        response = self.session.get(endpoint)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Fetch profile 3rd party Id
    @authenticate
    def fetch_profile_trd_party(self, trd_party_id: str) -> Response:
        """
        Fetch profile via 3rd party Id

        :param tnt_id: 3rd party Id
        :returns: requests.Response with Profile data
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = 'https://{client_code}.tt.omtrdc.net/rest/v1/profiles/' \
                   'thirdPartyId/{trd_party_id}?client={client_code}'.format(
                    client_code=self.tenant_name,
                    trd_party_id=trd_party_id)
        # Profile Access Token is required in HTTP Header for retrieving
        # Profile data
        profile_response = self.get_profile_authentication_token()
        profile_authentication_token = \
            profile_response.json()['accessToken']
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'access_token': profile_authentication_token,
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
        })
        response = self.session.get(endpoint)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    # Updating Profiles
    """
    A user profile contains demographic and behavioral information of a web
    page visitor, such as age, gender, products purchased, last time of visit,
    and so on that Target uses to personalize the content it serves to the
    visitor.

    The profile information for each visitor is either stored in cookies or
    in third-party apps.

    If your web page implements the Target code, the profile information from
    the cookies is passed to Target using profile parameters. Target
    identifies each visitor uniquely through a pcID that it generates the
    visitor’s cookies. However, you can pass profile parameters from an
    external app through mbox calls using mbox3rdPartyIds.

    Use the profile APIs when you have profile data about your visitors to
    send to Target that you either can’t or don’t want to send as part of your
    page-based integration with Target. This might be data from a CRM or POS
    that isn’t available on the page, or data of a more sensitive nature that
    does not make sense to pass on the page.

    There are two ways to update profiles via API:
    1. Single profile API
    2. Bulk profile update via batch
    """

    # Single Profile Update
    """
    The Single Profile Update API allows sending a profile update for a single
    user and is generally used when an update must occur in relation to a
    transaction occurring in a channel that has not implemented Target.

    The Single Profile Update API is limited to performing 1 million updates
    in any rolling 24-hour period. Updates generally occur in under 1 hour,
    but may take as long as 24 hours to be reflected. If you need to send more
    updates, or require updates to be processed in shorter timeframes,
    consider sending transactional profile updates via client-side update
    (preferred), or via the Server-Side Delivery API.
    """
    @authenticate
    def single_profile_update_tnt(self,
                                  tnt_id: str,
                                  profile_params: typing.Dict[str, str]) \
            -> Response:
        """
        Single profile update via TNT Id

        :param tnt_id: TNT Id
        :param profile_params: Profile parameters to update
        profile prefix will be automatically prepended if missing
        :returns: requests.Response with Profile data
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = 'https://{client_code}.tt.omtrdc.net/m2/client/profile/' \
                   'update'.format(
                    client_code=self.tenant_name)
        # Profile Access Token is required in HTTP Header for retrieving
        # Profile data
        profile_response = self.get_profile_authentication_token()
        profile_authentication_token = \
            profile_response.json()['accessToken']
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'access_token': profile_authentication_token,
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
        })
        # The current size limitations for limit is 8KB for
        # GET and 60KB for POST.
        # This will check if GET is feasible otherwise POST will be send.
        enhanced_map = self._enchance_profile_map(profile_params)
        params = {
            'mboxPC': tnt_id,
            **enhanced_map,
        }
        response = None
        size_in_kb = size_in_kbs(urllib.parse.urlencode(enhanced_map))
        if size_in_kb <= 8:
            response = self.session.get(endpoint, params=params)
        elif size_in_kb <= 60:
            response = self.session.post(endpoint, json=params)
        else:
            raise PayloadTooLargeError(size_in_kb)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    @authenticate
    def single_profile_update_trd_party(self,
                                        trd_party_id: str,
                                        profile_params: typing.Dict[str, str])\
            -> Response:
        """
        Single profile update via TNT Id

        :param trd_party_id: 3td party Id
        :param profile_params: Profile parameters to update
        profile prefix will be automatically prepended if missing
        :returns: requests.Response with Profile data
        :raises ResponseError: Response error if status code not 200
        """
        endpoint = 'https://{client_code}.tt.omtrdc.net/m2/client/profile/' \
                   'update'.format(
                    client_code=self.tenant_name)
        # Profile Access Token is required in HTTP Header for retrieving
        # Profile data
        profile_response = self.get_profile_authentication_token()
        profile_authentication_token = \
            profile_response.json()['accessToken']
        # Target API uses different versions for endpoints
        self.session.headers.update({
            'access_token': profile_authentication_token,
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
        })
        # The current size limitations for limit is 8KB for
        # GET and 60KB for POST.
        # This will check if GET is feasible otherwise POST will be send.
        enhanced_map = self._enchance_profile_map(profile_params)
        params = {
            'mboxPC': trd_party_id,
            **enhanced_map,
        }
        response = None
        size_in_kb = size_in_kbs(urllib.parse.urlencode(enhanced_map))
        if size_in_kb <= 8:
            response = self.session.get(endpoint, params=params)
        elif size_in_kb <= 60:
            response = self.session.post(endpoint, json=params)
        else:
            raise PayloadTooLargeError(size_in_kb)
        if response.status_code != 200:
            raise ResponseError(response)
        return response

    def _enchance_profile_map(self, profile_params: typing.Dict[str, str])\
            -> typing.Dict[str, str]:
        enhanced_map = {}
        for key_val in profile_params.items():
            [key, val] = key_val
            if not key.startswith('profile'):
                key = f'profile.{key}'
            enhanced_map[key] = val
        return enhanced_map
