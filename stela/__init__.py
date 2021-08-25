"""Import Stela Data.

If you need to reload data inside you application,
use the stela_reload function.

"""

from loguru import logger

from stela.stela import Stela
from stela.stela_cut import StelaCut
from stela.stela_options import StelaOptions

__version__ = "3.0.1"


def get_stela() -> Stela:
    stela_config = StelaOptions.get_config()

    try:
        import conf_stela  # noqa
    except ImportError:
        pass

    if stela_config.show_logs:
        logger.enable("stela")
    else:
        logger.disable("stela")

    stela = Stela(options=stela_config)

    return stela


settings: StelaCut = get_stela().get_project_settings()
