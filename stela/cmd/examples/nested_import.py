def foo():
    from stela import settings as env

    number = env.get("cats.number", 10)
    names = env.CATS_NAMES
    return number, names
