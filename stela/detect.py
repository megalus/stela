import os
import re
from os import listdir, path
from typing import Any, Optional

import six

DEFAULT_PATH = "stela"
DEFAULT_ROOT_FILENAME_MATCH_PATTERN = ".git|pyproject\.toml;"


def detect(current_path: Optional[str] = None, pattern: Optional[str] = None) -> Any:
    """Find Project Root.

    Find project root path from specified file/directory path,
    based on common project root file pattern.
    """
    current_path = current_path or os.getcwd()
    current_path = path.abspath(path.normpath(path.expanduser(current_path)))
    pattern = pattern or DEFAULT_ROOT_FILENAME_MATCH_PATTERN

    if not path.isdir(current_path):
        current_path = path.dirname(current_path)

    def find_root_path(current_path, pattern=None):
        if isinstance(pattern, six.string_types):
            pattern = re.compile(pattern)

        detecting = True

        found_more_files = None
        found_root = None
        found_system_root = None

        file_names = None
        root_file_names = None

        while detecting:
            file_names = listdir(current_path)
            found_more_files = bool(len(file_names) > 0)

            if not found_more_files:
                detecting = False

                return None

            root_file_names = filter(pattern.match, file_names)
            root_file_names = list(root_file_names)  # type: ignore

            found_root = bool(len(root_file_names) > 0)

            if found_root:
                detecting = False

                return current_path

            found_system_root = bool(current_path == path.sep)

            if found_system_root:
                return None

            current_path = path.abspath(path.join(current_path, ".."))

    return find_root_path(current_path, pattern)  # type: ignore
