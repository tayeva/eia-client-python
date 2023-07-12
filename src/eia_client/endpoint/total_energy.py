"""
EIA Client endpoing for total-energy endpoint.

You can browse different MSN facets here:
https://www.eia.gov/opendata/browser/total-energy

"""

from eia_client import utils
from eia_client.api_key import ApiKey
from eia_client.endpoint.builder import EndpointBuilder


class TotalEnergy(EndpointBuilder):
    """Total Energy API endpoint.

    :param api_key: ApiKey data class
    :param frequency: The frequency of data to return ("monthly", "annual")
    :param msn: Mnemonic Series Names (MSN) - This is a unique identifier used by EIA for data series.
    :param start: Start date (YYYY-MM)
    :param end: End date (YYYY-MM)
    :param sort: Server-side sorting on return.
    :param offset: Offset
    :param length: Number of observations to return (5000 max)
    """

    VALID_FREQUENCY = (
        "monthly",
        "annual",
    )
    DEFAULT_MSN = "ELETPUS"
    DATA = ["value"]
    ENDPOINT = "/total-energy/data"

    def __init__(
        self,
        api_key: ApiKey = None,
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
        msn = utils.list_if_str(msn)
        msn = [self.DEFAULT_MSN] if msn is None else msn
        return {"msn": msn}
