from typing import Any, Callable, Dict, Optional


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class StelaLoader(metaclass=SingletonMeta):
    def __init__(self):
        self.pre_load_function = None
        self.pre_load_function: Optional[Callable] = None
        self.custom_load_function: Optional[Callable] = None
        self.post_load_function: Optional[Callable] = None

        self.pre_data: Optional[Dict[Any, Any]] = None
        self.embed_data: Optional[Dict[Any, Any]] = None
        self.file_data: Optional[Dict[Any, Any]] = None
        self.custom_data: Optional[Dict[Any, Any]] = None
        self.post_data: Optional[Dict[Any, Any]] = None
