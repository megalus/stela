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

    from stela.stela_options import StelaOptions

    if not getattr(StelaOptions, "pre_load", None):
        setattr(StelaOptions, "pre_load", f)

    return wrapper


def load(f):
    """Run Custom Loader decorator.

    This loader will be invoked instead
    the default_loader.

    :param f: decorated function
    :return: wrapper function
    """

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        return f(self, *args, **kwargs)

    from stela.stela_options import StelaOptions

    if not getattr(StelaOptions, "load", None):
        setattr(StelaOptions, "load", f)

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

    from stela.stela_options import StelaOptions

    if not getattr(StelaOptions, "post_load", None):
        setattr(StelaOptions, "post_load", f)

    return wrapper
