import pytest

from stela.decorators import custom_load, post_load, pre_load
from stela.utils import stela_reload


@pytest.mark.parametrize(
    "decorator, value",
    [(pre_load, "pre_value"), (custom_load, "custom_value"), (post_load, "post_value")],
)
def test_decorators(decorator, value, prepare_decorators):
    # Arrange
    @decorator
    def decorator_for_unit_test(*args, **kwargs):
        return {
            f"{pre_load.__name__}": value,
        }

    stela_reload()

    # Act
    from stela import settings

    # Assert
    assert settings[f"{pre_load.__name__}"] == value
