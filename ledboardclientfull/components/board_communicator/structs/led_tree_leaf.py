from dataclasses import dataclass

from pythonarduinoserial.types import *

from ledboardclientfull.core.entities.mapping_tree.leaf import MappingTreeLeaf


@dataclass
class MappingTreeLeafStruct:
    led_number: IntegerType() = 0
    universe_number: IntegerType() = -1
    pixel_number: IntegerType() = 0
    do_clear_tree: IntegerType() = 0

    @staticmethod
    def from_entity(source: MappingTreeLeaf):
        new = MappingTreeLeafStruct(**vars(source))
        new.do_clear_tree = int(source.do_clear_tree)
        return new

    def to_entity(self) -> MappingTreeLeaf:
        new = MappingTreeLeaf(**vars(self))
        new.do_clear_tree = bool(self.do_clear_tree)
        return new
