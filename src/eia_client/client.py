"""EIA client module."""

from dataclasses import asdict
import json

from requests import Session

from eia_client.endpoint import Endpoint, EndpointParams


def _headers(params: EndpointParams) -> dict:
    return {"X-Params": json.dumps(asdict(params))}


class Client:
    """
    EIA Client class.
    """

    def __init__(self, session=None):
        if session is None:
            session = Session()
        self._session = session

    def get(self, endpoint: Endpoint):
        """EIA Client get endpoint."""
        return self._session.get(endpoint.endpoint, headers=_headers(endpoint.params))
