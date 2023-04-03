"""Stela Initialization.

What we need here?

First of all, check if project already uses stela.

# Existing project (only)
1. Check if it needs to convert old keys.
2. If needed, convert old keys and create .env files.
3. Check if .gitignore exists. If not, create it. On this file, add the stela ignored files.

# New project
1. Check if .gitignore exists. If not, create it. On this file, add the stela ignored files.
2. Ask for stela env name, default is STELA_ENV.
3. Ask for default environment, default is development.

"""
import os
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import click
import toml

from stela.cmd.stela_converter import StelaConverter
from stela.config import StelaOptions

STELA_INI_FILE = ".stela"

PYPROJECT_TOML = "pyproject.toml"


@dataclass
class StelaInit:
    root_dir: str
    old_env_config_found: bool = False
    env_file: str = StelaOptions.env_file
    default_environment: Optional[str] = None
    dotenv_file_path: str = StelaOptions.config_file_path

    def upsert_gitignore(self) -> bool:
        file_exists = os.path.exists(".gitignore")
        if file_exists:
            old_content = open(".gitignore", "r").read()
        else:
            old_content = ""
            self.old_env_config_found = True
        new_content = deepcopy(old_content)
        if ".env\n" in new_content:
            new_content.replace(".env\n", "!.env  # Modified by Stela\n")
            self.old_env_config_found = True
        if "*.stela.back" not in new_content:
            new_content += "\n# Stela\n"
            new_content += "*.stela.back\n"
        if f"{self.env_file}.local" not in new_content:
            new_content += f"{self.env_file}.local\n"
        if f"{self.env_file}.*.local" not in new_content:
            new_content += f"{self.env_file}.*.local\n"
        if new_content != old_content:
            click.secho("Updating .gitignore file.", fg="green")
            with open(".gitignore", "w") as f:
                f.write(new_content)

    def add_stela_config(self, use_default):
        from stela.parsers.other_files import StelaFileReader

        reader = StelaFileReader()
        stela_config = {}
        pyproject_content = None
        if os.path.exists(STELA_INI_FILE):
            stela_config = reader.load_ini(STELA_INI_FILE)
        if not stela_config and os.path.exists(PYPROJECT_TOML):
            pyproject_content = toml.load(PYPROJECT_TOML)
            toml_settings = reader.load_toml(PYPROJECT_TOML)
            stela_config = toml_settings.get("tool", {}).get("stela", {})

        if use_default:
            new_stela_config = {
                "environment_variable_name": StelaOptions.environment_variable_name,
                "evaluate_data": StelaOptions.evaluate_data,
                "show_logs": StelaOptions.show_logs,
                "dotenv_overwrites_memory": StelaOptions.dotenv_overwrites_memory,
                "env_file": StelaOptions.env_file,
                "config_file_path": StelaOptions.config_file_path,
            }
        else:
            new_stela_config = {
                "environment_variable_name": click.prompt(
                    "Stela environment variable name",
                    default=stela_config.get(
                        "environment_variable_name",
                        StelaOptions.environment_variable_name,
                    ),
                ),
            }
            use_default_env = click.confirm("Use default environment?", default=False)
            if use_default_env:
                self.default_environment = click.prompt(
                    "Default environment",
                    default=stela_config.get("default_environment", "development"),
                )
                new_stela_config["default_environment"] = self.default_environment
            new_stela_config["evaluate_data"] = click.confirm(
                "Evaluate data from env files?",
                default=stela_config.get("evaluate_data", StelaOptions.evaluate_data),
            )
            new_stela_config["show_logs"] = click.confirm(
                "Show logs?",
                default=stela_config.get("show_logs", StelaOptions.show_logs),
            )
            if new_stela_config["show_logs"]:
                new_stela_config["log_filtered_value"] = click.confirm(
                    "Show filtered values in logs?",
                    default=stela_config.get(
                        "log_filtered_value", StelaOptions.log_filtered_value
                    ),
                )
            new_stela_config["dotenv_overwrites_memory"] = click.confirm(
                "Dotenv overwrites memory?",
                default=stela_config.get(
                    "dotenv_overwrites_memory", StelaOptions.dotenv_overwrites_memory
                ),
            )
            self.env_file = click.prompt(
                "Default env file",
                default=stela_config.get("env_file", StelaOptions.env_file),
            )
            new_stela_config["env_file"] = self.env_file
            self.dotenv_file_path = click.prompt(
                "Default relative path for dotenv files?",
                default=stela_config.get(
                    "config_file_path", StelaOptions.config_file_path
                ),
            )
            new_stela_config["config_file_path"] = self.dotenv_file_path

        if use_default:
            use_toml = (
                click.confirm("Save stela config in pyproject.toml file?", default=True)
                if pyproject_content
                else False
            )
        else:
            use_toml = False

        if use_toml:
            pyproject_content["tool"]["stela"] = new_stela_config
            toml.dump(pyproject_content, open(PYPROJECT_TOML, "w"))
            if os.path.exists(STELA_INI_FILE):
                os.remove(STELA_INI_FILE)
        else:
            with open(STELA_INI_FILE, "w") as f:
                f.write("[stela]\n")
                for k, v in new_stela_config.items():
                    f.write(f"{k} = {v}\n")
            if pyproject_content and "stela" in pyproject_content.get("tool"):
                del pyproject_content["tool"]["stela"]
                toml.dump(pyproject_content, open(PYPROJECT_TOML, "w"))

    @staticmethod
    def check_for_old_format() -> bool:
        root_dir = "."
        converter = StelaConverter(root_dir)

        converter.run(check_only=True)

        return converter.files_found > 0

    def run(self, use_default, convert):
        if use_default:
            click.secho("Using default stela config options.", fg="green")
        self.add_stela_config(use_default)
        if self.check_for_old_format():
            can_convert = False
            if convert:
                can_convert = True
            if not can_convert and not use_default:
                can_convert = click.confirm(
                    "Old stela data format found. Do you want to convert to new format? (Recommended).",
                    default=True,
                )
            if can_convert:
                converter = StelaConverter(
                    self.root_dir,
                    env_file=self.env_file,
                    config_file_path=self.dotenv_file_path,
                )
                converter.run()
        self.upsert_gitignore()
        self.create_env_files()
        click.secho("Stela successfully initialized.", fg="green", bold=True)

    def _create_env_file(self, filename, comment):
        path = os.path.join(Path.cwd(), self.dotenv_file_path)
        if not os.path.exists(path):
            os.makedirs(path)
        file_path = os.path.join(path, filename)
        file_exists = os.path.exists(file_path)
        if not file_exists:
            click.secho(f"Creating {file_path} file", dim=True)
            with open(file_path, "w") as f:
                f.write(f"# {comment}\n")

    def create_env_files(self):
        file_exists = os.path.exists(".env")
        if file_exists:
            if self.old_env_config_found:
                click.secho("Found old .env file. Renaming to .env.local", fg="yellow")
                os.rename(".env", ".env.local")
        else:
            self._create_env_file(
                self.env_file,
                "Add here your settings and fake secrets. You can commit this file.",
            )
            self._create_env_file(
                f"{self.env_file}.local",
                "Add here your local settings and/or real secrets. DO NOT commit this file.",
            )
            if self.default_environment:
                self._create_env_file(
                    f"{self.env_file}.{self.default_environment}",
                    "Add here your settings for the default environment. You can commit this file.",
                )
                self._create_env_file(
                    f"{self.env_file}.{self.default_environment}.local",
                    "Add here your local settings for the default environment. DO NOT commit this file.",
                )
