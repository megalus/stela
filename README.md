# Welcome to Stela

[Stela](https://en.wikipedia.org/wiki/Stele) were the "configuration
files" of ancient times. This library aims to simplify your project
configurations, from json, yaml, ini or toml files in a single Python
dictionary, which values can be easily be override by environment
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

#### How Stela find the configuration files?

By default, Stela will use the value from `ENVIRONMENT` environment
variable to find correspondent INI file. For example, if
`ENVIRONMENT=development` Stela will look for `development.ini` file.

You can change this behaviour inside `pyproject.toml` file:

```toml
[tools.stela]
environment_name = "ENVIRONMENT"
config_file_extension = "INI" # YAML, TOML, JSON
config_file_prefix = ""  # You can add a prefix before name - ex.: env_development.ini
config_file_suffix = ""  # You can add a suffix after name - ex.: development_v1.ini
```

#### How Stela find the Environment Variables?

When asked for a value, Stela will try to find a environment variable
using the full uppercase sluggish path key: for `foo.bar` a env called
`FOO_BAR` will be looked first before returning his dict value. Also,
you can add a prefix/suffix in calculated environment name (ex.:
`MYPROJECT_FOO_BAR`), using `pyproject.toml`:

```toml
[tools.stela]
environment_prefix = "MYPROJECT_"
environment_suffix = ""
```

For example, Stela will look for the `MYPROJECT_FOO_BAR` env:

```python
# FOO_BAR = "hello_world" or
# MYPROJECT_FOO_BAR = "hello world" if you define environment_prefix
from stela import settings

my_conf = settings["foo.bar"]
# my_conf = "hello world"
```

#### How Stela handle more complex cases?

Stela uses a simple lifecycle to handle the settings load:

```text
Pre-Load -> Load or Default Load > Post-Load
```

If you have more complex case to find your project settings (ex.:
reading external services, load settings from database or parse from a
different file format or library), you can use Stela decorators for
`pre_load`, `load` and `post_load` phases:

* If you use the `pre_load` decorator, data parsed in this phase will be
  passed to **Load** phase.
* If you use the `load` decorator, it will be used instead the Stela
  `default_loader`. The data parsed here will update the dictionary
  received in previous phase
* If you use the `post_load` decorator, data parsed in this phase will
  update the dictionary received in previous phase.

In any case these loaders need to return a valid Python dictionary.

##### Lifecycle example:

```python
from stela.decorators import pre_load, load, post_load
from typing import Dict, Any
from stela import StelaOptions

@pre_load
def pre_load(options: StelaOptions) -> Dict[Any, Any]:
    return {"foo": "bar"}

@load
def load(data: dict, options: StelaOptions) -> Dict[Any, Any]:
    # data is: {"foo": "bar"}
    return {"has_dogs": True}

@post_load
def post_load(data: dict, options: StelaOptions) -> Dict[Any, Any]:
    # data is {"foo": "bar", "has_dogs": True}
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
def post_load(data: dict, options: StelaOptions) -> Dict[Any, Any]:
    """Load settings from SSM to Stela.
    
    This loader will be called after Stela default loader.
    Data returned must be a Python Dictionary.
    
    :param data (dict): Data parsed from previous phases
    :param options (obj): Stela Options from pyproject.toml
    :return Dict[Any, Any]
    """
    ssm = boto3.client('ssm')
    environment = options.environment
    parameters = ssm.get_parameters_by_path(
        Name=f'/foo/bar/{environment}',
        WithDecryption=True
    )
    return parameters
```

