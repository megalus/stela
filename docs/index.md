![](images/stela.png)

# Welcome to Stela

[Stela](https://en.wikipedia.org/wiki/Stele) were the "information
files" of ancient times. This library aims to simplify your project
configurations, proposing an opinionated way to manage your project
using dotenv files, or using any source you need.

## Motivation

Working with _environment variables_ vs project _**settings**_ and _**secrets**_ can be _hard_.

* Sometimes we need to define a default value for a _secret_, like a database url, to run unit tests.
* Sometimes, we need to set different values for a _setting_, like an API url, for different environments.
* Sometimes, we use **dotenv** on local development, but need to use other services, like _vaults_ or _secret managers_,
to retrieve these same _settings_ and _secrets_ on production.

This library was created to help simplify this process, by providing a single interface to access all data from
multiple dotenv files, or if you need, from your custom logic to retrieve your project _settings_ and _secrets_ from
another source.

!!! note "About settings and secrets"
    In this documentation we talk a lot about these two concepts. What we meant:

    * `settings`: Any nonsensible value, which can be different between different environments. This data can be safety
    committed in your project. Example: API urls, Timeout values, etc..
    * `secrets`: Any sensible value, which you can't commit in you project. Examples: Tokens, Passwords, etc..

## Why another library?

There are a lot of good libraries to work with project settings:

* [python-dotenv](https://github.com/theskumar/python-dotenv) - One of the most popular. In fact, we use it under the
  hood to load the dotenv files.
* [python-decouple](https://github.com/HBNetwork/python-decouple) - Another good one, this library together with
  [Dynaconf](https://github.com/dynaconf/dynaconf) and [Plaster](https://github.com/Pylons/plaster) were the main
  inspirations for this project until version 5.x
* [Pydantic](https://github.com/pydantic/pydantic) - A very powerful solution for data validation, they provide a
  [Settings Management](https://docs.pydantic.dev/usage/settings/) tool, which is an good solution for that environment.

### Why use Stela?

Our key features:

1. _**Learn once, use everywhere**_. Stela aims to be easily used in any Python project or Framework.
2. _**Separate settings from secrets from environments**_. Instead of using a single dotenv file to store all your settings,
   we use multiple dotenv files, one for each environment. This way, you can split _secrets_ from _settings_, and you can
   have different values for the same environment variable in different environments.
3. _**Easy to implement**_. Use the command `stela init` to initialize your project and configure `.env` and `.gitignore`
   files.
4. _**Easy to use**_. To access you configuration just include `from stela import env` in your code. Simple as that.
5. _**One Interface, Any Source**_. You're not limited to dotenv files. Create your custom logic to import data from any
source you need.

---

## Install

```shell
pip install stela
```

!!! info "Currently this project supports:"
    * Python 3.10, 3.11 and 3.12
