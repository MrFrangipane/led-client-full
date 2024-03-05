from ledboardclientfull.core.components import Components
from ledboardclientfull.core.entities.board.configuration import BoardConfiguration
from ledboardclientfull.core.entities.board.list import BoardsList
from ledboardclientfull.core.entities.mapping_tree.leaf import MappingTreeLeaf
from ledboardclientfull.core.entities.mapping_tree.structures import MappingTreeStructure


#
# Boards Lister
def available_boards() -> BoardsList:
    return Components().board_lister.list_boards()


def index_from_hardware_id(hardware_id: str) -> int:
    return Components().board_lister.index_from_hardware_id(hardware_id)


#
# Board Communicator
def get_selected_board() -> BoardConfiguration:
    return Components().board_lister.get_current_board()


def select_board(board_configuration: BoardConfiguration) -> None:
    Components().board_lister.set_current_board(board_configuration)
    Components().board_communicator.set_serial_port_name(board_configuration.serial_port_name)


def get_configuration() -> BoardConfiguration:
    # FIXME: races can mix ports names
    Components().board_communicator.set_serial_port_name(Components().board_lister.get_current_board().serial_port_name)
    return Components().board_communicator.get_configuration()


def set_configuration(configuration: BoardConfiguration):
    Components().board_communicator.configure(configuration)


#
# Mapping Tree
def set_mapping_tree_structure(structure: MappingTreeStructure):
    Components().board_communicator.set_mapping_tree_structure(structure)


def send_mapping_tree_leaf(leaf: MappingTreeLeaf):
    Components().board_communicator.send_mapping_tree_leaf(leaf)
