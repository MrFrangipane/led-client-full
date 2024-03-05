import logging

# FIXME move this to  board_communicator
from serial.serialutil import SerialException

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
            try:
                Components().board_communicator.set_serial_port_name(port_name)
                configuration = Components().board_communicator.get_configuration()
                self._boards[configuration.hardware_id] = configuration
            except (ValueError, SerialException) as e:
                _logger.info(f"Not a Board {port_name}: {e}")
                pass

        _logger.info(f"Detected {len(self._boards)} boards")

        return self._boards

    def index_from_hardware_id(self, hardware_id: str) -> int:
        return list(self._boards.keys()).index(hardware_id)

    def set_current_board(self, board_configuration: BoardConfiguration):
        # FIXME: !! can desync with serial port name !!
        self._current_board = board_configuration

    def get_current_board(self) -> BoardConfiguration:
        return self._current_board
