"""API Key Module

It is assumed that the API Key for EIA is stored in
your home directory as .eia.config or an environment
variable called EIA_API_KEY

"""

from pathlib import Path
from dataclasses import dataclass
import logging
import os


ENV_KEY = "EIA_API_KEY"

FILE_BASE_NAME = ".eia.config"

LOGGER = logging.getLogger(__name__)


def _get_api_key_from_env() -> str:
    """Get an API from environment variables."""
    env = os.environ
    api_key = ""
    if ENV_KEY in env:
        api_key = env[ENV_KEY]
    return api_key


def get_default_config_file_path() -> Path:
    """Get the default config file path."""
    home = Path().home()
    return home.joinpath(FILE_BASE_NAME)


def _load_api_key_from_file(file_path : Path) -> str:
    """Load api key from file (text file, utf-8)."""
    api_key = ""
    if file_path.exists():
        with open(file_path, encoding="utf-8") as file:
            api_key = file.read()
            LOGGER.info("Loaded api key from file:%s", str(file_path))
    if not api_key:
        LOGGER.warning("No API key. Please configure.")
    return api_key


@dataclass
class ApiKey:
    """API Key dataclass."""
    key: str


def load_api_key(config_file_path: Path = None) -> ApiKey:
    """
    Load the API key.

    (1) Try from environment.
    (2) If not exists, try from .eia.config file in '~/` home directory or
        specified config_file_path.
    """
    api_key = _get_api_key_from_env()
    if api_key:
        LOGGER.info("Loaded api key from env.")
        return ApiKey(key=api_key)
    if config_file_path is None:
        config_fp = get_default_config_file_path()
    else:
        config_fp = config_file_path
    api_key = _load_api_key_from_file(config_fp)
    if not api_key:
        raise RuntimeError("No API key. Please configure... see docs..")
    return ApiKey(key=api_key)


def write_api_key(file_path: Path, api_key : ApiKey) -> None:
    """Write api key."""
    with open(file_path, encoding="utf-8", mode="w") as file:
        file.write(api_key.key)
    LOGGER.info("Wrote api key to:%s", file_path)
