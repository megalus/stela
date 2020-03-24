import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Optional

import rootpath
import toml

from stela.exceptions import StelaEnvironmentNotFoundError, StelaFileTypeError
from stela.utils import StelaFileType


@dataclass
class StelaOptions:
    environment: Optional[str] = None
    environment_name: str = "ENVIRONMENT"
    config_file_prefix: str = ""
    config_file_suffix: str = ""
    environment_prefix: str = ""
    environment_suffix: str = ""
    config_file_extension: StelaFileType = StelaFileType.INI
    evaluate_data: bool = True
    config_file_path: str = "."
    filenames: List[str] = field(default_factory=list)

    def get_extensions(self) -> List[str]:
        return self.config_file_extension.value

    @classmethod
    def get_from_env_or_settings(cls, key: str, file_settings: dict, default: Any):
        environment_name = f"STELA_{key.upper().replace('.', '_')}"
        return os.getenv(environment_name, file_settings.get(key, default))

    @classmethod
    def get_config(cls) -> "StelaOptions":
        from loguru import logger

        path = rootpath.detect()
        filepath = Path(path).joinpath(f"pyproject.toml")
        logger.debug(f"Looking for file {filepath}")
        if filepath.exists():
            toml_settings = toml.load(filepath)
            file_settings = toml_settings.get("tool", {}).get("stela", {})
        else:
            file_settings = {}
        settings = {
            "environment_name": cls.get_from_env_or_settings(
                "environment_name", file_settings, cls.environment_name
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
        settings["environment"] = os.getenv(settings["environment_name"])
        if not settings["environment"]:
            raise StelaEnvironmentNotFoundError(f"Environment not found")
        settings["filenames"] = [
            f"{settings['config_file_prefix']}{settings['environment']}{extension}"
            for extension in settings["config_file_extension"].value
        ]
        return cls(**settings)
