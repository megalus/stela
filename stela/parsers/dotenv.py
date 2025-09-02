from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import dotenv_values, find_dotenv

from stela.utils import show_value


def read_dotenv(
    config_file_path: str,
    env_file: str,
    verbose: bool,
    encoding: str,
    show_logs: bool = False,
    filter_logs: bool = True,
) -> Dict[Any, Any]:
    """Stela DotEnv Loader.

    :param config_file_path: relative path for config files
    :param env_file: dotenv file name
    :param verbose: warn if dotenv file is not found
    :param encoding: encoding for dotenv file
    :param show_logs: show logs for dotenv file reading
    :param filter_logs: Filter variable value in logs
    :return: Dict
    """
    from loguru import logger

    def look_for_file(current_path: Path, file_name: str) -> Optional[Path]:
        test_path = current_path.joinpath(file_name)
        if show_logs:
            logger.debug(f"Looking for file '{env_file}' in '{current_path}'")
        if test_path.exists():
            return test_path
        if str(current_path) in ["/", "\\"] or current_path.parent == current_path:
            return None
        return look_for_file(current_path.parent, file_name)

    path = Path.cwd().joinpath(config_file_path)
    env_path = look_for_file(path, env_file)
    if not env_path:
        if show_logs:
            logger.debug(f"File {env_file} not found starting at path {path}.")
        return {}
    logger.info(f"Reading file: {env_path}")  # always log the file being read
    dotenv_path = find_dotenv(str(env_path), usecwd=True)
    if not dotenv_path:
        return {}

    env_data = dotenv_values(
        dotenv_path=dotenv_path, verbose=verbose, encoding=encoding, interpolate=False
    )
    if env_data and show_logs:
        logger.debug(
            f"Filtered values from {dotenv_path}: {[f'{k}={show_value(v, filter_logs)}' for k, v in env_data.items()]}"
        )
    return env_data
