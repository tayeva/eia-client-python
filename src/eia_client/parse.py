"""EIA client parse module."""

import logging

from requests import Request
import pandas as pd


LOGGER = logging.getLogger(__name__)


def as_dataframe(resp: Request) -> pd.DataFrame:
    """
    Parse a requests response as a dataframe.

    :param resp: a requests response from EIA API.

    :return: A pandas dataframe containing requested data.
    :rtype: pd.DataFrame
    
    """
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
