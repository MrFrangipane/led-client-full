from dataclasses import dataclass

from pythonarduinoserial.types import *

from ledboardclientfull.core.entities.board.illumination import BoardIllumination


@dataclass
class IlluminationStruct:
    type: IntegerType() = 0
    led_single: IntegerType() = 0
    led_start: IntegerType() = 0
    led_end: IntegerType() = 0
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
        return BoardIllumination(**vars(self))
