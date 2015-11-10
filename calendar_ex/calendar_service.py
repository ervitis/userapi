from libs.apiclient import discovery
from libs.oauth2client import client
from libs.oauth2client import appengine
from google.appengine.api import memcache

from libs import httplib2
import os

MISSING_CLIENT_SECRETS = """
Client secrets not found
"""


class CalendarService():

    def __init__(self):
        self._service = None
        self._scope = 'https://www.googleapis.com/auth/calendar'
        self._http = None
        self._client_secrets = None
        self._decorator = None

    def _create_http(self):
        self._http = httplib2.Http(memcache)

    def _create_client_secrets(self):
        self._client_secrets = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

    def _create_service(self):
        self._service = discovery.build(
            serviceName='calendar',
            version='v3',
            http=self._http
        )

    def create_decorator(self):
        if not self._client_secrets:
            self._create_client_secrets()

        try:
            self._decorator = appengine.oauth2decorator_from_clientsecrets(
                filename=self._client_secrets,
                scope=self._scope,
                message=MISSING_CLIENT_SECRETS)

            return self._decorator
        except Exception:
            return None

    def create_service(self):
        if not self._http:
            self._create_http()

        if not self._decorator:
            return None

        self._http = self._decorator.http()

        if not self._service:
            self._create_service()

    def get_calendars(self):
        calendar_list = self._service.calendarList().list().execute(http=self._http)

        return calendar_list['items']