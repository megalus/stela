import pytest

from stela.exceptions import StelaValueError


def test_lock_values():
    # Arrange
    from stela import env

    assert env.FOO == "BAR"

    with pytest.raises(StelaValueError):
        # Act / Assert
        env.FOO = "12345"
