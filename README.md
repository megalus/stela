# Welcome to Stela

[![Build](https://github.com/chrismaille/stela/workflows/tests/badge.svg)](https://github.com/chrismaille/stela/actions)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stela)](https://www.python.org)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
<a href="https://github.com/psf/black"><img alt="Code style: black"
src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

[Stela](https://en.wikipedia.org/wiki/Stele) were the "configuration
files" of ancient times. This library aims to simplify your project
configurations, from *json*, *yaml*, *ini* or *toml* files in a single
Python dictionary, which values can be easily be override by environment
variables.

### Install

```shell
$ pip install stela
```

### Example

You can use `.yaml`, `.ini`, `.json` and `.toml` files. Suppose a file
called `development.ini` which contains:

```ini
[foo]
bar = value
```

Stela will convert data into a python dictionary:

```python
{
    "foo": {
        "bar": "value"
    }
}
```

And you can use the settings like this:

```python
from stela import settings

my_conf = settings["foo.bar"]
# my_conf = "value"
```

This is possible because Stela uses under the hood the
[Scalpl](https://github.com/ducdetronquito/scalpl) library.

### How Stela find the configuration files?

By default, Stela will use the value from `ENVIRONMENT` environment
variable to find correspondent INI file. For example, if you set
`ENVIRONMENT=development` Stela will look for `development.ini` file in
project root.

You can change this behaviour inside `pyproject.toml` file:

```toml
[tools.stela]
environment_variable_name = "ENVIRONMENT"
config_file_extension = "INI" # YAML, TOML, JSON
config_file_prefix = ""  # You can add a prefix before name - ex.: env_development.ini
config_file_suffix = ""  # You can add a suffix after name - ex.: development_v1.ini
default_environment = "development" # use this if you do not want to define the ENVIRONMENT key
config_file_path = "."  # relative path from project root for configuration files
```

### How Stela find the Environment Variables?

When asked for a value, Stela will try to find a environment variable
using the full uppercase slug path. For example, if key is `foo.bar`,
Stela will search for a env called `FOO_BAR` before returning his dict
value. Also, you can add a prefix/suffix in this calculated environment
name (ex.: `MYPROJECT_FOO_BAR`). To do this, define them in
`pyproject.toml`:

```toml
[tools.stela]
environment_prefix = "MYPROJECT_"
environment_suffix = ""
```

In above case, Stela will look for the `MYPROJECT_FOO_BAR` env:

```python
# FOO_BAR = "hello_world" or
# MYPROJECT_FOO_BAR = "hello world" if you define environment_prefix
from stela import settings

my_conf = settings["foo.bar"]
# my_conf = "hello world"
```

Also, you can define Stela to never get values from environment
variables, only from dictionary:

```toml
[tools.stela]
do_not_read_environment = true
```

### How Stela handle more complex cases?

Stela uses this lifecycle to handle the settings load:

```text
Pre-Load (optional) -> Load or Default Load > Post-Load (optional)
```

If you have more complex cases to retrieve your project settings (ex.:
reading external services, load settings from database or parse from a
different file format or library), you can use Stela decorators for
`pre_load`, `load` and `post_load` phases:

* If you use the `pre_load` decorator, data parsed in this phase will be
  passed to **Load** phase.
* If you use the `load` decorator, it will be used instead the Stela's
  `default_loader`. The data returned here will update the dictionary
  received in previous phase
* If you use the `post_load` decorator, data returned in this phase will
  update the dictionary received in previous phase.

Only one function are allowed per phase.

>  These loaders need to return a valid Python dictionary.

##### Lifecycle example:

```python
from stela.decorators import pre_load, load, post_load
from typing import Dict, Any
from stela import StelaOptions

@pre_load
def pre_load(options: StelaOptions) -> Dict[Any, Any]:
    # data value is: {}
    # Stela Options are available in options object.
    return {"foo": "bar"}

@load
def load(data: dict, options: StelaOptions) -> Dict[Any, Any]:
    # data value is: {"foo": "bar"}
    # Using load, default_loader will not be invoked
    return {"has_dogs": True}

@post_load
def post_load(data: dict, options: StelaOptions) -> Dict[Any, Any]:
    # data value is: {"foo": "bar", "has_dogs": True}
    return {"number_of_dogs": 1}

# Final data is {"foo": "bar", "has_dogs": True, "number_of_dogs": 1}
```

##### Post-Load SSM Example:

```python
# stela_loader.py
import boto3
from stela.decorators import post_load
from stela import StelaOptions
from typing import Dict, Any

@post_load
def add_ssm_parameters(data: dict, options: StelaOptions) -> Dict[Any, Any]:
    """Load settings from SSM to current Stela data.
    
    This loader will be called after Stela default loader.
    Data returned must be a Python Dictionary.
    
    :param data (dict): Data parsed from previous phases
    :param options (obj): Stela Options from pyproject.toml
    :return Dict[Any, Any]
    """
    ssm = boto3.client('ssm')
    environment = options.current_environment
    parameters = ssm.get_parameters_by_path(
        Name=f'/foo/bar/{environment}',
        WithDecryption=True
    )
    return parameters
```

### When Stela read the data?

Stela are imported once, at module level. This is the python equivalent
for a Singleton object - project settings are load and immediately
available:

```python
from stela import settings
from flask import Flask

app = Flask(__name__)
app.config.update(
    SECRET_KEY=settings["my_app.secret"] # will read from dict or MY_APP_SECRET value
)

@app.route("/")
def hello():
    return f"Hello, Environment is {settings.stela_options.current_environment}"
```

If you need to reload settings, use the `stela.stela_reload` function:

```python
from stela import stela_reload

def test_different_environments(monkeypatch):
    from stela import settings
    assert settings.stela_options.current_environment == "test"
    
    monkeypatch.setenv("ENVIRONMENT", "production")
    settings = stela_reload()
    assert settings.stela_options.current_environment == "production"
    monkeypatch.delenv("ENVIRONMENT")
```

### How Stela read the dictionary values?

Stela will respect the file format limitations. For example, INI files
always return values as string, TOML files returning datetime objects,
etc...

For environment variables, Stela will return value as string, by
default. For example: `NUMBER_OF_CATS=3` will return a string.

You can set Stela to literal evaluate these values, as per
[ast.literal_eval](https://docs.python.org/3.7/library/ast.html?highlight=literal_eval#ast.literal_eval)
rules. To do this, add in `pyproject.toml`:

```toml
[tool.stela]
evaluate_data = true
```

### All Stela Configuration Options:

All configuration files can be override using a environment variable,
using the `STELA_` prefix. For example, `default_environment` turns
`STELA_DEFAULT_ENVIRONMENT`.

```toml
# All keys and default values available in pyproject.toml
[tool.stela]
environment_variable_name = "ENVIRONMENT"
config_file_extension = "INI" # YAML, TOML, JSON
config_file_prefix = ""  # You can add a prefix before name - ex.: env_development.ini
config_file_suffix = ""  # You can add a suffix after name - ex.: development_v1.ini
config_file_path = "."
environment_prefix = ""  # ex.: settings["foo.bar"'] looks for MY_PREFIX_FOO_BAR
environment_suffix = ""  # ex.: settings["foo.bar"'] looks for FOO_BAR_MY_SUFFIX
default_environment = ""
evaluate_data = false
do_not_read_environment = false
show_logs = true  # as per loguru settings.
```

### Not working?

Dont panic. Get a towel and, please, open a
[issue](https://github.com/chrismaille/stela/issues).
