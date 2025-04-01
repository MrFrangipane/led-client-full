from ledboardclientfull.board_api import BoardApi


board = BoardApi(serial_port='COM9')
configuration = board.get_configuration()

print(configuration)
