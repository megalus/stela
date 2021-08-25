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
    loader.add_pre_loader(f)

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
    loader.add_custom_loader(f)

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
    loader.add_post_loader(f)

    return wrapper


def stela_enable_logs(f):
    from loguru import logger

    @wraps(f)
    def wrapper(*args, **kwargs):
        logger.enable("stela")
        ret = f(*args, **kwargs)
        logger.disable("stela")
        return ret

    return wrapper


def stela_disable_logs(f):
    from loguru import logger

    from stela import settings

    @wraps(f)
    def wrapper(*args, **kwargs):
        logger.disable("stela")
        ret = f(*args, **kwargs)
        if settings.stela_options.show_logs:
            logger.enable("stela")
        return ret

    return wrapper
