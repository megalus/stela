# Quick Setup

Let's start with a quick setup. Suppose your project has a `.env` file with the following content:

```ini
# .env
API_URL="http://localhost:8000"
DB_URL="db://fake_user:fake_password@local_db:0000/name"
```

Import the `env` object from `stela` and use it:

```python
# settings.py
from stela import env

API_URL = env.API_URL  # http://localhost:8000
DATABASE_URL_CONNECTION = env.DB_URL  # db://fake_user:fake_password@local_db:0000/name

```

Now, create a `.env.local` file and add the real secret value:

```ini
# .env.local
DB_URL="db://real_user:real_password@real_db:0000/name"
```

```python
# settings.py
from stela import env

API_URL = env.API_URL  # http://localhost:8000
DATABASE_URL_CONNECTION = env.DB_URL  # db://real_user:real_password@real_db:0000/name
```

This is because Stela will first load the content from `.env` file, and then will override the values with the content from `.env.local` file.

### But how about the environments?

Ok, let's add another file: `.env.remote`:

```ini
# .env.remote
API_URL="https://remote.api.com"
```

And we export the `STELA_ENV` variable:

```bash
export STELA_ENV=remote
```

When we run the python code, we will get the following values:

```python
from stela import env

API_URL = env.API_URL  # https://remote.api.com
DATABASE_URL_CONNECTION = env.DB_URL  # db://real_user:real_password@real_db:0000/name
```

!!! info "What's happened here?"
    1. Stela will load the content from `.env` file.
    2. Then, it will load the content from `.env.local` file, overriding previous content, because Stela always looks for `.env.*.local` files
    3. Finally, it will load the content from `.env.remote` file, overriding previous content, because STELA_ENV is set to `remote`.

And that's it! Now you can use Stela to manage your settings in any python project.

Stela is highly customizable, so you can use it in any way you want. It can handle several use cases you can have
handling your project settings.

---

For the next pages, let's see each one of these options with more details.
