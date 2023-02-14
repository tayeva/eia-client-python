"""Test eia_client.api_endpoint module.

TODO: finish updating these 
"""
from dataclasses import asdict

from eia_client.endpoint import TotalEnergy
from eia_client.api_key import ApiKey


def test_total_energy_endpoint():
    """Test the total energy endpoint with no arguments"""
    endpoint = TotalEnergy(api_key=ApiKey("TEST")).build()
    true_endpoint = "https://api.eia.gov/v2/total-energy/data"
    assert endpoint.endpoint == true_endpoint


def test_total_energy_endpoint_defautl_params():
    """Test the total energy endpoint with no arguments"""
    endpoint = TotalEnergy(api_key=ApiKey("TEST")).build()
    params = asdict(endpoint.params)
    assert params == {
        "frequency": "monthly",
        "data": ["value"],
        "facets": {"msn": ["ELETPUS"]},
        "start": None,
        "end": None,
        "sort": [{"column": "period", "direction": "desc"}],
        "offset": 0,
        "length": 5000,
    }


def test_total_energy_start_end():
    """Test the total energy endpoint with no arguments"""
    endpoint = TotalEnergy(
        api_key=ApiKey("TEST"), start="2020-01", end="2022-01"
    ).build()
    params = asdict(endpoint.params)
    assert params == {
        "frequency": "monthly",
        "data": ["value"],
        "facets": {"msn": ["ELETPUS"]},
        "start": "2020-01",
        "end": "2022-01",
        "sort": [{"column": "period", "direction": "desc"}],
        "offset": 0,
        "length": 5000,
    }
