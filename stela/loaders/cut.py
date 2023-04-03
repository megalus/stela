from typing import Any, Callable, Dict, Optional
from warnings import warn

from stela.exceptions import StelaTooManyLoadersError
from stela.loaders import SingletonMeta

WARN_MESSAGE = "Add Loader is deprecated and will be removed in 6.0. Please use the conf_stela.py file instead."


class StelaCutLoader(metaclass=SingletonMeta):
    """Stela Loader for full lifecycle.

    Will be removed on 6.0

    """

    def __init__(self):
        self.pre_load_function: Optional[Callable] = None
        self.custom_load_function: Optional[Callable] = None
        self.post_load_function: Optional[Callable] = None

        self.pre_data: Optional[Dict[Any, Any]] = None
        self.embed_data: Optional[Dict[Any, Any]] = None
        self.file_data: Optional[Dict[Any, Any]] = None
        self.custom_data: Optional[Dict[Any, Any]] = None
        self.post_data: Optional[Dict[Any, Any]] = None

    def add_pre_loader(self, function: Callable):
        warn(
            WARN_MESSAGE,
            DeprecationWarning,
            stacklevel=2,
        )
        if not self.pre_load_function:
            self.pre_load_function = function
        else:
            raise StelaTooManyLoadersError(
                f"A previous pre-load function was added: {self.pre_load_function.__name__}."
            )

    def add_custom_loader(self, function: Callable):
        warn(
            WARN_MESSAGE,
            DeprecationWarning,
            stacklevel=2,
        )
        if not self.custom_load_function:
            self.custom_load_function = function
        else:
            raise StelaTooManyLoadersError(
                f"A previous custom-load was added {self.custom_load_function.__name__}."
            )

    def add_post_loader(self, function: Callable):
        warn(
            WARN_MESSAGE,
            DeprecationWarning,
            stacklevel=2,
        )
        if not self.post_load_function:
            self.post_load_function = function
        else:
            raise StelaTooManyLoadersError(
                f"A previous post-load was added {self.post_load_function.__name__}."
            )
