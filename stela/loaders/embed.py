import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict

import toml
from scalpl import Cut

from stela.utils import find_pyproject_folder


def update_value(env_data, shared_data, env_key):
    """Update Sub Dicts.

    Example:

        [environment]
        test = true
        project.foo = "bar"

        [environment.local]
        project.bar = "foo"
        project.db.name = "test"

    Result for ENVIRONMENT=local:
        {
            "test": True,
            "project": {
                "foo": "bar,
                "bar": "foo",
                "db": {
                    "name": "test"
                }
            }

    """
    if isinstance(env_data[env_key], dict):
        for k in env_data[env_key]:
            if not shared_data[env_key].get(k):
                shared_data[env_key][k] = {}
            update_value(env_data[env_key], shared_data[env_key], k)
    else:
        shared_data[env_key] = env_data[env_key]


def read_embed(options: "StelaOptions") -> Dict[Any, Any]:
    """Stela Embed Loader.

    :param options: StelaOptions instance
    :return: Dict
    """
    from loguru import logger

    # Get toml data
    path = find_pyproject_folder() or Path().cwd()
    filepath = path.joinpath("pyproject.toml")
    toml_data = toml.load(filepath)
    table = options.env_table

    # Get environment layers
    with open(filepath, "r") as file:
        raw_data = file.read()
    pattern = fr"(?<=\[{table}\.)\w+"
    environment_list = re.findall(pattern, raw_data)

    logger.debug(f"Looking for table [{table}] inside pyproject.toml...")
    proxy = Cut(toml_data)
    table_data = proxy.get(options.env_table, {})
    first_level_data = deepcopy(table_data)

    #  remove keys which represent environments in first level
    keys = list(first_level_data.keys())
    for key in keys:
        if key in environment_list:
            del first_level_data[key]

    if options.use_environment_layers:
        sub_table = f"{table}.{options.current_environment}"
        logger.debug(f"Looking for sub-table [{sub_table}] inside pyproject.toml...")
        sub_table = proxy.get(sub_table, {})
        for key in sub_table.keys():
            update_value(sub_table, first_level_data, key)
    return first_level_data
