"""A module for interacting with the EIA API."""

from dataclasses import dataclass
import logging

from eia_client.api_key import ApiKey


LOGGER = logging.getLogger(__name__)


@dataclass
class ApiEndpoint:
    """
    Api endpoint dataclass.
    Use this data class to encapsulate an endpoint.
    Methods from EndpointBuilder return Endpoint classes.
    """
    endpoint: str


def _clean_msn(msn: str):
    """Ensure that MSN is properly formatted for EIA API."""
    return msn.upper()


def _join_api_key_and_query(api_key: ApiKey, query: str) -> str:
    split = query.split("?")
    return f"{split[0]}?api_key={api_key.key}&{split[1]}"


class ApiEndpointBuilder:
    """
    A class for building EIA endpoints with API key.
    
    Each method of this class represents an "interface" to
    an EIA endpoint. The output of each method is usable in the 
    `eia_client.client.get` function.
    
    :param api_key: ApiKey data class

    """
    # TODO: add more public methods abstracting API endpoint

    _BASE = "https://api.eia.gov/v2"

    def __init__(self, api_key: ApiKey) -> None:
        self._api_key = api_key

    def _join(self, query: str) -> str:
        """Join query to base and version to create fully formed endpoint."""
        return f"{self._BASE}{_join_api_key_and_query(self._api_key, query)}"

    def total_energy_monthly(self, msn: str) -> ApiEndpoint:
        """
        Total energy monthly by msn.

        :param msn: Mnemonic Series Names (MSN).
        :return: An ApiEndpoint dataclass.
        :rtype: ApiEndpoint.

        """
        # TODO: offset, length, and faces args
        msn = _clean_msn(msn)
        endpoint = (f"/total-energy/data/?frequency=monthly&data[0]=value&"
            F"facets[msn][]={msn}&sort[0][column]=period&sort[0]"
            "[direction]=desc&offset=0&length=5000")
        return ApiEndpoint(self._join(endpoint))
