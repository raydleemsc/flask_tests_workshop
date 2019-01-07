#
# CultureMesh API Client
#
# Inspired by: https://github.com/googlemaps/google-maps-services-python
# TODO: add license information.
#

"""
Core client functionality, common across all API requests (including performing
HTTP requests).
"""

import requests
import os
import json
from flask import abort
from culturemesh import app
from enum import IntEnum

# Relative from app.root_path
USER_DATA_LOC = os.path.join(app.root_path, "../data/mock/db_mock_users.json")
POST_DATA_LOC = os.path.join(app.root_path, "../data/mock/db_mock_posts.json")
POST_REPLY_DATA_LOC = os.path.join(app.root_path, "../data/mock/db_mock_post_replies.json")
EVENT_DATA_LOC = os.path.join(app.root_path, "../data/mock/db_mock_events.json")
EVENT_REGISTRATION_LOC = os.path.join(app.root_path, "../data/mock/db_mock_event_registration.json")
NET_REGISTRATION_LOC = os.path.join(app.root_path, "../data/mock/db_mock_network_registration.json")
NETWORK_DATA_LOC = os.path.join(app.root_path, "../data/mock/db_mock_networks.json")
LANG_DATA_LOC = os.path.join(app.root_path, "../data/mock/db_mock_languages.json")
CITY_DATA_LOC = os.path.join(app.root_path, "../data/mock/db_mock_location_cities.json")
REGION_DATA_LOC = os.path.join(app.root_path, "../data/mock/db_mock_location_regions.json")
COUNTRY_DATA_LOC = os.path.join(app.root_path, "../data/mock/db_mock_location_countries.json")
KEY = os.environ['CULTUREMESH_API_KEY']


class Request(IntEnum):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4


class Client(object):
    """Talks directly to the CultureMesh API.
    """
    _api_base_url_ = os.environ["CULTUREMESH_API_BASE_ENDPOINT"]

    def __init__(self, key=None, client_id=None, client_secret=None,
                 timeout=None, connect_timeout=None, read_timeout=None,
                 retry_timeout=60, queries_per_second=10,
                 channel=None, mock=True):

        self.mock = mock
        # See: http://docs.python-requests.org/en/master/user/advanced/
        # not used yet.
        self.session = requests.Session()

    def _request(self,
                 url,
                 request_method,
                 query_params=None,
                 body_data=None,
                 json=None,
                 body_extractor=None,
                 basic_auth=None):
        """
        Carries out HTTP requests.

        Returns body as JSON.
        """
        if self.mock:
            return self._mock_request(url, query_params, body_data)

        # This is always controlled by us, not by the user.
        url = "%s/%s?key=%s" % (self._api_base_url_, url, KEY)
        if query_params is not None:
            for param in query_params:
                url += "&%s=%s" % (param, query_params[param])

        if request_method == Request.GET:
            response = requests.get(url, auth=basic_auth)
        elif request_method == Request.POST:
            response = requests.post(
                url, json=json, data=body_data, auth=basic_auth
            )
        elif request_method == Request.PUT:
            response = requests.put(
                url, json=json, data=body_data, auth=basic_auth
            )
        elif request_method == Request.DELETE:
            response = requests.delete(
                url, json=json, data=body_data, auth=basic_auth
            )
        return self._get_body(response)

    def _get_body(self, response):
        """
        Gets the JSON body of a response.

        Raises HTTPError exceptions.
        """
        if response.status_code != 200:
            abort(response.status_code)
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            return response.text


""" Register the client with the API functions. """
from .posts import get_post
from .posts import get_post_replies
from .users import get_user
from .networks import get_network

# We may consider adding a wrapper around these assignments
# below to introduce more specific features for the client.

Client.get_post = get_post
Client.get_post_replies = get_post_replies
Client.get_user = get_user
Client.get_network = get_network
