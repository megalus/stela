# Migrating from older versions

Stela 5.x is a major rework from previous versions. Use this guideline to how to update your code and your settings to
the new format:

## TLDR;

1. Run `stela init`. When ask for convert old format, click "Yes". You can also run `stela convert` to run the
   conversion only.
2. Move all logic from `conf_stela.py` (if exists) to a single custom loader function (see [Using Loader](using_loader.md)).
3. Add the stela option `final_loader` for your custom loader in your Stela configuration.


!!! tip "Use the automatic conversion logic"
    For large projects, it betters to automate the conversion and just review the result.
    Before any modification, the script will back up your files.
    On errors, you can revert automatic conversion typing `stela convert --revert`

## Manual Update

For the previous versions, project configuration was to read data from an external file (like `pyproject.toml`) and save
it to Stela `settings` dictionary:

```toml
# pyproject.toml
[tool.stela]
use_environment_layers = true
default_environment = "development"

[environment]
project.secret = 1

[environment.development]
project.secret = 2
```

```python
# Stela 4.x
from stela import settings

secret = settings["project.secret"]
#> 2
```

The "dotenv" logic was to load the `.env` in memory and check if the SCREAMING_SNAKE_CASE version of the `settings` key
exists, before returning the value from configuration files:

```ini
# original .env
PROJECT_SECRET=3
```

```python
# Stela 4.x
from stela import settings

secret = settings["project.secret"]  # Will look for PROJECT_SECRET variable first
#> 3
```

### Converting old data format

To convert old format data you can replace `settings` for `env` in your imports and replace the settings key, for the
attribute equal to the variable inside the `.env` files:

```python
# Stela 5.x
from stela import env  # from stela import settings

secret = env.PROJECT_SECRET  # secret = settings["project.secret"]
#> 3
```

### Update your configuration files

Rename your existing `.env` to `.env.local` and move the data from your configuration files for the corresponding
`.env.*` file and your secrets to the corresponding `.env.*.local` file. Using the above example:

```ini
# original .env
PROJECT_DEBUG=3
```

```toml
# pyproject.toml
[tool.stela]
use_environment_layers = true
default_environment = "development"

[environment]
project.secret = 1

[environment.development]
project.secret = 2
```

Turns to:

```ini
# .env.local renamed from .env
PROJECT_SECRET=3
```

```ini
# .env
PROJECT_SECRET=1
```

```ini
# .env.development
PROJECT_SECRET=2
```

### The `conf_stela.py` file
This file is deprecated too. Please move all logic to your custom loader (see example below).

## Option: Using Stela 4.x behavior to load data

You can also still use the 4.x behavior, creating a custom final loader which mimics the original logic.
The example below is for a Stela 4.x configured to using `pyproject.toml` for store settings and using the
`conf_stela.py` file for custom logic:

```python
import toml
from stela.config import StelaOptions
from stela.utils import merge_dicts, flatten_dict
from typing import Any


def legacy_pyproject_loader(
        options: StelaOptions,
        env_data: dict[str, Any]
) -> dict[str, Any]:
    """Custom loader for Stela 4.x behavior.

    Add this function on Stela configuration using the
    `final_loader` option.

    Please remember to update your code as soon as possible.
    Using stela as a dictionary is deprecated and
    will be removed at next major release.

    Data returned by this function will use read data in the same way
    as Stela 4.x, but the data must be retrieved using Stela 5.x syntax.

    Toml::

        [environment]
        foo = "bar"

        [environment.development]
        foo = "baz"

    Code::

        from stela import env

        secret = env.PROJECT_SECRET

    """
    from stela.loaders.cut import StelaCutLoader  #  will be removed in Stela 6.0
    from stela.utils import merge_env, merge_dicts

    filepath = "pyproject.toml"

    # Read toml data
    toml_data = toml.load(filepath)

    # Get Global Environment
    global_env = toml_data.get(options.env_table, {})

    # Get Current Environment Environment
    current_env = global_env.get(options.current_environment, {})

    # Merge Current Environment data into Global data
    merge_dicts(current_env, global_env)

    # If you are using the stela_conf.py,
    # The logic will run here
    old_loader = StelaCutLoader()
    if old_loader.pre_load_function:
        merge_dicts(old_loader.pre_load_function(), global_env)
    if old_loader.custom_load_function:
        merge_dicts(old_loader.custom_load_function(), global_env)
    if old_loader.custom_load_function:
        merge_dicts(old_loader.post_load_function(), global_env)

    # Finally, we override global_env with data from dotenv files:
    project_settings = merge_env(global_env, env_data)

    return project_settings
```

Now, add this `legacy_pyproject_loader` in your `pyproject.toml` stela configuration:

=== "pyproject.toml"
    ```toml
    [tool.stela]
    ...
    final_loader = "path.to.legacy_pyproject_loader"
    ```

!!! warning "Please update your code"
    We strongly suggest moving Stela to the new format. Using Stela as a dictionary is deprecated and will be removed
    on the next major version, and we will drop support for use Stela as a dict.


---

For the next step, let's look for all Stela Configuration Options
