"""EIA client module."""

import requests

from eia_opendata.api_endpoint import ApiEndpoint


def get(endpoint: ApiEndpoint, **kwargs) -> requests.Response:
    """
    Issue a GET request to endpoint.
    
    :param api_endpoint: An ApiEndpoint dataclass.
    :return: A requests response object.
    :rtype: requests.Response
    """
    if kwargs.get("timeout") is None:
        timeout = 60
    else:
        timeout = timeout.pop("timeout")
    return requests.get(endpoint.endpoint, timeout=timeout, **kwargs)
