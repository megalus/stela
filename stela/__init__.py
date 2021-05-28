"""Import Stela Data.

If you need to reload data inside you application,
use the stela_reload function.

"""
from loguru import logger

from stela.stela import Stela
from stela.stela_cut import StelaCut
from stela.stela_options import StelaOptions

__version__ = "2.0.9"

_stela_config = StelaOptions.get_config()

try:
    import conf_stela  # noqa
except ImportError:
    pass

settings: StelaCut = Stela(options=_stela_config).get_project_settings()

if not settings.stela_options.show_logs:
    logger.disable("stela")
