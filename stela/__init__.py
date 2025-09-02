"""Import Stela Data.

If you need to reload data inside you application,
use the stela_reload function.

"""

import os
from ast import literal_eval
from typing import Any, List

from loguru import logger

from stela.config import StelaOptions
from stela.exceptions import StelaValueError
from stela.helpers.stub import create_stela_stub
from stela.main import StelaMain
from stela.utils import show_value

__version__ = "8.0.7"


def _get_stela() -> "Stela":
    stela_config = StelaOptions.get_config()

    stela_data = StelaMain(options=stela_config)
    stela_data.get_project_settings()

    # Enable or disable logs based on configuration
    # after the data is loaded
    if stela_config.show_logs:
        logger.enable("stela")
    else:
        logger.info("Disabling Stela logs.")
        logger.disable("stela")

    class Stela:
        __slots__ = (
            ["_locked"] + [str(k) for k in stela_data.settings.keys()]
            if stela_data.settings.keys()
            else ["_locked"]
        )
        _stela_options: StelaOptions = stela_config
        _stela_data: StelaMain = stela_data

        def _get_attributes(self, current_obj: object, data_dict: dict):
            for attr, value in data_dict.items():
                if isinstance(value, dict):

                    class StelaNestedObj:
                        __slots__ = [str(k) for k in value.keys()]

                    nested_obj = StelaNestedObj()
                    self._get_attributes(current_obj=nested_obj, data_dict=value)
                    setattr(current_obj, attr, nested_obj)
                else:
                    current_value = value
                    if stela_config.evaluate_data:
                        try:
                            current_value = literal_eval(current_value)
                        except Exception:
                            logger.debug(f"Can't eval value for: {attr}")
                    setattr(current_obj, attr, current_value)

        @property
        def current_environment(self):
            return (
                self._stela_options.current_environment
                or self._stela_options.no_env_name
            )

        @property
        def default_environment(self):
            return (
                self._stela_options.default_environment
                or self._stela_options.no_env_name
            )

        def __init__(self, *args, **kwargs):
            self._locked = False
            super().__init__(*args, **kwargs)

            self._get_attributes(current_obj=self, data_dict=stela_data.settings)

        def lock(self):
            self._locked = True

        def __getattribute__(self, item):
            # return from os.environ if exists
            if item in os.environ:
                value = os.environ[item]
                logger.debug(
                    f"Using environment value: {item}={show_value(value, stela_config.log_filtered_value)}"
                )
                return value
            try:
                value = super().__getattribute__(item)
                if not item.startswith("_"):
                    logger.debug(
                        f"Using stela value: {item}={show_value(value, stela_config.log_filtered_value)}"
                    )
                return value
            except AttributeError as exc:
                if stela_config.raise_on_missing_variable:
                    raise StelaValueError(
                        f"Stela did not found value for {item}."
                    ) from exc
                logger.warning(f"Stela did not found value for {item}. Returning None.")
                return None

        def __setattr__(self, key, value):
            if key in self.__slots__ and hasattr(self, key):
                if key != "_locked" and self._locked:
                    raise StelaValueError(f"Attribute {key} is ready-only.")
            super().__setattr__(key, value)

        def get(self, var_name: str, raise_on_missing: bool = True):
            if raise_on_missing:
                try:
                    return getattr(self, var_name)
                except AttributeError as exc:
                    raise StelaValueError(
                        f"Stela did not found value for {var_name}."
                    ) from exc
            return getattr(self, var_name, None)

        def get_or_default(self, var_name: str, default: Any):
            return getattr(self, var_name, default)

        def list(self) -> List[str]:
            return [k for k in self._stela_data.settings.keys()]

    create_stela_stub(stela_data.settings)

    stela = Stela()
    stela.lock()
    return stela


env = _get_stela()
