from dataclasses import dataclass

from ledboardclientfull.core.entities.board.illumination_type import BoardIlluminationType


@dataclass
class BoardIllumination:
    type: BoardIlluminationType = BoardIlluminationType.Range

    led_single: int = 0
    led_first: int = 0
    led_last: int = 0

    r: int = 0
    g: int = 0
    b: int = 0
    w: int = 0
