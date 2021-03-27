from pathlib import Path
from typing import Any, Dict

from dotenv import dotenv_values, find_dotenv

from stela.utils import find_pyproject_folder


def read_dotenv(config_file_path: str, env_file: str) -> Dict[Any, Any]:
    """Stela DotEnv Loader.

    :param config_file_path: relative path for config files
    :param env_file: dotenv file name
    :return: Dict
    """
    from loguru import logger

    path = find_pyproject_folder() or Path().cwd()
    filepath = path.joinpath(config_file_path, env_file)
    dotenv_path = find_dotenv(str(filepath))
    if dotenv_path:
        logger.debug(f"Looking for {env_file} file...")
    env_data = dotenv_values(dotenv_path)
    return env_data
