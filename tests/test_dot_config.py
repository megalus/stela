from stela.utils import read_env


def test_evaluated_value_from_env_file(monkeypatch):
    # Arrange
    monkeypatch.setenv("STELA_CONFIG_FILE_PATH", "./tests/fixtures")
    monkeypatch.setenv("STELA_ENV_FILE", ".test-env")
    monkeypatch.setenv("STELA_EVALUATE_DATA", True)
    monkeypatch.setenv("STELA_SHOW_LOGS", True)

    # Act
    env = read_env()

    # Assert
    assert env.APP_NUMBER_OF_CATS == 10


def test_get_current_environment(monkeypatch):
    # Arrange
    monkeypatch.setenv("STELA_CONFIG_FILE_PATH", "./tests/fixtures")
    monkeypatch.setenv("STELA_ENV", "test")

    # Act
    env = read_env()

    # Assert
    assert env.current_environment == "test"
    assert env.SECRET == "dotenv_secret"


def test_dotenv_overwrite_memory(monkeypatch):
    # Arrange
    monkeypatch.setenv("STELA_CONFIG_FILE_PATH", "./tests/fixtures")
    monkeypatch.setenv("STELA_ENV_FILE", ".test-env")

    # Act
    env = read_env()

    # Assert
    assert env.PROJECT_SECRET == "my-super-secret"

    # Act
    monkeypatch.setenv("STELA_DOTENV_OVERWRITES_MEMORY", False)
    monkeypatch.setenv("PROJECT_SECRET", "secret_in_memory")
    env = read_env()

    # Assert
    assert env.PROJECT_SECRET == "secret_in_memory"
