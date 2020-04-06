"""Stela Class.

This class run the Stela lifecycle:
   Pre-Load (optional) -> Load or Default Loader -> Post-Load (optional)
"""
import configparser
import json
from pathlib import Path
from typing import Any, Dict

import toml
import yaml

from stela.detect import detect
from stela.exceptions import StelaEnvironmentNotFoundError
from stela.stela_cut import StelaCut
from stela.stela_options import StelaOptions


class Stela:
    """Stela Class."""

    def __init__(self, stela_options: StelaOptions) -> None:
        """Initialize class.

        :param stela_options: StelaOptions instance
        """
        self.options = stela_options

    def default_loader(
        self, data: Dict[Any, Any], options: StelaOptions
    ) -> Dict[Any, Any]:
        """Stela Default Loader.

        :param data: Current data parsed from pre-load
        :param options: StelaOptions instance
        :return: Dict
        """
        from loguru import logger

        path = detect()
        for filename in options.filenames:
            filepath = Path(path).joinpath(self.options.config_file_path, filename)
            logger.debug(f"Looking for file {filepath}...")
            if filepath.exists():
                settings_data = self.load_from_file(filepath)
                data.update(settings_data)
                return data
        return data

    def get_project_settings(self) -> "StelaCut":
        """Get project settings running Stela Lifecycle.

        :return: Dict
        """
        settings_data = {}

        # Run pre_load
        if getattr(self.options, "pre_load", None) is not None:
            pre_load_data = self.options.pre_load(options=self.options)  # type: ignore
            settings_data.update(pre_load_data)

        # Run load or default_load
        if getattr(self.options, "load", None) is not None:
            load_data = self.options.load(data=settings_data, options=self.options)  # type: ignore
        else:
            load_data = self.default_loader(data=settings_data, options=self.options)
        settings_data.update(load_data)

        # Run post_load
        if getattr(self.options, "post_load", None) is not None:
            pre_load_data = self.options.post_load(  # type: ignore
                data=settings_data, options=self.options
            )
            settings_data.update(pre_load_data)

        proxy = StelaCut(settings_data)
        proxy.stela_options = self.options
        return proxy

    @property
    def environment(self) -> str:
        """Return Current Environment."""
        if not self.options.current_environment:
            raise StelaEnvironmentNotFoundError("Environment not found.")
        return self.options.current_environment

    def load_from_file(self, filepath: Path) -> Dict[Any, Any]:
        """Resolve correct function for file extension."""
        function_name = (
            f"load_{self.options.config_file_extension.value[0].replace('.', '')}"
        )
        return getattr(self, function_name)(filepath)  # type: ignore

    def load_ini(self, filepath: Path) -> Dict[Any, Any]:
        """Load INI files.

        :param filepath: Path instance
        :return: Dict
        """
        config = configparser.ConfigParser()
        config.read(filepath)
        ini_settings: Dict[Any, Any] = {}
        for main_key in config.keys():
            ini_settings[main_key] = {}
            for key in config[main_key].keys():
                ini_settings[main_key][key] = config[main_key][key]
        return ini_settings

    def load_yaml(self, filepath: Path) -> Dict[Any, Any]:
        """Load YAML files.

        :param filepath: Path instance
        :return: Dict
        """
        with open(filepath, "r") as yaml_file:
            config = yaml.safe_load(yaml_file)
            return config  # type: ignore

    def load_toml(self, filepath: Path) -> Dict[Any, Any]:
        """Load TOML files.

        :param filepath: Path instance
        :return: Dict
        """
        config = toml.load(filepath)
        return config  # type: ignore

    def load_json(self, filepath: Path) -> Dict[Any, Any]:
        """Load JSON files.

        :param filepath: Path instance
        :return: Dict
        """
        with open(filepath, "r") as json_file:
            config = json.load(json_file)
            return config  # type: ignore
