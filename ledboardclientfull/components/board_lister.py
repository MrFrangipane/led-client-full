import logging

from ledboardclientfull import BoardConfiguration
from ledboardclientfull.core.entities.board.list import BoardsList
from ledboardclientfull.core.components import Components  # FIXME Do we tolerate not to have a board_communicator API ?


_logger = logging.getLogger(__name__)


class BoardLister:
    def __init__(self):
        self._boards: BoardsList = BoardsList()
        self._current_board: BoardConfiguration = None

    def list_boards(self) -> BoardsList:
        _logger.info("Detecting boards...")
        self._boards = BoardsList()
        for port_name in Components().board_communicator.available_serial_port_names():
            Components().board_communicator.set_serial_port_name(port_name)
            configuration = Components().board_communicator.get_configuration()
            if configuration is not None:
                self._boards[configuration.hardware_id] = configuration

        _logger.info(f"Detected {len(self._boards)} boards")

        return self._boards

    def index_from_hardware_id(self, hardware_id: str) -> int:
        return list(self._boards.keys()).index(hardware_id)

    def set_current_board(self, board_configuration: BoardConfiguration):
        self._current_board = board_configuration

    def get_current_board(self) -> BoardConfiguration:
        return self._current_board
