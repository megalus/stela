"""Stela Class."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from loguru import logger

from stela.exceptions import StelaEnvironmentNotFoundError
from stela.loaders.embed import read_embed
from stela.loaders.file import read_file
from stela.stela_cut import StelaCut
from stela.stela_loader import StelaLoader
from stela.stela_options import StelaOptions
from stela.utils import merge_dicts, show_value


@dataclass
class Stela:
    """Stela Class."""

    options: StelaOptions
    loader: Optional[StelaLoader] = None
    settings: Dict[Any, Any] = field(default_factory=dict)

    def run_embed_loader(self):
        self.loader.embed_data = read_embed(self.options)
        merge_dicts(self.loader.embed_data, self.settings)
        return "pyproject.toml"

    def run_file_loader(self):
        origin, self.loader.file_data = read_file(self.options)
        merge_dicts(self.loader.file_data, self.settings)
        return origin

    def run_custom_loader(self):
        from stela.stela_loader import StelaLoader

        loader = StelaLoader()
        if loader.custom_load_function:
            loader.custom_data = loader.custom_load_function(
                data=self.settings, options=self.options
            )
            merge_dicts(loader.custom_data, self.settings)
            return loader.custom_load_function.__name__

    def get_project_settings(self) -> "StelaCut":
        """Get project settings running Stela Lifecycle.

        :return: Dict
        """

        self.loader = StelaLoader()

        # Pre-Load Phase
        logger.info("Starting Stela Pre-Load Phase...")
        if self.loader.pre_load_function:
            self.loader.pre_data = self.loader.pre_load_function(options=self.options)
            merge_dicts(self.loader.pre_data, self.settings)
            self.log_current_data(origin=self.loader.pre_load_function.__name__)

        # Load Phase
        logger.info(
            f"Starting Stela Load Phase. Order is: "
            f"[{', '.join(self.options.load_order)}] ..."
        )
        for loader_name in self.options.load_order:
            origin = getattr(self, f"run_{loader_name}_loader")()
            if origin:
                self.log_current_data(origin=origin)

        # Post-Load Phase
        logger.info("Starting Stela Post-Load Phase...")
        if self.loader.post_load_function:
            self.loader.post_data = self.loader.post_load_function(
                data=self.settings, options=self.options
            )
            merge_dicts(self.loader.post_data, self.settings)
            self.log_current_data(origin=self.loader.post_load_function.__name__)

        proxy = StelaCut(self.settings)
        proxy.stela_options = self.options
        proxy.stela_loader = self.loader
        return proxy

    @property
    def environment(self) -> str:
        """Return Current Environment."""
        if not self.options.current_environment:
            raise StelaEnvironmentNotFoundError("Environment not found.")
        return self.options.current_environment

    def log_current_data(self, origin: str) -> None:
        def log_dict(dict_key: Any, dict_value: Any, parents: List):
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
