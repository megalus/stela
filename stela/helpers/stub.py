import os
from pathlib import Path

from loguru import logger

STUB_TEMPLATE = """from typing import Any
from .config import StelaOptions
from .main import StelaMain

class Stela:
    _stela_options: StelaOptions
    _stela_data: StelaMain

    current_environment: str
    default_environment: str
    def get(self, var_name: str, raise_on_missing: bool = True) -> Any: ...
    def get_or_default(self, var_name: str, default: Any) -> Any: ...
    def list(self) -> list[str]: ...

    # Dynamic attributes
    {all_envs}


env: Stela

"""

STUB_MODULE = "__init__.pyi"


def create_stela_stub(settings) -> tuple[bool, str]:
    try:
        import stela

        # Get os.environ only for the keys that are in fact environment keys
        filtered_environ = {
            k: v for k, v in os.environ.items() if not k.startswith("_") and k.isupper()
        }

        all_env_info = {**filtered_environ, **settings}

        content = STUB_TEMPLATE.format(
            all_envs="\n    ".join(
                [f"{k}: {type(v).__name__}" for k, v in all_env_info.items()]
            )
        )
        stela_dir = os.path.dirname(os.path.abspath(stela.__file__))
        file_path = Path.cwd().joinpath(stela_dir, STUB_MODULE)
        if not file_path.exists():
            old_content = ""
        else:
            with open(file_path, "r") as f:
                old_content = f.read()
        if old_content != content:
            with open(file_path, "w") as f:
                f.write(content)
                message = f"Updated Stela Stub at: {file_path}"
            logger.success(message)
        else:
            message = f"Stela Stub is up to date at: {file_path}"
            logger.debug(message)
        return True, message
    except Exception as exc:
        message = f"Error while attempt to upsert Stela Stub: {exc}"
        logger.warning(message)
        return False, message
