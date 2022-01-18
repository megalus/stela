"""Import Stela Data.

If you need to reload data inside you application,
use the stela_reload function.

"""

from loguru import logger

from stela.stela import Stela
from stela.stela_cut import StelaCut
from stela.stela_options import StelaOptions

__version__ = "4.0.0"

from stela.utils import find_file_folder


def get_stela() -> Stela:
    stela_config = StelaOptions.get_config()

    conf_path = find_file_folder("conf_stela.py")
    if conf_path:
        logger.debug(f"Found conf_stela.py at: {conf_path} - Importing data...")
        import conf_stela  # noqa

    if stela_config.show_logs:
        logger.enable("stela")
    else:
        logger.disable("stela")

    stela = Stela(options=stela_config)

    return stela


settings: StelaCut = get_stela().get_project_settings()
