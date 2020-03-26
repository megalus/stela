import pytest

import stela
from stela import stela_reload
from stela.exceptions import StelaEnvironmentNotFoundError, StelaFileTypeError


def test_no_environment_found(mocker, monkeypatch):
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    mocker.patch.object(stela.stela_options.toml, "load", return_value={})
    with pytest.raises(StelaEnvironmentNotFoundError):
        stela_reload()


def test_wrong_file_type(monkeypatch):
    monkeypatch.setenv("STELA_CONFIG_FILE_EXTENSION", "DOC")
    with pytest.raises(StelaFileTypeError):
        stela_reload()
    monkeypatch.delenv("STELA_CONFIG_FILE_EXTENSION")
