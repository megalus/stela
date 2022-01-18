from typing import Any, Dict

from loguru import logger
from pydantic import BaseSettings


def stela_settings(settings: BaseSettings) -> Dict[str, Any]:
    """Read Stela data for use in Pydantic Settings.

    Will return stela settings as a python dictionary.
    """
    from stela import settings as stela_settings_data

    data = stela_settings_data.to_dict

    if (
        hasattr(settings.__config__, "log_stela_settings")
        and settings.__config__.log_stela_settings
    ):
        logger.debug(f"Stela settings dict are: {data}")

    return data
