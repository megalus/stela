## The Stela Final Loader

Stela Final Loader is a function which receives two arguments:

* The [Stela Options](settings.md) object: `options`
* The dictionary content the data from _dotenvs_ read based on current stela options: `env_data`

And it's the last code called for before returning the `env` object.

### Default Stela Final Loader code

Default behavior is just return data parsed from Env files:

```python
from stela.config import StelaOptions


def default_loader(
        options: StelaOptions,
        env_data: dict[str, any]
) -> dict[str, any]:
    """Stela Default Loader.

    Default Action is just return the env_data received.

    :param options: Stela Options
    :param env_data: Dict with environment data
    :return: Dict
    """
    from loguru import logger

    logger.info(
        f"Using Stela Default Loader. "
        f"Current environment is: {options.current_environment}"
    )
    return env_data
```

### The Stela Options object

All stela options are attributes in this object. Please check [Settings](settings.md) for the complete list.

### Creating your custom Final Loader

If you need to get your Environment variables from other sources than dotenv files, or need to mix data, you can use your
own logic for the Loader. Just inform Stela which function needs to be called:

=== ".stela"
    ```ini
    [stela]
    final_loader = "path.to.my.custom_loader"
    ...
    ```
=== "pyproject.toml"
    ```toml
    [tool.stela]
    final_loader="path.to.my.custom_loader"
    ...
    ```
=== "shell"
    ```bash
    $ export STELA_FINAL_LOADER="path.to.my.custom_loader"
    ```

This function will be called, and need to receive the two parameters above: `options` and `env_data` and it must return
a valid python dictionary.

## Examples

### Read data from toml file

```python
import toml
from typing import Any
from stela.config import StelaOptions
from stela.utils import merge_env


def pyproject_loader(options: StelaOptions, env_data: dict[str, Any]) -> dict[str, Any]:
    """Load settings from pyproject.toml to current Stela data.

    Data returned must be a Python Dictionary.

    :param env_data: Data parsed from dotenv files
    :param options: Stela Options obj
    :return Dict[str, Any]
    """
    filepath = "pyproject.toml"
    sub_table = "environment"  # The sub table inside toml which holds your settings

    # Read toml data for the sub table
    toml_data = toml.load(filepath)
    sub_table_data = toml_data.get(sub_table, {})

    # Update toml data with dotenv info
    # The sub_table_data are the "default" settings.
    # The env_data are the final ones.
    project_settings = merge_env(sub_table_data, env_data)

    return project_settings
```

### Read data from AWS System Manager Parameter Store

```python
import boto3
from typing import Any
from stela.config import StelaOptions


def ssm_loader(options: StelaOptions, env_data: dict[str, Any]) -> dict[str, Any]:
    """Load settings from AWS Parameter Store (SSM) to current Stela data.

    Data returned must be a Python Dictionary.

    :param env_data: Data parsed from dotenv file
    :param options: Stela Options obj
    :return Dict[str, Any]
    """
    ssm = boto3.client('ssm')
    environment = options.current_environment

    # Get from SSM
    response = ssm.get_parameters_by_path(
        Path=f'/my-project/{environment}',
        WithDecryption=True
    )
    ssm_data = {parameter["Name"].upper(): parameter["Value"] for parameter in response["Parameters"]}

    # Overwrite env_data with SSM data
    # Normally information on remote sources
    # like vaults, are the final ones
    env_data.update(ssm_data)

    return env_data
```

!!! tip "The goal here is: _One Interface, Any Sources_"
    You can use any source or logic to load your environment variables.
    They can have the complexity you need for the project you're working.
    But the interface to work with these values is always the same.

### Different Loaders per Environment

If you need different custom loaders per environment, you can use Stela Environment variables to do this:

```bash
# Development
$ export STELA_FINAL_LOADER="path.to.dev_loader"
```

```bash
# Production
$ export STELA_FINAL_LOADER="path.to.prod_loader"
```

---

For the next step, let's review how to integrate Stela with many popular Python packages and Frameworks.
