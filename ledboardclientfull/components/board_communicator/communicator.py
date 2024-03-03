import logging

from serial.tools.list_ports import comports as list_serial_ports

from pythonarduinoserial.communicator import SerialCommunicator

from ledboardclientfull.components.board_communicator.structs import (
    BoardConfigurationStruct, IlluminationStruct, MappingTreeStructureStruct, all_structs
)
from ledboardclientfull.core.entities.board.configuration import BoardConfiguration
from ledboardclientfull.core.entities.board.illumination import BoardIllumination
from ledboardclientfull.core.entities.mapping_tree.structure import MappingTreeStructure


_logger = logging.getLogger(__name__)


class BoardCommunicator:
    def __init__(self):
        self.serial_communicator = SerialCommunicator(structs=all_structs)

    @staticmethod
    def available_serial_port_names():
        return [port.name for port in list_serial_ports()]

    @property
    def serial_port_name(self):
        return self.serial_communicator.serial_port_name

    def set_serial_port_name(self, name):
        self.serial_communicator.set_port_name(name)

    def configure(self, configuration: BoardConfiguration):
        self.serial_communicator.send(BoardConfigurationStruct.from_entity(configuration))
        _logger.info(f"Configured board on {self.serial_communicator.serial_port_name} {configuration}")

    def get_configuration(self) -> BoardConfiguration:
        _logger.debug(f"Get board configuration from {self.serial_communicator.serial_port_name}")
        configuration_struct: BoardConfigurationStruct = self.serial_communicator.receive(BoardConfigurationStruct)
        if configuration_struct is not None:
            configuration = configuration_struct.to_entity()
            configuration.serial_port_name = self.serial_communicator.serial_port_name
            return configuration

        raise ValueError("Could not retrieve configuration")

    def illuminate(self, illumination: BoardIllumination):
        if self.serial_communicator.serial_port_name is None:
            return

        illumination_struct = IlluminationStruct.from_entity(illumination)
        self.serial_communicator.send(illumination_struct)
        _logger.debug(f"Illuminated {self.serial_communicator.serial_port_name} {illumination}")

    def get_illumination(self) -> BoardIllumination:
        _logger.debug(f"Get board illumination from {self.serial_communicator.serial_port_name}")
        illumination_struct: IlluminationStruct = self.serial_communicator.receive(IlluminationStruct)
        if illumination_struct is not None:
            illumination = illumination_struct.to_entity()
            return illumination

        raise ValueError("Could not retrieve illumination")

    def set_mapping_tree_structure(self, structure: MappingTreeStructure):
        mapping_tree_structure_struct = MappingTreeStructureStruct.from_entity(structure)
        self.serial_communicator.send(mapping_tree_structure_struct)
        _logger.debug(f"Sent MappingTreeStructure {self.serial_communicator.serial_port_name}")
