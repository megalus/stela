from stela.stela_options import StelaOptions
from stela.utils import stela_reload


def test_get_default_config(stela_default_settings, monkeypatch):
    monkeypatch.delenv("STELA_CONFIG_FILE_EXTENSION", raising=False)
    stela_reload()
    stela_config = StelaOptions.get_config()
    assert (
        stela_config.environment_variable_name
        == stela_default_settings["environment_variable_name"]
    )
    assert (
        stela_config.config_file_extension.value
        == stela_default_settings["config_file_extension"].value
    )
    assert (
        stela_config.config_file_prefix == stela_default_settings["config_file_prefix"]
    )
    assert (
        stela_config.environment_prefix == stela_default_settings["environment_prefix"]
    )
    assert stela_config.evaluate_data == stela_default_settings["evaluate_data"]
    assert stela_config.config_file_path == stela_default_settings["config_file_path"]
    assert (
        stela_config.do_not_read_environment
        == stela_default_settings["do_not_read_environment"]
    )
    assert stela_config.show_logs == stela_default_settings["show_logs"]


def test_different_environments(monkeypatch):
    from stela import settings

    assert settings.stela_options.current_environment == "test"

    monkeypatch.setenv("ENVIRONMENT", "production")
    settings = stela_reload()
    assert settings.stela_options.current_environment == "production"
    monkeypatch.delenv("ENVIRONMENT")


def test_get_environment_from_env(dotenv2_settings, monkeypatch):
    # From .env
    assert dotenv2_settings.stela_options.current_environment == "homolog"

    # From Environment
    monkeypatch.setenv("ENVIRONMENT", "staging")
    settings = stela_reload()
    assert settings.stela_options.current_environment == "staging"
