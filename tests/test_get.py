import pytest

from stela.exceptions import StelaValueError


def test_return_none_on_missing_var():
    # Arrange
    from stela import env

    # Act / Assert
    with pytest.raises(StelaValueError):
        _ = env.MISSING_VAR

    # Act
    value = env.get("MISSING_VAR", raise_on_missing=False)

    # Assert
    assert value is None


def test_return_default_value_on_missing_var():
    # Arrange
    from stela import env

    # Act / Assert
    with pytest.raises(StelaValueError):
        _ = env.MISSING_VAR

    # Act
    value = env.get_or_default("MISSING_VAR", default="default")

    # Assert
    assert value == "default"
