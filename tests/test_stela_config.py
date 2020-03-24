from stela.stela_options import StelaOptions


def test_get_default_config(stela_default_settings, monkeypatch):
    monkeypatch.delenv("STELA_CONFIG_FILE_EXTENSION", raising=False)
    stela_config = StelaOptions.get_config()
    assert stela_config.environment_name == stela_default_settings["environment_name"]
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
