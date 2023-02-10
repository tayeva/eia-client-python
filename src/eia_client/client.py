"""EIA client module."""

import requests

from eia_client.endpoint import Endpoint


def get(endpoint: Endpoint, **kwargs) -> requests.Response:
    """
    Issue a GET request to endpoint.
    
    :param endpoint: An Endpoint dataclass.
    :return: A requests response object.
    :rtype: requests.Response
    """
    if kwargs.get("timeout") is None:
        timeout = 60
    else:
        timeout = timeout.pop("timeout")
    return requests.get(endpoint.endpoint, timeout=timeout, **kwargs)
