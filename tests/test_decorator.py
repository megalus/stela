from stela import Stela, __version__


def test_run_pre_load(stela_default_settings, options_with_pre_loader):
    # Arrange
    stela = Stela(options=options_with_pre_loader)

    # Act
    stela.run_preload()

    # Assert
    assert stela.settings == {
        "environment_name": stela.options.environment_variable_name,
        "pre_attribute": True,
    }


def test_run_custom_load(stela_default_settings, options_with_custom_loader):
    # Arrange
    stela = Stela(options=options_with_custom_loader)

    # Act
    stela.run_custom_loader()

    # Assert
    assert stela.settings == {
        "evaluate_data": stela.options.evaluate_data,
        "attribute": True,
    }


def test_run_post_load():
    # Arrange
    from stela import settings

    # Assert
    assert settings["stela_version"] == __version__
