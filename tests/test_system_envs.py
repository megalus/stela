from stela.utils import read_env


def test_custom_loader(monkeypatch):
    # Arrange
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "AWSDUMMYKEYID")
    read_env()

    # Act
    from stela import env

    # Assert
    assert env.AWS_ACCESS_KEY_ID == "AWSDUMMYKEYID"
