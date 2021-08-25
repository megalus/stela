from stela.utils import stela_reload


def test_different_environments(monkeypatch, embed_settings):
    """Test reload Stela data from different environments."""

    """Scenario 1: Read from environment table, in pyproject.toml. """

    # Act
    from stela import settings

    # Assert
    assert settings.stela_options.current_environment == "test"
    assert settings["api_timeout"] == 60

    """Scenario 2: Read from environment subtable, in pyproject.toml. """

    # Arrange
    monkeypatch.setenv("ENVIRONMENT", "production")
    stela_reload()

    # Act
    from stela import settings

    # Assert
    assert settings.stela_options.current_environment == "production"
    assert settings["api_timeout"] == 10

    """Scenario 3: Read from environment variable. """

    # Arrange
    monkeypatch.setenv("API_TIMEOUT", "30")
    monkeypatch.setenv("STELA_EVALUATE_DATA", "true")
    stela_reload()

    # Act
    from stela import settings

    # Assert
    assert settings.stela_options.current_environment == "production"
    assert settings["api_timeout"] == 30
