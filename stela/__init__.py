from stela.stela import Stela
from stela.stela_cut import StelaCut
from stela.stela_options import StelaOptions

settings: StelaCut = Stela(
    stela_options=StelaOptions.get_config()
).get_project_settings()
