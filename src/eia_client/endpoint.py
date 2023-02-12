"""A module for interacting with the EIA Open Data API."""

from dataclasses import dataclass
import logging

import eia_client.api_key as ak


LOGGER = logging.getLogger(__name__)


@dataclass
class Endpoint:
    """
    Api endpoint dataclass.
    Use this data class to encapsulate an endpoint.
    Methods from EndpointBuilder return Endpoint classes.
    """
    endpoint: str


class EndpointBuilder:
    """
    A class for building EIA endpoints with API key.
    
    Each method of this class represents an "interface" to
    an EIA endpoint. The output of each method is usable in the 
    `eia_client.client.get` function.
    
    :param api_key: ApiKey data class

    """

    _BASE = "https://api.eia.gov/v2"

    def __init__(self, api_key: ak.ApiKey = None) -> None:
        self._api_key = ak.load() if api_key is None else api_key

    def _join(self, query: str) -> str:
        """Join query to base and version to create fully formed endpoint."""
        split = query.split("?")
        return f"{self._BASE}{split[0]}?api_key={self._api_key.key}&{split[1]}"

    def total_energy(self,  msn : str ="ELEPTUS", start : str = "", end : str = "",
                     frequency : str = "monthly") -> Endpoint:
        """
        Total energy endpoint.
        
        Use the EIA API browser to find an msn:
        https://www.eia.gov/opendata/browser/total-energy

        :param msn: Mnemonic Series Names (MSN).
        :start: The start date of the series (YYYY-MM; optional)
        :end: The end date of the series (YYYY-MM; optional)
        :frequency: The frequency to the series (monthly or annual)
        :return: An ApiEndpoint dataclass.
        :rtype: ApiEndpoint.
        """
        msn = msn.upper()
        # TODO: check frequency to ensure it is properly formed
        endpoint = (f"/total-energy/data/?frequency={frequency}&data[0]=value&"
            F"facets[msn][]={msn}&sort[0][column]=period&sort[0]"
            "[direction]=desc&offset=0&length=5000")
        # TODO: check start and end to ensure the properly formed
        if start:
            endpoint += f"&start={start}"
        if end:
            endpoint += f"&end={end}"
        return Endpoint(self._join(endpoint))
