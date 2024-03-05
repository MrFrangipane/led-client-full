import logging

from serial.tools.list_ports import comports as list_serial_ports

from ledboardclientfull.core.entities.mapping_tree.leaf import MappingTreeLeaf
from pythonarduinoserial.communicator import SerialCommunicator

from ledboardclientfull.components.board_communicator.structs import (
    BoardConfigurationStruct, IlluminationStruct, MappingTreeStructureStruct, MappingTreeLeafStruct, all_structs
)
from ledboardclientfull.core.entities.board.configuration import BoardConfiguration
from ledboardclientfull.core.entities.board.illumination import BoardIllumination
from ledboardclientfull.core.entities.mapping_tree.structures import MappingTreeStructure


_logger = logging.getLogger(__name__)


class BoardCommunicator:
    def __init__(self):
        self.serial_communicator = SerialCommunicator(structs=all_structs)

    #
    # Serial
    @staticmethod
    def available_serial_port_names():
        return [port.name for port in list_serial_ports()]

    @property
    def serial_port_name(self):
        return self.serial_communicator.serial_port_name

    def set_serial_port_name(self, name):
        self.serial_communicator.set_port_name(name)

    #
    # Configuration
    def configure(self, configuration: BoardConfiguration):
        _logger.info(f"Configuring board on {self.serial_communicator.serial_port_name} {configuration}")
        self.serial_communicator.send(BoardConfigurationStruct.from_entity(configuration))

    def get_configuration(self) -> BoardConfiguration:
        _logger.debug(f"Get board configuration from {self.serial_communicator.serial_port_name}")
        configuration_struct: BoardConfigurationStruct = self.serial_communicator.receive(BoardConfigurationStruct)
        if configuration_struct is not None:
            configuration = configuration_struct.to_entity()
            configuration.serial_port_name = self.serial_communicator.serial_port_name
            return configuration

        raise ValueError("Could not retrieve configuration")

    #
    # Illumination
    def illuminate(self, illumination: BoardIllumination):
        if self.serial_communicator.serial_port_name is None:
            return

        illumination_struct = IlluminationStruct.from_entity(illumination)
        _logger.debug(f"Illuminating {self.serial_communicator.serial_port_name} {illumination}")
        self.serial_communicator.send(illumination_struct)

    def get_illumination(self) -> BoardIllumination:
        _logger.debug(f"Get board illumination from {self.serial_communicator.serial_port_name}")
        illumination_struct: IlluminationStruct = self.serial_communicator.receive(IlluminationStruct)
        if illumination_struct is not None:
            illumination = illumination_struct.to_entity()
            return illumination

        raise ValueError("Could not retrieve illumination")

    #
    # Mapping Tree
    def set_mapping_tree_structure(self, structure: MappingTreeStructure):
        mapping_tree_structure_struct = MappingTreeStructureStruct.from_entity(structure)
        _logger.info(f"Sending MappingTreeStructure {self.serial_communicator.serial_port_name}")
        self.serial_communicator.send(mapping_tree_structure_struct)

    def send_mapping_tree_leaf(self, leaf: MappingTreeLeaf):
        mapping_tree_leaf_struct = MappingTreeLeafStruct.from_entity(leaf)
        _logger.debug(f"Sending MappingTreeLeaf {self.serial_communicator.serial_port_name} {leaf}")
        self.serial_communicator.send(mapping_tree_leaf_struct)
