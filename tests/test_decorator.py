import pytest

from stela import Stela
from stela.stela_options import StelaOptions
from stela.utils import stela_reload


@pytest.mark.parametrize(
    "options, method",
    [
        (pytest.lazy_fixture("options_with_pre_loader"), "pre_load"),
        (pytest.lazy_fixture("options_with_custom_loader"), "load"),
        (pytest.lazy_fixture("options_with_post_loader"), "post_load"),
    ],
    ids=["With Pre-Loader", "With Loader", "With Post-Loader"],
)
def test_decorator_in_options(options, method, stela_default_settings):
    stela_options = StelaOptions(**stela_default_settings)
    assert getattr(stela_options, method) is not None


def test_run_pre_load(stela_default_settings, options_with_pre_loader):
    # Arrange
    stela_options = StelaOptions(**stela_default_settings)
    stela = Stela(options=stela_options)

    # Act
    stela.run_preload()

    # Assert
    assert stela.settings == {
        "environment_name": stela_options.environment_variable_name,
        "pre_attribute": True,
    }

    settings = stela_reload()
    assert settings["app.number_of_cats"] == "1"
    assert settings.get("post_attribute", None) is None
    assert settings["pre_attribute"] is True


def test_run_custom_load(stela_default_settings, options_with_custom_loader):
    # Arrange
    stela_options = StelaOptions(**stela_default_settings)
    stela = Stela(options=stela_options)

    # Act
    stela.run_custom_loader()

    # Assert
    assert stela.settings == {
        "evaluate_data": stela_options.evaluate_data,
        "attribute": True,
    }

    settings = stela_reload()
    assert settings.get("app.number_of_cats", None) == "1"  # INI file
    assert settings.get("post_attribute", None) is None
    assert settings.get("pre_attribute", None) is None
    assert settings["attribute"] is True


def test_run_post_load(stela_default_settings, options_with_post_loader):
    # Arrange
    stela_options = StelaOptions(**stela_default_settings)
    stela = Stela(options=stela_options)

    # Act
    stela.run_postload()

    # Assert
    assert stela.settings == {
        "environment": stela_options.current_environment,
        "post_attribute": True,
    }
    settings = stela_reload()

    assert settings["app.number_of_cats"] == "1"  # INI file
    assert settings.get("pre_attribute", None) is None
    assert settings["post_attribute"] is True
