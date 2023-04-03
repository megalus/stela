# Quick Setup

Let's start with a quick setup: suppose a project add with a `.env` file with the following content:

```ini
# .env
API_URL="http://localhost:8000"
DB_URL="db://user:password@db:0000/name"
```

```python
# settings.py
from stela import env

API_URL = env.API_URL  # http://localhost:8000
DATABASE_URL_CONNECTION = env.DB_URL  # db://user:password@db:0000/name

```

Now, create a `.env.local` file and add the secret value:

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

Ok, lets add another file: `.env.remote`:

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

And that's it! Now you can use Stela to manage your settings in any python project.

Stela is highly customizable, so you can use it in any way you want. It can handle several use cases you can have
handling your project settings.

---

For the next pages, lets see each one of these options with more details.
