import configparser
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Tuple

import toml
import yaml

from stela.utils import get_base_path


@dataclass
class StelaFileReader:
    """Read other files to load settings.

    Will be removed on 6.0
    """

    def load_from_file(self, filepath: Path, options: "StelaOptions") -> Dict[Any, Any]:
        """Resolve correct function for file extension."""
        function_name = (
            f"load_{options.config_file_extension.value[0].replace('.', '')}"
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


def read_file(options: "StelaCutOptions") -> Tuple[str, Dict[Any, Any]]:
    """Stela File Loader.

    Will be removed on 6.0

    :param options: StelaOptions instance
    :return: Dict
    """
    from loguru import logger

    path = get_base_path()
    reader = StelaFileReader()
    settings_data = {}
    file_name = ""
    for filename in options._filenames:
        filepath = path.joinpath(options.config_file_path, filename)
        if filepath.exists():
            logger.info(f"Reading file {filepath}...")
            settings_data = reader.load_from_file(filepath, options)
            file_name = "multiple-files" if len(options._filenames) > 1 else filename
    return file_name, settings_data
