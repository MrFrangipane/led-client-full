from dataclasses import dataclass

from ledboardclientfull.core.configuration import Configuration
from ledboardclientfull.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class Components(metaclass=SingletonMetaclass):
    configuration = Configuration()
