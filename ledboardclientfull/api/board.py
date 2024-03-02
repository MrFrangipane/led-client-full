
from ledboardclientfull.core.board.configuration import BoardConfiguration
from ledboardclientfull.core.board.list import BoardsList
from ledboardclientfull.core.components import Components


#
# Boards Lister
def available_boards() -> BoardsList:
    return Components().board_lister.list_boards()


def index_from_hardware_id(hardware_id: str) -> int:
    return Components().board_lister.index_from_hardware_id(hardware_id)


def get_selected_board() -> BoardConfiguration:
    return Components().board_lister.get_current_board()


#
# Board Communicator
def select_board(board_configuration: BoardConfiguration) -> None:
    Components().board_lister.set_current_board(board_configuration)
    Components().board_communicator.set_serial_port_name(board_configuration.serial_port_name)


def get_configuration() -> BoardConfiguration:
    return Components().board_communicator.get_configuration()


def set_configuration(configuration: BoardConfiguration):
    Components().board_communicator.configure(configuration)
