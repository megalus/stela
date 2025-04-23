Project runs on a virtualenv inside WSL. Python interpreter can be found using command `poetry env info`.

Test runner is `pytest`. To run can use command `poetry run pytest -v`.

Always use type hints in the code. Always use TypeDicts for dictionaries.

Always use dataclasses for objects.

Always add docstrings in objects with more than seven lines of code. Use Google style.

Use `pre-commit run --all` to check for linter and format errors.

Project python version is 3.11.10.

This is a public python library hosted in PyPI. All configuration is inside `pyproject.toml` file.

Use semantic versioning for commit messages. Create a one-line commit. Do not use "`".

Use `feat:` if commit create new code in both ./stela and ./tests.

Use `fix:` if commit only changes the code in both ./stela and ./tests.

Use `chore:` if commit changes files outside ./stela and ./tests.

Use `BREAKING CHANGE:` if a python version changes in pyproject.toml.

Use `ci:` if commit changes files only in ./.github or the pyproject.toml.

Use `docs:` if commit changes files only in README.

Use `refactor:` if commit changes files in ./stela but not in ./tests.

Project versioning is done during GitHub actions `.github/publish.yml` workflow, using the [auto-changelog](https://github.com/KeNaCo/auto-changelog) library.

Always update the README at the root of the project.

README always contains [shields.io](https://shields.io/docs) badges for (when applicable): python versions, django versions, pypi version, license and build status.

Always write the README for developers with no or low experience with multiple environments, dotenv, but be pragmatic and short. The README should be a quick start guide for developers to use the library.

The ./docs folder contains detailed instructions of how to use the library, including examples and diagrams. Reading order for the markdown files is located in mkdocs.yml at `nav` key. On these docs you can be very didactic.

The ./examples folder contains examples of how to use the library with popular frameworks.

Always use mermaid diagrams on docs.

Always use English on code and docs.

Do not run terminal commands until Jetbrains fixes Junie support to WSL.
