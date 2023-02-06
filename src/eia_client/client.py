"""EIA Client"""

import logging

import pandas as pd
import requests

import eia_client as ec


LOGGER = logging.getLogger(__name__)


def get(endpoint: ec.ApiEndpoint, **kwargs) -> requests.Response:
    """Get endpoint"""
    if kwargs.get("timeout") is None:
        timeout = timeout.pop("timeout")
    else:
        timeout = 60
    return requests.get(endpoint.endpoint, timeout=timeout, **kwargs)


def parse_as_dataframe(resp: requests.Response) -> pd.DataFrame:
    """Get the endpoint as a dataframe."""
    if resp.status_code == 200:
        data = resp.json()
        data_resp = data["response"]
        resp_warning = data_resp.get("warning")
        if resp_warning:
            LOGGER.warning(resp_warning)
        data_df = pd.DataFrame(data_resp["data"])
    else:
        data_df = pd.DataFrame()
        LOGGER.warning("status:%s", resp.status_code)
    return data_df
