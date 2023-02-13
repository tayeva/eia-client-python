"""A module for interacting with the EIA Open Data API."""

from dataclasses import dataclass
from abc import ABC, abstractmethod
import logging
from typing import Tuple

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


class EndpointBuilder(ABC):
    """
    A class for building EIA endpoints with API key.
    
    Each method of this class represents an "interface" to
    an EIA endpoint. The output of each method is usable in the 
    `eia_client.client.get` function.
    
    :param api_key: ApiKey data class

    """

    BASE = "https://api.eia.gov/v2"
    SORT = [{"column": "period", "direction": "desc"}]

    def __init__(self, api_key: ak.ApiKey = None) -> None:
        self._api_key : ak.ApiKey = ak.load() if api_key is None else api_key

    def join(self, endpoint: Endpoint) -> Endpoint:
        """Join query to base and version to create fully formed endpoint."""
        endpoint.endpoint = f"{self.BASE}{endpoint.endpoint}/?api_key={self._api_key.key}"
        return endpoint

    @abstractmethod
    def build(self, frequency : str = "monthly", data : list = None,
              facets : dict = None, start : str = None, end : str = None,
              sort : list = None, offset : int = 0,
              length : int = 5000) -> Tuple[Endpoint, EndpointParams]:
        """Build the endpoint."""
        params = EndpointParams(frequency=frequency, data=data, facets=facets,
                                start=start, end=end, sort=sort, offset=offset, length=length)
        return (self.join(Endpoint("")), params)



class TotalEnergy(EndpointBuilder):
    """Total Energy API endpoint."""

    VALID_FREQUENCY = ("monthly", "annual",)

    def build(self, frequency : str = "monthly", data : list = None,
              facets : dict = None, start : str = None, end : str = None,
              sort : list = None, offset : int = 0,
              length : int = 5000) -> Tuple[Endpoint, EndpointParams]:
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
        endpoint = Endpoint("/total-energy/data")
        endpoint.endpoint = self.join(endpoint)
        facets = {} if facets is None else facets
        sort = self.SORT if sort is None else sort
        data =  ["value"] if data is None else data
        params = EndpointParams(frequency=frequency, data=data,
                                facets=facets, start=start, end=end,
                                sort=self.SORT, offset=offset, length=length)
        return (endpoint, params)


class ElectricityRetailSales(EndpointBuilder):
    """Electricity Retail sales endpoint."""

    VALID_FREQUENCY = ("monthly", "annual",)
    VALID_DATA = ("customers", "price", "revenue", "sales")

    def build(self, frequency : str = "monthly", data : list = None,
              facets : dict = None, start : str = None, end : str = None,
              sort : list = None, offset : int = 0,
              length : int = 5000) -> Tuple[Endpoint, EndpointParams]:
        endpoint = Endpoint("/electricity/retail-sales")
        # TOOD: this is where you left off
        params = EndpointParams()
        return (endpoint, params)
