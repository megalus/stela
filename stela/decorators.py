"""Stela Decorators."""

from functools import wraps


def stela_enable_logs(f):
    from loguru import logger

    from stela import env

    @wraps(f)
    def wrapper(*args, **kwargs):
        logger.enable("stela")
        ret = f(*args, **kwargs)
        logger.disable("stela")
        if env._stela_options.show_logs:
            logger.enable("stela")
        return ret

    return wrapper


def stela_disable_logs(f):
    from loguru import logger

    from stela import env

    @wraps(f)
    def wrapper(*args, **kwargs):
        logger.disable("stela")
        ret = f(*args, **kwargs)
        if env._stela_options.show_logs:
            logger.enable("stela")
        return ret

    return wrapper
