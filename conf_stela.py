from typing import Any, Dict, Mapping

from stela import StelaOptions
from stela.decorators import custom_load, post_load, pre_load


@pre_load
def pre_load_test(options: StelaOptions) -> Dict[Any, Any]:
    return {"stele": "rosetta", "project": {"secret": "pre_load_secret"}, "pre_key": 1}


@custom_load
def custom_load_test(data: Mapping[Any, Any], options: StelaOptions) -> Dict[Any, Any]:
    return {
        "stele": "code of hammurabi",
        "project": {"secret": "custom_load_secret"},
        "custom_key": 2,
    }


@post_load
def post_load_test(data: Mapping[Any, Any], options: StelaOptions) -> Dict[Any, Any]:
    return {
        "stele": "merneptah",
        "project": {"secret": "post_load_secret"},
        "post_key": 3,
    }
