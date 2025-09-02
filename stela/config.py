import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from loguru import logger

from stela.exceptions import StelaEnvironmentNotFoundError, StelaFileTypeError
from stela.parsers.dotenv import read_dotenv
from stela.parsers.reader import StelaFileReader
from stela.utils import StelaFileType, find_file_folder


@dataclass
class StelaOptions:
    config_file_extension: StelaFileType = StelaFileType.INI
    env_file: str = ".env"
    log_filtered_value: bool = True
    show_logs: bool = False
    config_file_path: str = "."
    warn_if_env_is_missing: bool = False
    dotenv_encoding: str = "utf-8"
    _dotenv_data: Optional[Dict[Any, Any]] = None
    current_environment: Optional[str] = None
    env_table: str = "environment"
    _filenames: List[str] = field(default_factory=list)
    environment_variable_name: str = "STELA_ENV"
    final_loader: str = "stela.main.default_loader"
    raise_on_missing_variable: bool = True
    evaluate_data: bool = True
    default_environment: Optional[str] = None
    no_env_name: str = "GLOBAL"

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
        normalized_key = key.upper().replace(".", "_")
        if key.startswith("STELA_"):
            environment_name = normalized_key
        else:
            environment_name = f"STELA_{normalized_key}"
        value = os.getenv(environment_name, file_settings.get(key, default))
        if value and isinstance(value, str) and isinstance(default, bool):
            return value.lower() == "true"
        return value

    @classmethod
    def _get_current_environment(cls, settings):
        # Get from Memory
        settings["current_environment"] = os.getenv(
            settings["environment_variable_name"]
        )

        # Get from .env if available
        if not settings["current_environment"]:
            settings["current_environment"] = settings["_dotenv_data"].get(
                settings["environment_variable_name"]
            )

        # Get from Default
        if not settings["current_environment"]:
            settings["current_environment"] = settings["default_environment"]

        # No environment found.
        if not settings["current_environment"] and settings.get(
            "use_environment_layers"
        ):
            raise StelaEnvironmentNotFoundError("Environment not found.")

    @classmethod
    def _get_dotenv_data(cls, settings, update_environs: bool):
        """Get data from dotenv files."""
        settings["_dotenv_data"] = {}
        if not settings.get("do_not_read_dotenv"):
            files = [
                settings["env_file"],
                f"{settings['env_file']}.local",
            ]
            if (
                settings.get("default_environment")
                and settings["default_environment"] != "GLOBAL"
            ):
                files += [
                    f"{settings['env_file']}.{settings['default_environment'].lower()}",
                    f"{settings['env_file']}.{settings['default_environment'].lower()}.local",
                ]
            for file in files:
                settings["_dotenv_data"] |= read_dotenv(
                    config_file_path=settings["config_file_path"],
                    env_file=file,
                    overwrites_memory=True,
                    encoding=settings["dotenv_encoding"],
                    verbose=settings["warn_if_env_is_missing"],
                    update_environs=update_environs,
                    show_logs=settings["show_logs"],
                    filter_logs=settings["log_filtered_value"],
                )
            # Filter dict for keys which start with "STELA_"
            settings["_dotenv_data"] = {
                k: v
                for k, v in settings["_dotenv_data"].items()
                if k.startswith("STELA_")
            }

    def get_extensions(self) -> List[str]:
        """Return file extensions for project configuration files."""
        return self.config_file_extension.value  # type: ignore

    @classmethod
    def get_config(cls) -> "StelaOptions":
        """Get config from pyproject.toml."""

        file_settings, settings = cls.get_settings()
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
        cls._get_dotenv_data(settings, update_environs=False)
        cls._get_current_environment(settings)
        settings["_filenames"] = [
            f"{settings.get('config_file_prefix', '')}{settings['current_environment']}{extension}"
            for extension in settings["config_file_extension"].value
        ]
        return cls(**settings)

    @classmethod
    def get_settings(cls):
        file_settings = {}
        reader = StelaFileReader()
        toml_path = find_file_folder("pyproject.toml")
        if toml_path:
            toml_settings = reader.load_toml(toml_path.joinpath("pyproject.toml"))
            file_settings = toml_settings.get("tool", {}).get("stela", {})
            if file_settings:
                logger.info("Using pyproject.toml for stela settings.")
        if not file_settings:
            ini_path = find_file_folder(".stela")
            if ini_path:
                ini_settings = reader.load_ini(ini_path.joinpath(".stela"))
                file_settings = ini_settings.get("stela", {})
                if file_settings:
                    logger.info("Using .stela for stela settings.")
        if not file_settings:
            logger.info(
                "No stela file configuration found. Using default stela settings."
            )
        settings = {
            "environment_variable_name": cls.get_from_env_or_settings(
                "environment_variable_name",
                file_settings,
                cls.environment_variable_name,
            ),
            "default_environment": cls.get_from_env_or_settings(
                "default_environment", file_settings, cls.default_environment
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
            "env_file": cls.get_from_env_or_settings(
                "env_file", file_settings, cls.env_file
            ),
            "warn_if_env_is_missing": cls.get_from_env_or_settings(
                "warn_if_env_is_missing", file_settings, cls.warn_if_env_is_missing
            ),
            "dotenv_encoding": cls.get_from_env_or_settings(
                "dotenv_encoding", file_settings, cls.dotenv_encoding
            ),
            "final_loader": cls.get_from_env_or_settings(
                "final_loader", file_settings, cls.final_loader
            ),
            "raise_on_missing_variable": cls.get_from_env_or_settings(
                "raise_on_missing_variable",
                file_settings,
                cls.raise_on_missing_variable,
            ),
            "no_env_name": cls.get_from_env_or_settings(
                "no_env_name", file_settings, cls.no_env_name
            ),
        }
        return file_settings, settings
