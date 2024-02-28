import logging

from serial.tools.list_ports import comports as list_serial_ports
from pythonarduinoserial.communicator import SerialCommunicator

from ledboardclientfull.components.board_communicator.structs import BoardConfigurationStruct, IlluminationStruct, all_structs
from ledboardclientfull.core.board_configuration import BoardConfiguration
from ledboardclientfull.core.illumination import Illumination


_logger = logging.getLogger(__name__)


class BoardCommunicator:
    def __init__(self):
        self.serial_communicator = SerialCommunicator(structs=all_structs)

    @staticmethod
    def available_serial_port_names():
        return [port.name for port in list_serial_ports()]

    def set_serial_port_name(self, name):
        self.serial_communicator.set_port_name(name)

    def configure(self, configuration: BoardConfiguration):
        self.serial_communicator.send(BoardConfigurationStruct.from_entity(configuration))
        _logger.info(f"Configured board on {self.serial_communicator.serial_port_name} {configuration}")

    def get_configuration(self) -> BoardConfiguration:
        _logger.info(f"Get board configuration from {self.serial_communicator.serial_port_name}")
        configuration_struct: BoardConfigurationStruct = self.serial_communicator.receive(BoardConfigurationStruct)
        if configuration_struct is not None:
            return configuration_struct.to_entity()

    def illuminate(self, illumination: Illumination):
        if self.serial_communicator.serial_port_name is None:
            return

        illumination_struct = IlluminationStruct.from_entity(illumination)
        self.serial_communicator.send(illumination_struct)
        _logger.debug(f"Illuminated {self.serial_communicator.serial_port_name} {illumination}")
