import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict

import toml
from scalpl import Cut

from stela.utils import find_file_folder, merge_dicts


def read_embed(options: "StelaOptions") -> Dict[Any, Any]:
    """Stela Embed Loader.

    :param options: StelaOptions instance
    :return: Dict
    """
    from loguru import logger

    # Get toml data
    path = find_file_folder("pyproject.toml") or Path().cwd()
    filepath = path.joinpath("pyproject.toml")
    toml_data = toml.load(filepath)
    table = options.env_table

    # Get environment layers
    with open(filepath, "r") as file:
        raw_data = file.read()
    pattern = fr"(?<=\[{table}\.)\w+"
    environment_list = re.findall(pattern, raw_data)

    logger.info(f"Looking for table [{table}] inside pyproject.toml...")
    proxy = Cut(toml_data)
    table_data = proxy.get(options.env_table, {})
    first_level_data = deepcopy(table_data)

    #  remove keys which represent environments in first level
    keys = list(first_level_data.keys())
    for key in keys:
        if key in environment_list:
            del first_level_data[key]

    if options.use_environment_layers:
        sub_table_name = f"{table}.{options.current_environment}"
        logger.info(
            f"Looking for sub-table [{sub_table_name}] inside pyproject.toml..."
        )
        sub_table = proxy.get(sub_table_name, {})
        merge_dicts(source_dict=sub_table, target_dict=first_level_data)
    return first_level_data
