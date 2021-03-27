import configparser
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import toml
import yaml


@dataclass
class StelaFileReader:
    options: "StelaOptions"

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
