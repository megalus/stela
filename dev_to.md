## Manage Your Python Environment Variables Like a Pro with Stela

Getting started with environment variables in Python can feel overwhelming. You juggle multiple .env files, try to keep secrets out of version control, and write boilerplate code to parse types. Stela turns this chaos into a smooth, predictable workflow by giving you:

* Automatic type inference
* A clear separation between settings and secrets
* Environment-specific .env files
* A simple, consistent API
* Extensible support for custom loaders

Whether you’re building a small script or a large web service, Stela makes your configuration clean, safe, and maintainable.

### Why Environment Variables Matter

Environment variables let you keep configuration out of your codebase. Instead of hard-coding API URLs, database credentials, or feature flags, you store them externally and load them at runtime. This approach:

* Keeps secrets out of your Git history
* Makes it easy to switch configs for development, testing, and production
* Simplifies deployment to containers, CI pipelines, and cloud services

Yet most libraries leave you writing the same boilerplate: read a file, parse strings into ints or booleans, and override defaults. Stela automates all of that.

### Introducing Stela

Stela divides configuration into two concepts:

* **Settings**: Non-sensitive values you can commit (API endpoints, timeouts, etc.)
* **Secrets**: Sensitive values you must keep out of your repo (passwords, tokens, etc.)

It loads files in a well-defined order, casts strings to Python types automatically, and lets you add a final loader to pull from AWS Parameter Store, HashiCorp Vault, or any other source.

### Installing Stela

Install via pip:

```terminaloutput
pip install stela
```
### Quick Start: Initialize Your Project

Run the built-in init command:

```terminaloutput
stela init --default
```

This creates four files and updates your .gitignore:

* .env — default settings (committed)
* .env.local — secrets (ignored)
* .env.example — template for collaborators
* .stela — Stela configuration

### Understanding Your .env Files and Precedence

Stela follows a clear loading order to merge variables from dotenv files, and also defines how they interact with in-memory (process) environment variables.

Dotenv load order:

* .env
* .env.local
* .env.{environment}
* .env.{environment}.local

For example, if STELA_ENV=development, Stela will also look for:

* .env.development
* .env.development.local

Precedence rules (what wins when the same key exists in multiple places):

1. System environment variable already set in memory (os.environ) always wins. Example: MY_VAR=1 python app.py. Stela will never overwrite an existing os.environ key.
2. .env.{environment}.local
3. .env.{environment}
4. .env.local
5. .env
6. If not found anywhere, Stela raises a StelaValueError by default (configurable).

This means you can:

* Store safe defaults in .env
* Override with real secrets in .env.local
* Customize per-environment values without touching your defaults
* And still override anything at runtime via process envs (e.g., docker, CI, shell) without changing files

### Accessing Settings and Secrets

In your Python code, just import and use:

```python
from stela import env

API_URL      = env.API_URL        # str
TIMEOUT      = env.TIMEOUT        # int
FEATURE_FLAG = env.FEATURE_FLAG   # bool
DB_URL       = env.DB_URL         # str with secrets if overridden
```

Stela reads all your .env files under the hood and merges them into a single env object.

### Type Inference Out of the Box

Stela automatically parses values into the right Python types:
```ini
# .env
PORT=8000
DEBUG=true
RETRY_TIMES=3
PI=3.14159
FEATURES=["search","login","signup"]
EXTRA_SETTINGS={"cache":true,"timeout":30}
```
```python
from stela import env

assert isinstance(env.PORT, int)
assert isinstance(env.DEBUG, bool)
assert isinstance(env.PI, float)
assert isinstance(env.FEATURES, list)
assert isinstance(env.EXTRA_SETTINGS, dict)
```
No more manual casting or custom parsing routines. Stela handles JSON, booleans, numbers, lists, and dictionaries seamlessly.

### Managing Multiple Environments

Create files like `.env.testing` or `.env.production`:
```ini
# .env.production
API_URL="https://api.example.com"
```
Switch environments by setting STELA_ENV:
```terminaloutput
export STELA_ENV=production
```
Your code stays the same—Stela picks the right values based on STELA_ENV.

### Separating Settings from Secrets

Out of the box, stela init updates your .gitignore so that:

* `.env` is committed
* `.env.local` and `.env.*.local` are ignored

Use .env for harmless defaults and .env.local for real credentials. This pattern keeps secrets safe and makes it easy for teammates to get started.

### Advanced: Custom Final Loader

Stela doesn’t just read dotenv files. You can register a final loader in your .stela config:

```ini
[stela]
final_loader = "myproject.loaders.custom_loader"
```
Then implement `myproject/loaders.py`:

```python
# myproject/loaders.py
from typing import Any
from stela.config import StelaOptions


def custom_loader(options: StelaOptions, env_data: dict[str, Any]) -> dict[str, Any]:
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
Use Stela in your app as usual:

```python
from stela import env

# Values can come from dotenv files or your custom source.
# If a key is already set in os.environ at runtime, that in-memory value wins.
API_URL = env.API_URL
DB_PASSWORD = env.DB_PASSWORD
API_TIMEOUT = env.API_TIMEOUT  # From custom loader
```
On startup, Stela loads your dotenv files, then calls the custom loader, merging its results into env_data. Existing os.environ values are never overwritten.

### Extensively customizable
Don't want to infer types? Prefer a different file format? Stela has a lot of customization options. Check out the full docs for: https://megalus.github.io/stela/

### Conclusion & Next Steps

Stela brings structure, safety, and simplicity to environment variable management in Python. You get:

* Zero-boilerplate type inference
* Easy separation of settings and secrets
* Clear multi-environment support
* Extensible custom loader

Ready to give it a try? Check out the full docs at https://megalus.github.io/stela/ and start cleaning up your configuration today!

Happy coding! 🚀
