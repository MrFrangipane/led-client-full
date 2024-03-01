from ledboardclientfull.components.board_communicator.communicator import BoardCommunicator
from ledboardclientfull.core.board.list import BoardsList


class BoardLister:
    def __init__(self):
        self._boards: BoardsList = BoardsList()

    def list_boards(self) -> BoardsList:
        communicator = BoardCommunicator()

        self._boards = BoardsList()
        for port_name in communicator.available_serial_port_names():
            communicator.set_serial_port_name(port_name)
            configuration = communicator.get_configuration()
            if configuration is not None:
                self._boards[configuration.hardware_id] = configuration

        return self._boards
