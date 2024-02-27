from ledboardclientfull.components.board_communicator.communicator import BoardCommunicator
from ledboardclientfull.components.board_lister import BoardLister
from ledboardclientfull.core.board_configuration import BoardConfiguration
from ledboardclientfull.core.illumination import Illumination


class LEDBoardClientAPI:

    def __init__(self):
        self._communicator = BoardCommunicator()

    #
    # Configuration
    @staticmethod
    def available_boards() -> [BoardConfiguration]:
        return BoardLister().list_boards()

    def set_serial_port(self, port_name: str):
        self._communicator.set_serial_port_name(port_name)

    def get_configuration(self) -> BoardConfiguration:
        return self._communicator.get_configuration()

    def set_configuration(self, configuration: BoardConfiguration):
        self._communicator.configure(configuration)

    #
    # Illumination
    def illuminate(self, illumination: Illumination):
        self._communicator.illuminate(illumination)
