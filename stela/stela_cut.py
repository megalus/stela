import os
from ast import literal_eval
from typing import Any, Optional

from scalpl import Cut
from scalpl.scalpl import index_error, key_error


class FakeNone:
    pass


class StelaCut(Cut):
    @property
    def stela_options(self) -> "StelaOptions":
        return self._options

    @stela_options.setter
    def stela_options(self, options: "StelaOptions"):
        self._options = options

    @property
    def to_dict(self):
        return dict(self)

    def get(self, path: str, default: Optional[Any] = FakeNone) -> Any:
        try:
            return self[path]
        except (KeyError, IndexError) as error:
            if default is not FakeNone:
                return default
            raise error

    def pop(self, path: str, default: Any = FakeNone) -> Any:
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

    def __getitem__(self, path, *args, **kwargs) -> Any:
        if not "[" in path:
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
