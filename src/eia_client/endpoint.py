"""A module for interacting with the EIA Open Data API."""

from dataclasses import dataclass
import logging

import eia_client.api_key as ak


LOGGER = logging.getLogger(__name__)


@dataclass
class EndpointParams:
    """
    API Endpoint params.
    """

    frequency: str
    data: list
    facets: dict
    start: str
    end: str
    sort: list
    offset: int
    length: int


@dataclass
class Endpoint:
    """
    Api endpoint dataclass.
    Use this data class to encapsulate an endpoint.
    Methods from EndpointBuilder return Endpoint classes.
    """

    endpoint: str
    params: EndpointParams


def _list_if_str(obj) -> list:
    return [obj] if isinstance(obj, str) else obj


def _list_if_none(obj) -> list:
    return [] if obj is None else obj


class EndpointBuilder:
    """
    A class for building EIA endpoints with API key.

    Each method of this class represents an "interface" to
    an EIA endpoint. The output of each method is usable in the
    `eia_client.client.get` function.

    :param api_key: ApiKey data class

    """

    BASE = "https://api.eia.gov/v2"
    ENDPOINT = ""
    SORT = [{"column": "period", "direction": "desc"}]

    def __init__(
        self,
        api_key: ak.ApiKey = None,
        frequency: str = "monthly",
        data: list = None,
        facets: dict = None,
        start: str = None,
        end: str = None,
        sort: list = None,
        offset: int = 0,
        length: int = 5000,
    ) -> None:
        self._api_key: ak.ApiKey = ak.load() if api_key is None else api_key
        self.set_params(
            frequency=frequency,
            data=data,
            facets=facets,
            start=start,
            end=end,
            sort=sort,
            offset=offset,
            length=length,
        )
        self._endpoint = None

    def _join_api_key_to_endpoint(self) -> None:
        """
        Join query to base and version to create fully formed endpoint.

        All queries to the EIA API request an API. This method will join
        the base endpoint and API key to endpoint of interest.


        """
        api_key = f"/?api_key={self._api_key.key}"
        self._endpoint.endpoint = f"{self.BASE}{self._endpoint.endpoint}{api_key}"

    def set_params(
        self,
        frequency: str = "monthly",
        data: list = None,
        facets: dict = None,
        start: str = None,
        end: str = None,
        sort: list = None,
        offset: int = 0,
        length: int = 5000,
    ) -> EndpointParams:
        """Set endpoint query parameters."""
        data = [] if data is None else data
        facets = {} if facets is None else facets
        sort = self.SORT if sort is None else sort
        self._params = EndpointParams(
            frequency=frequency,
            data=data,
            facets=facets,
            start=start,
            end=end,
            sort=sort,
            offset=offset,
            length=length,
        )

    def build(self) -> Endpoint:
        """Build the endpoint."""
        self._endpoint = Endpoint(self.ENDPOINT, self._params)
        self._join_api_key_to_endpoint()
        return self._endpoint


class TotalEnergy(EndpointBuilder):
    """Total Energy API endpoint."""

    VALID_FREQUENCY = (
        "monthly",
        "annual",
    )
    DEFAULT_MSN = "ELETPUS"
    DATA = ["value"]
    ENDPOINT = "/total-energy/data"

    def __init__(
        self,
        api_key: ak.ApiKey = None,
        frequency: str = "monthly",
        msn: list = None,
        start: str = None,
        end: str = None,
        sort: list = None,
        offset: int = 0,
        length: int = 5000,
    ):
        super().__init__(
            api_key,
            frequency=frequency,
            data=self.DATA,
            facets=self._facets(msn),
            start=start,
            end=end,
            sort=sort,
            offset=offset,
            length=length,
        )

    def _facets(self, msn: list = None):
        msn = [self.DEFAULT_MSN] if msn is None else msn
        return {"msn": msn}


class ElectricityRetailSales(EndpointBuilder):
    """Electricity Retail sales endpoint."""

    VALID_FREQUENCY = (
        "monthly",
        "annual",
    )
    VALID_DATA = ("customers", "price", "revenue", "sales")
    ENDPOINT = "/electricity/retail-sales/data"

    def __init__(
        self,
        api_key: ak.ApiKey = None,
        frequency: str = "monthly",
        state: list = None,
        sector: list = None,
        data: list = None,
        start: str = None,
        end: str = None,
        sort: list = None,
        offset: int = 0,
        length: int = 5000,
    ):
        if frequency not in self.VALID_FREQUENCY:
            raise RuntimeError(f"Invalid frequency argument:{frequency}")
        super().__init__(
            api_key,
            frequency=frequency,
            data=self._data(data),
            facets=self._facets(state=state, sector=sector),
            start=start,
            end=end,
            sort=sort,
            offset=offset,
            length=length,
        )

    def _data(self, data: list = None) -> list:
        data = _list_if_none(_list_if_str(data))
        if any(d not in self.VALID_DATA for d in data):
            raise RuntimeError("Invalid data argument")
        if not data:
            # You have to pass it at least one data series.
            data = [self.VALID_DATA[0]]
        return data

    def _facets(self, state: list = None, sector: list = None) -> dict:
        state = _list_if_none(_list_if_str(state))
        sector = _list_if_none(_list_if_str(sector))
        facets = {}
        if state:
            facets["stateid"] = state
        if sector:
            facets["sectorid"] = sector
        return facets
