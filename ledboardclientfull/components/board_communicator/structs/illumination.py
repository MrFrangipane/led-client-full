from dataclasses import dataclass

from pythonarduinoserial.types import *

from ledboardclientfull.core.entities.board.illumination import BoardIllumination


@dataclass
class IlluminationStruct:
    led_start: IntegerType() = 0
    led_end: IntegerType() = 0
    r: IntegerType() = 0
    g: IntegerType() = 0
    b: IntegerType() = 0
    w: IntegerType() = 0

    @staticmethod
    def from_entity(source: BoardIllumination):
        return IlluminationStruct(**vars(source))

    def to_entity(self):
        return BoardIllumination(**vars(self))
