from pathlib import Path
from typing import Any, Dict, Tuple

from stela.stela_file_reader import StelaFileReader
from stela.utils import find_file_folder


def read_file(options: "StelaOptions") -> Tuple[str, Dict[Any, Any]]:
    """Stela File Loader.

    :param options: StelaOptions instance
    :return: Dict
    """
    from loguru import logger

    path = find_file_folder("pyproject.toml") or Path().cwd()
    reader = StelaFileReader(options)
    settings_data = {}
    file_name = ""
    for filename in options.filenames:
        filepath = path.joinpath(options.config_file_path, filename)
        if filepath.exists():
            logger.info(f"Reading file {filepath}...")
            settings_data = reader.load_from_file(filepath)
            file_name = "multiple-files" if len(options.filenames) > 1 else filename
    return file_name, settings_data
