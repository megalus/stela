from copy import deepcopy

from stela import StelaOptions
from stela.loaders.embed import read_embed
from stela.loaders.file import read_file


def test_dotenv_loader(dotenv_settings):
    from stela import settings

    # Assert
    assert settings["secret"] == "dotenv_secret"


def test_embed_loader(stela_default_settings, prepare_decorators):
    # Arrange
    options = deepcopy(stela_default_settings)
    options.update(
        {
            "do_not_read_dotenv": True,
            "env_table": "env",
            "use_environment_layers": True,
            "current_environment": "test",
        }
    )
    test_config = StelaOptions(**options)

    # Act
    test_data = read_embed(test_config)

    # Arrange
    assert test_data["project"]["secret"] == "embed_secret"


def test_file_loader(stela_default_settings):
    # Arrange
    test_config = StelaOptions(**stela_default_settings).get_config()

    # Act
    file_name, test_data = read_file(test_config)

    # Assert
    assert file_name == "test.ini"
    assert test_data["project"]["secret"] == "foo"
