<p align="center">
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
<a href="https://github.com/megalus/stela/blob/main/LICENSE" target="_blank">
<img alt="License" src="https://img.shields.io/github/license/megalus/stela"/></a>
</p>

## Welcome to Stela

[Stela](https://en.wikipedia.org/wiki/Stele) were the "information
files" of ancient times. This library helps you manage your project
settings and secrets with ease, using a simple and consistent approach.

### What is Stela?

Stela is a Python library that simplifies how you handle:
- **Settings**: Non-sensitive values that can be committed to your repository (API URLs, timeouts, etc.)
- **Secrets**: Sensitive values that should not be committed (passwords, tokens, etc.)
- **Environment-specific configurations**: Different values for development, testing, and production

### TL;DR

1. pip install stela
2. stela init --default --no-confirm
3. Uncomment the `MY_SECRET` line in `.env`
4. Add `from stela import env` and run `print(env.MY_SECRET)` in your code
5. Uncomment the `MY_SECRET` line in `.env.local` and get the code again.
6. Add `export MY_SECRET=memory_value` in your terminal and get the code again.

New to multi-environment setups? Start with the Quick Setup guide: https://megalus.github.io/stela/quick_setup/

### Install

```shell
pip install stela
```

### Documentation

For detailed documentation, visit: https://megalus.github.io/stela/

### Key Features

1. **Learn once, use everywhere** - Works with any Python project or framework
2. **Separate settings from secrets** - Use multiple dotenv files to organize your configuration
3. **Environment-specific settings** - Easily switch between development, testing, and production environments
4. **Simple API** - Access your settings with `from stela import env`
5. **Extensible** - Not limited to dotenv files, can load settings from any source (AWS Parameter Store, Vault, etc.)


## Quick Start Guide

### Step 1: Initialize Your Project

Run the Stela initialization command to set up your project:

```bash
stela init --default
```

This creates four files:
- `.env` - Store your default settings (will be committed to git)
- `.env.local` - Store your secrets (will be ignored by git)
- `.stela` - Stela configuration file
- Updates `.gitignore` to exclude sensitive files

### Step 2: Configure Your Settings and Secrets

Add your settings to `.env`:

```ini
# .env - This file WILL be committed to your repository
# Store default settings and fake credentials here
API_URL="http://localhost:8000"
DB_URL="db://fake_user:fake_password@local_db:0000/name"
```

Add your real secrets to `.env.local`:

```ini
# .env.local - This file will NOT be committed (ignored by git)
# Store real credentials and secrets here
DB_URL="db://real_user:real_password@real_db:0000/name"
```

### Step 3: Access Your Settings in Code

Use the simple API to access your settings and secrets:

```python
# my_script.py
from stela import env

# Access your settings with dot notation
API_URL = env.API_URL  # http://localhost:8000
DATABASE_URL = env.DB_URL  # db://real_user:real_password@real_db:0000/name
```

Stela automatically loads values from `.env` first, then overrides them with values from `.env.local`.

## Environment-Specific Configuration

Stela makes it easy to manage different environments (development, testing, production):

### Step 1: Create Environment-Specific Files

Create a file for each environment:

```ini
# .env.development
API_URL="http://localhost:8000"

# .env.production
API_URL="https://api.example.com"
```

### Step 2: Set the Environment

Set the `STELA_ENV` environment variable to specify which environment to use:

```bash
# For development
export STELA_ENV=development

# For production
export STELA_ENV=production
```

### Step 3: Access Your Settings

Your code remains the same, but Stela will load the appropriate values:

```python
from stela import env

# Will be "http://localhost:8000" when STELA_ENV=development
# Will be "https://api.example.com" when STELA_ENV=production
API_URL = env.API_URL
```

## Advanced: Custom Data Sources

Stela isn't limited to dotenv files. You can load settings from any source:

### Step 1: Configure a Final Loader

Add a final loader in your `.stela` configuration file:

```ini
# .stela
[stela]
final_loader = "path.to.my.final_loader"
```

### Step 2: Create Your Loader Function

```python
# my_loaders.py
from typing import Any
from stela.config import StelaOptions


def final_loader(options: StelaOptions, env_data: dict[str, Any]) -> dict[str, Any]:
    """Load settings from a custom source and merge into env_data.

    Args:
        options: Stela configuration options (includes current_environment).
        env_data: Data already loaded from dotenv files.

    Returns:
        Updated data dictionary.
    """
    # Example: pretend we fetched data from an external source
    external = {"API_TIMEOUT": "5", "FEATURE_FLAG": "true"}

    # Merge/override values
    env_data.update(external)
    return env_data
```

### Step 3: Use Your Settings as Usual

```python
from stela import env

# Values can come from dotenv files or your custom source
API_URL = env.API_URL
DB_PASSWORD = env.DB_PASSWORD
```

## Need Help?

- **Documentation**: For detailed guides and examples, visit [the documentation](https://megalus.github.io/stela/)
- **Issues**: Found a bug? Have a question? [Open an issue](https://github.com/megalus/stela/issues)
- **Contribute**: Pull requests are welcome!
