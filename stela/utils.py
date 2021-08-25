"""Stela Utils module."""
from enum import Enum, unique
from importlib import reload
from pathlib import Path
from typing import Any, Dict, Optional


@unique
class StelaFileType(Enum):
    """Available formats for configuration files."""

    INI = [".ini"]
    JSON = [".json"]
    YAML = [".yaml", ".yml"]
    TOML = [".toml"]
    ENV = [".env"]


def stela_reload() -> "StelaCut":  # type: ignore
    """Reload Stela configuration.

    This helper will import again stela module
    to update settings.

    """
    import stela

    reload(stela)
    return stela.settings


def find_file_folder(file_name: str) -> Optional[Path]:
    """Find base folder for named file.

    For pyproject.toml and conf_stela.py files.

    Look for:
        1. Current working directory up to root
        2. Current file directory up to root


    :return: Optional Path
    """

    def look_for_file(current_path: Path) -> Optional[Path]:
        if current_path.joinpath(file_name).exists():
            return current_path
        if str(current_path) in ["/", "\\"] or current_path.parent == current_path:
            return None
        return look_for_file(current_path.parent)

    found_path = look_for_file(Path().cwd())
    if found_path:
        return found_path

    found_path = look_for_file(Path(__file__))
    return found_path


def merge_dicts(source_dict: Dict[Any, Any], target_dict: Dict[Any, Any]) -> None:
    """Merge source dictionary into target.

    Example:
        # from pyproject.toml

        [environment]
        test = true
        project.foo = "bar"
        project.x = "a"

        [environment.local]
        project.bar = "foo"
        project.x = "b"
        project.db.name = "test"

    Expected data for ENVIRONMENT=local:
        settings.to_dict = {
            "test": True,
            "project": {
                "foo": "bar,
                "project": {
                    "x": "b"
                },
                "bar": "foo",
                "db": {
                    "name": "test"
                },
            }
        }
    :param source_dict: The Source dictionary
    :param target_dict: The Target dictionary, which will me merged
    :current_key: Current Source Dictionary Key
    """

    def _merge_dicts(source, target, current_key):
        if isinstance(source[current_key], dict):
            if not target.get(current_key):
                target[current_key] = {}
            for k in source[current_key]:
                if not target[current_key].get(k):
                    target[current_key][k] = {}
                _merge_dicts(source[current_key], target[current_key], k)
        else:
            target[current_key] = source[current_key]

    for key in source_dict.keys():
        _merge_dicts(source_dict, target_dict, key)


def show_value(value: str, filter_values: bool) -> str:
    """Shows dictionary value as plain text or filtered.

    For filtered values with less than 3 characters
    *** will be printed.

    """
    value = str(value)
    if filter_values:
        if len(value) < 4:
            return "***"
        visible_chars = min(int(len(value) / 3), 3)
        value = f"{value[:visible_chars]}***{value[-visible_chars:]}"
    return value
