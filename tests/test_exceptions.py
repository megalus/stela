import pytest

from stela.exceptions import StelaFileTypeError
from stela.utils import read_env


def test_wrong_file_type(monkeypatch):
    monkeypatch.setenv("STELA_CONFIG_FILE_EXTENSION", "DOC")
    with pytest.raises(StelaFileTypeError):
        read_env()
    monkeypatch.delenv("STELA_CONFIG_FILE_EXTENSION")
    read_env()
