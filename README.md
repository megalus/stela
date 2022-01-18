# Welcome to Stela

[![PyPI](https://img.shields.io/pypi/v/stela)](https://pypi.org/project/stela/)
[![Build](https://github.com/chrismaille/stela/workflows/tests/badge.svg)](https://github.com/chrismaille/stela/actions)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stela)](https://www.python.org)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

[Stela](https://en.wikipedia.org/wiki/Stele) were the "configuration
files" of ancient times. This library aims to simplify your project
configurations, from *json*, *yaml*, *ini* or *toml* files in a single
Python dictionary, which values can be easily be overridden by
environment variables.

### Index

1. [Install](#install)
2. [Basic Use](#basic-use)
3. [Environment Variables from Shell](#environment-variables-from-shell)
4. [Using layered environments](#using-layered-environments)
5. [Customize Stela](#customize-stela)
6. [Advanced Use](#advanced-use)
7. [Using with Pydantic](#using-with-pydantic)
8. [How Stela find the configuration files?](#how-stela-find-the-configuration-files)
9. [How Stela find the Environment Variables?](#how-stela-find-the-environment-variables)
10. [How Stela handle more complex cases?](#how-stela-handle-more-complex-cases)
11. [Full Lifecycle example](#full-lifecycle-example)
12. [When Stela read the data?](#when-stela-read-the-data)
13. [Refreshing Stela settings](#refreshing-stela-settings)
14. [How Stela read the dictionary values?](#how-stela-read-the-dictionary-values)
15. [Logging Data](#logging-data)
16. [All Stela Configuration Options](#all-stela-configuration-options)
17. [Migrating from version 3.x](#migrating-from-version-3x)
18. [Migrating from version 2.x](#migrating-from-version-2x)
19. [Migrating from version 1.x](#migrating-from-version-1x)


## Install

```shell
$ pip install stela
```

## Basic Use

For your *project settings*, you need to create a `pyproject.toml` file, and
under the table `environment` add the key/values you need:

```toml
# pyproject.toml
[environment]
my_file_path = "/foo/bar"
my_api_url = "https://foo.bar"
db.url = "user@password:db"
```

In Python you will access these settings importing stela like this:

```python
from stela import settings

API_URL = settings["my_api_url"]
# API_URL = "https://foo.bar"
```

### Environment Variables from Shell

Stela will check first, for the requested key, his SCREAMING_SNAKE_CASE
format in environment memory or `.env` file. If no data is found, Stela
will return the value from `pyproject.toml` tables.

Some examples:

| Variable in toml   | Environment Variable Name |
|:-------------------|:--------------------------|
| debug              | DEBUG                     |
| 3rd_party_api_url  | 3_RD_PARTY_API_URL        |
| db.password        | DB_PASSWORD               |

For example, for `db.url` Stela will look for
`DB_URL` in the following order:

1. Import `.env` data, if exists, in python environment,
using [python-dotenv](https://github.com/theskumar/python-dotenv) library.
2. Check for `DB_URL` in `os.environ`
3. Fallback to `db.url` in `pyproject.toml`

If data does not exist, Stela will raise a `KeyError`, like a dictionary.

```toml
# pyproject.toml
db.url = "fake@credentials"
```

```dotenv
# .env file
DB_URL=real@credentials  # will override info from pyproject.toml
```

```python
from stela import settings

DATABASE_URL = settings["db.url"]
# DATABASE_URL = "real@credentials"
```

### Using layered environments

For now, Stela are looking only for the `environment` table in your
`pyproject.toml`. But you may need to define
your settings *per environment layer* (i.e. development, tests, staging,
production, etc.)

First add `use_environment_layers` in Stela options:

```toml
# pyproject.toml
[tool.stela]
use_environment_layers = true
```

Then define `environment` sub-tables in
`pyproject.toml`:

```toml
# pyproject.toml
[tool.stela]
use_environment_layers = true

[environment]  # now is a shared data between environments
my_api_timeout = 30

[environment.local]
my_api_url = "http://localhost:8000"

[environment.production]
my_api_url = "https://foo.bar"
```

When you add `use_environment_layers = true` in config, Stela will now
always try to find the current environment looking for the `ENVIRONMENT`
variable. If this variable is not defined, Stela will use the default
environment, if available. If not, will raise a
`StelaEnvironmentNotFoundError`.

To add a default environment, use the `default_environment` option:

```toml
# pyproject.toml
[tool.stela]
use_environment_layers = true
default_environment = "local"

[environment]  # now is a shared data between environments
my_api_timeout = 30

[environment.local]
my_api_url = "http://localhost:8000"

[environment.production]
my_api_url = "https://foo.bar"
```

To use different environment variable, use the `environment_variable_name` option:

```toml
# pyproject.toml
[tool.stela]
use_environment_layers = true
default_environment = "local"
environment_variable_name = "ENV"

[environment]  # now is a shared data between environments
my_api_timeout = 30

[environment.local]
my_api_url = "http://localhost:8000"

[environment.production]
my_api_url = "https://foo.bar"
```

### Customize Stela

Use the following variables to customize Stela behavior:

```toml
# You can also set these as environment variables too using STELA_ prefix.
# For example, environment_variable_name can be override from STELA_ENVIRONMENT_VARIABLE_NAME

[tool.stela]
environment_variable_name = "ENVIRONMENT"   # The Environment variable
default_environment = ""                    # The default value for Environment variable
env_table = "environment"                   # The main environment table in pyproject.toml
use_environment_layers = false              # Use environment layers
env_file = ".env"                           # dotenv file name
config_file_path = "."                      # relative path for configuration files
do_not_read_dotenv = false                  # If True, will load dotenv file in os.environ
dotenv_overwrites_memory = true             # If True, will not overwrite keys from dotenv file if they exists on environ
show_logs = false                           # Show Stela Logs
log_filtered_value = true                  # Show Value from Stela settings in logs filtered. Use with caution.
```

Example:

```bash
# shell
$ export DJANGO_ENV=production
```

```toml
# pyproject.toml
[tool.stela]
use_environment_layers = true
environment_variable_name = "DJANGO_ENV"
env_table = "my_project.config"

[my_project.config]
project.debug = true

[my_project.config.production]
project.debug = false
```

```python
# settings.py
from stela import settings

DEBUG = settings["project.debug"]  # False from pyproject.toml or from PROJECT_DEBUG in environment
```

## Advanced Use

For very large projects, you can use separate environment layer per config files
(like `development.ini`, `staging.ini`, etc.)

Also, you can use `.yaml`, `.ini`, `.json` and `.toml` files.

In all files, Stela will always respect nested data. Suppose a file
called `development.ini` which contains:

```ini
[foo]
bar = value
```

As we know, Stela will convert data into a python dictionary:

```python
{
    "foo": {
        "bar": "value"
    }
}
```

You can use the settings like this:

```python
from stela import settings

my_conf = settings["foo.bar"]  # my_conf = "value"
```

This is possible because Stela uses under the hood the
[Scalpl](https://github.com/ducdetronquito/scalpl) library.

### Using with Pydantic
[Pydantic](https://pydantic-docs.helpmanual.io/) is a very popular library for data validation and settings management.
Stela can enhance pydantic experience, by being a additional settings for it. You can import stela settings as a dictionary
and import in pydantic settings, as per [Customize settings sources](https://pydantic-docs.helpmanual.io/usage/settings/#customise-settings-sources) documentation:

```toml
# pyproject.toml
[tool.stela]
use_environment_layers = true
default_environment = "local"
environment_variable_name = "ENV"

[environment]  # Shared data between environments
my_api_timeout = 30
db.host = "localhost"

[environment.local]
my_api_url = "http://localhost:8000"

[environment.production]
my_api_url = "https://foo.bar"
```

```python
from pydantic import BaseSettings, Extra
from stela.pydantic import stela_settings

class DbSettings(BaseSettings):
    host: str
    port: int = 5432

class Settings(BaseSettings):
    my_api_url: str
    my_api_timeout: int
    db: DbSettings

    class Config:
        # If you need to debug stela dictionary,
        # you can use this option to log stela settings dictionary
        log_stela_settings = True

        # If Stela dictionary has extra fields,
        # you can use this option to ignore them
        extra = Extra.ignore

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                stela_settings,  # Add stela settings before env_settings
                env_settings,
                file_secret_settings,
            )

print(Settings())  # for ENV=local
#> my_api_url='http://localhost:8000', my_api_timeout=30, db=DbSettings(host='localhost', port=5432)
```

Both config options (`log_stela_settings` and `extra`) are optional.

Please check file `test_pydantic.py` in tests folder for additional info.

### How Stela find the configuration files?

By default, Stela will use the value from `ENVIRONMENT` environment
variable to find correspondent INI file. For example, if you set
`ENVIRONMENT=development` Stela will look for `development.ini` file in
project root.

You can change this behaviour inside `pyproject.toml` file:

```toml
[tools.stela]
environment_variable_name = "ENVIRONMENT"   # Default Enviroment variable name
config_file_extension = "INI"               # YAML, TOML, JSON
config_file_prefix = ""                     # You can add a prefix before name - ex.: env_development.ini
config_file_suffix = ""                     # You can add a suffix after name - ex.: development_v1.ini
default_environment = "development"         # use this if you do not want to define the ENVIRONMENT key
config_file_path = "."                      # relative path from project root for configuration files
```

### How Stela find the Environment Variables?

We know Stela will try to find an environment variable using his
SCREAMING_SNAKE_CASE version. In this case, when the key is `foo.bar`,
Stela will search for an env called `FOO_BAR` in `os.environ`
files, before returning his dict value. Also, you can add a
prefix/suffix in this name (ex.: `MYPROJECT_FOO_BAR`). To do this,
define them in `pyproject.toml`:

```toml
[tools.stela]
environment_prefix = "MYPROJECT_"
environment_suffix = ""
```

```python
from stela import settings

my_conf = settings["foo.bar"]
# my_conf = "hello world" from MYPROJECT_FOO_BAR
```

Also, you can define Stela to never get values from shell and/or dotenv,
only from dictionary:

```toml
[tools.stela]
do_not_read_environment = true
do_not_read_dotenv = true
```

### How Stela handle more complex cases?

Stela uses this lifecycle to handle the settings load, using the `pre_load`, `custom_load` and `post_load` decorators
to modified data received from files and pyproject.toml, before importing settings.

To use this:

1. The decorated function **must** return a valid python dictionary.
2. Just one decorated function per phase.
3. Import the decorated functions before import stela settings for the first time. If you create the file
`conf_stela.py` at project root, decorated functions in there will be imported automatically.


#### The Pre-Load Phase (optional)

If defined, will always be the first step. To setup, create a
`conf_stela.py` file on project root and use the `pre_load` decorator
for your code.

Pre-Load Example:

```python
# conf_stela.py at project root
import plaster
from stela.decorators import pre_load
from stela.stela_options import StelaOptions
from typing import Dict, Any

@pre_load
def get_from_plaster(options: StelaOptions) -> Dict[Any, Any]:
    """Get data from plaster.

    Must return a valid Python dictionary.

    :param options: StelaOptions instance
    :return dict
    """
    env = options.current_environment  # get current environment during lifecycle
    config_uri = f"{env}.ini#myapp"
    settings = plaster.get_settings(config_uri, 'my-settings')
    return settings
```

#### The Load Phase

In this phase Stela will run 2 default loaders and a third optional
custom loader (if defined) on this default order:

1. Runs `embed` loader (retrieve data from `pyproject.toml`, if exists)
2. Runs `file` loader (retrieve data from config files, if exists)
3. Runs `custom` loader if defined (from `custom_load` decorator, if
   exists)

Each step updates data received from the previous step. You can change
this order, modifying the `load_order` in config:

```toml
# Or STELA_LOAD_ORDER env
[tool.stela]
# Default value is ["embed", "file", "custom"]
load_order = ["custom"]
```

Custom Load Example:

```python
# conf_stela.py at project root
from stela.decorators import custom_load
from stela.stela_options import StelaOptions
from typing import Dict, Any

@custom_load
def remove_bad_data(data: Dict[Any, Any], options: StelaOptions) -> Dict[Any, Any]:
    """Remove bad data.

    Must return a valid Python dictionary.

    :param options: StelaOptions instance
    :return dict
    """
    can_remove_bad_data = options.dotenv_data.get("REMOVE_BAD_DATA")  # reading dotenv during lifecycle
    if can_remove_bad_data:
        data.pop("bad_key", None)
    return data
```

#### The Post-Load Phase

This is, always, the last phase.

```python
# conf_stela.py at project root
import boto3
from stela.decorators import post_load
from stela import StelaOptions
from typing import Dict, Any

@post_load
def add_ssm_parameters(data: dict, options: StelaOptions) -> Dict[Any, Any]:
    """Load settings from SSM to current Stela data.

    Data returned must be a Python Dictionary.

    :param data (dict): Data parsed from previous phases
    :param options (obj): Stela Options from pyproject.toml
    :return Dict[Any, Any]
    """
    ssm = boto3.client('ssm')
    environment = options.current_environment
    response = ssm.get_parameters_by_path(
        Path=f'/foo/bar/{environment}',
        WithDecryption=True
    )
    return {parameter["Name"]: parameter["Value"] for parameter in response["Parameters"]}
```

### Full Lifecycle example

```toml
# pyproject.toml
[environment]
test = true
```

```python
# conf_stela.py at project root
from stela.decorators import pre_load, custom_load, post_load
from typing import Dict, Any
from stela import StelaOptions

@pre_load
def pre_load(options: StelaOptions) -> Dict[Any, Any]:
    # data value is: {}
    # Stela Options are available in options object.
    return {"foo": "bar"}

@custom_load
def load(data: dict, options: StelaOptions) -> Dict[Any, Any]:
    # data value is: {"foo": "bar", "test": True} from from pre_load and pyproject.toml
    return {"has_dogs": True}

@post_load
def post_load(data: dict, options: StelaOptions) -> Dict[Any, Any]:
    # data value is: {"foo": "bar", "has_dogs": True, "test": True}
    return {"number_of_dogs": 1}
```

```python
from stela import settings

print(settings)
# {"foo": "bar", "has_dogs": True, "number_of_dogs": 1, "test": True}
```

### When Stela read the data?

Stela are imported once, at module level - project settings are load and
immediately available:

```python
from stela import settings
from flask import Flask

app = Flask(__name__)
app.config.update(
    SECRET_KEY=settings["my_app_secret"] # will read from dict or MY_APP_SECRET value, after run all lifecycle
)

@app.route("/")
def hello():
    return f"Hello, Environment is {settings.stela_options.current_environment}"
```

### Refreshing Stela settings

If you need to reload settings, use the `stela.stela_reload` function.
Check the [unit tests](/tests/test_environments.py) for additional input.

### How Stela read the dictionary values?

Stela will respect the file format limitations. For example, INI files
always return values as string, TOML files returning datetime objects,
etc...

For environment variables, Stela will return value as string, by
default. For example: `NUMBER_OF_CATS=3` will return a string.

You can set Stela to evaluate these values, as per
[ast.literal_eval](https://docs.python.org/3.7/library/ast.html?highlight=literal_eval#ast.literal_eval)
rules. To do this, add in `pyproject.toml`:

```toml
[tool.stela]
evaluate_data = true
```

### Logging data
Stela use the [loguru](https://github.com/Delgan/loguru) package for logging, using `INFO` for general messages
and `DEBUG` for key/values retrieved in toml, environment keys, decorators, etc...
You can use the logs to debug data during Stela lifecycle.

By default, log are disabled. You can modify this behavior globally with the following configurations:

```toml
[tool.stela]
show_logs = true
log_filtered_value = true
```

Also, you can use decorators for fine-tuning logging:

```python
from stela import settings
from stela.decorators import stela_enable_logs, stela_disable_logs

@stela_enable_logs
def my_bugged_code():
    return settings["my_api_url"]

@stela_disable_logs
def my_sensible_code():
    return settings["my_credentials"]
```

The log level can be defined using the `LOGURU_LOG_LEVEL` as per loguru documentation.

### All Stela Configuration Options

All configuration files can be override using a environment variable,
using the `STELA_` prefix. For example, `default_environment` turns
`STELA_DEFAULT_ENVIRONMENT`.

```toml
# All keys and default values available in pyproject.toml
[tool.stela]
config_file_extension = "INI"                       # or YAML, TOML, JSON
config_file_path = "."                              # relative path from project root, for config files (i.e. .env, development.ini, etc.)
config_file_prefix = ""                             # You can add a prefix before name - ex.: env_development.ini
config_file_suffix = ""                             # You can add a suffix after name - ex.: development_v1.ini
default_environment = ""                            # The default value for Environment variable
do_not_read_environment = false                     # Do not read environment variables from shell
do_not_read_dotenv = false                          # Do not read dotenv file
env_file = ".env"                                   # dotenv file name
env_table = "environment"                           # The main environment table in pyproject.toml
environment_prefix = ""                             # ex.: settings["foo.bar"] looks for MY_PREFIX_FOO_BAR
environment_suffix = ""                             # ex.: settings["foo.bar"] looks for FOO_BAR_MY_SUFFIX
environment_variable_name = "ENVIRONMENT"           # The Environment variable
evaluate_data = false                               # Evaluate data received from config files
load_order = ["embed", "file", "custom"]            # Default order for Loaders in Load Phase
show_logs = false                                   # As per loguru settings.
log_filtered_value = true                           # When logging data, filter values from dict/env.
use_environment_layers = false                      # Use environment layers
dotenv_overwrites_memory = true                     # If True, values from os.environ will be override with dotenv values. If False, order is os.environ -> dotenv values -> files
```

### Migrating from version 3.x
* Support for Python 3.7 was dropped

### Migrating from version 2.x

* Logs are now disabled, by default. Too re-enable Stela logs:

```toml
[tool.stela]
show_logs = true
```

Or set `STELA_SHOW_LOGS=true` environment variable.

### Migrating from version 1.x

* Support for Python 3.6 was dropped
* The `stela_reload` function now is imported now from `stela.utils`
* The `@load` decorator now was renamed to `@custom_load`
* To mimic Stela load behavior from 1.x (Pre -> Load or Custom -> Post),
  please configure the old lifecycle in `pyproject.toml`:

```toml
[tool.stela]
use_environment_layers = true
do_not_read_dotenv = true
load_order = ["file"] # or ["custom"] with @custom_load decorator
```

### Not working?

Dont panic. Get a towel and, please, open a
[issue](https://github.com/chrismaille/stela/issues).
