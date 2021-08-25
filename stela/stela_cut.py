"""Stela Cut subclass.

Based on Scalpl project: https://github.com/ducdetronquito/scalpl

"""
import os
from ast import literal_eval
from typing import Any, Dict, Optional, Tuple

from scalpl import Cut
from scalpl.scalpl import index_error, key_error, split_path, traverse, type_error

from stela.utils import show_value


class FakeNone:
    """Fake None for Stela Cut.

    Resolves StelaCut.cut() and StelaCut.pop()
    issues when default=None.
    See: https://github.com/ducdetronquito/scalpl/issues/16
    """

    pass


class StelaCut(Cut):  # type: ignore
    """StelaCut subclass."""

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
                            f"Error when evaluating value: "
                            f"{environment_variable}={value[:3]}***"
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
