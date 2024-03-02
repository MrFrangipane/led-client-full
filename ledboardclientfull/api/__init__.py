from ledboardclientfull.components.board_communicator.communicator import BoardCommunicator
from ledboardclientfull.components.board_lister import BoardLister
from ledboardclientfull.components.project_persistence import ProjectPersistence
from ledboardclientfull.core.components import Components
from ledboardclientfull.core.apis import APIs


def init_ledboard_client():
    #
    # Components
    Components().project_persistence = ProjectPersistence()
    Components().board_communicator = BoardCommunicator()
    Components().board_lister = BoardLister()

    #
    # APIs
    from ledboardclientfull import board_api
    APIs().board = board_api

    from ledboardclientfull import illumination_api
    APIs().illumination = illumination_api
