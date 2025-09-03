Getting started with environment variables in Python can feel overwhelming. You may juggle multiple .env files, try to keep secrets out of version control, and write repetitive code to parse types. Stela turns that chaos into a smooth, predictable workflow by offering:

* Automatic type inference
* A clear separation between settings and secrets
* Environment-specific .env files
* A simple, consistent API
* Extensible support for custom loaders

Whether you’re building a small script or a large web service, Stela makes configuration clean, safe, and maintainable.

### Why environment variables matter

Environment variables let you keep configuration out of your codebase. Instead of hard-coding API URLs, database credentials, or feature flags, you store them externally and load them at runtime. This approach:

* Keeps secrets out of your Git history
* Makes it easy to switch configs for development, testing, and production
* Simplifies deployment to containers, CI pipelines, and cloud services

Yet most libraries leave you you to write the same boilerplate: read files, parse strings into ints or booleans, and override defaults. Stela automates all of that.

### Introducing Stela

Stela divides configuration into two concepts:

* **Settings**: Non-sensitive values you can commit (API endpoints, timeouts, etc.)
* **Secrets**: Sensitive values you must keep out of your repo (passwords, tokens, etc.)

It loads files in a well-defined order, casts strings to Python types automatically, and lets you add an optional final loader to pull values from other sources (AWS Parameter Store, HashiCorp Vault, etc.).

### Installing Stela

Install via pip:

```bash
pip install stela
```

### Quick start: initialize your project

Run the built-in init command:

```bash
stela init --default
```

This creates a set of configuration files and updates your `.gitignore`. Typical files are:

* `.env` — default settings (committed)
* `.env.local` — secrets (ignored)
* `.stela` — Stela configuration

Try this quick test to observe precedence:
1. Add or uncomment a `MY_SECRET` line in `.env`, then open a Python REPL and run:
   ```python
   from stela import env
   print(env.MY_SECRET)
   ```
2. Stop the REPL. Add or uncomment `MY_SECRET` in `.env.local`, restart the REPL and run the same code — the value from `.env.local` should take precedence over `.env`.
3. Set `MY_SECRET` in your process environment and run the REPL again. On macOS/Linux:
   ```bash
   export MY_SECRET="value_from_memory"
   python -c "from stela import env; print(env.MY_SECRET)"
   ```
   On Windows PowerShell:
   ```powershell
   $env:MY_SECRET="value_from_memory"
   python -c "from stela import env; print(env.MY_SECRET)"
   ```

### Understanding your dotenv files and precedence

By default Stela reads dotenv files in this order:

* `.env`
* `.env.local`

If you set STELA_ENV (for example `STELA_ENV=development`), Stela will also look for:
* `.env.development`
* `.env.development.local`

When the same key exists in multiple places, precedence (what wins) is:
1. System environment variable already set in memory (`os.environ`) — always wins.
2. `.env.{environment}.local` (if STELA_ENV is set)
3. `.env.{environment}` (if STELA_ENV is set)
4. `.env.local`
5. `.env`
6. If a value is not found anywhere, Stela raises a `StelaValueError` by default (this is configurable).

This lets you:
* Keep safe defaults in `.env`
* Override with real secrets in `.env.local`
* Customize per-environment values without changing defaults
* Still override anything at runtime via process envs (Docker, CI, shell) without editing files

### Accessing settings and secrets

In your Python code, just import and use:

```python
from stela import env

API_URL      = env.API_URL        # str
TIMEOUT      = env.TIMEOUT        # int
FEATURE_FLAG = env.FEATURE_FLAG   # bool
DB_URL       = env.DB_URL         # str (may come from secrets if overridden)
```

Stela reads your `.env` files under the hood and exposes a single `env` object.

### Type inference out of the box

Stela parses values into native Python types automatically:

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

Stela handles _JSON_, _booleans_, _numbers_, _lists_, and _dictionaries_ — no manual casting required.

### Managing multiple environments

Create files like `.env.testing` or `.env.production`:

```ini
# .env.production
API_URL="https://api.example.com"
```

Switch environments by setting STELA_ENV:

```bash
export STELA_ENV=production
```

Your code stays the same — Stela picks values based on `STELA_ENV` automatically.

### Separating settings from secrets

The `stela init` command updates your .gitignore so:

* `.env` is committed
* `.env.local` and `.env.*.local` are ignored

Use `.env` for harmless defaults and `.env.local` for real credentials. This keeps secrets out of your repo while making it easy for teammates to get started.

### Advanced: custom final loader

Stela doesn’t only read dotenv files. You can register an optional final loader in your .stela config:

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

    # Merge/override values from the external source into env_data
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

On startup, Stela loads your dotenv files, then calls the custom loader and merges its returned values into the loaded data. Values already present in `os.environ` are never overwritten.

### Extensibility

Don't want automatic type inference? Prefer a different file format? Define a deafult environment? Disable logs? Stela is flexible — check https://megalus.github.io/stela/ for all customization options.

### Conclusion & next steps

Stela brings structure, safety, and simplicity to environment variable management in Python. You get:

* Zero-boilerplate type inference
* Clear separation of settings and secrets
* Straightforward multi-environment support
* Extensible custom loaders

Ready to try it? Visit the docs at https://megalus.github.io/stela/ and start cleaning up your configuration today.

If this helped or you have questions, please leave a comment below — I'm happy to answer.

Happy coding! 🚀
