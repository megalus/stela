async def test_load_env_async():
    # Act
    from stela import env

    # Assert
    assert env.list() == ["ONE", "FOO", "SECRET"]


def test_load_env():
    # Act
    from stela import env

    # Assert
    assert env.list() == ["ONE", "FOO", "SECRET"]
