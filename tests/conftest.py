from importlib import reload

import pytest

import stela
from stela import StelaOptions
from stela.decorators import custom_load, post_load, pre_load
from stela.stela_options import DEFAULT_ORDER
from stela.utils import StelaFileType


@pytest.fixture
def stela_default_settings():
    return {
        "environment_variable_name": "ENVIRONMENT",
        "default_environment": "test",
        "config_file_extension": StelaFileType.INI,
        "config_file_prefix": "",
        "config_file_suffix": "",
        "config_file_path": "./tests/fixtures",
        "environment_prefix": "",
        "environment_suffix": "",
        "evaluate_data": False,
        "show_logs": True,
        "do_not_read_environment": False,
        "do_not_read_dotenv": False,
        "env_file": ".env",
        "load_order": DEFAULT_ORDER,
        "env_table": "environment",
    }


@pytest.fixture()
def json_settings(monkeypatch):
    import stela

    monkeypatch.setenv("STELA_CONFIG_FILE_EXTENSION", "JSON")
    reload(stela)
    yield stela.settings
    monkeypatch.delenv("STELA_CONFIG_FILE_EXTENSION")


@pytest.fixture()
def yaml_settings(monkeypatch):
    import stela

    monkeypatch.setenv("STELA_CONFIG_FILE_EXTENSION", "YAML")
    reload(stela)
    yield stela.settings
    monkeypatch.delenv("STELA_CONFIG_FILE_EXTENSION")


@pytest.fixture()
def dotenv_settings(monkeypatch):
    import stela

    monkeypatch.setenv("STELA_ENV_FILE", ".env.test")
    reload(stela)
    yield stela.settings
    monkeypatch.delenv("STELA_ENV_FILE")


@pytest.fixture()
def dotenv2_settings(monkeypatch):
    import stela

    monkeypatch.setenv("STELA_ENV_FILE", ".env.test2")
    reload(stela)
    yield stela.settings
    monkeypatch.delenv("STELA_ENV_FILE")


@pytest.fixture()
def embed_settings(monkeypatch):
    import stela

    monkeypatch.setenv("STELA_ENV_TABLE", "env")
    monkeypatch.setenv("STELA_USE_ENVIRONMENT_LAYERS", "True")
    reload(stela)
    yield stela.settings
    monkeypatch.delenv("STELA_ENV_TABLE")
    monkeypatch.delenv("STELA_USE_ENVIRONMENT_LAYERS")


@pytest.fixture()
def toml_settings(monkeypatch):

    monkeypatch.setenv("STELA_CONFIG_FILE_EXTENSION", "TOML")
    reload(stela)
    yield stela.settings
    monkeypatch.delenv("STELA_CONFIG_FILE_EXTENSION")


@pytest.fixture()
def options_with_pre_loader():
    reload(stela)

    @pre_load
    def pre_load_test(self, options: StelaOptions):
        return {
            "environment_name": options.environment_variable_name,
            "pre_attribute": True,
        }

    yield
    delattr(StelaOptions, "pre_load")


@pytest.fixture()
def options_with_custom_loader():
    reload(stela)

    @custom_load
    def custom_load_test(self, data: dict, options: StelaOptions):
        return {"evaluate_data": options.evaluate_data, "attribute": True}

    yield
    delattr(StelaOptions, "load")


@pytest.fixture()
def options_with_post_loader():
    reload(stela)

    @post_load
    def post_load_test(self, data: dict, options: StelaOptions):
        return {"environment": options.current_environment, "post_attribute": True}

    yield
    delattr(StelaOptions, "post_load")


@pytest.fixture()
def full_lifecycle(monkeypatch):
    monkeypatch.setenv("STELA_USE_ENVIRONMENT_LAYERS", "True")
    monkeypatch.setenv("STELA_ENV_TABLE", "env")
    monkeypatch.setenv("STELA_ENV_FILE", ".env.test")
    reload(stela)

    @pre_load
    def pre_load_test(self, options: StelaOptions):
        return {
            "secret": "pre_load_secret",
        }

    @custom_load
    def custom_load_test(self, data: dict, options: StelaOptions):
        return {
            "secret": "custom_load_secret",
        }

    @post_load
    def post_load_test(self, data: dict, options: StelaOptions):
        return {
            "secret": "post_load_secret",
        }

    yield
    delattr(StelaOptions, "pre_load")
    delattr(StelaOptions, "load")
    delattr(StelaOptions, "post_load")
    monkeypatch.delenv("STELA_ENV_TABLE")
    monkeypatch.delenv("STELA_ENV_FILE")
    monkeypatch.delenv("STELA_USE_ENVIRONMENT_LAYERS")
