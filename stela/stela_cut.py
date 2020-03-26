"""Stela Cut subclass.

Based on Scalpl project: https://github.com/ducdetronquito/scalpl

"""
import os
from ast import literal_eval
from typing import Any, Dict, Optional, Tuple

from scalpl import Cut
from scalpl.scalpl import index_error, key_error


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
    def to_dict(self) -> Dict[Any, Any]:
        """Return Cut as Python Dictionary.

        When thinking on Scalpl context, its fair to
        convert data from Cut to dict.

        But in Stela, the main context is to use the full
        path key to investigate possible environment variables
        before returning the combined keys' value.

        For example, suppose we have:
        APP = "my project" and
        APP_SECRET = "bar"

        Our dictionary:
        {
            "app": {
                "secret": "foo"
                }
            }
        }

        Retrieving settings["app.secret"] can reach both values (dict and env) correctly.
        Retrieving settings["app"] correct gives us the env value.

        But if you're looking only at the Dict, determine both
        environment variables can be tricky.

        We suggest use this property for dictionary-only contexts
        or for tests.
        """
        return dict(self)

    def get(self, path: str, default: Optional[Any] = FakeNone) -> Any:
        """Override Get from Dict code."""
        try:
            return self[path]
        except (KeyError, IndexError) as error:
            if default is not FakeNone:
                return default
            raise error

    def pop(self, path: str, default: Any = FakeNone) -> Any:
        """Oveerride Pop from Dict code."""
        parent, last_key = self._traverse(self.data, path)
        try:
            return parent.pop(last_key)
        except IndexError as error:
            if default is not FakeNone:
                return default
            raise index_error(last_key, path, error)
        except (AttributeError, KeyError) as error:
            if default is not FakeNone:
                return default
            raise key_error(last_key, path, error)

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
        if not "[" in path and not self.stela_options.do_not_read_environment:
            environment_variable = (
                f"{self.stela_options.environment_prefix}"
                f"{path.replace('.', '_')}"
                f"{self.stela_options.environment_suffix}".upper()
            )
            value = os.getenv(environment_variable)
            if value:
                from loguru import logger

                logger.debug(f"Using value from variable {environment_variable}")
                if self.stela_options.evaluate_data:
                    try:
                        value = literal_eval(value)
                    except:
                        pass
                return value

        parent, last_key = self._traverse(self.data, path)

        try:
            return parent[last_key]
        except KeyError as error:
            raise key_error(last_key, path, error)
        except IndexError as error:
            raise index_error(last_key, path, error)
