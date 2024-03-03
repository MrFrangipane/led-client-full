from dataclasses import dataclass

from pythonarduinoserial.types import *

from ledboardclientfull.core.entities.board.led_tree_leaf import LEDTreeLeaf


@dataclass
class LEDTreeLeafStruct:
    led_number: IntegerType() = 0
    universe_number: IntegerType() = -1
    pixel_number: IntegerType() = 0
    do_clear_tree: IntegerType() = 0

    @staticmethod
    def from_entity(source: LEDTreeLeaf):
        new = LEDTreeLeafStruct(**vars(source))
        new.do_clear_tree = int(source.do_clear_tree)
        return new

    def to_entity(self) -> LEDTreeLeaf:
        new = LEDTreeLeaf(**vars(self))
        new.do_clear_tree = bool(self.do_clear_tree)
        return new
