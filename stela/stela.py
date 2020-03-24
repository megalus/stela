import configparser
import json
from pathlib import Path

import rootpath
import toml
import yaml

from stela.exceptions import StelaEnvironmentNotFoundError
from stela.stela_cut import StelaCut
from stela.stela_options import StelaOptions


class Stela:
    def __init__(self, stela_options: StelaOptions):
        self.options = stela_options

    def default_loader(self, data, options):
        from loguru import logger

        path = rootpath.detect()
        for filename in options.filenames:
            filepath = Path(path).joinpath(self.options.config_file_path, filename)
            logger.debug(f"Looking for file {filepath}...")
            if filepath.exists():
                settings_data = self.load_from_file(filepath)
                data.update(settings_data)
                return data
        return data

    def get_project_settings(self) -> "StelaCut":

        settings_data = {}

        # Run pre_load
        if getattr(self.options, "pre_load", None) is not None:
            pre_load_data = self.options.pre_load(options=self.options)
            settings_data.update(pre_load_data)

        # Run load or default_load
        if getattr(self.options, "load", None) is not None:
            load_data = self.options.load(data=settings_data, options=self.options)
        else:
            load_data = self.default_loader(data=settings_data, options=self.options)
        settings_data.update(load_data)

        # Run post_load
        if getattr(self.options, "post_load", None) is not None:
            pre_load_data = self.options.post_load(
                data=settings_data, options=self.options
            )
            settings_data.update(pre_load_data)

        proxy = StelaCut(settings_data)
        proxy.stela_options = self.options
        return proxy

    @property
    def environment(self):
        if not self.options.environment:
            raise StelaEnvironmentNotFoundError("Environment not found.")
        return self.options.environment

    def load_from_file(self, filepath):
        function_name = (
            f"load_{self.options.config_file_extension.value[0].replace('.', '')}"
        )
        return getattr(self, function_name)(filepath)

    def load_ini(self, filepath):
        config = configparser.ConfigParser()
        config.read(filepath)
        ini_settings = {}
        for main_key in config.keys():
            ini_settings[main_key] = {}
            for key in config[main_key].keys():
                ini_settings[main_key][key] = config[main_key][key]
        return ini_settings

    def load_yaml(self, filepath):
        with open(filepath, "r") as yaml_file:
            config = yaml.safe_load(yaml_file)
            return config

    def load_toml(self, filepath):
        config = toml.load(filepath)
        return config

    def load_json(self, filepath):
        with open(filepath, "r") as json_file:
            config = json.load(json_file)
            return config
