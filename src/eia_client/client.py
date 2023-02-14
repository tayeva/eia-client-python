"""EIA client module."""

from dataclasses import asdict
import json

from requests import Session

from eia_client import api_key as ak
from eia_client.endpoint import Endpoint, EndpointParams, join_api_key


def _headers(params: EndpointParams) -> dict:
    return {"X-Params": json.dumps(asdict(params))}


class Client:
    """
    EIA Client class.
    """

    def __init__(self, session: Session = None, api_key: ak.ApiKey = None):
        self._session = Session() if session is None else session
        self._api_key = ak.load() if api_key is None else api_key

    def get(self, endpoint: Endpoint):
        """EIA Client get endpoint."""
        endpoint = join_api_key(endpoint, self._api_key)
        headers = _headers(endpoint.params)
        return self._session.get(endpoint.endpoint, headers=headers)
