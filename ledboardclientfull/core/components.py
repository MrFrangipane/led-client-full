from dataclasses import dataclass

from ledboardclientfull.components.board_communicator.communicator import BoardCommunicator
from ledboardclientfull.components.image_processor.image_processor import ScanImageProcessor
from ledboardclientfull.components.project_persistence import ProjectPersistence
from ledboardclientfull.core.configuration import Configuration
from ledboardclientfull.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class Components(metaclass=SingletonMetaclass):
    configuration = Configuration()
    board_communicator = BoardCommunicator()
    image_processor = ScanImageProcessor()
    project_persistence = ProjectPersistence()
