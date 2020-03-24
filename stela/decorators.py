from functools import wraps


def pre_load(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        return f(self, *args, **kwargs)

    from stela.stela_options import StelaOptions

    if not getattr(StelaOptions, "pre_load", None):
        setattr(StelaOptions, "pre_load", f)

    return wrapper


def load(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        return f(self, *args, **kwargs)

    from stela.stela_options import StelaOptions

    if not getattr(StelaOptions, "load", None):
        setattr(StelaOptions, "load", f)

    return wrapper


def post_load(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        return f(self, *args, **kwargs)

    from stela.stela_options import StelaOptions

    if not getattr(StelaOptions, "post_load", None):
        setattr(StelaOptions, "post_load", f)

    return wrapper
