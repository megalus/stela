from typing import Any, Dict

from stela.config import StelaOptions


def default_loader(options: StelaOptions, env_data: Dict[str, Any]) -> Dict[str, Any]:
    """Stela Default Loader.

    :param options: Stela Options
    :param env_data: Dict with environment data
    :return: Dict
    """
    from loguru import logger

    logger.info(
        f"Using Stela Default Loader. Current environment is: {options.current_environment}"
    )
    return env_data
