from stela import Stela, StelaOptions


def test_dotenv_loader(dotenv_settings):
    # Assert
    assert dotenv_settings.to_dict == {
        "DEFAULT": {},
        "app": {"number_of_cats": "1", "secret": "foo", "use_scalpl": "true"},
    }
    assert dotenv_settings["secret"] == "dotenv_secret"


def test_embed_loader(embed_settings):
    # Assert
    assert embed_settings.to_dict == {
        "DEFAULT": {},
        "shared_attribute": "foo.bar",
        "secret": "embed_secret",
        "app": {"number_of_cats": "1", "secret": "foo", "use_scalpl": "true"},
    }


def test_file_loader(stela_default_settings):
    # Arrange
    test_config = StelaOptions(**stela_default_settings).get_config()

    # Act
    test_settings = Stela(options=test_config).get_project_settings()

    # Assert
    assert test_settings.to_dict == {
        "DEFAULT": {},
        "app": {"number_of_cats": "1", "secret": "foo", "use_scalpl": "true"},
    }
