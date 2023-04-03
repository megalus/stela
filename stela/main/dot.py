import importlib
import os
from dataclasses import dataclass
from typing import Any, Dict

from loguru import logger

from stela.main import StelaBaseMain
from stela.parsers.dotenv import read_dotenv
from stela.utils import show_value


@dataclass
class StelaDotMain(StelaBaseMain):
    def get_project_settings(self):
        env_data = self.read_env_files()

        module_path = ".".join(self.options.final_loader.split(".")[:-1])
        loader_fn = self.options.final_loader.split(".")[-1]
        module = importlib.import_module(module_path)
        self.settings = getattr(module, loader_fn)(
            options=self.options, env_data=env_data
        )
        logger.debug(
            f"Settings after running loader: "
            f"{[f'{k}={show_value(v, self.options.log_filtered_value)}' for k, v in self.settings.items()]}"
        )

    def read_env_files(self) -> Dict[str, Any]:
        settings = {}
        current_environment = self.options.current_environment
        dotenv_files = [
            self.options.env_file,
            f"{self.options.env_file}.local",
        ]
        if current_environment:
            dotenv_files += [
                f"{self.options.env_file}.{current_environment.lower()}",
                f"{self.options.env_file}.{current_environment.lower()}.local",
            ]
        logger.debug(f"Looking for dotenv files: {dotenv_files}")
        for file in dotenv_files:
            env_settings = read_dotenv(
                config_file_path=self.options.config_file_path,
                env_file=file,
                overwrites_memory=self.options.dotenv_overwrites_memory,
                encoding=self.options.dotenv_encoding,
                verbose=self.options.warn_if_env_is_missing,
                filter_logs=self.options.log_filtered_value,
            )
            for k, v in env_settings.items():
                settings[k] = v
        for k, v in settings.items():
            if k in os.environ and not self.options.dotenv_overwrites_memory:
                continue
            if v is not None:
                os.environ[k] = v
        logger.debug(
            f"Settings after load all dotenv files: "
            f"{[f'{k}={show_value(v, self.options.log_filtered_value)}' for k, v in settings.items()]}"
        )
        return settings
