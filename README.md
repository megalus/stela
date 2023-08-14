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

Run Stela initialization command. This command will create `.env`, `.env.local` and `.gitignore` files.

```bash
$ stela init --default
```

```dotenv
# Add this to .env
API_URL="http://localhost:8000"
DB_URL="db://user:password@db:0000/name"
```

```python
# my_script.py
from stela import env

API_URL = env.API_URL  # http://localhost:8000
DATABASE_URL_CONNECTION = env.DB_URL  # db://user:password@db:0000/name
```

```dotenv
# Add to .env.local
DB_URL="db://real_user:real_password@real_db:0000/name"
```

```python
# my_script.py
from stela import env

API_URL = env.API_URL  # http://localhost:8000
DATABASE_URL_CONNECTION = env.DB_URL  # db://real_user:real_password@real_db:0000/name
```

That's it! Just check our [Documentation](https://megalus.github.io/stela/) for tons of customization and advice.

### Migrating from version 4.x
* Stela 5.0 is a major rework. The old format still works, but we strongly advise updating your code as soon as possible.
Please check [this document](https://megalus.github.io/stela/update) to understand how to update your existing project.
* Drop support to Python 3.8

### Not working?

Don't panic. Get a towel and, please, open an
[issue](https://github.com/megalus/stela/issues).
