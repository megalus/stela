# Using Stela

Stela usage is very simple. Just import the `env` object:

```python
from stela import env

MY_VAR = env.MY_VAR
```

If you want to get the environment variable programmatically, use the `get` function:

```python
from stela import env

var = "MY_VAR"
env = env.get(var)
```

If the variable did not exist, Stela will raise a `StelaValueError`. You can change this using the `raise_on_missing`
parameter. You can also add a default value if you want, using the `default` parameter too:

```python
from stela import env

var = "MY_VAR"
env = env.get(var, raise_on_missing=False, default="foo")
```

You can also list all environment variables:

```python
from stela import env

all_vars = env.list()
#> ["MY_VAR"]
```

And you can use the `env` object to get information about the current environment:

```python
from stela import env

ENV = env.current_environment
DEFAULT_ENV = env.default_environment
```

### When Stela read the data?

Stela is imported once at _module_ level - project settings are load and immediately available:

```python
from stela import env
from flask import Flask

app = Flask(__name__)
app.config.update(
    SECRET_KEY=env.FLASK_SECRET
)


@app.route("/")
def hello():
    return f"Hello, Environment is {env.current_environment}"
```

### Refreshing Stela settings

If you need to reload settings, use the `stela.utils.read_env` function:

```python
from stela.utils import read_env

def reload_app():
    env = read_env()
```

### Logging data

Stela use the [loguru](https://github.com/Delgan/loguru) package for logging, using `INFO` for general messages
and `DEBUG` for key/values retrieved in toml, environment keys, decorators, etc...
You can use the logs to debug data during Stela operation.

By default, the log is disabled. You can modify this behavior globally with the following configurations:

=== ".stela"
    ```ini
    [stela]
    show_logs = true
    log_filtered_value = true
    ```

=== "pyproject.toml"
    ```toml
    [tool.stela]
    show_logs = true
    log_filtered_value = true
    ```
=== "shell"
    ```bash
    $ export STELA_SHOW_LOGS=true
    $ export STELA_LOG_FILTERED_VALUE=true
    ```

Also, you can use decorators for fine-tuning logging per function:

```python
from stela import env
from stela.decorators import stela_enable_logs, stela_disable_logs


@stela_enable_logs
def my_bugged_code():
    return env.MY_API_URL


@stela_disable_logs
def my_sensible_code():
    return env.MY_SECRET_KEY
```

The log level can be defined using the `LOGURU_LOG_LEVEL` as per loguru documentation.

---

For the next step, we will look at how IDEs can autocomplete Stela environment variables.
