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

    from stela.stela_loader import StelaLoader

    loader = StelaLoader()
    loader.pre_load_function = f

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

    from stela.stela_loader import StelaLoader

    loader = StelaLoader()
    loader.custom_load_function = f

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

    from stela.stela_loader import StelaLoader

    loader = StelaLoader()
    loader.post_load_function = f

    return wrapper
