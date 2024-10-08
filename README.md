poetry <p align="center">
   <img src="docs/images/stela.png" alt="Stela" />
</p>
<p align="center">
<em>Easily manage your application settings and secrets</em>
</p>
<p align="center">
<a href="https://pypi.org/project/stela/" target="_blank">
<img alt="PyPI" src="https://img.shields.io/pypi/v/stela"/></a>
<a href="https://github.com/megalus/stela/actions" target="_blank">
<img alt="Build" src="https://github.com/megalus/stela/workflows/tests/badge.svg"/></a>
<a href="https://www.python.org" target="_blank">
<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/stela"/></a>
</p>

## Welcome to Stela

[Stela](https://en.wikipedia.org/wiki/Stele) were the "information
files" of ancient times. This library aims to simplify your project
configurations, proposing an opinionated way to manage your project
using dotenv files, or using any source you need.

### Install

```shell
$ pip install stela
```

---

### Documentation

* Docs: https://megalus.github.io/stela/

---

### Key features:

1. _**Learn once, use everywhere**_. Stela aims to be easily used in any Python project or Framework.
2. _**Separate settings from secrets from environments**_. Instead of using a single dotenv file to store all your settings,
   we use multiple dotenv files, one for each environment. This way, you can split secrets from settings, and you can
   have different values for the same setting in different environments.
3. _**Easy to implement**_. Use the command `stela init` to initialize your project and configure `.env` and `.gitignore`
   files.
4. _**Easy to use**_. To access you configuration just include `from stela import env` in your code. Simple as that.
5. _**One Interface, Any Source**_. You're not limited to dotenv files. Create your custom logic to import data from any
source you need.


### Quick Start

Run Stela initialization command. This command will create `.env`, `.env.local`, `.stela` and `.gitignore` files.

```bash
$ stela init --default
```

Create the dotenv files and add your settings and secrets.

```dotenv
# Add project settings and fake project secrets to .env
# This file will be commited to your repository
API_URL="http://localhost:8000"
DB_URL="db://fake_user:fake_password@local_db:0000/name"
```

```python
# my_script.py
from stela import env

API_URL = env.API_URL  # http://localhost:8000
DATABASE_URL_CONNECTION = env.DB_URL  # db://fake_user:fake_password@local_db:0000/name
```

```dotenv
# Add real secrets to .env.local
# This file will be ignored by git
DB_URL="db://real_user:real_password@real_db:0000/name"
```

A single, simple API to access your settings and secrets:

```python
# my_script.py
from stela import env

API_URL = env.API_URL  # http://localhost:8000
DATABASE_URL_CONNECTION = env.DB_URL  # db://real_user:real_password@real_db:0000/name
```

### Custom Sources

Use a custom, optional, final loader function to load your settings from any source you need.

```ini
# .stela
[stela]
final_loader = "path.to.my.final_loader"  # Add your final loader to Stela
```

```python
# Use SSM Parameter Store to load your settings

import boto3
from stela.config import StelaOptions

def final_loader(options: StelaOptions, env_data: dict[str, any]) -> dict[str, any]:
    """Load settings from AWS Parameter Store (SSM) to current Stela data.

    Data returned must be a Python Dictionary.
    Dict keys will be converted to env properties.
    Ex. {'Foo': 'Bar'} will be available as env.Foo

    :param env_data: Data parsed from dotenv file (the first loader)
    :param options: Stela Options obj
    :return dict[str, any]
    """
    ssm = boto3.client('ssm')
    environment = options.current_environment  # The value from STELA_ENV variable. Ex. production

    # Get from SSM
    response = ssm.get_parameters_by_path(
        Path=f'/my-project/settings/{environment}',
        WithDecryption=True
    )
    api_url = response['Parameters']['ApiUrl']  # https://real-api-url.com
    env_data.update({'API_URL': api_url})
    return env_data
```

Got your settings and secrets from both dotenv files and SSM Parameter Store:

```python
# my_script.py
from stela import env

API_URL = env.API_URL  # https://real-api-url.com
DATABASE_URL_CONNECTION = env.DB_URL  # db://real_user:real_password@real_db:0000/name
```


That's it! Check our [Documentation](https://megalus.github.io/stela/) for tons of customization and advice.

### Not working?

Don't panic. Get a towel and, please, open an
[issue](https://github.com/megalus/stela/issues).
