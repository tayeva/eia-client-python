"""Test eia_client.api_key module."""

from tempfile import TemporaryDirectory
from pathlib import Path
import os

from eia_client import api_key


TEST_API_KEY: str = "TEST_API_KEY"


def test_get_api_key_from_env_empty():
    """Test if there is no api key in the current environment."""
    assert api_key.get_from_env() == ""


def test_get_api_key_from_env_exists():
    """Test api key in env."""
    os.environ["EIA_API_KEY"] = TEST_API_KEY
    assert api_key.get_from_env() == TEST_API_KEY


def test_get_default_config_file_path():
    """Test get defautl config file path."""
    os.environ["HOME"] = "test"
    assert str(api_key.get_default_config_file_path()) == "test/.eia.config"


def test_load_api_from_file():
    """Test load api from file."""
    with TemporaryDirectory() as tmp_dir:
        test_config_fp = Path(tmp_dir).joinpath(".eia.config")
        with open(test_config_fp, "w", encoding="utf-8") as file:
            true_api_key = "z8aTHIS1ndIS3rj1lAkfaTEST9asdfj"
            file.write(true_api_key)
        key =  api_key.read_config_file(test_config_fp)
        assert key == true_api_key


def test_load_api_key_in_env():
    """Test load api key when the key is an env variable."""
    os.environ["EIA_API_KEY"] = TEST_API_KEY
    key: api_key.ApiKey = api_key.load()
    assert key.key == TEST_API_KEY


def test_load_api_key_key_from_file():
    """Test load api key from file."""
    with TemporaryDirectory() as tmp_dir:
        test_config_fp = Path(tmp_dir).joinpath(".eia.config")
        with open(test_config_fp, "w", encoding="utf-8") as file:
            true_api_key = "z8aTHIS1ndIS3rj1lAkfaTEST9asdfj"
            file.write(true_api_key)
        os.environ["HOME"] = tmp_dir
        del os.environ["EIA_API_KEY"]
        key: api_key.ApiKey = api_key.load()
        assert key.key == true_api_key
