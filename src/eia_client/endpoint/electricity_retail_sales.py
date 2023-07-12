"""
EIA Client endpoint builder for electricity retail-sales endpoint.
"""

from eia_client import utils
from eia_client.api_key import ApiKey
from eia_client.endpoint.builder import EndpointBuilder


class ElectricityRetailSales(EndpointBuilder):
    """Electricity Retail sales endpoint.

    :param api_key: ApiKey data class
    :param frequency: The frequency of data to return ("monthly", "annual")
    :param data: The data series to return ("customers", "price", "revenue", "sales")
    :param state: The state id to filter by.
    :param sector: The sector id to filter by.
    :param end: End date (YYYY-MM)
    :param sort: Server-side sorting on return.
    :param offset: Offset
    :param length: Number of observations to return (5000 max)

    """

    VALID_FREQUENCY = (
        "monthly",
        "annual",
    )
    VALID_DATA = ("customers", "price", "revenue", "sales")
    ENDPOINT = "/electricity/retail-sales/data"

    def __init__(
        self,
        api_key: ApiKey = None,
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
        data = utils.list_if_none(utils.list_if_str(data))
        if any(d not in self.VALID_DATA for d in data):
            raise RuntimeError("Invalid data argument")
        if not data:
            # You have to pass it at least one data series.
            data = [self.VALID_DATA[0]]
        return data

    def _facets(self, state: list = None, sector: list = None) -> dict:
        state = utils.list_if_none(utils.list_if_str(state))
        sector = utils.list_if_none(utils.list_if_str(sector))
        facets = {}
        if state:
            facets["stateid"] = state
        if sector:
            facets["sectorid"] = sector
        return facets
