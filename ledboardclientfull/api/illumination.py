from ledboardclientfull.core.entities.board.illumination import BoardIllumination
from ledboardclientfull.core.components import Components


def illuminate(illumination: BoardIllumination):
    Components().board_communicator.illuminate(illumination)
    Components().board_illumination = illumination


def get_illumination() -> BoardIllumination:
    return Components().board_communicator.get_illumination()
