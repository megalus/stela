from pathlib import Path
from typing import Any, Dict, Optional

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

    :param filter_logs: Filter variable value in logs
    :param config_file_path: relative path for config files
    :param env_file: dotenv file name
    :param overwrites_memory: dotenv data overwrites os.environ
    :param verbose: warn if dotenv file is not found
    :param encoding: encoding for dotenv file
    :param update_environs: update os.environ with dotenv data
    :return: Dict
    """
    from loguru import logger

    def look_for_file(current_path: Path, file_name: str) -> Optional[Path]:
        test_path = current_path.joinpath(file_name)
        logger.debug(f"Looking for file '{env_file}' in '{current_path}'")
        if test_path.exists():
            return test_path
        if str(current_path) in ["/", "\\"] or current_path.parent == current_path:
            return None
        return look_for_file(current_path.parent, file_name)

    path = Path.cwd().joinpath(config_file_path)
    env_path = look_for_file(path, env_file)
    if not env_path:
        logger.debug(f"File {env_file} not found starting at path {path}.")
        return {}
    logger.info(f"Reading file: {env_path}")
    dotenv_path = find_dotenv(str(env_path), usecwd=True)
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
