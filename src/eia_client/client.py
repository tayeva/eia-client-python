"""EIA client module."""

from requests import Session
from eia_client.endpoint import Endpoint


class Client:
    """
    EIA Client class.
    """

    def __init__(self, session=None):
        if session is None:
            session = Session()
        self._session = session

    def get(self, endpoint : Endpoint):
        """EIA Client get endpoint."""
        return self._session.get(endpoint.endpoint)
