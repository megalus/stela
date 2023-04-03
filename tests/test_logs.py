import pytest

from stela import settings
from stela.decorators import stela_disable_logs, stela_enable_logs
from stela.utils import read_env


@pytest.mark.parametrize(
    "decorator, expected_log",
    [(stela_enable_logs, "PROJECT_SECRET=my-***ret"), (stela_disable_logs, "")],
)
def test_cut_logs_decorator(caplog, monkeypatch, decorator, expected_log):
    # Arrange
    @decorator
    def get_secret():
        return settings["project.secret"]

    monkeypatch.setenv("PROJECT_SECRET", "my-super-secret")

    # Act
    get_secret()

    # Assert
    assert expected_log in caplog.text


@pytest.mark.parametrize(
    "decorator, expected_log",
    [(stela_enable_logs, "PROJECT_SECRET=my-***ret"), (stela_disable_logs, "")],
)
def test_dot_logs_decorator(caplog, monkeypatch, decorator, expected_log):
    # Arrange
    @decorator
    def get_secret():
        return env.PROJECT_SECRET

    monkeypatch.setenv("STELA_ENV_FILE", ".test-env")
    monkeypatch.setenv("STELA_CONFIG_FILE_PATH", "./tests/fixtures")
    env = read_env()

    # Act
    get_secret()

    # Assert
    assert expected_log in caplog.text
