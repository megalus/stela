# Using dotenv files

Stela uses [dotenv](https://github.com/theskumar/python-dotenv) to load additional environment variables from the
following files:

```bash
.env                        # loaded in all cases
.env.local                  # loaded in all cases, ignored by git
.env.[environment]          # only loaded in specified environment
.env.[environment].local    # only loaded in specified environment, ignored by git
```

Using default settings, Stela will use the value from `STELA_ENV` to determine the current environment and will look for
dotenv files at the root of the project. You can change this behavior using the `environment_variable_name`
and `config_file_path` options as described before.

!!! tip "The goal here is: _Familiarity_"
    If you are a frontend developer, probably you already see this naming convention in some node projects,
    especially [Vite](https://vitejs.dev/guide/env-and-mode.html#env-files). This is intended: learn _once_ to
    manipulate `dotenvs`, and use it in all your backend and frontend projects.

### A generic example

```ini
# .env
API_URL="http://localhost:8000"
API_TOKEN="mock_token"
```

```ini
# .env.local
API_TOKEN="local_token"
```

```ini
# env.development
API_URL="https://develop.api.com"
API_TOKEN="development_token"
```

```ini
# env.development.local
API_TOKEN="local_development_token"
```

In the following example, the value for each environment will be:

| Environment         | API_URL                 | API_TOKEN                 |
|---------------------|-------------------------|---------------------------|
| Global              | http://localhost:8000   | `mock_token`              |
| Global (local)      | http://localhost:8000   | `local_token`             |
| development         | https://develop.api.com | `development_token`       |
| development (local) | https://develop.api.com | `local_development_token` |


### Dotenv Load Priorities

Stela will return the variable value using this priority order:

1. The value from the system environment, if it did not exist in dotenv file. Ex.: `MY_VAR=1 python my_script.py`
2. The value from the `.env.[environment].local` if it exists and Stela can find the current environment.
3. The value from the `.env.[environment]` if it exists and Stela can find the current environment.
4. The value from the `.env.local` if it exists.
5. The value from the `.env` if it exists.
6. Will raise a `StelaValueError`.

Stela will always raise a `StelaValueError` if you ask for a variable that does not exist in any of the dotenv files or  in memory.
You can change this behavior using the `raise_on_missing_variable` options as described before.

Also, Stela will always overwrite the `os.environ` values with the values from the dotenv files.

### A more concrete Example

Let's create a more complex example, using Django. In this example we will want to run unit tests using the _local_
settings, but run the local server using the _remote_ settings, for debugging purposes.

After running `stela init` add these variables on the created dotenv files:

```ini
# .env
API_URL="http://localhost:8000"
API_TOKEN="fake_token"
DB_USER="foo"
DB_PASSWORD="bar"
DB_HOST="localhost"
DB_PORT=5432
DB_NAME="test_db"
DEBUG=False
```

```ini
# env.local
DEBUG=True
DB_PORT=5433
```

And add two more dotenv files:

```ini
# env.remote
API_URL="https://remote.api.com"
```

```ini
# env.remote.local
API_TOKEN="real_token"
DB_USER="real_user"
DB_PASSWORD="real_password"
DB_HOST="real_host"
DB_PORT=5432
DB_NAME="real_name"
DEBUG=True
```

And finally, let's change the default environment name:

=== ".stela"
    ```ini
    [stela]
    environment_variable_name = MY_PROJECT_ENV  # change here
    ...
    ```

=== "pyproject.toml"
    ```toml
    [tool.stela]
    environment_variable_name = MY_PROJECT_ENV  # change here
    ...
    ```

=== "shell"
    ```bash
    $ export STELA_ENVIRONMENT_VARIABLE_NAME=MY_PROJECT_ENV
    ```

Let's run unit tests using the local settings:

```bash
# Running django tests locally using default settings
$ python manage.py test
```

```python
# settings.py
from stela import env

ENV = env.current_environment  # "GLOBAL" because no environment was declared
DEBUG = env.DEBUG  # True from .env.local
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.DB_NAME,  # "test_db" from .env
        'USER': env.DB_USER,  # "foo" from .env
        'PASSWORD': env.DB_PASSWORD,  # "bar" from .env
        'HOST': env.DB_HOST,  # "localhost" from .env
        'PORT': env.DB_PORT,  # 5433 from .env.local
    }
}
API_URL = env.API_URL  # "http://localhost:8000" from .env
API_TOKEN = env.API_TOKEN  # "fake_token" from .env
```

Running again the server using the _remote_ settings:

```bash
# Running django tests locally using remote settings
$ MY_PROJECT_ENV=remote python manage.py runserver
```

```python
# settings.py
from stela import env

ENV = env.current_environment  # "remote" from MY_PROJECT_ENV in memory
DEBUG = env.DEBUG  # True from .env.remote.local
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.DB_NAME,  # "real_name" from .env.remote.local
        'USER': env.DB_USER,  # "real_user" from .env.remote.local
        'PASSWORD': env.DB_PASSWORD,  # "real_password" from .env.remote.local
        'HOST': env.DB_HOST,  # "real_host" from .env.remote.local
        'PORT': env.DB_PORT,  # 5432 from .env.remote.local
    }
}
API_URL = env.API_URL  # "https://remote.api.com" from .env.remote
API_TOKEN = env.API_TOKEN  # "real_token" from .env.remote.local
```

---

In the next step, we will understand how to commit these new settings.
