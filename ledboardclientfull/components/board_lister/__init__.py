from ledboardclientfull.components.board_communicator.communicator import BoardCommunicator
from ledboardclientfull.core.board_configuration import BoardConfiguration


class BoardLister:

    def __init__(self):
        self._communicator = BoardCommunicator()

    def list_boards(self) -> [BoardConfiguration]:
        for port_name in self._communicator.available_serial_port_names():
            self._communicator.set_serial_port_name(port_name)
            configuration = self._communicator.get_configuration()
            if configuration is not None:
                yield port_name, configuration
