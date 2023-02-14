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


def join_api_key(endpoint: Endpoint, api_key: ak.ApiKey):
    """Join an endpoint and API key (required for all requests to API)."""
    endpoint.endpoint = f"{endpoint.endpoint}/?api_key={api_key.key}"
    return endpoint


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

    def build(self, **kwargs) -> Endpoint:
        """Build the endpoint."""
        endpoint_str = f"{self.BASE}{self.ENDPOINT}"
        # TODO: feature: ability to update params via kwargs and rebuild
        self._endpoint = Endpoint(endpoint_str, self._params)
        return self._endpoint

    @property
    def endpoint(self):
        """Get the built endpoint (won't rebuild if already built)."""
        if self._endpoint is None:
            self.build()
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
        msn = [msn] if isinstance(msn, str) else msn
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
