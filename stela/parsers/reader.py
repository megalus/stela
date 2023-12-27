import configparser
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import toml


@dataclass
class StelaFileReader:
    """Read other files to load settings.

    Will be removed on 6.0
    """

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

    def load_toml(self, filepath: Path) -> Dict[Any, Any]:
        """Load TOML files.

        :param filepath: Path instance
        :return: Dict
        """
        config = toml.load(filepath)
        return config  # type: ignore
