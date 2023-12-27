# Using Frameworks

Stela runs at the module level, when you use the `from stela import env` import. Because that, it will work
seamlessly with many python packages and frameworks. Below are the recommendations and best practices for many of them:

!!! tip "Please check the folder: /examples"
    It contains working implementations for many frameworks.

## Popular Framework Examples

### Django

The best practice for [Django](https://github.com/django/django) projects is to consume the Stela `env` object on
django `settings.py` module. This is because many django packages look at this file to consume and define his own
settings.

```python
# Django settings.py
from stela import env

DEBUG = env.DEBUG
```

### Pydantic 2.x

Pydantic uses the [BaseSettings](https://docs.pydantic.dev/latest/usage/pydantic_settings/) logic to handle environment
variables. If you want to use Pydantic Settings with Stela dotenv file combinations (`.env`, `.env.local`, etc..) you
can use:

```ini
# .env.local
FOO__BAR=123
```
Use class `StelaConfigSettingsSource` to **replace** the original `env_settings` in your Settings class:

```python
from typing import Tuple, Type
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)
from stela.helpers.pydantic import StelaConfigSettingsSource


class FooSettings(BaseSettings):
    bar: str


class Settings(BaseSettings):

    model_config = SettingsConfigDict(extra="ignore", env_nested_delimiter="__", log_stela_settings=True)

    foo: FooSettings

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


print(Settings().foo.bar)
#> 123
```

### FastAPI

You can use [FastAPI](https://github.com/tiangolo/fastapi) with Stela directly ou via Pydantic
Settings (if you use the settings above).

### AWS Chalice

We currently don't support Chalice `autoreload` in local server. To work around this please
use the command `chalice local --no-autoreload` or import `env` inside a function.

### Jupyter Notebooks

The recommended practice is to import Stela data at the first cell, using the `%set_env` variables to define Stela behavior and
then call `read_env` function to retrieve the Environment Variables:

```python
# %%
from stela.utils import read_env

### You can change Stela behavior here
%set_env STELA_ENV = remote
%set_env STELA_SHOW_LOGS = False

### And use the `read_env` helper to reload environment variables
env = read_env()

print(f"Current Environment: {env.current_environment}")
print(f"My Secret: {env.MY_SECRET}")
# %%
```

---

For the next step, let's review all Stela options
