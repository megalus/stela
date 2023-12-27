from typing import Tuple, Type

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from stela.helpers.pydantic import StelaConfigSettingsSource


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
