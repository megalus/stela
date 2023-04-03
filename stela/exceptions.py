"""Stela exceptions."""


class StelaEnvironmentNotFoundError(Exception):
    """Environment not found Error."""


class StelaFileTypeError(Exception):
    """File Type Error."""


class StelaTooManyLoadersError(Exception):
    """Too Many Loaders Error."""


class StelaValueError(AttributeError):
    """Stela Value Error."""
