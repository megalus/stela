from stela.utils import read_env


def test_multiple_envs(monkeypatch):
    # Arrange
    monkeypatch.setenv("STELA_DEFAULT_ENVIRONMENT", "remote")
    monkeypatch.setenv("STELA_CONFIG_FILE_PATH", "./tests/fixtures")
    monkeypatch.setenv("STELA_ENV_FILE", ".over-env")
    monkeypatch.setenv("STELA_SHOW_LOGS", True)

    # Act
    env = read_env()

    # Assert
    assert env.current_environment == "remote"
    assert env.MY_SECRET == "override"
