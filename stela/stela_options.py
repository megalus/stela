"""Stela Options module."""
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import toml
from loguru import logger

from stela.exceptions import StelaEnvironmentNotFoundError, StelaFileTypeError
from stela.loaders.dotenv import read_dotenv
from stela.utils import StelaFileType, find_file_folder

DEFAULT_ORDER = ["embed", "file", "custom"]


@dataclass
class StelaOptions:
    """Stela Options data class."""

    current_environment: Optional[str] = None
    dotenv_data: Optional[Dict[Any, Any]] = None

    default_environment: Optional[str] = None
    environment_variable_name: str = "ENVIRONMENT"
    config_file_prefix: str = ""
    config_file_suffix: str = ""
    environment_prefix: str = ""
    environment_suffix: str = ""
    config_file_extension: StelaFileType = StelaFileType.INI
    evaluate_data: bool = False
    config_file_path: str = "."
    filenames: List[str] = field(default_factory=list)
    show_logs: bool = False
    log_filtered_value: bool = True
    do_not_read_environment: bool = False
    do_not_read_dotenv: bool = False
    env_file: str = ".env"
    load_order: List[str] = field(default_factory=list)
    env_table: str = "environment"
    use_environment_layers: bool = False
    dotenv_overwrites_memory: bool = True

    def get_extensions(self) -> List[str]:
        """Return file extensions for project configuration files."""
        return self.config_file_extension.value  # type: ignore

    @classmethod
    def get_from_env_or_settings(
        cls, key: str, file_settings: Dict[str, Any], default: Any
    ) -> Any:
        """Get from environment or settings the Stela Option argument.

        :param key: Current stela argument.
        :param file_settings: Stela Data from pyproject.toml.
        :param default: default value for argument.
        :return: Any
        """
        environment_name = f"STELA_{key.upper().replace('.', '_')}"
        value = os.getenv(environment_name, file_settings.get(key, default))
        if value and isinstance(value, str) and isinstance(default, bool):
            return value.lower() == "true"
        return value

    @classmethod
    def get_config(cls) -> "StelaOptions":
        """Get config from pyproject.toml."""

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
        }
        try:
            config_file_extension = cls.get_from_env_or_settings(
                "config_file_extension",
                file_settings,
                cls.config_file_extension.value[0].replace(".", "").upper(),
            )
            settings["config_file_extension"] = StelaFileType[config_file_extension]
        except KeyError:
            raise StelaFileTypeError(
                f"Invalid file type: {file_settings.get('config_file_extension')}"
            )
        cls._get_dotenv_data(settings)
        cls._get_current_environment(settings)
        settings["filenames"] = [
            f"{settings['config_file_prefix']}"
            f"{settings['current_environment']}{extension}"
            for extension in settings["config_file_extension"].value
        ]
        return cls(**settings)

    @classmethod
    def _get_current_environment(cls, settings):
        # Get from Memory
        settings["current_environment"] = os.getenv(
            settings["environment_variable_name"]
        )

        # Get from .env if available
        if not settings["current_environment"]:
            settings["current_environment"] = settings["dotenv_data"].get(
                settings["environment_variable_name"]
            )

        # Get from Default
        if not settings["current_environment"]:
            settings["current_environment"] = settings["default_environment"]

        # No environment found.
        if not settings["current_environment"] and settings["use_environment_layers"]:
            raise StelaEnvironmentNotFoundError("Environment not found.")

        if (
            not settings["current_environment"]
            and not settings["use_environment_layers"]
        ):
            logger.debug(
                f"No Environment found. Stela will lookup only "
                f"in table [{settings['env_table']}] in pyproject.toml"
            )

    @classmethod
    def _get_dotenv_data(cls, settings):
        """Get data from dotenv files."""
        if settings["do_not_read_dotenv"]:
            settings["dotenv_data"] = {}
        else:
            settings["dotenv_data"] = read_dotenv(
                config_file_path=settings["config_file_path"],
                env_file=settings["env_file"],
                overwrites_memory=settings["dotenv_overwrites_memory"],
            )
