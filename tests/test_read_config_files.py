import pytest

from stela import stela_reload


def test_get_from_ini_file():
    settings = stela_reload()

    assert settings.to_dict == {
        "DEFAULT": {},
        "app": {"use_scalpl": "true", "secret": "foo", "number_of_cats": "1"},
    }
    assert settings["app.number_of_cats"] == "1"


def test_evaluated_value_from_ini_file(monkeypatch):
    monkeypatch.setenv("APP_NUMBER_OF_CATS", 10)
    monkeypatch.setenv("STELA_EVALUATE_DATA", True)
    settings = stela_reload()

    assert settings["app.number_of_cats"] == 10


@pytest.mark.parametrize(
    "settings",
    [
        pytest.lazy_fixture("json_settings"),
        pytest.lazy_fixture("yaml_settings"),
        pytest.lazy_fixture("toml_settings"),
    ],
    ids=["From JSON file", "From YAML file", "From TOML file"],
)
def test_get_from_config_file(settings):
    assert settings.to_dict == {
        "cats": {"number": 3, "names": ["garfield", "tabby", "goose"]}
    }
    assert settings["cats.names[0]"] == "garfield"


@pytest.mark.parametrize(
    "settings",
    [
        pytest.lazy_fixture("json_settings"),
        pytest.lazy_fixture("yaml_settings"),
        pytest.lazy_fixture("toml_settings"),
    ],
    ids=["From JSON file", "From YAML file", "From TOML file"],
)
def test_evaluated_value_from_environment(settings, monkeypatch):
    monkeypatch.setenv("STELA_EVALUATE_DATA", True)
    monkeypatch.setenv("CAT_NAMES", "['Mr. Bigglesworth','Grumpy Cat']")
    settings = stela_reload()
    assert settings["cat.names"] == ["Mr. Bigglesworth", "Grumpy Cat"]
    assert settings.get("cat.names") == ["Mr. Bigglesworth", "Grumpy Cat"]


def test_do_not_read_from_environment(monkeypatch):
    monkeypatch.setenv("STELA_DO_NOT_READ_ENVIRONMENT", True)
    monkeypatch.setenv("NUMBER_OF_CATS", "10")
    settings = stela_reload()
    assert settings["app.number_of_cats"] == "1"
