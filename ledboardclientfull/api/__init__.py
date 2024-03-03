from ledboardclientfull import BoardIllumination

from ledboardclientfull.components.board_communicator.communicator import BoardCommunicator
from ledboardclientfull.components.board_lister import BoardLister
from ledboardclientfull.components.project_persistence import ProjectPersistence
from ledboardclientfull.components.scanner import Scanner
from ledboardclientfull.components.scan_to_tree_mapper import ScanToTreeMapper

from ledboardclientfull.core.components import Components
from ledboardclientfull.core.apis import APIs


def init_ledboard_client():
    #
    # Components
    Components().board_communicator = BoardCommunicator()
    Components().board_illumination = BoardIllumination()
    Components().board_lister = BoardLister()
    Components().project_persistence = ProjectPersistence()
    Components().scanner = Scanner()
    Components().scan_to_tree_mapper = ScanToTreeMapper()


    #
    # APIs
    from ledboardclientfull import board_api
    APIs().board = board_api

    from ledboardclientfull import illumination_api
    APIs().illumination = illumination_api

    from ledboardclientfull import scan_api
    APIs().scan = scan_api
