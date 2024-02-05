from stela.utils import read_env


def test_custom_loader(monkeypatch):
    # Arrange
    monkeypatch.setenv("STELA_FINAL_LOADER", "tests.custom_loader.custom_loader")
    read_env()

    # Act
    from stela import env

    # Assert
    assert env.NEW_ATTRIBUTE == "NEW_ATTRIBUTE"
    assert env.SECRET == "ANOTHER_SECRET"
