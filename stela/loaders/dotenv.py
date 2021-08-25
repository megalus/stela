from pathlib import Path
from typing import Any, Dict

from dotenv import dotenv_values, find_dotenv, load_dotenv

from stela.utils import find_file_folder


def read_dotenv(
    config_file_path: str, env_file: str, overwrites_memory: bool
) -> Dict[Any, Any]:
    """Stela DotEnv Loader.

    :param config_file_path: relative path for config files
    :param env_file: dotenv file name
    :param overwrites_memory: dotenv data overwrites os.environ
    :return: Dict
    """
    from loguru import logger

    path = find_file_folder("pyproject.toml") or Path().cwd()
    filepath = path.joinpath(config_file_path, env_file)
    dotenv_path = find_dotenv(str(filepath))
    if dotenv_path:
        logger.info(f"Looking for {env_file} file...")

    load_dotenv(dotenv_path=dotenv_path, override=overwrites_memory)
    env_data = dotenv_values(dotenv_path)
    return env_data
