import logging
from importlib import reload

import pytest
from _pytest.logging import caplog as _caplog  # noqa
from loguru import logger

import stela
from stela.stela_options import DEFAULT_ORDER
from stela.utils import StelaFileType, stela_reload


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
        "show_logs": False,
        "log_filtered_value": True,
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


@pytest.fixture()
def yaml_settings(monkeypatch):
    import stela

    monkeypatch.setenv("STELA_CONFIG_FILE_EXTENSION", "YAML")
    reload(stela)
    yield stela.settings


@pytest.fixture()
def dotenv_settings(monkeypatch):
    import stela

    monkeypatch.setenv("STELA_ENV_FILE", ".env.test")
    reload(stela)
    yield


@pytest.fixture()
def dotenv2_settings(monkeypatch):
    import stela

    monkeypatch.setenv("STELA_ENV_FILE", ".env.test2")
    reload(stela)
    yield stela.settings


@pytest.fixture()
def embed_settings(monkeypatch):
    import stela

    monkeypatch.setenv("STELA_ENV_TABLE", "env")
    monkeypatch.setenv("STELA_USE_ENVIRONMENT_LAYERS", True)
    monkeypatch.setenv("STELA_DO_NOT_READ_DOTENV", True)
    reload(stela)
    yield stela.settings


@pytest.fixture()
def env_settings(monkeypatch):
    import stela

    monkeypatch.setenv("STELA_ENV_TABLE", "env")
    monkeypatch.setenv("STELA_USE_ENVIRONMENT_LAYERS", True)
    reload(stela)
    yield stela.settings


@pytest.fixture()
def toml_settings(monkeypatch):

    monkeypatch.setenv("STELA_CONFIG_FILE_EXTENSION", "TOML")
    reload(stela)
    yield stela.settings


@pytest.fixture()
def full_lifecycle(monkeypatch, stela_default_settings):
    monkeypatch.setenv("STELA_USE_ENVIRONMENT_LAYERS", "True")
    monkeypatch.setenv("STELA_ENV_TABLE", "env")
    monkeypatch.setenv("STELA_ENV_FILE", ".env.test")
    monkeypatch.setenv("STELA_SHOW_LOGS", "true")
    monkeypatch.setenv("STELA_LOG_FILTERED_VALUE", "False")
    stela_reload()
    yield


@pytest.fixture()
def prepare_decorators():
    from stela.stela_loader import StelaLoader

    loader = StelaLoader()
    old_pre_loader = loader.pre_load_function
    old_custom_loader = loader.custom_load_function
    old_post_loader = loader.post_load_function
    old_pre_data = loader.pre_data
    old_custom_data = loader.custom_data
    old_post_data = loader.post_data

    loader.pre_load_function = None
    loader.custom_load_function = None
    loader.post_load_function = None
    loader.pre_data = None
    loader.custom_data = None
    loader.post_data = None

    yield

    loader.pre_load_function = old_pre_loader
    loader.custom_load_function = old_custom_loader
    loader.post_load_function = old_post_loader
    loader.pre_data = old_pre_data
    loader.custom_data = old_custom_data
    loader.post_data = old_post_data


@pytest.fixture
def caplog(_caplog):  # noqa
    class PropogateHandler(logging.Handler):
        def emit(self, record):
            logging.getLogger(record.name).handle(record)

    logger.add(PropogateHandler(), format="{message}")
    yield _caplog
