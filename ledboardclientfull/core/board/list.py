from ledboardclientfull.core.board.configuration import BoardConfiguration


class BoardsList(dict):  # fixme type hint me

    @property
    def boards(self) -> list[BoardConfiguration]:
        return list(self.values())

    def index_from_hardware_id(self, hardware_id: str) -> int:  # fixme move to BoardLister
        return list(self.keys()).index(hardware_id)
