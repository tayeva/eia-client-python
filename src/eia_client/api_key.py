"""EIA API key related functions.

The EIA API expects an API key in requests.
"""


from dataclasses import dataclass
from pathlib import Path
import logging
import os


ENV_KEY = "EIA_API_KEY"

FILE_BASE_NAME = ".eia.config"

LOGGER = logging.getLogger(__name__)


def get_from_env() -> str:
    """
    Get an API from environment variables.

    This function looks for the API key in the current environment
    variables as: "EIA_API_KEY"
    
    :return: API key from environment variables.
    :rtype: str
    """
    env = os.environ
    key = ""
    if ENV_KEY in env:
        key = env[ENV_KEY]
    return key


def get_default_config_file_path() -> Path:
    """
    Get the default config file path.
    
    This function retrieves the current home path and
    joins it with the default API key config file base name, which is
    ".eia.config" to return a path.

    :return: default Path to API key.
    :rtype: Path
    """
    home = Path().home()
    return home.joinpath(FILE_BASE_NAME)


@dataclass
class ApiKey:
    """
    API Key dataclass.

    EIA requires an API key to be submitted with requests. This dataclass
    is how that API key is represented in code. Available for import from
    head of package.

    :param key: You EIA API key.
    """

    key: str


def read_config_file(file_path : Path) -> str:
    """Load api key from file (text file, utf-8).
    
    :param file_path: The file path to the API key config file.
    :return:  API key as string if file exits otherwise an empty string.
    :rtype: str
    """
    key = ""
    if file_path.exists():
        with open(file_path, encoding="utf-8") as file:
            key = file.read()
            LOGGER.info("Loaded api key from file:%s", str(file_path))
    if not key:
        LOGGER.warning("No API key. Please configure.")
    return key


def load(config_file_path: Path = None) -> ApiKey:
    """
    Load the API key.

    (1) Try from environment.
    (2) If not exists, try from .eia.config file in '~/` home directory or
        specified config_file_path.

    :param config_file_path: The API key config file path (optional). If this
     parameter is not provided the function tries the default location.

    :return: The API key either loaded from env or file
    :rtype: ApiKey
    """
    key = get_from_env()
    if key:
        LOGGER.info("Loaded api key from env.")
        return ApiKey(key=key)
    if config_file_path is None:
        config_fp = get_default_config_file_path()
    else:
        config_fp = config_file_path
    key = read_config_file(config_fp)
    if not key:
        raise RuntimeError("No API key. Please configure... see docs..")
    return ApiKey(key=key)


def write(file_path: Path, key : ApiKey) -> None:
    """Write api key.
    
    :param file_path: The file path to write the API key.
    :param key: The API key to write to file
    """
    with open(file_path, encoding="utf-8", mode="w") as file:
        file.write(key.key)
    LOGGER.info("Wrote api key to:%s", file_path)
