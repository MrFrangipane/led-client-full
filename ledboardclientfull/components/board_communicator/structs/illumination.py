from dataclasses import dataclass

from pythonarduinoserial.types import *

from ledboardclientfull.core.entities.board.illumination import BoardIllumination
from ledboardclientfull.core.entities.board.illumination_type import BoardIlluminationType


@dataclass
class IlluminationStruct:
    type: IntegerType() = 0
    led_single: IntegerType() = 0
    led_first: IntegerType() = 0
    led_last: IntegerType() = 0
    r: IntegerType() = 0
    g: IntegerType() = 0
    b: IntegerType() = 0
    w: IntegerType() = 0

    @staticmethod
    def from_entity(source: BoardIllumination):
        as_dict = vars(source)
        as_dict["type"] = source.type.value
        return IlluminationStruct(**as_dict)

    def to_entity(self):
        illumination = BoardIllumination(**vars(self))
        illumination.type = BoardIlluminationType(self.type)
        return illumination
