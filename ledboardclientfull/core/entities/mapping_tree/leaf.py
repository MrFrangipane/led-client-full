from dataclasses import dataclass


@dataclass
class MappingTreeLeaf:
    led_number: int = 0
    universe_number: int = -1
    pixel_number: int = 0
