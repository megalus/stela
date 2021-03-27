from typing import Any, Dict, Mapping

from stela import StelaOptions, __version__
from stela.decorators import post_load


@post_load
def post_load_test(data: Mapping[Any, Any], options: StelaOptions) -> Dict[Any, Any]:
    return {"stela_version": __version__}
