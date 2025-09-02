import os

from stela.utils import read_env


def test_system_env_overrides_dotenv(monkeypatch) -> None:
    """System environment variables must always override dotenv values.

    Setup uses test fixtures .over-env and .over-env.remote which define
    MY_SECRET in dotenv files. We then set MY_SECRET in memory and expect
    Stela to return the in-memory value, not the dotenv one.
    """

    # Arrange
    monkeypatch.setenv("STELA_DEFAULT_ENVIRONMENT", "remote")
    monkeypatch.setenv("STELA_CONFIG_FILE_PATH", "./tests/fixtures")
    monkeypatch.setenv("STELA_ENV_FILE", ".over-env")
    monkeypatch.setenv("STELA_SHOW_LOGS", "True")

    # Set a new in-memory environment value
    monkeypatch.setenv("MY_SECRET", "from_memory")

    # Make sure MY_SECRET is in the list of forbbiden keys that Stela won't override
    # This simulates that MY_SECRET was already in the environment before Stela read
    # the dotenv files.
    forbidden_keys = os.getenv("_ORIGINAL_ENVIRON_KEYS", "").split(",")
    forbidden_keys.append("MY_SECRET")
    monkeypatch.setenv("_ORIGINAL_ENVIRON_KEYS", ",".join(forbidden_keys))

    # Assert
    assert os.getenv("MY_SECRET") == "from_memory"

    # Act
    env = read_env()

    # Assert: in-memory value must take precedence over dotenv values
    assert os.getenv("MY_SECRET") == "from_memory"
    assert env.MY_SECRET == "from_memory"
