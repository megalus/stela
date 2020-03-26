import copy


def test_pop(stela_default_settings):
    from stela import settings

    test_settings = copy.deepcopy(settings)
    test_settings.pop("app.secret")
    assert test_settings.get("app.secret", None) is None
    assert test_settings.get("app") == {"number_of_cats": "1", "use_scalpl": "true"}


def test_pop_non_existent(stela_default_settings):
    from stela import settings

    test_settings = copy.deepcopy(settings)
    test_settings.pop("app.secret.wrong", None)
