"""Stela exceptions."""


class StelaEnvironmentNotFoundError(Exception):
    """Environment not found Error."""


class StelaFileTypeError(Exception):
    """File Type Error."""


class StelaValueError(AttributeError):
    """Stela Value Error."""
