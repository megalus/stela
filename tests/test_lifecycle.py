from stela import Stela
from stela.utils import stela_reload


def test_default_lifecycle(full_lifecycle, monkeypatch):
    """Test Stela Full Lifecycle.

    Value for key "secret" using default Order:
        1. From pre_load:       "pre_load_secret" (@pre_load function)
        2. From embed table:    "embed_secret" (pyproject.toml)
        3. From config file:    "foo" (test.ini)
        4. From custom loader:  "custom_load_secret" (@custom_load function)
        5. From post_load:      "post_load_secret" (@post_load function)
    """
    test_stela = Stela(options=full_lifecycle)
    test_settings = test_stela.get_project_settings()

    assert test_stela._pre_loader_data["secret"] == "pre_load_secret"
    assert test_stela._embed_data["secret"] == "embed_secret"
    assert test_stela._file_loader_data["app"]["secret"] == "foo"
    assert test_stela._custom_loader_data["secret"] == "custom_load_secret"
    assert test_stela._post_loader_data["secret"] == "post_load_secret"

    # From dotenv file
    assert test_settings["secret"] == "dotenv_secret"

    stela_reload()
    from stela import settings

    assert settings["secret"] == "dotenv_secret"

    monkeypatch.setenv("SECRET", "my_super_secret")
    assert settings["secret"] == "my_super_secret"
    monkeypatch.delenv("SECRET")
    stela_reload()
