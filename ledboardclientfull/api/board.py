from ledboardclientfull.components.board_lister import list_boards
from ledboardclientfull.core.board.configuration import BoardConfiguration
from ledboardclientfull.core.components import Components


def available_boards() -> [BoardConfiguration]:
    return list_boards()


def set_serial_port(port_name: str):
    Components().board_communicator.set_serial_port_name(port_name)


def get_configuration() -> BoardConfiguration:
    return Components().board_communicator.get_configuration()


def set_configuration(configuration: BoardConfiguration):
    Components().board_communicator.configure(configuration)
