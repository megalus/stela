"""Stela Utils module."""
from enum import Enum, unique
from importlib import reload
from pathlib import Path
from typing import Optional

from loguru import logger


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


def find_pyproject_folder() -> Optional[Path]:
    """Find pyproject.toml file.

    Look for:
        1. Current working directory up to root
        2. Current file directory up to root


    :return: Optional Path
    """

    def look_for_file(current_path: Path) -> Optional[Path]:
        logger.debug(f"Looking for pyproject.toml in folder: {current_path}")
        if current_path.joinpath("pyproject.toml").exists():
            logger.debug(f"File pyproject.toml found in folder: {current_path}")
            return current_path
        if str(current_path) == Path().root:
            logger.debug("File pyproject.toml not found.")
            return None
        return look_for_file(current_path.parent)

    found_path = look_for_file(Path().cwd())
    if found_path:
        return found_path

    found_path = look_for_file(Path(__file__))
    return found_path
