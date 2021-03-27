"""Stela Decorators."""
from functools import wraps


def pre_load(f):
    """Pre-Loader decorator.

    Use this decorator to handle data
    before invoking
    the custom load or default_loader.

    :param f: decorated function
    :return: wrapper function
    """

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        return f(self, *args, **kwargs)

    from stela import _stela_config

    if not getattr(_stela_config, "pre_load", None):
        setattr(_stela_config, "pre_load", f)

    return wrapper


def custom_load(f):
    """Run Custom Loader decorator.

    This loader will be invoked instead
    the default_loader.

    :param f: decorated function
    :return: wrapper function
    """

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        return f(self, *args, **kwargs)

    from stela import _stela_config

    if not getattr(_stela_config, "load", None):
        setattr(_stela_config, "load", f)

    return wrapper


def post_load(f):
    """Post-Loader decorator.

    Use this decorator to handle data
    after invoking
    the custom load or default_loader.

    :param f: decorated function
    :return: wrapper function
    """

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        return f(self, *args, **kwargs)

    from stela import _stela_config

    if not getattr(_stela_config, "post_load", None):
        setattr(_stela_config, "post_load", f)

    return wrapper
