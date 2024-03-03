from dataclasses import dataclass

# from ledboardclientfull import BoardIllumination
# from ledboardclientfull.components.board_communicator.communicator import BoardCommunicator
# from ledboardclientfull.components.board_lister import BoardLister
from ledboardclientfull.components.image_processor.image_processor import ScanImageProcessor
# from ledboardclientfull.components.project_persistence import ProjectPersistence
# from ledboardclientfull.components.scanner import Scanner
# from ledboardclientfull.components.segment_exporter import SegmentExporter
from ledboardclientfull.core.entities.configuration import Configuration
from ledboardclientfull.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class Components(metaclass=SingletonMetaclass):
    configuration = Configuration()
    board_communicator = None  # FIXME : use an AbstractBoardCommunicator
    board_illumination = None  # FIXME : use an AbstractBoardIllumination
    board_lister = None  # FIXME : use an AbstractBoardLister
    image_processor = ScanImageProcessor()
    project_persistence = None  # FIXME : use an AbstractProjectPersistence
    scanner = None  # FIXME : use an AbstractScanner
    segment_exporter = None  # FIXME : use an AbstractSegmentExporter

    def __getattribute__(self, item):
        attribute = super().__getattribute__(item)
        if attribute is None:
            raise RuntimeError(f"Component '{item}' is not initialized")
        return attribute
