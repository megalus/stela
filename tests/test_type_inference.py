from typing import Any

import pytest

from stela.utils import read_env


def test_type_inference_from_dotenv(monkeypatch: Any) -> None:
    """Ensure dotenv values are parsed into correct Python types.

    This test uses a temporary dotenv file name within tests/fixtures and
    points Stela to that directory so we don't affect other tests.
    It validates int, bool, float, list and dict parsing just like the
    example shown in the docs and dev.to article.
    """
    # Arrange: point to fixtures and use a dedicated env filename
    monkeypatch.setenv("STELA_CONFIG_FILE_PATH", "./tests/fixtures")
    monkeypatch.setenv("STELA_ENV_FILE", ".types-env")
    monkeypatch.setenv("STELA_SHOW_LOGS", "True")

    # Act
    env = read_env()

    # Assert: types
    assert isinstance(env.PORT, int)
    assert isinstance(env.DEBUG, bool)
    assert isinstance(env.RETRY_TIMES, int)
    assert isinstance(env.PI, float)
    assert isinstance(env.FEATURES, list)
    assert isinstance(env.EXTRA_SETTINGS, dict)

    # Assert: values (basic spot checks)
    assert env.PORT == 8000
    assert env.DEBUG is True
    assert env.RETRY_TIMES == 3
    assert env.PI == 3.14159
    assert env.FEATURES == ["search", "login", "signup"]
    assert env.EXTRA_SETTINGS == {"cache": True, "timeout": 30}


@pytest.mark.parametrize(
    "raw_value, expected",
    [
        ("[123, 456]", [123, 456]),
        ("['a', 'b']", ["a", "b"]),
        ('["123", 456]', ["123", 456]),
    ],
)
def test_type_inference_list_variants(
    raw_value: str, expected: list, monkeypatch
) -> None:
    # Arrange
    monkeypatch.setenv("TEST_LIST_VALUE", raw_value)

    # Act
    env = read_env()

    # Assert
    assert isinstance(env.TEST_LIST_VALUE, list)
    assert env.TEST_LIST_VALUE == expected
