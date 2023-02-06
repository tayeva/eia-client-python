"""EIA API Endpoint Builder class."""

from dataclasses import dataclass

from eia_client.api_key import ApiKey


@dataclass
class ApiEndpoint:
    """Api endpoint dataclass."""
    endpoint: str


class ApiEndpointBuilder:
    """Api endpoint builder class."""
    # TODO: add more public methods abstracting API endpoing

    _BASE = "https://api.eia.gov/v2"

    def __init__(self, api_key: ApiKey) -> None:
        self._api_key = api_key

    def _add_api_key(self, query: str) -> str:
        split = query.split("?")
        query = f"{split[0]}?api_key={self._api_key.key}&{split[1]}"
        return query
    
    def _join(self, query: str) -> str:
        """Join query to base and version to create fully formed endpoint."""
        query = self._add_api_key(query)
        return f"{self._BASE}{query}"

    def total_energy_monthly(self, msn: str):
        """Total energy monthly by msn."""
        # TODO: offset, length, and faces args
        endpoint = (f"/total-energy/data/?frequency=monthly&data[0]=value&"
            F"facets[msn][]={msn}&sort[0][column]=period&sort[0]"
            "[direction]=desc&offset=0&length=5000")
        return ApiEndpoint(self._join(endpoint))
