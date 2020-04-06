"""Stela Options module."""
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import toml

from stela.exceptions import StelaEnvironmentNotFoundError, StelaFileTypeError
from stela.utils import StelaFileType, find_pyproject_folder


@dataclass
class StelaOptions:
    """Stela Options data class."""

    current_environment: Optional[str] = None
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
    show_logs: bool = True
    do_not_read_environment: bool = False

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
        return os.getenv(environment_name, file_settings.get(key, default))

    @classmethod
    def get_config(cls) -> "StelaOptions":
        """Get config from pyproject.toml."""

        file_settings = {}
        path = find_pyproject_folder()
        if path:
            filepath = path.joinpath(f"pyproject.toml")
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
            "evaluate_data": bool(
                cls.get_from_env_or_settings(
                    "evaluate_data", file_settings, cls.evaluate_data
                )
            ),
            "config_file_path": cls.get_from_env_or_settings(
                "config_file_path", file_settings, cls.config_file_path
            ),
            "show_logs": cls.get_from_env_or_settings(
                "show_logs", file_settings, cls.show_logs
            ),
            "do_not_read_environment": cls.get_from_env_or_settings(
                "do_not_read_environment", file_settings, cls.do_not_read_environment
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
        settings["current_environment"] = os.getenv(
            settings["environment_variable_name"]
        )
        if not settings["current_environment"]:
            settings["current_environment"] = settings["default_environment"]
        if not settings["current_environment"]:
            raise StelaEnvironmentNotFoundError(f"Environment not found")
        settings["filenames"] = [
            f"{settings['config_file_prefix']}{settings['current_environment']}{extension}"
            for extension in settings["config_file_extension"].value
        ]
        return cls(**settings)
