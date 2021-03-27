from pathlib import Path
from typing import Any, Dict

from stela.stela_file_reader import StelaFileReader
from stela.utils import find_pyproject_folder


def read_file(options: "StelaOptions") -> Dict[Any, Any]:
    """Stela File Loader.

    :param options: StelaOptions instance
    :return: Dict
    """
    from loguru import logger

    path = find_pyproject_folder() or Path().cwd()
    reader = StelaFileReader(options)
    settings_data = {}
    for filename in options.filenames:
        filepath = path.joinpath(options.config_file_path, filename)
        logger.debug(f"Looking for file {filepath}...")
        if filepath.exists():
            settings_data = reader.load_from_file(filepath)
    return settings_data
