from stela.utils import merge_dicts


def test_merge_dicts():
    # Arrange
    target_dict = {
        "test": True,
        "project": {"foo": "bar", "x": "a"},
        "db": {"credentials": {"user": "hello"}},
    }
    source_dict = {
        "project": {"bar": "foo", "x": "b"},
        "db": {"name": "test", "credentials": {"user": "foo", "password": "bar"}},
    }

    # Act
    merge_dicts(source_dict, target_dict)

    # Assert
    assert target_dict == {
        "test": True,
        "project": {"foo": "bar", "bar": "foo", "x": "b"},
        "db": {"name": "test", "credentials": {"user": "foo", "password": "bar"}},
    }
