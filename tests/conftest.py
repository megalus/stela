from importlib import reload

import pytest

import stela
from stela import StelaOptions
from stela.decorators import load, post_load, pre_load
from stela.utils import StelaFileType


@pytest.fixture
def stela_default_settings():
    return {
        "environment_name": "ENVIRONMENT",
        "config_file_extension": StelaFileType.INI,
        "config_file_prefix": "",
        "config_file_path": "./tests/fixtures",
        "environment_prefix": "",
        "evaluate_data": True,
    }


@pytest.fixture()
def json_settings(monkeypatch):
    import stela

    monkeypatch.setenv("STELA_CONFIG_FILE_EXTENSION", "JSON")
    reload(stela)
    from stela import settings

    return settings


@pytest.fixture()
def yaml_settings(monkeypatch):
    import stela

    monkeypatch.setenv("STELA_CONFIG_FILE_EXTENSION", "YAML")
    reload(stela)
    from stela import settings

    return settings


@pytest.fixture()
def toml_settings(monkeypatch):

    monkeypatch.setenv("STELA_CONFIG_FILE_EXTENSION", "TOML")
    reload(stela)
    from stela import settings

    return settings


@pytest.fixture()
def options_with_pre_loader():
    reload(stela)

    @pre_load
    def pre_load_test(self, options: StelaOptions):
        return {"environment_name": options.environment_name, "pre_attribute": True}

    yield
    delattr(StelaOptions, "pre_load")


@pytest.fixture()
def options_with_loader():
    reload(stela)

    @load
    def post_load_test(self, data: dict, options: StelaOptions):
        return {"evaluate_data": options.evaluate_data, "attribute": True}

    yield
    delattr(StelaOptions, "load")


@pytest.fixture()
def options_with_post_loader():
    reload(stela)

    @post_load
    def post_load_test(self, data: dict, options: StelaOptions):
        return {"environment": options.environment, "post_attribute": True}

    yield
    delattr(StelaOptions, "post_load")
