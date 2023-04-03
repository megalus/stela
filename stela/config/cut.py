"""Stela Options module."""
from dataclasses import dataclass, field
from typing import List

import toml

from stela.config import DEFAULT_ORDER, StelaBaseOptions
from stela.utils import find_file_folder


@dataclass
class StelaCutOptions(StelaBaseOptions):
    """Stela Options data class for Cut class.

    Will be removed on 6.0
    """

    environment_variable_name: str = "ENVIRONMENT"

    do_not_read_dotenv: bool = False
    load_order: List[str] = field(default_factory=list)
    use_environment_layers: bool = False
    do_not_read_environment: bool = False
    environment_suffix: str = ""
    environment_prefix: str = ""
    config_file_prefix: str = ""
    config_file_suffix: str = ""

    @classmethod
    def get_settings(cls):
        file_settings = {}
        path = find_file_folder("pyproject.toml")
        if path:
            filepath = path.joinpath("pyproject.toml")
            toml_settings = toml.load(filepath)
            file_settings = toml_settings.get("tool", {}).get("stela", {})
        settings = {
            "environment_variable_name": cls.get_from_env_or_settings(
                "environment_variable_name",
                file_settings,
                cls.environment_variable_name,
            ),
            "default_environment": cls.get_from_env_or_settings(
                "default_environment", file_settings, cls.default_environment
            ),
            "config_file_prefix": cls.get_from_env_or_settings(
                "config_file_prefix", file_settings, cls.config_file_prefix
            ),
            "config_file_suffix": cls.get_from_env_or_settings(
                "config_file_suffix", file_settings, cls.config_file_suffix
            ),
            "environment_prefix": cls.get_from_env_or_settings(
                "environment_prefix", file_settings, cls.environment_prefix
            ),
            "environment_suffix": cls.get_from_env_or_settings(
                "environment_suffix", file_settings, cls.environment_suffix
            ),
            "evaluate_data": cls.get_from_env_or_settings(
                "evaluate_data", file_settings, cls.evaluate_data
            ),
            "config_file_path": cls.get_from_env_or_settings(
                "config_file_path", file_settings, cls.config_file_path
            ),
            "show_logs": cls.get_from_env_or_settings(
                "show_logs", file_settings, cls.show_logs
            ),
            "log_filtered_value": cls.get_from_env_or_settings(
                "log_filtered_value",
                file_settings,
                cls.log_filtered_value,
            ),
            "do_not_read_environment": cls.get_from_env_or_settings(
                "do_not_read_environment",
                file_settings,
                cls.do_not_read_environment,
            ),
            "do_not_read_dotenv": cls.get_from_env_or_settings(
                "do_not_read_dotenv",
                file_settings,
                cls.do_not_read_dotenv,
            ),
            "env_file": cls.get_from_env_or_settings(
                "env_file", file_settings, cls.env_file
            ),
            "load_order": cls.get_from_env_or_settings(
                "load_order", file_settings, DEFAULT_ORDER
            ),
            "env_table": cls.get_from_env_or_settings(
                "env_table", file_settings, cls.env_table
            ),
            "use_environment_layers": cls.get_from_env_or_settings(
                "use_environment_layers", file_settings, cls.use_environment_layers
            ),
            "dotenv_overwrites_memory": cls.get_from_env_or_settings(
                "dotenv_overwrites_memory", file_settings, cls.dotenv_overwrites_memory
            ),
            "warn_if_env_is_missing": cls.get_from_env_or_settings(
                "warn_if_env_is_missing", file_settings, cls.warn_if_env_is_missing
            ),
            "dotenv_encoding": cls.get_from_env_or_settings(
                "dotenv_encoding", file_settings, cls.dotenv_encoding
            ),
        }
        return file_settings, settings
