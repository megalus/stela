from pathlib import Path
from typing import Any, Dict

from dotenv import dotenv_values, find_dotenv, load_dotenv

from stela.utils import show_value


def read_dotenv(
    config_file_path: str,
    env_file: str,
    overwrites_memory: bool,
    verbose: bool,
    encoding: str,
    update_environs: bool = False,
    filter_logs: bool = True,
) -> Dict[Any, Any]:
    """Stela DotEnv Loader.

    :param config_file_path: relative path for config files
    :param env_file: dotenv file name
    :param overwrites_memory: dotenv data overwrites os.environ
    :param verbose: warn if dotenv file is not found
    :param encoding: encoding for dotenv file
    :param update_environs: update os.environ with dotenv data
    :return: Dict
    """
    from loguru import logger

    path = Path.cwd()
    filepath = path.joinpath(config_file_path, env_file)
    dotenv_path = find_dotenv(str(filepath))
    if not dotenv_path:
        return {}

    if update_environs:
        load_dotenv(
            dotenv_path=dotenv_path,
            override=overwrites_memory,
            verbose=verbose,
            encoding=encoding,
        )
    env_data = dotenv_values(
        dotenv_path=dotenv_path,
        verbose=verbose,
        encoding=encoding,
    )
    if env_data:
        logger.debug(
            f"Data from {dotenv_path}: {[f'{k}={show_value(v, filter_logs)}' for k, v in env_data.items()]}"
        )
    return env_data
