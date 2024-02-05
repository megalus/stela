# Initializing Stela

For new projects we recommend running the command `stela init` to create your project settings configuration.

```shell
stela init
```

This command will prompt for the following configurations:

#### Environment variable name (`environment_variable_name`)

This is the name of the environment variable that Stela will use to find the current environment.
By default, is `STELA_ENV` but you can change it to whatever you want, like ENV, DJANGO_ENV, etc...

#### Default environment (`default_environment`)

If you define a Environment variable name, but not the value for it, Stela can use this optional default environment
value.
By default, this is disabled and his default value, if enabled, is `development`.

#### Evaluate dotenv values (`evaluate_data`)

If you want to evaluate the values in your dotenv files, you can enable this option. By default, every value from dotenv
files are treated as string. If you enable this option, Stela will try to evaluate the values as
per [ast.literal_eval](https://docs.python.org/3.9/library/ast.html?highlight=literal_eval#ast.literal_eval) rules.
If the value can't be evaluated, you still receive the string value.

#### Show Stela info in logs (`show_logs`)

If you want to see Stela info in your logs, you can enable this option. By default, this is disabled. Also, if you
enable logs, you can filter the values displayed (the default value for this sub-option is
enabled) (`log_filtered_value`).

#### Dotenv file name (`env_file`)

If you want to use a different name for your dotenv files, you can change it here. By default, this is `.env`.

## Stela Project Files

Using the information provided, Stela will save their configuration in the `.stela` file.

!!! info "Tip: You can use your `pyproject.toml` too."
    If you use this file, the command will ask if you want to save stela configuration inside toml file.

After that, Stela will create the following files if they don't exist:

* `.env` (or the name you defined in the previous step)
* `.env.local`
* `.env.[environment]` (or the name you defined in the previous step if you enabled default environment)
* `.env.[environment].local`
* `.gitignore`

### Configuration file example:

Using default settings

=== ".stela"
    ```ini
    [stela]
    environment_variable_name = STELA_ENV
    evaluate_data = True
    show_logs = False
    env_file = .env
    config_file_path = .
    ```

=== "pyproject.toml"
    ```toml
    [tool.stela]
    environment_variable_name = "STELA_ENV"
    evaluate_data = true
    show_logs = false
    env_file = ".env"
    config_file_path = "."
    ```

=== "shell"
    ```bash
    $ export STELA_ENVIRONMENT_VARIABLE_NAME="STELA_ENV"
    $ export STELA_EVALUATE_DATA=true
    $ export STELA_SHOW_LOGS=false
    $ export STELA_ENV_FILE=".env"
    $ export STELA_CONFIG_FILE_PATH="."
    ```

See section [Settings](settings.md) for the complete Stela options list.

---

In the next step, we will deep dive how Stela uses dotenv files.
