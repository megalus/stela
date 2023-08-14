from typing import List, Tuple, Type
from unittest.mock import MagicMock

import pytest
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

import stela
from stela.helpers.pydantic import StelaConfigSettingsSource, stela_settings


def test_pydantic_helper():
    # Arrange
    settings_mock = MagicMock(__config__=MagicMock())

    # Act
    data = stela_settings(settings=settings_mock)

    # Assert
    assert data == {
        "DEFAULT": {},
        "custom_key": 2,
        "post_key": 3,
        "pre_key": 1,
        "project": {
            "number_of_cats": "1",
            "secret": "post_load_secret",
            "use_scalpl": "true",
        },
        "stele": "merneptah",
    }


def test_pydantic_helper_with_dotenv():
    """Test Pydantic read from dotenv.

    Configuration: in pyproject.toml file on [tool.stela] section.
    Dotenv file: /tests/fixtures/.env-test

    """
    # Arrange

    class TestfromIniSettings(BaseSettings):
        model_config = SettingsConfigDict(extra="ignore")

        foo: str
        secret: str

        @classmethod
        def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
        ) -> Tuple[PydanticBaseSettingsSource, ...]:
            return (
                init_settings,
                StelaConfigSettingsSource(settings_cls),
                file_secret_settings,
            )

    # Act
    settings = TestfromIniSettings()

    # Assert
    assert settings.foo == "BAR"
    assert settings.secret == "dotenv_secret"


@pytest.mark.parametrize(
    "test_settings",
    [
        pytest.lazy_fixture("json_settings"),
        pytest.lazy_fixture("yaml_settings"),
        pytest.lazy_fixture("toml_settings"),
    ],
    ids=["From JSON file", "From YAML file", "From TOML file"],
)
def test_pydantic_helper_from_files(test_settings, mocker):
    # Arrange
    mocker.patch.object(
        stela.helpers.pydantic, "stela_env_settings", return_value=test_settings
    )

    class ProjectSettings(BaseSettings):
        secret: str

    class CatSettings(BaseSettings):
        number: int
        names: List[str]

    class TestfromFileSettings(BaseSettings):
        model_config = SettingsConfigDict(extra="ignore", log_stela_settings=True)

        custom_key: int
        pre_key: int
        post_key: int
        project: ProjectSettings
        stele: str
        cats: CatSettings

        @classmethod
        def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
        ) -> Tuple[PydanticBaseSettingsSource, ...]:
            return (
                init_settings,
                StelaConfigSettingsSource(settings_cls),
                file_secret_settings,
            )

    # Act
    settings = TestfromFileSettings()

    # Assert
    assert settings.custom_key == 2
    assert settings.pre_key == 1
    assert settings.post_key == 3
    assert settings.project.secret == "post_load_secret"
    assert settings.stele == "merneptah"
    assert settings.cats.names == ["garfield", "tabby", "goose"]
    assert settings.cats.number == 3
