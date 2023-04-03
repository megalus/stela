import ast
import os
import re
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import click
from scalpl import Cut


@dataclass
class StelaConverter:
    root_dir: str
    settings_name: str = "settings"
    key_attr_map: dict[str, str] = field(default_factory=dict)
    processed_files: list[str] = field(default_factory=list)
    not_processed_files: list[str] = field(default_factory=list)
    files_found: int = 0
    env_file: str = ".env"
    config_file_path: str = "."

    def run(self, check_only: bool = False):
        for subdir, _, files in os.walk(self.root_dir):
            for file in files:
                filepath = os.path.join(subdir, file)
                if (
                    filepath.endswith(".py")
                    and not filepath.endswith("stela_cmd.py")
                    and not filepath.endswith("stela_converter.py")
                    and not filepath.endswith("stela_init.py")
                    and not filepath.endswith("stela_conf.py")
                ):
                    self.process_python_file(
                        filepath, process_python_file=not check_only
                    )

        self.show_result()

        if self.processed_files:
            self.create_env_file()
            if self.not_processed_files:
                click.secho(
                    "Warning: Some files have old stela data format, but we cannot change "
                    "automatically. Please check.",
                    bold=True,
                    fg="yellow",
                )
            else:
                click.secho(
                    "Success: Done convert files. Please check the .env file.",
                    fg="green",
                    bold=True,
                )
        if not self.files_found:
            click.secho("Success: No old keys found.", fg="green", bold=True)

    def show_result(self):
        # print key-attribute mapping
        if len(self.key_attr_map.keys()) > 0:
            click.secho("Old Keys found and converted names:", fg="white")
            for key, attr in self.key_attr_map.items():
                click.secho(f"* {key} -> {attr}", fg="blue")
        for fn in self.not_processed_files:
            click.secho(
                f"File {fn} has old stela data format, but we cannot change automatically. Please check.",
                bold=True,
                fg="yellow",
            )

    def process_python_file(self, filepath: str, process_python_file: bool = True):
        with open(filepath, "r") as f:
            file_contents = f.read()
            old_contents = deepcopy(file_contents)

        for node in ast.walk(ast.parse(file_contents)):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    if hasattr(node, "module") and "stela" in node.module:
                        self.files_found += 1
                        if process_python_file:
                            self.convert(alias, file_contents, filepath, old_contents)

    def convert(self, alias, file_contents, filepath, old_contents):
        need_backup = False
        self.settings_name = alias.asname if alias.asname else "settings"
        regex = re.compile(
            rf"(?<!\w){self.settings_name}(?!\.env)(?:(?<=\.)[A-Za-z_][A-Za-z0-9_]*)?"
        )
        need_backup = self.find_old_and_new_keys(file_contents, need_backup)
        file_contents = self.replace_in_file_keys(file_contents)
        file_contents = regex.sub(
            lambda match: match.group().replace(self.settings_name, "env"),
            file_contents,
        )
        if need_backup:
            self.backup_python_file(file_contents, filepath, old_contents)
            self.processed_files.append(filepath)
        elif not os.path.exists(f"{filepath}.stela.bak"):
            self.not_processed_files.append(filepath)

    @staticmethod
    def backup_python_file(file_contents, filepath, old_contents):
        backup_file = f"{filepath}.stela.bak"
        if not os.path.exists(backup_file):
            click.secho(f"Creating backup file {backup_file}...", dim=True)
            with open(backup_file, "w") as f:
                f.write(old_contents)
        with open(filepath, "w") as f:
            f.write(file_contents)

    @property
    def settings_dot_regex(self):
        return rf"\b{self.settings_name}\[(['\"])([\w\.]+)\1\]"

    @property
    def settings_get_regex(self):
        return rf"\b{self.settings_name}\.get\((['\"])([\w\.]+)\1\)"

    def replace_in_file_keys(self, file_contents):
        # replace dot with underscore
        file_contents = re.sub(
            self.settings_dot_regex,
            lambda match: f"{self.settings_name}.{match.group(2).replace('.', '_').upper()}",
            file_contents,
            flags=re.ASCII,
        )
        file_contents = re.sub(
            self.settings_get_regex,
            lambda match: f"{self.settings_name}.{match.group(2).replace('.', '_').upper()}",
            file_contents,
            flags=re.ASCII,
        )
        return file_contents

    def find_old_and_new_keys(self, file_contents, need_backup):
        matches = re.findall(
            self.settings_dot_regex,
            file_contents,
            flags=re.ASCII,
        )
        for match in matches:
            need_backup = True
            key = match[1]
            attr = key.replace(".", "_").upper()
            self.key_attr_map[key] = attr
        matches = re.findall(
            self.settings_get_regex,
            file_contents,
            flags=re.ASCII,
        )
        for match in matches:
            need_backup = True
            key = match[1]
            attr = key.replace(".", "_").upper()
            self.key_attr_map[key] = attr
        return need_backup

    def _process_env_data(self, filename: str, origin: Cut):
        can_continue = len(origin.keys()) > 0
        path = os.path.join(Path.cwd(), self.config_file_path)
        file_path = os.path.join(path, filename)
        if can_continue and os.path.exists(file_path):
            can_continue = click.confirm(
                click.style(
                    f"Warning: File {file_path} already exists. Overwrite?", fg="yellow"
                ),
                abort=False,
            )
        if can_continue:
            if not os.path.exists(path):
                os.makedirs(path)
            with open(file_path, "w") as f:
                today = datetime.now().strftime("%Y-%m-%d")
                f.write(
                    f"# Created by Stela in {today} using data from old configuration files.\n"
                )
                for fn in self.processed_files:
                    f.write(f"# {fn}\n")
                f.write("\n")
                all_keys = [k for k in self.key_attr_map]
                all_keys.sort()
                for key in all_keys:
                    line = f"{self.key_attr_map[key]}={origin.get(key, '')}\n"
                    f.write(line)
            click.secho(f"Success: Created file {file_path}.", fg="green")

    def create_env_file(self):
        from stela import settings

        filename = f"{self.env_file}.{settings.stela_current_environment.lower()}.local"
        self._process_env_data(filename, settings)

    def revert(self):
        backup_found = False
        for subdir, _, files in os.walk(self.root_dir):
            for file in files:
                filepath = os.path.join(subdir, file)
                if filepath.endswith(".stela.bak"):
                    backup_found = True
                    click.secho(f"Reverting {filepath}...", dim=True)
                    python_file = filepath.replace(".stela.bak", "")
                    os.remove(python_file)
                    os.rename(filepath, python_file)
        if backup_found:
            click.secho("Success: Done revert convert files.", fg="green", bold=True)
