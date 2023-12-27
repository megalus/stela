# Committing your settings

Stela is better suited for new projects. This is because, traditionally, the `.env` file is not committed on python
projects. So, you need special attention when porting an existing project to Stela.

## Changes on .gitignore

By default, Stela will add your `.env.local` and `.env.*.local` files to project's `.gitignore` and will comment
the `.env` entry if exists. This is because you shouldn't commit your secret values, even if you want to use them in
your local machine. But some values in this file aren't secrets, and you may want to commit these values. That's why you combine
both `.env` and `.env.local` files.

For example, you may want to commit the `API_URL` and a fake value, but not the real one for the `API_TOKEN`:

```ini
# .env - can be committed
# the value for API_TOKEN here can be used in your CI/CD
# for running tests, for example
API_URL=https://foo.bar
API_TOKEN=foo
```

```ini
# .env.local - Do not commit! The value for API_TOKEN here is as secret!
# You don't need to repeat the API_URL here, because
# it will be loaded from .env file
API_TOKEN=real_token
```

The standard python `.gitignore` need to be updated to reflect this:

```bash
# .gitignore

# .env  # Comment or remove this line
.env.local  # Add this
.env.*.local  # Add this
```

!!! tip "Use the `stela init` command"
    The command `stela init` will make these changes for you on an existing `.gitignore` file. If you don't have
    a `.gitignore` file, the command will create one for you. And if you have a existing `.env` file in your project,
    Stela will automatically rename this file to `.env.local`

!!! warning "Be careful with the original .env file"
    If you already use a `.env` file in your project, chances are high this file contains secrets. Please,
    make sure you rename this file to `.env.local` (manually or using `stela init`) or split his contents between these
    two files (the `.env` for settings and `.env.local` for secrets).

## I'm not comfortable changing these settings. Can I use Stela?

Sure, just don't run the `stela init` file and create manually the `.stela` file, renaming the dotenv file to be used
(we suggest: `.environs`), like this:

```ini
# A very conservative configuration.
[stela]
environment_variable_name = STELA_ENV
evaluate_data = False
show_logs = False
dotenv_overwrites_memory = False
env_file = .environs
config_file_path = .
```

In your `.gitignore` just add:

```bash
.environs.local
.environs.*.local
```

Stela will read the original `.env` file, and will overwrite the values using the `.environs` files.

---

In the next step, we will look closely on how to use Stela in your code.
