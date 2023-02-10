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


def _clean_msn(msn: str):
    """Ensure that MSN is properly formatted for EIA API."""
    return msn.upper()


def _join_api_key_and_query(api_key: ak.ApiKey, query: str) -> str:
    split = query.split("?")
    return f"{split[0]}?api_key={api_key.key}&{split[1]}"


class EndpointBuilder:
    """
    A class for building EIA endpoints with API key.
    
    Each method of this class represents an "interface" to
    an EIA endpoint. The output of each method is usable in the 
    `eia_client.client.get` function.
    
    :param api_key: ApiKey data class

    """
    # TODO: add more public methods abstracting API endpoint

    _BASE = "https://api.eia.gov/v2"

    def __init__(self, api_key: ak.ApiKey = None) -> None:
        self._api_key = ak.load() if api_key is None else api_key

    def _join(self, query: str) -> str:
        """Join query to base and version to create fully formed endpoint."""
        return f"{self._BASE}{_join_api_key_and_query(self._api_key, query)}"

    def total_energy_monthly(self, msn: str) -> Endpoint:
        """
        Total energy monthly by msn.
        
        Use the EIA API browser to find an msn:
        https://www.eia.gov/opendata/browser/total-energy

        :param msn: Mnemonic Series Names (MSN).
        :return: An ApiEndpoint dataclass.
        :rtype: ApiEndpoint.
        """
        # TODO: offset, length, and faces args
        msn = _clean_msn(msn)
        endpoint = (f"/total-energy/data/?frequency=monthly&data[0]=value&"
            F"facets[msn][]={msn}&sort[0][column]=period&sort[0]"
            "[direction]=desc&offset=0&length=5000")
        return Endpoint(self._join(endpoint))
