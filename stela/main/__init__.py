from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from loguru import logger

from stela.config import StelaOptions
from stela.config.cut import StelaCutOptions
from stela.exceptions import StelaEnvironmentNotFoundError
from stela.loaders.cut import StelaCutLoader
from stela.utils import show_value


@dataclass
class StelaBaseMain:
    options: Union[StelaCutOptions, StelaOptions]
    loader: Optional[StelaCutLoader] = None
    settings: Dict[Any, Any] = field(default_factory=dict)

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

    @property
    def environment(self) -> str:
        """Return Current Environment."""
        if not self.options.current_environment:
            raise StelaEnvironmentNotFoundError("Environment not found.")
        return self.options.current_environment

    @abstractmethod
    def get_project_settings(self):
        """Get project settings running Stela Lifecycle.

        :return: Dict
        """
