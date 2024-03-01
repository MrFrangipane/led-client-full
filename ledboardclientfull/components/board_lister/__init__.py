from ledboardclientfull.components.board_communicator.communicator import BoardCommunicator
from ledboardclientfull.core.board.configuration import BoardConfiguration


def list_boards() -> [BoardConfiguration]:
    communicator = BoardCommunicator()

    for port_name in communicator.available_serial_port_names():
        communicator.set_serial_port_name(port_name)
        configuration = communicator.get_configuration()
        if configuration is not None:
            yield port_name, configuration
