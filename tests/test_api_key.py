"""Test eia_client.api_key module."""

from tempfile import TemporaryDirectory
from pathlib import Path
import os

import eia_client as ec


TEST_API_KEY: str = "TEST_API_KEY"


def test_get_api_key_from_env_empty():
    """Test if there is no api key in the current environment."""
    assert ec.api_key._get_api_key_from_env() == ""


def test_get_api_key_from_env_exists():
    """Test api key in env."""
    os.environ["EIA_API_KEY"] = TEST_API_KEY
    assert ec.api_key._get_api_key_from_env() == TEST_API_KEY


def test_get_default_config_file_path():
    """Test get defautl config file path."""
    os.environ["HOME"] = "test"
    assert str(ec.api_key._get_default_config_file_path()) == "test/.eia.config"


def test_load_api_from_file():
    """Test load api from file."""
    with TemporaryDirectory() as tmp_dir:
        test_config_fp = Path(tmp_dir).joinpath(".eia.config")
        with open(test_config_fp, "w", encoding="utf-8") as file:
            true_api_key = "z8aTHIS1ndIS3rj1lAkfaTEST9asdfj"
            file.write(true_api_key)
        api_key =  ec.api_key._load_api_from_file(test_config_fp)
        assert api_key == true_api_key
