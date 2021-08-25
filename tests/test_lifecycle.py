def test_default_lifecycle(full_lifecycle, monkeypatch):
    """Test Stela Full Lifecycle.

    Value for key "secret" using default Order:
        1. From pre_load:       "pre_load_secret" (@pre_load function)
        2. From embed table:    "embed_secret" (pyproject.toml)
        3. From config file:    "foo" (test.ini)
        4. From custom loader:  "custom_load_secret" (@custom_load function)
        5. From post_load:      "post_load_secret" (@post_load function)
    """

    from stela import settings

    monkeypatch.delenv("SECRET")
    assert settings["project.secret"] == "post_load_secret"

    assert settings.stela_loader.pre_data["project"]["secret"] == "pre_load_secret"
    assert settings.stela_loader.embed_data["project"]["secret"] == "embed_secret"
    assert settings.stela_loader.file_data["project"]["secret"] == "foo"
    assert (
        settings.stela_loader.custom_data["project"]["secret"] == "custom_load_secret"
    )
    assert settings.stela_loader.post_data["project"]["secret"] == "post_load_secret"

    assert settings.to_dict == {
        "DEFAULT": {},
        "api_timeout": 60,
        "custom_key": 2,
        "post_key": 3,
        "pre_key": 1,
        "project": {
            "number_of_cats": "1",
            "secret": "post_load_secret",
            "shared_attribute": "foo.bar",
            "use_scalpl": "true",
        },
        "stele": "merneptah",
    }

    monkeypatch.setenv("PROJECT_SECRET", "good_dog")
    assert settings["project.secret"] == "good_dog"
