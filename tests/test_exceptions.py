from importlib import reload

import pytest

import stela
from stela.exceptions import StelaEnvironmentNotFoundError, StelaFileTypeError


def test_no_environment_found(monkeypatch):
    monkeypatch.delenv("ENVIRONMENT")
    with pytest.raises(StelaEnvironmentNotFoundError):
        reload(stela)


def test_wrong_file_type(monkeypatch):
    monkeypatch.setenv("STELA_CONFIG_FILE_EXTENSION", "DOC")
    with pytest.raises(StelaFileTypeError):
        reload(stela)
    monkeypatch.delenv("STELA_CONFIG_FILE_EXTENSION")
