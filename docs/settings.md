# All Stela Settings options

You can define any of these options as an environment variable, using the `STELA_` prefix. Some examples:

```bash
$ export STELA_SHOW_LOGS=true
$ export STELA_FINAL_LOADER="foo.bar"
```

| Stela Option                | Description                                                                                                         |
|-----------------------------|---------------------------------------------------------------------------------------------------------------------|
| `config_file_path`          | Relative path for dotenv files. **Default**: `.`                                                                    |
| `default_environment`       | Default environment value, used if `environment_variable_name` if not informed. **Default**: `None`                 |
| `dotenv_encoding`           | Use this encoding to read dotenv files. **Default**: `utf-8`                                                        |
| `env_file`                  | Stela "env" file name. **Default**: `.env`                                                                          |
| `env_table`                 | The table or section to read data in custom files (toml, ini, etc...). **Default**: `env`                           |
| `environment_variable_name` | Stela environment variable to define project current environment. **Default**: `STELA_ENV`                          |
| `evaluate_data`             | Use `ast.literal_eval` to evaluate variable values. **Default**: `True`                                             |
| `final_loader`              | Stela Loader function which will be called after read dotenv files. **Default**: `stela.main.loader.default_loader` |
| `log_filtered_value`        | When logging data, show values filtered. **Default**: `True`                                                        |
| `raise_on_missing_variable` | Raise error if ask Stela for a unknown variable. **Default**: `True`                                                |
| `show_logs`                 | Stela will use loguru to show logs. **Default**: `False`                                                            |
| `warn_if_env_is_missing`    | Warn if Stela did not find the `.env` file. **Default**: `False`                                                    |


!!! tip "All these options are available in code"
    When you create a custom loader, all options above are available in the `options` object:
    ```python
    def my_custom_loader(options: StelaOptions, env_data: dict) -> dict:
        dotenv_encoding = options.dotenv_encoding
    ```
