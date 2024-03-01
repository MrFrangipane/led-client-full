from ledboardclientfull.core.board.illumination import BoardIllumination
from ledboardclientfull.core.components import Components


def illuminate(illumination: BoardIllumination):
    Components().board_communicator.illuminate(illumination)
