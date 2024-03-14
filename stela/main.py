import importlib
import os
from dataclasses import dataclass, field

from loguru import logger

from stela.config import StelaOptions
from stela.exceptions import StelaEnvironmentNotFoundError
from stela.parsers.dotenv import read_dotenv
from stela.utils import show_value


@dataclass
class StelaMain:
    options: StelaOptions
    settings: dict[str, any] = field(default_factory=dict)

    def log_current_data(self, origin: str) -> None:
        def log_dict(dict_key: str, dict_value: any, parents: list):
            if isinstance(dict_value, dict):
                for k, v in dict_value.items():
                    if dict_key not in parents:
                        parents.append(dict_key)
                    log_dict(k, v, parents)
            else:
                parents_key = (
                    parents + [dict_key] if dict_key not in parents else parents
                )
                logger.debug(
                    f"[{origin}] {'.'.join(parents_key)} = "
                    f"{show_value(dict_value, self.options.log_filtered_value)}"
                )

        for key, value in self.settings.items():
            log_dict(key, value, [])

    @property
    def environment(self) -> str:
        """Return Current Environment."""
        if not self.options.current_environment:
            raise StelaEnvironmentNotFoundError("Environment not found.")
        return self.options.current_environment

    def get_project_settings(self):
        env_data = self.read_env_files()

        module_path = ".".join(self.options.final_loader.split(".")[:-1])
        loader_fn = self.options.final_loader.split(".")[-1]
        module = importlib.import_module(module_path)
        self.settings = getattr(module, loader_fn)(
            options=self.options, env_data=env_data
        )
        for k, v in self.settings.items():
            if k in os.environ and v is not None:
                os.environ[k] = v
        logger.debug(
            f"Settings after running loader: "
            f"{[f'{k}={show_value(v, self.options.log_filtered_value)}' for k, v in self.settings.items()]}"
        )

    def read_env_files(self) -> dict[str, any]:
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
                overwrites_memory=True,
                encoding=self.options.dotenv_encoding,
                verbose=self.options.warn_if_env_is_missing,
                filter_logs=self.options.log_filtered_value,
            )
            settings |= env_settings
        for k, v in settings.items():
            if k in os.environ and v is not None:
                os.environ[k] = v
        logger.debug(
            f"Settings after load all dotenv files: "
            f"{[f'{k}={show_value(v, self.options.log_filtered_value)}' for k, v in settings.items()]}"
        )
        return settings


def default_loader(options: StelaOptions, env_data: dict[str, any]) -> dict[str, any]:
    """Stela Default Loader.

    :param options: Stela Options
    :param env_data: Dict with environment data
    :return: Dict
    """
    from loguru import logger

    logger.info(
        f"Using Stela Default Loader. Current environment is: {options.current_environment}"
    )
    return env_data
