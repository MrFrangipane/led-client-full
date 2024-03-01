
from ledboardclientfull.core.board.configuration import BoardConfiguration
from ledboardclientfull.core.board.list import BoardsList
from ledboardclientfull.core.components import Components


def available_boards() -> BoardsList:
    return Components().board_lister.list_boards()


def select_board(board_configuration: BoardConfiguration) -> None:
    Components().board_communicator.set_serial_port_name(board_configuration.serial_port_name)


def get_selected_board() -> BoardConfiguration:
    return Components().board_communicator.get_configuration()  # fixme use cache


def get_configuration() -> BoardConfiguration:
    return Components().board_communicator.get_configuration()


def set_configuration(configuration: BoardConfiguration):
    Components().board_communicator.configure(configuration)
