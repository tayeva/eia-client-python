"""Test eia_client.api_endpoint module."""

from eia_client.endpoint import EndpointBuilder
from eia_client.api_key import ApiKey


def test_total_energy():
    """Test the total energy endpoint with no arguments"""
    builder = EndpointBuilder(ApiKey("TEST"))
    endpoint = builder.total_energy()
    true_endpoint = ("https://api.eia.gov/v2/total-energy/data/?"
                     "api_key=TEST&frequency=monthly&data[0]=value"
                     "&facets[msn][]=ELEPTUS&sort[0][column]=period"
                     "&sort[0][direction]=desc&offset=0&length=5000")
    assert endpoint.endpoint == true_endpoint


def test_total_energy_start_end():
    """Test the total energy endpoint with no arguments"""
    builder = EndpointBuilder(ApiKey("TEST"))
    endpoint = builder.total_energy(start="2020-01", end="2022-01")
    true_endpoint = ("https://api.eia.gov/v2/total-energy/data/"
                     "?api_key=TEST&frequency=monthly&data[0]=value"
                     "&facets[msn][]=ELEPTUS&sort[0][column]=period"
                     "&sort[0][direction]=desc&offset=0&length=5000"
                     "&start=2020-01&end=2022-01")
    assert endpoint.endpoint == true_endpoint
