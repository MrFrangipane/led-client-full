from dataclasses import dataclass

from pythonarduinoserial.types import *

from ledboardclientfull.core.entities.mapping_tree.leaf import MappingTreeLeaf


@dataclass
class MappingTreeLeafStruct:
    led_id: IntegerType() = 0
    mapping_id: IntegerType() = 0
    pixel_number: IntegerType() = 0
    universe_number: IntegerType() = 0

    @staticmethod
    def from_entity(source: MappingTreeLeaf):
        new = MappingTreeLeafStruct(**vars(source))
        return new

    def to_entity(self) -> MappingTreeLeaf:
        new = MappingTreeLeaf(**vars(self))
        return new
