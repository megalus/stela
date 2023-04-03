from typing import Any, Dict

from loguru import logger
from pydantic import BaseSettings

from stela.utils import read_env


def stela_settings(settings: BaseSettings) -> Dict[str, Any]:
    """Read Stela data for use in Pydantic Settings.

    Will return stela settings as a python dictionary.
    """
    from stela import settings as stela_settings_data

    data = stela_settings_data.to_dict

    if getattr(settings.__config__, "log_stela_settings", False):
        logger.debug(f"Stela settings dict are: {data}")

    return data


def stela_env_settings(settings: BaseSettings) -> dict[str, Any]:
    """
    Read Stela Data from many dotenv files.
    """
    delimiter = getattr(settings.__config__, "env_nested_delimiter", "")

    # Ask Stela to read envs as per his configuration
    env = read_env()

    if delimiter:
        data = {
            ".".join(var.split(delimiter)).lower(): env.get(var) for var in env.list()
        }
    else:
        data = {var.lower(): env.get(var) for var in env.list()}

    if getattr(settings.__config__, "log_stela_settings", False):
        logger.debug(f"Stela settings dict are: {data}")

    return data
