"""Stela Class."""
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from loguru import logger

from stela.exceptions import StelaEnvironmentNotFoundError
from stela.loaders.embed import read_embed
from stela.loaders.file import read_file
from stela.stela_cut import StelaCut
from stela.stela_options import StelaOptions
from stela.utils import merge_dicts


@dataclass
class Stela:
    """Stela Class."""

    options: StelaOptions
    settings: Dict[Any, Any] = field(default_factory=dict)

    _pre_loader_data: Optional[Dict[Any, Any]] = None
    _embed_data: Optional[Dict[Any, Any]] = None
    _file_loader_data: Optional[Dict[Any, Any]] = None
    _custom_loader_data: Optional[Dict[Any, Any]] = None
    _post_loader_data: Optional[Dict[Any, Any]] = None

    def run_preload(self):
        if getattr(self.options, "pre_load", None) is not None:
            self._pre_loader_data = self.options.pre_load(options=self.options)
            merge_dicts(self._pre_loader_data, self.settings)

    def run_embed_loader(self):
        self._embed_data = read_embed(self.options)
        merge_dicts(self._embed_data, self.settings)

    def run_file_loader(self):
        self._file_loader_data = read_file(self.options)
        merge_dicts(self._file_loader_data, self.settings)

    def run_custom_loader(self):
        if getattr(self.options, "load", None) is not None:
            self._custom_loader_data = self.options.load(
                data=self.settings, options=self.options
            )
            merge_dicts(self._custom_loader_data, self.settings)

    def run_postload(self):
        if getattr(self.options, "post_load", None) is not None:
            self._post_loader_data = self.options.post_load(  # type: ignore
                data=self.settings, options=self.options
            )
            merge_dicts(self._post_loader_data, self.settings)

    def get_project_settings(self) -> "StelaCut":
        """Get project settings running Stela Lifecycle.

        :return: Dict
        """

        # Pre-Load Phase
        logger.debug("Starting Stela Pre-Load Phase...")
        self.run_preload()

        # Load Phase
        logger.debug(
            f"Starting Stela Load Phase. Order is: "
            f"[{', '.join(self.options.load_order)}] ..."
        )
        for loader_name in self.options.load_order:
            getattr(self, f"run_{loader_name}_loader")()

        # Post-Load Phase
        logger.debug("Starting Stela Post-Load Phase...")
        self.run_postload()

        proxy = StelaCut(self.settings)
        proxy.stela_options = self.options
        return proxy

    @property
    def environment(self) -> str:
        """Return Current Environment."""
        if not self.options.current_environment:
            raise StelaEnvironmentNotFoundError("Environment not found.")
        return self.options.current_environment
