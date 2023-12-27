from typing import Any, Dict, Tuple

from loguru import logger
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

from stela.utils import read_env


def stela_env_settings(settings: BaseSettings) -> dict[str, Any]:
    """
    Read Stela Data from many dotenv files.
    """

    delimiter = settings.config.get("env_nested_delimiter") or ""
    log_settings = settings.config.get("env_nested_delimiter") or False

    # Ask Stela to read envs as per his configuration
    env = read_env()

    if delimiter:
        data = {
            ".".join(var.split(delimiter)).lower(): env.get(var) for var in env.list()
        }
    else:
        data = {var.lower(): env.get(var) for var in env.list()}

    if log_settings:
        logger.debug(f"Stela settings dict are: {data}")

    return data


class StelaConfigSettingsSource(PydanticBaseSettingsSource):
    """
    Stela Config Settings Source.
    """

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> Tuple[Any, str, bool]:
        stela_data = stela_env_settings(self)
        field_value = stela_data.get(field_name)
        return field_value, field_name, False

    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        return value

    def __call__(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(
                field, field_name
            )
            field_value = self.prepare_field_value(
                field_name, field, field_value, value_is_complex
            )
            if field_value is not None:
                d[field_key] = field_value

        return d
