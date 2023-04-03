"""Stela Class."""
import os
from ast import literal_eval
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

from _warnings import warn
from loguru import logger
from scalpl import Cut
from scalpl.scalpl import index_error, key_error, split_path, traverse, type_error

from stela.loaders.cut import StelaCutLoader
from stela.main import StelaBaseMain
from stela.parsers.embed import read_embed
from stela.parsers.other_files import read_file
from stela.utils import merge_dicts, show_value


class FakeNone:
    """Fake None for Stela Cut.

    Resolves StelaCut.cut() and StelaCut.pop()
    issues when default=None.
    See: https://github.com/ducdetronquito/scalpl/issues/16
    """


class StelaCut(Cut):  # type: ignore
    """StelaCut subclass."""

    def __init__(self, data: Optional[dict] = None, sep: str = "."):
        super().__init__(data, sep)
        self._options = None
        self._loader = None

    @property
    def stela_options(self) -> "StelaOptions":  # type: ignore
        """Return Stela Options."""
        return self._options

    @stela_options.setter
    def stela_options(self, options: "StelaOptions"):  # type: ignore
        """Save Stela Options in instance."""
        self._options = options

    @property
    def stela_loader(self) -> "StelaLoader":  # type: ignore
        """Return Stela Loader."""
        return self._loader

    @stela_loader.setter
    def stela_loader(self, loader: "StelaLoader"):  # type: ignore
        """Save Stela Loader in instance."""
        self._loader = loader

    @property
    def stela_current_environment(self) -> str:
        """Return Current Environment."""
        return self._options.current_environment

    @property
    def to_dict(self) -> Dict[Any, Any]:
        """Return Cut as Python Dictionary."""
        return dict(self)

    def get(self, path: str, default: Optional[Any] = FakeNone) -> Any:
        """Override Get from Dict code."""
        try:
            return self[path]
        except (KeyError, IndexError) as error:
            if default is not FakeNone:
                return default
            raise error

    def pop(self, path: str, default: Any = FakeNone, *args) -> Any:  # type: ignore
        """Override Pop from Dict code."""
        *keys, last_key = split_path(path, self.sep)

        try:
            item = traverse(data=self.data, keys=keys, original_path=path)
        except (KeyError, IndexError) as error:
            if default is not FakeNone:
                return default
            raise error

        try:
            return item.pop(last_key)
        except (AttributeError, KeyError) as error:
            if default is not FakeNone:
                return default
            raise key_error(last_key, path, error)
        except IndexError as error:
            if default is not FakeNone:
                return default
            raise index_error(last_key, path, error)

    def __getitem__(
        self, path: str, *args: Tuple[Any], **kwargs: Dict[Any, Any]
    ) -> Any:
        """Override getitem from Dict.

        Before invoking  original code, we will
        use the full path received to check for
        a environment variable value, using StelaOptions
        options.

        :param path: full dict path
        :param args: python arguments
        :param kwargs: python keyword arguments
        :return: Any
        """

        warn(
            "Using Stela as Dictionary is deprecated and will be removed in 6.0",
            DeprecationWarning,
            stacklevel=2,
        )

        if "[" not in path:
            environment_variable = self.get_environment_variable_name(path)
            value = self.get_value_from_memory(environment_variable)
            if value:
                if self.stela_options.evaluate_data:
                    try:
                        value = literal_eval(value)
                    except ValueError:
                        from loguru import logger

                        logger.debug(
                            f"Error when evaluating value: {environment_variable}={value[:3]}***"
                        )
                return value

        *keys, last_key = split_path(path, self.sep)
        item = traverse(data=self.data, keys=keys, original_path=path)

        try:
            return item[last_key]
        except KeyError as error:
            raise key_error(last_key, path, error)
        except IndexError as error:
            raise index_error(last_key, path, error)
        except TypeError:
            raise type_error(last_key, path, item)

    def get_value_from_memory(self, environment_variable):
        from loguru import logger

        if (
            self.stela_options.do_not_read_environment
            and environment_variable != self.stela_options.environment_variable_name
        ):
            logger.debug("Ignoring Environment variables in memory.")
            return

        value = os.getenv(environment_variable)
        if value:
            logger.debug(
                f"Using environment value: {environment_variable}="
                f"{show_value(value, self.stela_options.log_filtered_value)}"
            )
        return value

    def get_environment_variable_name(self, path):
        environment_variable = (
            f"{self.stela_options.environment_prefix}"
            f"{path.replace('.', '_')}"
            f"{self.stela_options.environment_suffix}".upper().strip()
        )
        return environment_variable


@dataclass
class StelaCutMain(StelaBaseMain):
    """Stela Cut Main Class.

    Will be removed on 6.0
    """

    def run_embed_loader(self):
        self.loader.embed_data = read_embed(self.options)
        merge_dicts(self.loader.embed_data, self.settings)
        return "pyproject.toml"

    def run_file_loader(self):
        origin, self.loader.file_data = read_file(self.options)
        merge_dicts(self.loader.file_data, self.settings)
        return origin

    def run_custom_loader(self):
        from stela.loaders.cut import StelaCutLoader

        loader = StelaCutLoader()
        if loader.custom_load_function:
            loader.custom_data = loader.custom_load_function(
                data=self.settings, options=self.options
            )
            merge_dicts(loader.custom_data, self.settings)
            return loader.custom_load_function.__name__

    def get_project_settings(self) -> StelaCut:
        """Get project settings running Stela Lifecycle.

        :return: Dict
        """

        self.loader = StelaCutLoader()

        # Pre-Load Phase
        logger.info("Starting Stela Pre-Load Phase...")
        if self.loader.pre_load_function:
            self.loader.pre_data = self.loader.pre_load_function(options=self.options)
            merge_dicts(self.loader.pre_data, self.settings)
            self.log_current_data(origin=self.loader.pre_load_function.__name__)

        # Load Phase
        logger.info(
            f"Starting Stela Load Phase. Order is: [{', '.join(self.options.load_order)}] ..."
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
