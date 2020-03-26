"""Stela Utils module."""
from enum import Enum, unique
from importlib import reload


@unique
class StelaFileType(Enum):
    """Available formats for configuration files."""

    INI = [".ini"]
    JSON = [".json"]
    YAML = [".yaml", ".yml"]
    TOML = [".toml"]


def stela_reload() -> "StelaCut":  # type: ignore
    """Reload Stela configuration.

    This helper will import again stela module
    to update settings.

    """
    import stela

    reload(stela)
    return stela.settings
