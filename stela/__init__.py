"""Import Stela Data.

If you need to reload data inside you application,
use the stela_reload function.

"""
from loguru import logger

from stela.stela import Stela
from stela.stela_cut import StelaCut
from stela.stela_options import StelaOptions
from stela.utils import stela_reload

settings: StelaCut = Stela(
    stela_options=StelaOptions.get_config()
).get_project_settings()

if not settings.stela_options.show_logs:
    logger.disable("stela")
