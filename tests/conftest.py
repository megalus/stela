from importlib import reload

import pytest

import stela
from stela import StelaOptions
from stela.stela_options import DEFAULT_ORDER
from stela.utils import StelaFileType


@pytest.fixture
def stela_default_settings():
    return {
        "environment_variable_name": "ENVIRONMENT",
        "default_environment": "test",
        "current_environment": "test",
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
        "filenames": ["test.ini"],
        "use_environment_layers": True,
        "dotenv_overwrites_memory": True,
    }


@pytest.fixture()
def json_settings(monkeypatch):
    import stela

    monkeypatch.setenv("STELA_CONFIG_FILE_EXTENSION", "JSON")
    reload(stela)
    yield stela.settings
    monkeypatch.delenv("STELA_CONFIG_FILE_EXTENSION")
    reload(stela)


@pytest.fixture()
def yaml_settings(monkeypatch):
    import stela

    monkeypatch.setenv("STELA_CONFIG_FILE_EXTENSION", "YAML")
    reload(stela)
    yield stela.settings
    monkeypatch.delenv("STELA_CONFIG_FILE_EXTENSION")
    reload(stela)


@pytest.fixture()
def dotenv_settings(monkeypatch):
    import stela

    monkeypatch.setenv("STELA_ENV_FILE", ".env.test")
    reload(stela)
    yield stela.settings
    monkeypatch.delenv("STELA_ENV_FILE")
    reload(stela)


@pytest.fixture()
def dotenv2_settings(monkeypatch):
    import stela

    monkeypatch.setenv("STELA_ENV_FILE", ".env.test2")
    reload(stela)
    yield stela.settings
    monkeypatch.delenv("STELA_ENV_FILE")
    reload(stela)


@pytest.fixture()
def embed_settings(monkeypatch):
    import stela

    monkeypatch.setenv("STELA_ENV_TABLE", "env")
    monkeypatch.setenv("STELA_USE_ENVIRONMENT_LAYERS", True)
    monkeypatch.setenv("STELA_DO_NOT_READ_DOTENV", True)
    reload(stela)
    yield stela.settings
    monkeypatch.delenv("STELA_ENV_TABLE")
    monkeypatch.delenv("STELA_USE_ENVIRONMENT_LAYERS")
    monkeypatch.delenv("STELA_DO_NOT_READ_DOTENV")
    reload(stela)


@pytest.fixture()
def toml_settings(monkeypatch):

    monkeypatch.setenv("STELA_CONFIG_FILE_EXTENSION", "TOML")
    reload(stela)
    yield stela.settings
    monkeypatch.delenv("STELA_CONFIG_FILE_EXTENSION")
    reload(stela)


@pytest.fixture()
def options_with_pre_loader(stela_default_settings) -> StelaOptions:
    def pre_load_test(options: StelaOptions):
        return {
            "environment_name": options.environment_variable_name,
            "pre_attribute": True,
        }

    stela_options = StelaOptions(**stela_default_settings)
    setattr(stela_options, "pre_load", pre_load_test)

    yield stela_options


@pytest.fixture()
def options_with_custom_loader(stela_default_settings):
    def custom_load_test(data: dict, options: StelaOptions):
        return {"evaluate_data": options.evaluate_data, "attribute": True}

    stela_options = StelaOptions(**stela_default_settings)
    setattr(stela_options, "load", custom_load_test)

    yield stela_options


@pytest.fixture()
def full_lifecycle(monkeypatch, stela_default_settings):
    monkeypatch.setenv("STELA_USE_ENVIRONMENT_LAYERS", "True")
    monkeypatch.setenv("STELA_ENV_TABLE", "env")
    monkeypatch.setenv("STELA_ENV_FILE", ".env.test")

    def pre_load_test(options: StelaOptions):
        return {
            "secret": "pre_load_secret",
        }

    def custom_load_test(data: dict, options: StelaOptions):
        return {
            "secret": "custom_load_secret",
        }

    def post_load_test(data: dict, options: StelaOptions):
        return {
            "secret": "post_load_secret",
        }

    stela_options = StelaOptions().get_config()
    setattr(stela_options, "pre_load", pre_load_test)
    setattr(stela_options, "load", custom_load_test)
    setattr(stela_options, "post_load", post_load_test)

    yield stela_options

    monkeypatch.delenv("STELA_ENV_TABLE")
    monkeypatch.delenv("STELA_ENV_FILE")
    monkeypatch.delenv("STELA_USE_ENVIRONMENT_LAYERS")
    reload(stela)
