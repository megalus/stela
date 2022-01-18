from typing import Tuple, List
from unittest.mock import MagicMock

import pytest
from pydantic import BaseSettings, Extra
from pydantic.env_settings import SettingsSourceCallable

from stela.pydantic import stela_settings


def test_pydantic_helper(mocker):
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


def test_pydantic_helper_with_ini_files():
    # Arrange
    class ProjectSettings(BaseSettings):
        number_of_cats: int
        secret: str
        use_scalpl: bool

    class TestfromIniSettings(BaseSettings):
        custom_key: int
        pre_key: int
        post_key: int
        project: ProjectSettings
        stele: str

        class Config:
            extra = Extra.ignore

            @classmethod
            def customise_sources(
                cls,
                init_settings: SettingsSourceCallable,
                env_settings: SettingsSourceCallable,
                file_secret_settings: SettingsSourceCallable,
            ) -> Tuple[SettingsSourceCallable, ...]:
                return (
                    init_settings,
                    stela_settings,
                    env_settings,
                    file_secret_settings,
                )

    # Act
    settings = TestfromIniSettings()

    # Assert
    assert settings.custom_key == 2
    assert settings.pre_key == 1
    assert settings.post_key == 3
    assert settings.project.number_of_cats == 1
    assert settings.project.secret == "post_load_secret"
    assert settings.project.use_scalpl is True
    assert settings.stele == "merneptah"


@pytest.mark.parametrize(
    "test_settings",
    [
        pytest.lazy_fixture("json_settings"),
        pytest.lazy_fixture("yaml_settings"),
        pytest.lazy_fixture("toml_settings"),
    ],
    ids=["From JSON file", "From YAML file", "From TOML file"],
)
def test_pydantic_helper_from_files(test_settings):
    # Arrange
    class ProjectSettings(BaseSettings):
        secret: str

    class CatSettings(BaseSettings):
        number: int
        names: List[str]

    class TestfromFileSettings(BaseSettings):
        custom_key: int
        pre_key: int
        post_key: int
        project: ProjectSettings
        stele: str
        cats: CatSettings

        class Config:
            @classmethod
            def customise_sources(
                cls,
                init_settings: SettingsSourceCallable,
                env_settings: SettingsSourceCallable,
                file_secret_settings: SettingsSourceCallable,
            ) -> Tuple[SettingsSourceCallable, ...]:
                return (
                    init_settings,
                    stela_settings,
                    env_settings,
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
