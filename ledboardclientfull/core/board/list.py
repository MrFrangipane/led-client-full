from ledboardclientfull.core.board.configuration import BoardConfiguration


class BoardsList(dict):  # fixme type hint me

    @property
    def boards(self) -> list[BoardConfiguration]:
        return list(self.values())
