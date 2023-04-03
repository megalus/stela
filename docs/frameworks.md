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

### Pydantic

Pydantic uses the [BaseSettings](https://docs.pydantic.dev/usage/settings/) logic to handle environment
variables. If you want to use Pydantic Settings with Stela dotenv file combinations (`.env`, `.env.local`, etc..) you
can use the helper `stela_env_settings` to **replace** the original `env_settings` in your Settings class:

```ini
# .env.local
FOO__BAR=123
```

```python
from pydantic import BaseSettings
from stela.helpers.pydantic import stela_env_settings


class FooSettings(BaseSettings):
    bar: str


class Settings(BaseSettings):
    foo: FooSettings

    class Config:
        env_nested_delimiter = '__'
        log_stela_settings = True  # Use to see Stela logs here

        @classmethod
        def customise_sources(
                cls,
                init_settings,
                env_settings,
                file_secret_settings,
        ):
            # Do not include original env_settings here
            # Replace it with stela_env_settings
            return (
                init_settings,
                stela_env_settings,
                file_secret_settings,
            )


print(Settings().foo.bar)
# > 123
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
%set_env
STELA_ENV = remote
%set_env
STELA_SHOW_LOGS = False

### And use the `read_env` helper to reload environment variables
env = read_env()

print(f"Current Environment: {env.current_environment}")
print(f"My Secret: {env.MY_SECRET}")
# %%
```

## Stela and Asynchronous Code
If you need to (re)load Stela envs inside an asynchronous method, and you have a complex blocking custom loader, which
needs to run inside the loop, you can use the asynchronous `aread_env` method:

```python
from my_project import app
from stela.asyncio import aread_env


@app.get("/")
async def root():
    env = await aread_env()
    return {
        "message": "Hello World",
        "environment": env.current_environment,
        "secret": env.MY_SECRET,
    }
```

!!! tip "This can be used in any asynchronous frameworks"
    You can use this helper in projects
    like [Django-Ninja](https://github.com/vitalik/django-ninja), [Starlite](https://github.com/starlite-api/starlite)
    or [Sanic](https://github.com/sanic-org/sanic), but only if you have troubles using the default
    import. Almost all the time the `from stela import env` import works successfully.

---

For the next step, let's see how to migrate Stela 4.x to Stela 5.0
