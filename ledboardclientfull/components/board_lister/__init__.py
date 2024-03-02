from ledboardclientfull import BoardConfiguration
from ledboardclientfull.core.board.list import BoardsList
from ledboardclientfull.core.components import Components


class BoardLister:
    def __init__(self):
        self._boards: BoardsList = BoardsList()
        self._current_board: BoardConfiguration = None

    def list_boards(self) -> BoardsList:
        self._boards = BoardsList()
        for port_name in Components().board_communicator.available_serial_port_names():
            Components().board_communicator.set_serial_port_name(port_name)
            configuration = Components().board_communicator.get_configuration()
            if configuration is not None:
                self._boards[configuration.hardware_id] = configuration

        return self._boards

    def index_from_hardware_id(self, hardware_id: str) -> int:
        return list(self._boards.keys()).index(hardware_id)

    def set_current_board(self, board_configuration: BoardConfiguration):
        self._current_board = board_configuration

    def get_current_board(self) -> BoardConfiguration:
        return self._current_board
