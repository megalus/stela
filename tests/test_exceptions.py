import pytest

import stela
from stela.exceptions import StelaEnvironmentNotFoundError, StelaFileTypeError
from stela.utils import stela_reload


def test_no_environment_found(mocker, monkeypatch):
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.setenv("STELA_USE_ENVIRONMENT_LAYERS", True)
    mocker.patch.object(stela.stela_options.toml, "load", return_value={})
    with pytest.raises(StelaEnvironmentNotFoundError):
        stela_reload()
    monkeypatch.delenv("STELA_USE_ENVIRONMENT_LAYERS")


def test_wrong_file_type(monkeypatch):
    monkeypatch.setenv("STELA_CONFIG_FILE_EXTENSION", "DOC")
    with pytest.raises(StelaFileTypeError):
        stela_reload()
    monkeypatch.delenv("STELA_CONFIG_FILE_EXTENSION")
