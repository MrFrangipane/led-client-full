from dataclasses import dataclass

from ledboardclientfull.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class APIs(metaclass=SingletonMetaclass):
    # FIXME find a way to autocomplete (abstract classes ?)
    board = None
    illumination = None

    def __getattribute__(self, item):
        attribute = super().__getattribute__(item)
        if attribute is None:
            raise RuntimeError(f"API '{item}' is not initialized")
        return attribute
