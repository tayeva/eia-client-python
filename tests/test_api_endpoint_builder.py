"""Test eia_client.api_endpoint module."""

from eia_client.endpoint import EndpointBuilder
from eia_client.api_key import ApiKey

def test_api_endpoint_total_monthly_energy():
    """Test api endpoint total monthly energy."""
    msn = "TEST"
    builder = EndpointBuilder(ApiKey("TEST"))
    endpoint = builder.total_energy_monthly(msn)
    true_endpoint = ('https://api.eia.gov/v2/total-energy/data/?api_key=TEST'
                     '&frequency=monthly&data[0]=value&facets[msn][]=TEST'
                     '&sort[0][column]=period&sort[0][direction]=desc'
                     '&offset=0&length=5000')
    assert endpoint.endpoint == true_endpoint
