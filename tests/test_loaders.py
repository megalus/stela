from copy import deepcopy

from stela import Stela, StelaOptions


def test_dotenv_loader(dotenv_settings):
    # Assert
    assert dotenv_settings.to_dict == {
        "DEFAULT": {},
        "app": {"number_of_cats": "1", "secret": "foo", "use_scalpl": "true"},
    }
    assert dotenv_settings["secret"] == "dotenv_secret"


def test_embed_loader(stela_default_settings):
    options = deepcopy(stela_default_settings)
    options.update(
        {
            "do_not_read_dotenv": True,
            "env_table": "env",
            "use_environment_layers": True,
            "current_environment": "test",
        }
    )
    # Arrange
    test_config = StelaOptions(**options)

    # Act
    test_settings = Stela(options=test_config).get_project_settings()

    # Arrange
    assert test_settings["project.secret"] == "embed_secret"


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
