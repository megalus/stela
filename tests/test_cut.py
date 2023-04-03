import copy

from stela.utils import stela_reload


def test_pop(monkeypatch):
    # Arrange
    monkeypatch.setenv("STELA_DO_NOT_READ_ENVIRONMENT", True)
    settings = stela_reload()

    # Act
    test_settings = copy.deepcopy(settings)
    test_settings.pop("project.secret")

    # Assert
    assert test_settings.get("project.secret", None) is None
    assert test_settings.get("project") == {"number_of_cats": "1", "use_scalpl": "true"}


def test_pop_non_existent(stela_default_settings):
    from stela import settings

    test_settings = copy.deepcopy(settings)
    test_settings.pop("app.secret.wrong", None)
