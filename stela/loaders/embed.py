from copy import deepcopy
from pathlib import Path
from typing import Any, Dict

import toml
from scalpl import Cut

from stela.utils import find_pyproject_folder


def read_embed(options: "StelaOptions") -> Dict[Any, Any]:
    """Stela Embed Loader.

    :param options: StelaOptions instance
    :return: Dict
    """
    from loguru import logger

    path = find_pyproject_folder() or Path().cwd()
    filepath = path.joinpath("pyproject.toml")
    toml_data = toml.load(filepath)
    table = options.env_table
    logger.debug(f"Looking for table [{table}] inside pyproject.toml...")
    proxy = Cut(toml_data)
    table_data = proxy.get(options.env_table, {})
    first_level_data = deepcopy(table_data)
    #  remove sub dicts
    keys = list(first_level_data.keys())
    for key in keys:
        if isinstance(first_level_data[key], dict):
            del first_level_data[key]
    if options.use_environment_layers:
        sub_table = f"{table}.{options.current_environment}"
        logger.debug(f"Looking for sub-table [{sub_table}] inside pyproject.toml...")
        sub_table = proxy.get(sub_table, {})
        first_level_data.update(sub_table)
    return first_level_data
