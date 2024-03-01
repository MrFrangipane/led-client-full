from ledboardclientfull.components.board_communicator.communicator import BoardCommunicator
from ledboardclientfull.components.board_lister import BoardLister
from ledboardclientfull.components.project_persistence import ProjectPersistence
from ledboardclientfull.core.components import Components


def init_ledboard_client():
    Components().project_persistence = ProjectPersistence()
    Components().board_communicator = BoardCommunicator()
    Components().board_lister = BoardLister()
